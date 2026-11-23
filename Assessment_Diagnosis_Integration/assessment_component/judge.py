"""Independent, post-interview assessments. Identifiers and denominators are checked in code."""
from uuid import uuid4
from .harness.providers import LLMCaller, ResponseCache
from .harness.runlog import EventLog
from .harness.util import dump_json, load_json
from .run import fields, require, nonempty, ids_valid

def rows_for(items, key, expected):
    require(isinstance(items, list), f"{key}: expected an array")
    ids = [entry[key] for entry in items]
    require(len(ids) == len(set(ids)) and set(ids) == set(expected), f"{key}: rate every supplied ID exactly once")

def check_turns(turns, allowed, needed=False):
    require(ids_valid(turns, allowed) and (not needed or turns), "Cite applicable turn IDs")

def grade(folder, judge, judge_model, prompts, actor, key, targets, mock, output):
    history = [t for t in load_json(folder/"transcript.json") if t["kind"] not in ("assessment_summary", "closing", "care_question", "care_answer")]
    findings = load_json(folder/"evidence.json")
    plans = load_json(folder/"planner_decisions.json")
    synthesis = load_json(folder/"synthesis.json")
    turns = {t["message_id"]:i for i,t in enumerate(history)}
    patient_ids = {t["message_id"] for t in history if t["speaker"]=="patient"}
    questions = {t["message_id"] for t in history if t["kind"]=="follow_up"}
    finding_ids = {f["finding_id"] for f in findings}
    target_map = {f"k{i}":target for i,target in enumerate(targets,1)}
    def check_interview(o):
        fields(o,"findings facts questions observations")
        rows_for(o["findings"],"id",finding_ids)
        for f in o["findings"]:
            fields(f,"id supported turns reason")
            require(type(f["supported"]) is bool and nonempty(f["reason"]), "Explain each finding")
            check_turns(f["turns"],patient_ids,True)
        require(isinstance(o["facts"],list), "Enumerate disclosed facts")
        for f in o["facts"]:
            fields(f,"fact turn matched")
            require(nonempty(f["fact"]) and f["turn"] in patient_ids and ids_valid(f["matched"],finding_ids), "Invalid fact match")
        rows_for(o["questions"],"turn",questions)
        for q in o["questions"]:
            fields(q,"turn repeated earlier_turn reason")
            require(type(q["repeated"]) is bool and nonempty(q["reason"]),"Explain question rating")
            earlier=q["earlier_turn"]
            if q["repeated"]:
                require(earlier in patient_ids and turns[earlier]<turns[q["turn"]],"Repeat needs an earlier patient answer")
            else:
                require(earlier is None,"Use null for a non-repeat")
        require(isinstance(o["observations"],list),"Provide observations array")
        for a in o["observations"]:
            fields(a,"issue turns comment")
            require(a["issue"] in ("assumption","missed_followup","ignored_decline","appropriate_followup","premature_finish","unnecessary_continuation","communication") and nonempty(a["comment"]),"Invalid observation")
            check_turns(a["turns"],turns,True)
        return []

    def check_conclusion(o):
        fields(o,"aligned supported turns reason coverage simulator_deviations")
        require(type(o["aligned"]) is bool and type(o["supported"]) is bool and nonempty(o["reason"]),"Explain both verdicts")
        check_turns(o["turns"],patient_ids,True)
        rows_for(o["coverage"],"id",target_map)
        for t in o["coverage"]:
            fields(t,"id status turns")
            require(t["status"] in ("disclosed","partial","declined_unknown","not_addressed"),"Invalid coverage")
            check_turns(t["turns"],patient_ids,t["status"]!="not_addressed")
            require(t["status"]!="not_addressed" or not t["turns"],"An unaddressed fact has no turn")
        require(isinstance(o["simulator_deviations"],list),"Provide deviation array")
        for d in o["simulator_deviations"]:
            fields(d,"turn reason")
            require(d["turn"] in patient_ids and nonempty(d["reason"]),"Invalid deviation")
        return []

    log=EventLog(output/f"judge_events_{uuid4().hex[:8]}.jsonl")
    cache=ResponseCache(output/"judge_responses.jsonl")
    caller=LLMCaller(judge,judge_model,log,cache,{"temperature":0,"max_tokens":judge_model["max_tokens"]})
    def evaluate(role,payload,validate):
        obj,details=caller.call_json(role,prompts[role],payload,validate,context=payload)
        if obj is None:
            raise ValueError(f"{role}: {details['errors']}")
        return obj
    try:
        a=evaluate("judge_interview",{"transcript":history,"findings":findings,"plans":plans,
                    "end_reason":load_json(folder/"status.json")["end_reason"]},check_interview)
        dump_json(output/"judge_interview.json",a)
        ref={k:key[k] for k in ("reference_presentation","reasoning_expected","common_error","qualifier","case_specific_evidence")}
        b=evaluate("judge_conclusion",{"transcript":history,"synthesis":synthesis,"findings":findings,"reference":ref,
                     "targets":target_map,"actor_baseline":actor},check_conclusion)
        dump_json(output/"judge_conclusion.json",b)
        counts={"aligned_and_supported":int(b["aligned"] and b["supported"]),
                "supported_findings":sum(x["supported"] for x in a["findings"]),"extracted":len(findings),
                "captured_facts":sum(bool(x["matched"]) for x in a["facts"]),"disclosed_facts":len(a["facts"]),
                "repeat_questions":sum(x["repeated"] for x in a["questions"]),"followup_questions":len(questions),
                "covered_targets":sum(x["status"]=="disclosed" for x in b["coverage"]),"reference_targets":len(targets)}
        dump_json(output/"score.json",{"mock":mock,**counts})
        return counts
    finally:
        dump_json(output/"judge_usage.json",{"returned_models":sorted(caller.models_returned),"usage":caller.usage})
        log.close()
        cache.close()
