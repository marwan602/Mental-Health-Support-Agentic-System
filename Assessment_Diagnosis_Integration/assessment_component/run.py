"""Run the Part 1 adaptive interview with no external knowledge."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path


from .coverage import TOPICS, REPORTED, TERMINAL, eligible_topics
from .harness.providers import ChatClient, GeminiNativeClient, LLMCaller, ProviderError, QuotaExhausted, Response, ResponseCache
from .harness.runlog import EventLog
from .harness.util import ROOT, dump_json, load_json, write_text_atomically
from .handoff import CARE_FIELDS, PROTOCOL, build_handoff, checked_context, empty_notes


EXCLUDED_TOPICS = re.compile(
    r"\b(?:phq[- ]?[29]|gad[- ]?[27]|questionnaire|suicid\w*|self[- ]?(?:harm|injur\w*)|"
    r"kill yourself|end(?:ing)? your life|hurt(?:ing)? yourself|wish(?:ing)? to die|better off dead)\b",
    re.I,
)
BARE_UNKNOWN = re.compile(r"(?:i (?:do not|don't) (?:know|remember)|i(?: am|'m) not sure|no idea|not sure)[.!]?", re.I)
BARE_DECLINE = re.compile(
    r"(?:i(?:'d| would) (?:rather not|prefer not to)(?: (?:answer|say|talk about|discuss)(?: (?:it|that|this))?)?|"
    r"i (?:(?:don't|do not) want to|prefer not to) (?:answer|discuss|talk about)(?: (?:it|this|that)(?: question)?)?|"
    r"(?:please |can we |let's )?skip(?: (?:it|that|this|this question|that question))?)(?: please)?[.!?]?", re.I)
BARE_STOP = re.compile(r"(?:stop|please stop|i (?:want|would like) to stop)[.!]?", re.I)
def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def opening_message(template, patient_name):
    first_name = patient_name.split()[0] if nonempty(patient_name) else ""
    return template.format(greeting=f"Hi {first_name}" if first_name else "Hi")


def ids_valid(value, known):
    return isinstance(value, list) and all(isinstance(item, str) and item in known for item in value)


def fields(obj, expected):
    if not isinstance(obj, dict) or set(obj) != set(expected.split()):
        raise ValueError(f"Expected exactly these fields: {expected}")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def patient_summary(parts):
    order = ("experience", "meaning", "impression")
    fields(parts, " ".join(order))
    require(all(nonempty(parts[key]) for key in order),
            "Include the person's experience, its significance and the tentative conclusion.")
    return " ".join(parts[key].strip() for key in order)


CYCLE_GAP = re.compile(r"\b(?:menstr\w*|premenstr\w*|PMDD)\b", re.I)


def in_scope_gaps(gaps, coverage):
    return [gap for gap in gaps if not EXCLUDED_TOPICS.search(gap)
            and ("cycle_pattern" in coverage or not CYCLE_GAP.search(gap))]


def check_final_review(review, history, items, gaps, coverage):
    fields(review, "summary source_turns omit_item_indices material_gaps")
    patient_summary(review["summary"])
    sources = review["source_turns"]
    fields(sources, "experience meaning")
    patient_ids = {t["message_id"] for t in history if t["speaker"] == "patient"}
    for ids in sources.values():
        require(ids_valid(ids, patient_ids) and len(ids) > 0, "Cite patient turns for both experience and meaning.")
    omit = review["omit_item_indices"]
    require(isinstance(omit, list) and all(type(i) is int and 0 <= i < len(items) for i in omit),
            "Use zero-based indices of the supplied care items.")
    material = review["material_gaps"]
    require(isinstance(material, list), "Return an array of material gaps, or [].")
    seen = set()
    for row in material:
        fields(row, "index topic message_id quote why_it_matters")
        idx = row["index"]
        require(type(idx) is int and 0 <= idx < len(gaps) and idx not in seen, "Select distinct existing gap indices.")
        seen.add(idx)
        require(row["topic"] in TOPICS and nonempty(row["why_it_matters"]), "Identify a real topic and the decision this gap affects.")
        require(row["message_id"] in patient_ids and nonempty(row["quote"]) and
                any(t["message_id"] == row["message_id"] and row["quote"] in t["text"] for t in history),
                "Use an exact supporting patient quotation from the specified turn.")
        conditional = row["topic"] == "cycle_pattern" or CYCLE_GAP.search(gaps[idx])
        if conditional:
            require("cycle_pattern" in coverage, "Omit the menstrual branch when the interview never opened it.")


def check_reflection(text, sources):
    """Catch recurrent changes of meaning before delivery, allowing neutral questions."""
    text = text.casefold().replace("’", "'")
    sources = " ".join(sources).casefold().replace("’", "'")
    memory = r"\b(?:memory|amnesia|memory loss|(?:unable to|can't|cannot|couldn't) (?:recall|remember)|forget\w*|forgot\w*)\b"
    if re.search(memory, text):
        require(re.search(memory, sources) or re.search(r"\b(?:remember|recall)\w*\b", sources),
                "The patient did not describe a memory problem. Reflect their experience without introducing memory loss.")
    absolute = r"\b(?:constant(?:ly)?|all the time|every single day|always|nonstop|never lets up)\b"
    if re.search(absolute, text):
        require(re.search(absolute, sources) or re.search(r"\b(?:every day|each day|without (?:any )?break|never stops)\b", sources),
                "Avoid introducing an absolute frequency. Use the patient's frequency or omit it.")


def check_impression(text):
    require(not re.search(r"\b(?:rather than|without|not (?:a|an))\s+(?:(?:a|an)\s+)?(?:depression|depressive|anxiety disorder)\b", text, re.I),
            "Describe what the history supports. Avoid unqualified comparisons that dismiss a disorder.")


ROUTINE_THANKS = re.compile(
    r"(?:thanks|thank you)(?: (?:so much|very much))?"
    r"(?: for (?:sharing|clarifying|explaining|describing|telling me|letting me know)"
    r"(?: (?:that|this|it|more|that pattern|the pattern))?"
    r"(?: (?:with me|so clearly|about (?:your |the |those )?[\w -]+))?)?[.!]?", re.I)


def spoken_follow_up(reply, history):
    question = reply["question"].strip()
    acknowledgment = reply["acknowledgment"].strip()
    if not acknowledgment or ROUTINE_THANKS.fullmatch(acknowledgment) or re.search(r"\bnoted[.!]?$", acknowledgment, re.I):
        return question
    last_turn = next((m["text"] for m in reversed(history) if m["speaker"] == "interviewer"), "")
    if last_turn.casefold().startswith(acknowledgment.casefold() + " "):
        return question
    return acknowledgment + " " + question


def validate_follow_up(reply, target_id, history, listening_quote=None):
    fields(reply, "status acknowledgment question target_id")
    require(reply["target_id"] == target_id, "Copy the selected target_id.")
    acknowledgment, question = reply["acknowledgment"], reply["question"]
    if reply["status"] == "return_to_planner":
        require(acknowledgment == question == "", "Leave both spoken fields empty on an internal return.")
        return
    require(reply["status"] == "send" and isinstance(acknowledgment, str) and nonempty(question),
            "Use send with an optional acknowledgment and one question.")
    latest = next((m["text"] for m in reversed(history) if m["speaker"] == "patient"), "")
    check_reflection(acknowledgment, [latest])
    if re.match(r"^(?:you|your|since you|given (?:your|that you)|when you)\b", question, re.I):
        check_reflection(question, [m["text"] for m in history if m["speaker"] == "patient"])
    require(not re.search(r"[?؟]|[.!]\s+\S", acknowledgment.strip()),
            "Use a single brief acknowledgment without a question, or leave it empty when appropriate.")
    require(len(question.split()) <= 25 and question.strip().endswith("?") and question.count("?") == 1,
            "Ask one short question of at most 25 words.")
    require(not re.search(r"\b(?:and|or)\s+(?:when|where|why|who|what|how)\s+(?:did|do|does|is|was|were|are|has|have|can|would)\b", question, re.I),
            "Choose one detail. Ask the first relevant question and leave the second for later.")
    if listening_quote is not None:
        require(spoken_follow_up(reply, history) != question.strip() and
                not re.fullmatch(r"(?:yeah|okay|ok|i (?:see|understand|get (?:you|it)))[.!]?", acknowledgment.strip(), re.I),
                "Respond briefly to the experience in target.listening_quote before asking. Write it in your own words.")
    require(not re.search(r"[.!]\s+\S", question.strip()),
            "Place the acknowledgment in its own field. Start the question directly.")
    require(not re.match(r"(?:thanks|thank you)\b", question.strip(), re.I),
            "Begin with the actual question. Leave routine thanks out.")
    require(not EXCLUDED_TOPICS.search(acknowledgment + " " + question), "Use an in-scope follow-up.")
    earlier = [m["text"].strip().casefold() for m in history if m["speaker"] == "interviewer"]
    ending = question.strip().casefold()
    require(all(line != ending and not line.endswith(" " + ending) for line in earlier),
            "The same question has already been asked.")


def save_dialogue(folder, history):
    dump_json(folder / "transcript.json", history)
    lines = [f"# {folder.name}", ""]
    questions = answers = 0
    for row in history:
        if row["kind"] == "closing":
            label = "Closing"
        elif row["kind"] == "assessment_summary":
            label = "Assessment summary"
        elif row["speaker"] == "interviewer":
            questions += 1
            label = f"Question {questions}"
        else:
            answers += 1
            label = f"Answer {answers}"
        lines.extend((f"## {label}", "", row["text"], ""))
    write_text_atomically(folder / "conversation_qa.md", "\n".join(lines))


class MockClient:
    """Deterministic responses for a local wiring check."""

    def complete_role(self, role, messages, params, context):
        if role == "care_context":
            return Response(text=json.dumps(empty_notes()), model_returned="mock", finish_reason="stop")
        if role == "final_review":
            first = next(t["message_id"] for t in context["history"] if t["speaker"] == "patient")
            output = {"summary":context["synthesis"]["summary"], "source_turns":{"experience":[first],"meaning":[first]},
                      "omit_item_indices":[], "material_gaps":[]}
            return Response(text=json.dumps(output), model_returned="mock", finish_reason="stop")
        outputs = {
            "extractor": {"updates": [{
                "topic": "opening concern (offline fixture)", "status": "unclear", "time_reference": None,
                "attributes": {}, "quote": context["history"][-1]["text"],
                "message_id": context.get("latest_patient_message_id"), "context_message_ids": [],
                "related_finding_id": None,
            }], "coverage_updates": [], "reply_route": "engaged", "stop_quote": None},
            "planner": {"action": "ask",
                        "topic": context.get("eligible_topics", ["daily_impact"])[0],
                        "listening_quote": None,
                        "information_goal": "Clarify the selected topic.",
                        "reason": "Local wiring check.", "evidence_ids": []},
            "conversation": {"status": "send",
                             "acknowledgment": "", "question": "How has feeling low affected your day-to-day life?",
                             "target_id": (context.get("target") or {}).get("target_id")},
            "synthesis": {"summary": {"experience":"We talked about how things have been for you.",
                                     "meaning":"Some details are still unclear.",
                                     "impression":"There isn't enough information yet to tell what might explain this."},
                          "provisional_label": "INSUFFICIENT_INFORMATION", "rationale":"Offline wiring example.", "supporting_finding_ids": [],
                          "alternatives": [], "missing_information": ["Daily impact remains unclear."]},
        }
        if role == "planner" and len(context["evidence"]) >= 2:
            outputs[role] = {"action":"finish","topic":None,"information_goal":None,"listening_quote":None,"reason":"Offline early-finish exercise.","evidence_ids":[context["evidence"][0]["finding_id"]]}
        if role == "extractor" and len(context["history"]) > 2:
            outputs[role]["updates"][0].update(topic="work impact", time_reference=None)
        if role == "extractor":
            topic = context.get("pending_topic") or "mood"
            outputs[role]["coverage_updates"] = [{"topic": topic, "status": "answered",
                                                  "quote": context["history"][-1]["text"]}]
        if role == "conversation" and context["stage"] == "follow_up":
            topic = context["target"]["topic"].replace("_", " ")
            wording = f"Could you tell me more about {topic}?"
            if any(turn["text"] == wording for turn in context["history"]):
                wording = f"What would you like me to understand about {topic}?"
            outputs[role]["question"] = wording
        return Response(text=json.dumps(outputs[role]), model_returned="mock", finish_reason="stop")


def build_client(cfg, model, mock):
    if mock:
        return MockClient()
    provider = cfg["providers"][model["provider"]]
    cls = GeminiNativeClient if provider.get("api_style") == "gemini_native" else ChatClient
    return cls(provider, model)


class AwaitingReply(Exception):
    """The host application must supply the next fictional reply."""


def interview(folder, name, replies, cfg, assessor, prompts, model, mock):
    folder.mkdir(parents=True, exist_ok=True)
    prior = load_json(folder / "transcript.json") if (folder / "transcript.json").is_file() else []
    history, evidence, asked, decisions = [], [], [], []
    coverage = {}
    unrelated_streak = 0
    label_ids = {label["label_id"] for label in cfg["allowed_labels"]}
    scope = {"population": "Fictional adults aged 18 and older", "possible_formulations":cfg["allowed_labels"]}
    from uuid import uuid4
    log = EventLog(folder / f"events_{uuid4().hex}.jsonl")
    cache = ResponseCache(folder / "interviewer_responses.jsonl")
    params = {"temperature":model["temperature"], "max_tokens":model["max_tokens"],
              "seed":cfg["seed"] if model.get("send_seed", True) else None}
    caller = LLMCaller(assessor, model, log, cache, params)
    previous = load_json(folder / "status.json") if (folder / "status.json").is_file() else {}
    status = {"state": "running", "mock": mock, "case": folder.name, "model": model["model_id"],
              "started": previous.get("started", datetime.now(timezone.utc).isoformat())}
    dump_json(folder / "status.json", status)

    def add(speaker, text, kind):
        row = {"message_id": f"m{len(history)+1:04}", "speaker": speaker, "text": text, "kind": kind}
        history.append(row)
        require(len(history) > len(prior) or row == prior[len(history) - 1],
                "Replay differs from the saved dialogue. Review the archived attempt.")
        log.write("message", **row)
        if len(history) >= len(prior):
            save_dialogue(folder, history)
        return row

    def call(role, payload, check):
        system = prompts[role]
        payload = {**payload, "scope": scope}
        log.write("agent_input", role=role, input=payload)
        if role == "conversation":
            target_id = payload["target"]["target_id"]
            returned = folder / ("returned_" + target_id + ".json")
            if returned.exists():
                return load_json(returned)

        def validator(obj):
            check(obj)
            return []

        result, details = caller.call_json(role, system, payload, validator, context=payload)
        if result is None:
            if role == "conversation":
                log.write("wording_returned", target_id=target_id, errors=details["errors"])
                result = {"status":"return_to_planner", "acknowledgment":"", "question":"", "target_id":target_id}
                dump_json(returned, result)
                return result
            raise ValueError(f"{role} returned an invalid output: {details['errors']}")
        return result

    def extract(reply, pending_topic):
        nonlocal unrelated_streak
        def check(obj):
            fields(obj, "updates coverage_updates reply_route stop_quote")
            require(obj["reply_route"] in ("engaged", "unrelated", "unclear_choice"), "Invalid reply route.")
            if obj["reply_route"] != "engaged":
                require(obj["updates"] == [] and obj["coverage_updates"] == [] and obj["stop_quote"] is None,
                        "An unrelated reply or unclear choice must not change evidence or coverage.")
            if obj["reply_route"] == "unclear_choice":
                require(history[-2]["kind"] == "direction_check", "Unclear choice applies only to the direction check.")
            require(isinstance(obj["updates"], list), "Updates must be an array.")
            earlier = {m["message_id"] for m in history[:-1]}
            known = {f["finding_id"] for f in evidence}
            for u in obj["updates"]:
                fields(u, "topic status time_reference attributes quote message_id context_message_ids related_finding_id")
                require(nonempty(u["topic"]), "Finding topic is empty.")
                require(u["status"] in ("reported_present", "reported_absent", "unclear"), "Unknown finding status.")
                require(u["time_reference"] is None or nonempty(u["time_reference"]), "Invalid time reference.")
                require(isinstance(u["attributes"], dict), "Attributes must be an object.")
                require(nonempty(u["quote"]) and u["quote"] in reply["text"], "Quote must occur verbatim in the reply.")
                require(u["message_id"] == reply["message_id"], "Use the current patient message ID.")
                require(ids_valid(u["context_message_ids"], earlier), "Context must refer to earlier messages.")
                require(u["related_finding_id"] is None or u["related_finding_id"] in known, "Unknown related finding ID.")
            require(isinstance(obj["coverage_updates"], list), "Coverage updates must be an array.")
            seen = set()
            for entry in obj["coverage_updates"]:
                fields(entry, "topic status quote")
                require(isinstance(entry["topic"], str) and entry["topic"] in TOPICS
                        and entry["topic"] not in seen, "Use distinct supplied topic IDs.")
                seen.add(entry["topic"])
                require(entry["status"] in REPORTED, "Unknown coverage status.")
                require(nonempty(entry["quote"]) and entry["quote"] in reply["text"], "Use a verbatim patient quote.")
            require(obj["stop_quote"] is None or (nonempty(obj["stop_quote"])
                    and obj["stop_quote"] in reply["text"]), "Use a verbatim stop request or null.")

        normalized = reply["text"].strip().replace("’", "'")
        limit = None
        if pending_topic:
            if BARE_DECLINE.fullmatch(normalized):
                limit = "declined"
            elif BARE_UNKNOWN.fullmatch(normalized):
                limit = "unknown"
        if limit:
            updates = {"updates": [], "coverage_updates": [{"topic": pending_topic, "status": limit,
                       "quote": reply["text"]}], "reply_route": "engaged", "stop_quote": None}
            log.write("participation_limit", message_id=reply["message_id"], topic=pending_topic, status=limit)
        else:
            updates = call("extractor", {"history": history, "evidence": evidence,
                       "latest_patient_message_id": reply["message_id"], "pending_topic": pending_topic,
                       "topics": TOPICS, "coverage": coverage, "knowledge": cfg["knowledge"]}, check)
        for update in updates["updates"]:
            evidence.append({**update, "finding_id": f"f{len(evidence)+1:04}"})
        for entry in updates["coverage_updates"]:
            topic = entry["topic"]
            previous_status = coverage.get(topic, {}).get("status")
            if previous_status == "declined" or (previous_status in TERMINAL and entry["status"] == "partial"):
                continue
            coverage[topic] = {**entry, "message_id": reply["message_id"]}
        unrelated_streak = unrelated_streak + 1 if updates["reply_route"] != "engaged" else 0
        log.write("reply_route", message_id=reply["message_id"], pending_topic=pending_topic,
                  route=updates["reply_route"], unrelated_streak=unrelated_streak)
        if len(history) >= len(prior):
            dump_json(folder / "evidence.json", evidence)
            dump_json(folder / "coverage.json", {t: coverage.get(t, {"status": "unresolved"}) for t in TOPICS})
        return updates["stop_quote"] is not None or bool(BARE_STOP.fullmatch(normalized))

    def respond(pending_topic=None):
        question_id = history[-1]["message_id"]
        if question_id not in replies:
            raise AwaitingReply()
        return extract(add("patient", replies[question_id], "answer"), pending_topic)

    def known_findings(ids):
        return ids_valid(ids, {f["finding_id"] for f in evidence})

    def plan_check(obj):
        fields(obj, "action topic information_goal listening_quote reason evidence_ids")
        quote = obj["listening_quote"]
        require(quote is None or (obj["action"] == "ask" and nonempty(quote) and quote in history[-1]["text"]),
                "Use null or copy a short exact phrase from the latest patient reply. Use null for finish.")
        require(nonempty(obj["reason"]) and known_findings(obj["evidence_ids"]), "Invalid reason or evidence IDs.")
        if obj["action"] == "ask":
            require(nonempty(obj["topic"]) and nonempty(obj["information_goal"]), "A question needs a topic and goal.")
            require(obj["topic"] in eligible, "Select an eligible topic. Answered, unknown, declined and deferred topics are blocked.")
            require(not EXCLUDED_TOPICS.search(obj["topic"] + " " + obj["information_goal"]), "Choose an in-scope topic.")
        else:
            require(obj["action"] == "finish" and obj["topic"] is None and obj["information_goal"] is None,
                    "Finish requires null topic and goal.")
            require(obj["evidence_ids"] or not evidence, "Identify the finding(s) relevant to your finish decision.")

    def speak(target):
        def check(obj):
            validate_follow_up(obj, target["target_id"], history, target["listening_quote"])

        return call("conversation", {"stage": "follow_up", "history": history, "target": target,
                    "evidence": evidence, "coverage": coverage,
                    "knowledge": cfg["knowledge"]}, check)

    def synthesis_check(obj):
        fields(obj, "summary provisional_label rationale supporting_finding_ids alternatives missing_information")
        summary = patient_summary(obj["summary"])
        require(obj["provisional_label"] in label_ids, "Invalid provisional label.")
        require("?" not in summary,
                "End the provisional summary with a statement, without a question.")
        require(not re.search(r"\bone (?:possible explanation|possibility) is\b", summary, re.I),
                "Connect the tentative interpretation directly to what the person described.")
        require(not re.search(r"\byou (?:definitely have|are diagnosed with|meet (?:all )?(?:the )?(?:diagnostic )?criteria for)\b|\byour diagnosis is\b", summary, re.I),
                "Describe a working impression in patient-facing language without confirming a diagnosis.")
        require(nonempty(obj["rationale"]), "Explain the provisional conclusion and key uncertainty.")
        require(not EXCLUDED_TOPICS.search(summary), "Keep the patient-facing summary within the study scope.")
        require(known_findings(obj["supporting_finding_ids"]), "Unknown supporting evidence ID.")
        require(obj["provisional_label"] == "INSUFFICIENT_INFORMATION" or obj["supporting_finding_ids"],
                "A definite label needs cited evidence.")
        require(isinstance(obj["alternatives"], list), "Alternatives must be an array.")
        for alternative in obj["alternatives"]:
            fields(alternative, "label reason finding_ids")
            require(alternative["label"] in label_ids and nonempty(alternative["reason"])
                    and known_findings(alternative["finding_ids"]), "Invalid alternative.")
        require(isinstance(obj["missing_information"], list)
                and all(nonempty(x) for x in obj["missing_information"]), "Invalid missing-information list.")

    try:
        add("interviewer", opening_message(cfg["opening"], name), "opening")
        stop = respond()
        followups = 0
        end_reason = "question_budget"
        for attempt in range(cfg["max_followups"] + 3):
            if stop:
                end_reason = "patient_stop"
                break
            if followups >= cfg["max_followups"]:
                break
            if unrelated_streak >= 2:
                add("interviewer", "We can leave that there. Would you like to talk about something else that’s been affecting you, or pause here?", "direction_check")
                followups += 1
                stop = respond()
                if not stop and unrelated_streak:
                    end_reason = "no_interview_direction"
                    break
                continue
            eligible = eligible_topics(coverage, asked, followups + 1)
            if not eligible:
                end_reason = "no_eligible_topics"
                break
            priority = ("presenting_pattern" if "presenting_pattern" in eligible
                        and coverage["presenting_pattern"]["status"] == "partial"
                        and not any(goal["topic"] == "presenting_pattern" for goal in asked) else None)
            plan = call("planner", {"history": history, "evidence": evidence, "asked_targets": asked,
                        "topics": TOPICS, "coverage": coverage, "eligible_topics": eligible,
                        "priority_topic": priority,
                        "partly_answered_topics": [t for t in eligible if coverage.get(t, {}).get("status") == "partial"],
                        "remaining_turns": cfg["max_followups"] - followups,
                        "knowledge": cfg["knowledge"]}, plan_check)
            decisions.append({"after_turn":history[-1]["message_id"], **plan})
            dump_json(folder / "planner_decisions.json", decisions)
            if plan["action"] == "finish":
                end_reason = "planner_finish"
                break
            target = {**plan, "target_id": f"q{attempt+1:03}"}
            message = speak(target)
            asked.append({**target, "status": "sent" if message["status"] == "send" else "returned",
                          "answer_count": followups + 1})
            decisions[-1]["delivery"] = message["status"]
            dump_json(folder / "planner_decisions.json", decisions)
            if message["status"] == "return_to_planner":
                end_reason = "planner_attempt_budget"
                continue
            followups += 1
            spoken = spoken_follow_up(message, history)
            add("interviewer", spoken, "follow_up")
            stop = respond(target["topic"])
        else:
            end_reason = "planner_attempt_budget"
        if stop:
            end_reason = "patient_stop"
        elif end_reason != "no_interview_direction" and followups == cfg["max_followups"]:
            end_reason = "question_budget"
        synthesis = call("synthesis", {"history": history, "evidence": evidence, "end_reason": end_reason,
                         "coverage": {t: coverage.get(t, {"status": "unresolved"}) for t in TOPICS},
                         "allowed_labels": cfg["allowed_labels"], "knowledge": cfg["knowledge"]}, synthesis_check)
        gaps = in_scope_gaps(synthesis["missing_information"], coverage)
        if len(gaps) != len(synthesis["missing_information"]):
            log.write("scope_filter", omitted_missing_information=len(synthesis["missing_information"])-len(gaps))
        synthesis = {**synthesis, "missing_information":gaps}
        label_names = {entry["label_id"]: entry["name"] for entry in cfg["allowed_labels"]}
        notes = call("care_context", {"history":history, "evidence":evidence, "care_fields":CARE_FIELDS,
                     "assessment_end_reason":end_reason, "knowledge":None},
                     lambda obj: checked_context(obj, history, evidence))
        def review_check(obj):
            check_final_review(obj, history, notes["items"], gaps, coverage)
            synthesis_check({**synthesis, "summary":obj["summary"]})
            for field, ids in obj["source_turns"].items():
                check_reflection(obj["summary"][field], [t["text"] for t in history if t["message_id"] in ids])
            check_impression(obj["summary"]["impression"])
            closing_text = patient_summary(obj["summary"]).replace("’", "'")
            require(not re.search(r"\byou (?:do not|don't|cannot|can't) have (?:depression|(?:a |any )?(?:depressive|mental) disorder)\b|\b(?:we can|this|that) rules? out depression\b", closing_text, re.I),
                    "Describe the observed pattern and keep any conclusion about absence provisional.")

        review = call("final_review", {"history":history, "synthesis":synthesis, "items":notes["items"],
                      "end_reason":end_reason, "topics":TOPICS, "coverage":coverage, "knowledge":None}, review_check)
        notes = {**notes, "items":[row for i,row in enumerate(notes["items"]) if i not in review["omit_item_indices"]]}
        gap_review = [{"gap":gaps[row["index"]], **row} for row in review["material_gaps"]]
        synthesis = {**synthesis, "summary":patient_summary(review["summary"]), "summary_source_turns":review["source_turns"],
                     "missing_information":[row["gap"] for row in gap_review], "reviewed_gaps":gap_review}
        dump_json(folder / "synthesis.json", synthesis)
        if end_reason == "patient_stop":
            closing = "Of course, we can stop here. Thank you for sharing what you did."
        elif end_reason == "no_interview_direction":
            closing = "We can leave it here for today. Thank you for taking the time to talk."
        else:
            closing = synthesis["summary"]
        add("interviewer", closing, "closing")
        source = {"protocol":PROTOCOL, "case_id":status["case"], "run_id":folder.name,
                  "interview_finished_at":datetime.now(timezone.utc).isoformat(), "stop_reason":end_reason}
        dump_json(folder / "assessment_handoff.json", build_handoff(source, notes, history, evidence, synthesis, label_names))
        dump_json(folder / "planner_decisions.json", decisions)
        status.update(state="complete", end_reason=end_reason, followups=followups,
                      planner_chose_to_finish=(end_reason == "planner_finish"),
                      remaining_assessment_gaps=synthesis["missing_information"])
    except AwaitingReply:
        status.update(state="awaiting_reply")
    except QuotaExhausted as error:
        status.update(state="quota_limited", error=str(error))
    except KeyboardInterrupt:
        status.update(state="interrupted")
        raise
    except (ValueError, ProviderError, OSError) as error:
        status.update(state="failed", error=f"{type(error).__name__}: {error}")
    finally:
        status["finished"] = datetime.now(timezone.utc).isoformat()
        status["models_returned"] = {"assessment": sorted(caller.models_returned)}
        status["usage"] = {"assessment": caller.usage}
        dump_json(folder / "status.json", status)
        log.write("interview_end", **status)
        log.close()
        cache.close()
    return status
