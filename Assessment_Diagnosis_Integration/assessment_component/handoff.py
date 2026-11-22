"""Build a source-linked handoff using only the spoken interview and its assessment."""
from jsonschema import Draft202012Validator, FormatChecker

from .harness.util import ROOT, load_json

PROTOCOL = "adult-semi-structured-no-kb-v7-interactive-1"
SCHEMA = load_json(ROOT / "assessment_handoff.schema.json")
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
CARE_FIELDS = SCHEMA["properties"]["planning_context"]["required"]

def empty_notes():
    return {"items": [], "concern_ids": [], "function_ids": [], "next_step": None}

def checked_context(notes, history, evidence):
    if not isinstance(notes, dict) or set(notes) != set(empty_notes()):
        raise ValueError("Use exactly items, concern_ids, function_ids and next_step.")
    utterances = {t["message_id"]: t["text"] for t in history if t["speaker"] == "patient"}
    def citation(row):
        turn, quote = row["message_id"], row["quote"]
        if not isinstance(turn, str) or not isinstance(quote, str) or not quote.strip() or quote not in utterances.get(turn, ""):
            raise ValueError("Cite an exact nonempty quote from the indicated patient message.")
        return {"message_id":turn, "quote":quote}

    context = {name:{"status":"not_documented","statements":[]} for name in CARE_FIELDS}
    if not isinstance(notes["items"], list):
        raise ValueError("items must be a list.")
    for row in notes["items"]:
        if not isinstance(row,dict) or set(row) != {"field","status","message_id","quote"}:
            raise ValueError("Each item needs field, status, message_id and quote.")
        if row["field"] not in CARE_FIELDS or row["status"] not in ("reported","patient_unsure","declined"):
            raise ValueError("Unknown care field or status.")
        item = context[row["field"]]
        if item["status"] not in ("not_documented",row["status"]):
            raise ValueError("Use the latest applicable status for each field.")
        source = citation(row)
        item["status"] = row["status"]
        entry = {"text":source["quote"], "source":source}
        if entry not in item["statements"]:
            item["statements"].append(entry)
    choice = {"status":"not_discussed","source":None}
    row = notes["next_step"]
    if row is not None:
        if not isinstance(row,dict) or set(row) != {"status","message_id","quote"} or row["status"] not in ("wants_to_discuss","declined","undecided"):
            raise ValueError("Invalid next-step preference.")
        choice = {"status":row["status"], "source":citation(row)}
    known = {e["finding_id"] for e in evidence}
    for name in ("concern_ids","function_ids"):
        ids = notes[name]
        if not isinstance(ids,list) or any(not isinstance(i,str) or i not in known for i in ids):
            raise ValueError(f"{name} must contain only supplied finding IDs.")
    return context, choice

def build_handoff(source, notes, history, evidence, synthesis, labels):
    context, choice = checked_context(notes, history, evidence)
    by_id = {e["finding_id"]:e for e in evidence}
    def points(key):
        return [{"text":by_id[i]["quote"],"finding_ids":[i]} for i in dict.fromkeys(notes[key])]
    result = {
        "schema_version":SCHEMA["properties"]["schema_version"]["const"], "source":source,
        "presenting_concerns":points("concern_ids"), "functioning_baseline":points("function_ids"),
        "evidence":evidence, "assessment":{
            "review_status":"provisional_for_review","primary_label":synthesis["provisional_label"],
            "primary_label_display":labels[synthesis["provisional_label"]],
            "supporting_finding_ids":synthesis["supporting_finding_ids"], "alternatives":synthesis["alternatives"],
            "interpretation_limits":synthesis["missing_information"]},
        "planning_context":context,
        "open_questions":[{"question":"What is known about the following assessment gap? " + row["gap"],
                           "why_it_matters":row["why_it_matters"],
                           "related_finding_ids":[e["finding_id"] for e in evidence if e["message_id"] == row["message_id"]
                                                  and (e["quote"] in row["quote"] or row["quote"] in e["quote"])]}
                          for row in synthesis["reviewed_gaps"]],
        "next_step_preference":choice}
    error = next(VALIDATOR.iter_errors(result), None)
    if error:
        raise ValueError("Handoff schema: " + error.message)
    return result
