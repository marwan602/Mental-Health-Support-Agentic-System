"""Evaluate an already completed fictional session."""
import argparse
import json
from pathlib import Path
from uuid import uuid4

from .calibration import calibrate
from .handoff import VALIDATOR
from .harness.util import ROOT, dump_json, load_json
from .judge import grade
from .run import build_client
from .service import session_lock


def audit(folder):
    folder = Path(folder)
    status = load_json(folder/"status.json")
    if status["state"] != "complete":
        raise ValueError("Finish the interview before evaluation.")
    turns = {t["message_id"]: t for t in load_json(folder/"transcript.json")}
    evidence = load_json(folder/"evidence.json")
    handoff = load_json(folder/"assessment_handoff.json")
    problems = [e.message for e in VALIDATOR.iter_errors(handoff)]
    findings = {f["finding_id"] for f in evidence}
    def check_quote(source):
        turn = turns.get(source["message_id"], {})
        if turn.get("speaker") != "patient" or not source["quote"] or source["quote"] not in turn.get("text",""):
            problems.append("Unmatched patient quote at " + source["message_id"])
    for finding in evidence:
        check_quote(finding)
    if handoff.get("evidence") != evidence:
        problems.append("Handoff evidence differs from the extraction record.")
    if not problems:
        for field in handoff["planning_context"].values():
            for item in field["statements"]:
                check_quote(item["source"])
        if handoff["next_step_preference"]["source"]:
            check_quote(handoff["next_step_preference"]["source"])
        if not set(handoff["assessment"]["supporting_finding_ids"]) <= findings:
            problems.append("Conclusion cites an unknown finding.")
    report = {"passed":not problems,"checks":"Handoff structure, quoted patient text, evidence transfer and primary references",
              "issues":problems,"evidence_records":len(evidence),"end_reason":status["end_reason"]}
    dump_json(folder/"integration_audit.json", report)
    return report


def evaluate(folder, reference=None):
    folder = Path(folder)
    with session_lock(folder):
        report = audit(folder)
        if not report["passed"] or reference is None:
            return report
        if load_json(folder/"status.json")["mock"]:
            raise ValueError("Mock sessions demonstrate wiring only. Use a live fictional interview for judge scores.")
        case = load_json(reference)
        cfg = load_json(ROOT/"config.json")
        spec = cfg["judge"]
        client = build_client(cfg, spec, False)
        prompts = {r:(ROOT/"prompts"/(r+".txt")).read_text(encoding="utf8") for r in ("judge_interview","judge_conclusion")}
        output = folder/"evaluations"/uuid4().hex
        output.mkdir(parents=True)
        if not calibrate(output, client, spec, prompts["judge_interview"], False):
            raise ValueError(f"Judge failed calibration. See {output/'judge_check/report.json'}.")
        counts = grade(folder, client, spec, prompts, case["actor_baseline"], case["reference"], case["targets"], False, output)
        return {"evaluation_folder":str(output), "counts":counts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_folder", type=Path)
    parser.add_argument("--reference", type=Path, help="Optional fictional reference file for the separate AI judge")
    args = parser.parse_args()
    report = evaluate(args.session_folder, args.reference)
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if report.get("passed") is False else 0)
