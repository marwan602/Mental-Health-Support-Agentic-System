"""Unified patient record contract and prompt-formatting helpers.

Keeps Module 1's `assessment_handoff` immutable while maintaining `treatment_plan`
and live `therapy_state` (including `therapy_specific_parameters`) cleanly separated.
"""
import copy
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

SCHEMA_VERSION = "1.0.0"


def empty_therapy_state() -> dict[str, Any]:
    """Return the clean Session-1 therapy_state baseline."""
    return {
        "goals": [],
        "symptoms": [],
        "coping_strategies": [],
        "risk_history_notes": [],
        "therapy_specific_parameters": {
            "homework": [],
            "CBT": {
                "core_beliefs": [],
                "intermediate_beliefs": [],
                "automatic_thoughts": [],
            },
            "BA": {
                "avoidance_patterns": [],
                "target_activities": [],
            },
            "IPT": {
                "grief": [],
                "role_disputes": [],
                "role_transitions": [],
                "interpersonal_deficits": [],
            },
        },
    }


def create_record(
    *,
    name: str,
    age: int,
    gender: str = "Not specified",
    nationality: str = "Not specified",
    dob: Optional[str] = None,
    run_id: Optional[str] = None,
) -> dict[str, Any]:
    """Create a new unified patient record for a pipeline run."""
    if type(age) is not int or age < 18 or not isinstance(name, str) or not name.strip():
        raise ValueError("Supply an adult's name and integer age (18 or older).")
    clean_gender = gender.strip() if isinstance(gender, str) and gender.strip() else "Not specified"
    clean_nat = nationality.strip() if isinstance(nationality, str) and nationality.strip() else "Not specified"
    clean_dob = dob.strip() if isinstance(dob, str) and dob.strip() else None

    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id or uuid4().hex[:12],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "demographics": {
            "name": name.strip(),
            "age": age,
            "gender": clean_gender,
            "nationality": clean_nat,
            "dob": clean_dob,
        },
        "assessment_handoff": None,
        "assessment_meta": None,
        "treatment_input": None,
        "treatment_plan": None,
        "treatment_audit": None,
        "therapy_state": empty_therapy_state(),
        "sessions": [],
    }


def save_record(path: Path, record: dict[str, Any]) -> None:
    """Atomically write the patient record JSON to disk."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{uuid4().hex[:6]}.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def load_record(path: Path) -> dict[str, Any]:
    """Load a unified patient record JSON from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_treatment_input(record: dict[str, Any]) -> dict[str, Any]:
    """Package untouched assessment_handoff + demographics for Module 2."""
    handoff = record.get("assessment_handoff")
    if not isinstance(handoff, dict) or not handoff:
        raise ValueError("Cannot build treatment input before assessment_handoff is populated.")

    demo = record.get("demographics") or {}
    assessment = handoff.get("assessment") or {}
    label = assessment.get("primary_label")
    display = assessment.get("primary_label_display")
    if display and label:
        diagnosis = f"{display} ({label})"
    elif display or label:
        diagnosis = str(display or label)
    else:
        diagnosis = "Undetermined"

    finished_at = (handoff.get("source") or {}).get("interview_finished_at") or ""
    date_str = finished_at[:10] if len(finished_at) >= 10 else datetime.now(timezone.utc).date().isoformat()

    return {
        "name": demo.get("name", "N/A"),
        "age": demo.get("age", "N/A"),
        "dob": demo.get("dob") or "N/A",
        "date": date_str,
        "diagnosis": diagnosis,
        "review_status": assessment.get("review_status", "provisional_for_review"),
        "alternatives": copy.deepcopy(assessment.get("alternatives", [])),
        "interpretation_limits": copy.deepcopy(assessment.get("interpretation_limits", [])),
        "presenting_concerns": copy.deepcopy(handoff.get("presenting_concerns", [])),
        "functioning_baseline": copy.deepcopy(handoff.get("functioning_baseline", [])),
        "evidence": copy.deepcopy(handoff.get("evidence", [])),
        "planning_context": copy.deepcopy(handoff.get("planning_context", {})),
        "open_questions": copy.deepcopy(handoff.get("open_questions", [])),
        "next_step_preference": copy.deepcopy(handoff.get("next_step_preference", {})),
        "stop_reason": (handoff.get("source") or {}).get("stop_reason"),
    }


def extract_goals(record: dict[str, Any]) -> list[str]:
    """Return ordered, deduplicated patient goals from therapy_state and assessment_handoff."""
    ts_goals = (record.get("therapy_state") or {}).get("goals") or []
    pc_goals = (
        (record.get("assessment_handoff") or {})
        .get("planning_context", {})
        .get("goals", {})
        .get("statements", [])
    )
    handoff_goals = [s["text"] for s in pc_goals if isinstance(s, dict) and s.get("text")]

    combined: list[str] = []
    seen: set[str] = set()
    for g in [*ts_goals, *handoff_goals]:
        if isinstance(g, str) and g.strip():
            key = g.strip().casefold()
            if key not in seen:
                seen.add(key)
                combined.append(g.strip())
    return combined


def format_reported_findings(handoff: dict[str, Any]) -> list[str]:
    """Format active assessment evidence verbatim, keeping correction/retraction chains visible."""
    evidence = handoff.get("evidence") or []
    included_ids: set[str] = set()
    lines: list[str] = []

    for e in evidence:
        if not isinstance(e, dict):
            continue
        fid = e.get("finding_id") or "?"
        rel = e.get("related_finding_id")
        status = e.get("status")

        if status != "reported_present" and rel not in included_ids:
            continue
        if fid != "?":
            included_ids.add(fid)

        tag_parts = [f"{fid}, updates {rel}" if rel else fid]
        if status and status != "reported_present":
            tag_parts.append(status)
        tag = f"[{', '.join(tag_parts)}]"

        topic = e.get("topic") or "finding"
        tref = f" ({e['time_reference']})" if e.get("time_reference") else ""
        quote = e.get("quote") or ""
        lines.append(f'- {tag} {topic}{tref}: "{quote}"')

    return lines


def format_therapy_profile(record: dict[str, Any]) -> str:
    """Format the PATIENT PROFILE block for Therapy's Session Planner."""
    demo = record.get("demographics") or {}
    handoff = record.get("assessment_handoff") or {}
    assessment = handoff.get("assessment") or {}
    ts = record.get("therapy_state") or {}

    goals = extract_goals(record)
    findings = format_reported_findings(handoff)
    tracked_syms = [
        f"{s['name']} ({s.get('severity', 'unspecified')})"
        for s in ts.get("symptoms", [])
        if isinstance(s, dict) and s.get("name")
    ]
    homework = (ts.get("therapy_specific_parameters") or {}).get("homework", [])

    lines = [
        f"Age: {demo.get('age', 'Not specified')}, "
        f"Gender: {demo.get('gender', 'Not specified')}, "
        f"Nationality: {demo.get('nationality', 'Not specified')}"
    ]
    if assessment.get("primary_label_display"):
        lines.append(
            f"Provisional Assessment: {assessment['primary_label_display']} "
            f"({assessment.get('review_status', 'provisional_for_review')})"
        )
    lines.append(f"Goals: {goals if goals else ['Not documented yet']}")
    lines.append("Reported Findings (from assessment, verbatim):")
    lines.extend(findings if findings else ["- None documented"])
    if tracked_syms:
        lines.append(f"Tracked Symptoms (from therapy sessions): {tracked_syms}")
    lines.append(f"Active Homework: {homework}")
    return "\n".join(lines)


def format_therapy_brief(record: dict[str, Any]) -> str:
    """Format the PATIENT BRIEF block for DeliveryGuide generation."""
    handoff = record.get("assessment_handoff") or {}
    ts = record.get("therapy_state") or {}
    goals = extract_goals(record)
    findings = format_reported_findings(handoff)
    tracked_syms = [
        f"{s['name']} ({s.get('severity', 'unspecified')})"
        for s in ts.get("symptoms", [])
        if isinstance(s, dict) and s.get("name")
    ]

    lines = [
        f"Goals: {goals if goals else ['Not documented yet']}",
        "Reported Findings (from assessment, verbatim):",
    ]
    lines.extend(findings if findings else ["- None documented"])
    if tracked_syms:
        lines.append(f"Tracked Symptoms: {tracked_syms}")
    return "\n".join(lines)


def build_previous_session_summary(record: dict[str, Any]) -> str:
    """Build a concise summary string from prior completed therapy sessions."""
    sessions = record.get("sessions") or []
    if not sessions:
        return ""
    lines = []
    for idx, sess in enumerate(sessions, start=1):
        goal = sess.get("goal") or "N/A"
        interventions = sess.get("delivered_interventions") or []
        homework = sess.get("assigned_homework") or []
        lines.append(
            f"Session {idx}: Goal={goal}; "
            f"Delivered interventions={interventions}; "
            f"Assigned homework={homework}"
        )
    return "\n".join(lines)
