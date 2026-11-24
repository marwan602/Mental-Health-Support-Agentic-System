"""End-to-end orchestrator and CLI connecting Assessment -> Treatment Planning -> Therapy."""
import argparse
import getpass
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable, Optional

from assessment_component import AssessmentService
from assessment_component.evaluate import evaluate

from . import REPO_ROOT
from .patient_record import (
    build_previous_session_summary,
    build_treatment_input,
    create_record,
    load_record,
    save_record,
)
from .therapy_runner import TherapySession
from .treatment_runner import generate_treatment_plan

DEFAULT_RUNS_DIR = REPO_ROOT / "pipeline_runs"
GATE_STOP_REASONS = {"patient_stop"}
GATE_LABELS = {"NO_DISORDER", "INSUFFICIENT_INFORMATION"}


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def check_clinical_gate(handoff: dict[str, Any]) -> list[str]:
    """Return human-readable caution reasons if Assessment flags stopping or non-clinical results."""
    reasons: list[str] = []
    source = handoff.get("source") or {}
    assessment = handoff.get("assessment") or {}
    next_step = handoff.get("next_step_preference") or {}

    stop_reason = source.get("stop_reason")
    if stop_reason in GATE_STOP_REASONS:
        reasons.append(f"Assessment ended early at patient request (stop_reason='{stop_reason}').")

    primary_label = assessment.get("primary_label")
    if primary_label in GATE_LABELS or primary_label is None:
        reasons.append(f"Provisional assessment label is '{primary_label}'.")

    if next_step.get("status") == "declined":
        reasons.append("Patient declined discussing next steps (next_step_preference='declined').")

    return reasons


def check_treatment_gate(record: dict[str, Any]) -> list[str]:
    """Return caution reasons if Stage 2's plan was flagged and lacks recorded approval."""
    audit = record.get("treatment_audit")
    if (
        isinstance(audit, dict)
        and audit.get("critical_safety_violation")
        and not record.get("treatment_review_approved")
    ):
        return [
            "Stage 2 Clinical Auditor flagged critical_safety_violation=True; "
            "clinician review is required before starting Therapy."
        ]
    return []


def ensure_api_keys(*, need_nvidia: bool, need_google: bool) -> None:
    """Verify required API keys (prompting securely in interactive terminals if missing)."""
    if need_google and not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

    if need_nvidia and not os.environ.get("NVIDIA_API_KEY", "").strip():
        if sys.stdin.isatty():
            val = getpass.getpass("Enter NVIDIA_API_KEY (hidden): ").strip()
            if val:
                os.environ["NVIDIA_API_KEY"] = val
        if not os.environ.get("NVIDIA_API_KEY", "").strip():
            raise RuntimeError("NVIDIA_API_KEY is required and not set.")

    if need_google and not os.environ.get("GOOGLE_API_KEY", "").strip():
        if sys.stdin.isatty():
            val = getpass.getpass("Enter GOOGLE_API_KEY / GEMINI_API_KEY (hidden): ").strip()
            if val:
                os.environ["GOOGLE_API_KEY"] = val
        if not os.environ.get("GOOGLE_API_KEY", "").strip():
            raise RuntimeError("GOOGLE_API_KEY (or GEMINI_API_KEY) is required and not set.")


def run_assessment_stage(
    run_dir: Path,
    record: dict[str, Any],
    record_path: Path,
    *,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> dict[str, Any]:
    """Run Stage 1 (AssessmentService) interactively and persist 01_assessment_handoff.json."""
    demo = record["demographics"]
    session_storage = run_dir / "assessment_session"
    service = AssessmentService(session_storage, mock=False)

    output_fn("\n=== STAGE 1: ASSESSMENT & DIAGNOSIS ===")
    in_progress_sid = (record.get("assessment_meta") or {}).get("in_progress_session_id")
    if in_progress_sid:
        output_fn(f"Resuming in-progress assessment session: {in_progress_sid}")
        turn = service.get_session(in_progress_sid)
    else:
        turn = service.start_session(fictional_name=demo["name"], age=demo["age"])
        record["assessment_meta"] = {"in_progress_session_id": turn["session_id"]}
        save_record(record_path, record)

    while turn["state"] == "awaiting_reply":
        output_fn(f"\nInterviewer: {turn['text']}")
        while True:
            try:
                reply = input_fn("Patient: ").strip()
            except (EOFError, KeyboardInterrupt):
                output_fn(
                    f"\nAssessment paused cleanly; resume anytime with: "
                    f"python -m integration.pipeline --resume \"{run_dir}\""
                )
                return record
            if not reply:
                output_fn("Please enter a non-empty reply.")
                continue
            try:
                turn = service.submit_reply(turn["session_id"], question_id=turn["question_id"], text=reply)
                break
            except ValueError as exc:
                output_fn(f"Input rejected: {exc}")

    output_fn(f"\nInterviewer (Closing): {turn['text']}")

    handoff = turn["handoff"]
    _write_json(run_dir / "01_assessment_handoff.json", handoff)

    session_folder = session_storage / turn["session_id"]
    audit = evaluate(session_folder)
    output_fn(f"[Stage 1] Assessment local contract audit passed: {audit['passed']}")

    record["assessment_handoff"] = handoff
    record["assessment_meta"] = {
        "session_id": turn["session_id"],
        "session_folder": str(session_folder),
        "end_reason": turn.get("end_reason"),
        "accepted_replies": turn.get("accepted_replies"),
        "audit": audit,
    }
    save_record(record_path, record)
    return record


def run_treatment_stage(
    run_dir: Path,
    record: dict[str, Any],
    record_path: Path,
    *,
    backend: str = "gemini",
    generator_model: Optional[str] = None,
    judge_model: Optional[str] = None,
    run_judge: bool = True,
    output_fn: Callable[[str], None] = print,
) -> dict[str, Any]:
    """Run Stage 2 (Treatment Plan Generator + Clinical Audit) and persist outputs."""
    output_fn("\n=== STAGE 2: TREATMENT PLANNING ===")
    treatment_input = build_treatment_input(record)
    _write_json(run_dir / "02_treatment_input.json", treatment_input)

    result = generate_treatment_plan(
        treatment_input,
        backend=backend,  # type: ignore[arg-type]
        run_judge=run_judge,
        generator_model=generator_model,
        judge_model=judge_model,
    )

    _write_text(run_dir / "02_treatment_plan.txt", result["treatment_plan"])
    _write_text(run_dir / "02_guideline_context.txt", result["guideline_context"])
    audit_payload: dict[str, Any] = {
        "backend": result["backend"],
        "generator_model": result["generator_model"],
        "judge_model": result["judge_model"],
        "audit": result["audit"],
        "audit_raw": result["audit_raw"],
    }
    if not run_judge:
        audit_payload["skipped"] = True
    _write_json(run_dir / "02_treatment_audit.json", audit_payload)

    record["treatment_input"] = treatment_input
    record["treatment_plan"] = result["treatment_plan"]
    record["treatment_audit"] = result["audit"]
    record["treatment_review_approved"] = False
    save_record(record_path, record)

    output_fn("\n--- GENERATED TREATMENT PLAN ---")
    output_fn(result["treatment_plan"])

    audit = result.get("audit")
    if audit:
        output_fn(
            f"\n[Stage 2] Clinical Audit Overall Score: {audit['overall_score']:.2f} / 5.0 "
            f"| Critical Safety Violation: {audit['critical_safety_violation']}"
        )
        if audit.get("critical_safety_violation"):
            output_fn("[WARNING] CRITICAL SAFETY VIOLATION FLAGGED BY CLINICAL AUDITOR. Clinician review required.")
    elif run_judge:
        output_fn("\n[Stage 2] Warning: Clinical audit output could not be parsed; see 02_treatment_audit.json.")

    return record


def run_therapy_stage(
    run_dir: Path,
    record: dict[str, Any],
    record_path: Path,
    *,
    max_turns: int = 50,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> dict[str, Any]:
    """Run Stage 3 (Conversational Therapy Session + Delta StatePatch) interactively."""
    output_fn("\n=== STAGE 3: CONVERSATIONAL THERAPY ===")
    prev_summary = build_previous_session_summary(record)
    session = TherapySession(record, previous_session_summary=prev_summary, max_turns=max_turns)

    start_res = session.start()
    output_fn(f"\n[Session Plan Goal]: {start_res['session_plan']['session_goal']}")
    output_fn(f"\nTherapist: {start_res['text']}")
    output_fn("(Type 'quit' or 'exit' at any prompt to end the session and save progress.)")

    state = start_res["state"]
    while state == "awaiting_reply":
        try:
            reply = input_fn("\nPatient: ").strip()
        except (EOFError, KeyboardInterrupt):
            output_fn("\nEnding therapy session and saving state...")
            break
        if reply.lower() in ("quit", "exit"):
            break
        if not reply:
            output_fn("Please enter a non-empty reply (or type 'quit' to end).")
            continue

        try:
            turn_res = session.submit_reply(reply)
        except Exception as exc:
            if session.controller and session.controller.history_records:
                output_fn(
                    f"\n[Stage 3] Provider error ({type(exc).__name__}: {str(exc)[:160]}). "
                    "Saving completed turns..."
                )
                break
            raise
        output_fn(f"\nTherapist: {turn_res['text']}")
        state = turn_res["state"]

    finish_res = session.finish()
    archive = finish_res["session_archive"]
    if archive is None:
        output_fn("\n[Stage 3] Ended with 0 turns; no session recorded.")
        return record

    updated_record = finish_res["record"]
    session_num = archive["session_number"]

    _write_json(run_dir / f"03_therapy_session_{session_num}.json", archive)
    save_record(record_path, updated_record)

    output_fn(
        f"\n[Stage 3] Session {session_num} saved ({len(archive['history'])} turns). "
        f"StatePatch keys updated: {list(finish_res['state_patch'].keys())}"
    )
    return updated_record


def _prompt_adult_age(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> int:
    """Prompt until a valid whole-year adult age (18+) is entered."""
    while True:
        raw = input_fn("Fictional patient age (18+): ").strip()
        try:
            age = int(raw)
        except ValueError:
            output_fn("Please enter age as a whole number (e.g., 30).")
            continue
        if age < 18:
            output_fn("Age must be 18 or older.")
            continue
        return age


def _resolve_stages(record: dict[str, Any], stage: Optional[str]) -> list[str]:
    """Determine which pipeline stages to run given an optional explicit `--stage`."""
    if stage in ("assessment", "treatment", "therapy"):
        return [stage]
    stages: list[str] = []
    if not record.get("assessment_handoff"):
        stages.append("assessment")
    if not record.get("treatment_plan"):
        stages.append("treatment")
    stages.append("therapy")
    return stages


def run_pipeline(
    *,
    name: Optional[str] = None,
    age: Optional[int] = None,
    gender: str = "Not specified",
    nationality: str = "Not specified",
    dob: Optional[str] = None,
    resume_dir: Optional[Path] = None,
    stage: Optional[str] = None,
    treatment_backend: str = "gemini",
    treatment_model: Optional[str] = None,
    judge_model: Optional[str] = None,
    run_judge: bool = True,
    runs_dir: Path = DEFAULT_RUNS_DIR,
    max_therapy_turns: int = 50,
    force: bool = False,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> tuple[Path, dict[str, Any]]:
    """Run the full A->Z pipeline or resume from an existing run directory."""
    if resume_dir is not None:
        run_dir = Path(resume_dir).resolve()
        record_path = run_dir / "patient_record.json"
        if not record_path.is_file():
            raise FileNotFoundError(f"Cannot resume: {record_path} not found.")
        record = load_record(record_path)
    else:
        while not name or not name.strip():
            name = input_fn("Fictional patient name: ").strip()
        if age is None:
            age = _prompt_adult_age(input_fn=input_fn, output_fn=output_fn)
        record = create_record(
            name=name,
            age=age,
            gender=gender,
            nationality=nationality,
            dob=dob,
        )
        run_dir = Path(runs_dir).resolve() / record["run_id"]
        record_path = run_dir / "patient_record.json"
        save_record(record_path, record)

    output_fn(f"Pipeline run directory: {run_dir}")
    stages_to_run = _resolve_stages(record, stage)

    if "assessment" in stages_to_run:
        record = run_assessment_stage(run_dir, record, record_path, input_fn=input_fn, output_fn=output_fn)
        if not record.get("assessment_handoff"):
            return run_dir, record

    if "treatment" in stages_to_run:
        reasons = check_clinical_gate(record.get("assessment_handoff") or {})
        if reasons and not force:
            output_fn("\n[Clinical Gate Notice]")
            for r in reasons:
                output_fn(f"  - {r}")
            answer = input_fn("Continue to Treatment Planning anyway? [y/N]: ").strip().lower()
            if answer not in ("y", "yes"):
                output_fn("Pipeline paused before Treatment Planning. Use --resume to continue later.")
                return run_dir, record
        record = run_treatment_stage(
            run_dir,
            record,
            record_path,
            backend=treatment_backend,
            generator_model=treatment_model,
            judge_model=judge_model,
            run_judge=run_judge,
            output_fn=output_fn,
        )

    if "therapy" in stages_to_run:
        t_reasons = check_treatment_gate(record)
        if t_reasons and not force:
            output_fn("\n[Treatment Safety Gate Notice]")
            for r in t_reasons:
                output_fn(f"  - {r}")
            answer = input_fn("Continue to Therapy anyway? [y/N]: ").strip().lower()
            if answer not in ("y", "yes"):
                output_fn("Pipeline paused before Therapy. Review 02_treatment_plan.txt and use --resume when approved.")
                return run_dir, record
            record["treatment_review_approved"] = True
            save_record(record_path, record)
        record = run_therapy_stage(
            run_dir,
            record,
            record_path,
            max_turns=max_therapy_turns,
            input_fn=input_fn,
            output_fn=output_fn,
        )

    output_fn(f"\nPipeline run complete. Record saved to: {record_path}")
    return run_dir, record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", help="Fictional patient name (adult 18+)")
    parser.add_argument("--age", type=int, help="Fictional patient age in whole years (18+)")
    parser.add_argument("--gender", default="Not specified", help="Optional gender for Therapy planner context")
    parser.add_argument("--nationality", default="Not specified", help="Optional nationality for Therapy planner context")
    parser.add_argument("--dob", default=None, help="Optional date of birth for Treatment Plan header")
    parser.add_argument("--resume", type=Path, default=None, help="Path to existing pipeline_runs/<run_id> folder")
    parser.add_argument(
        "--stage",
        choices=("assessment", "treatment", "therapy"),
        default=None,
        help="Run only one specific stage (defaults to running remaining stages in sequence)",
    )
    parser.add_argument(
        "--treatment-backend",
        choices=("gemini", "nvidia", "local"),
        default="gemini",
        help="Model backend for Treatment Planning (default: gemini)",
    )
    parser.add_argument("--treatment-model", default=None, help="Override Treatment Plan generator model ID")
    parser.add_argument("--judge-model", default=None, help="Override Treatment Plan audit judge model ID")
    parser.add_argument("--skip-judge", action="store_true", help="Skip the Treatment Planning clinical audit step")
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR, help="Directory for pipeline_runs outputs")
    parser.add_argument("--max-therapy-turns", type=int, default=50, help="Maximum turns per therapy session")
    parser.add_argument("--force", action="store_true", help="Proceed past Stage 1 clinical gate without prompting")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if args.stage == "assessment":
        need_nvidia, need_google = True, False
    elif args.stage == "treatment":
        need_nvidia = args.treatment_backend == "nvidia"
        need_google = args.treatment_backend == "gemini"
    elif args.stage == "therapy":
        need_nvidia, need_google = True, True
    else:
        need_nvidia = True
        need_google = True  # Stage 3 always uses Gemma via Google API

    ensure_api_keys(need_nvidia=need_nvidia, need_google=need_google)

    run_pipeline(
        name=args.name,
        age=args.age,
        gender=args.gender,
        nationality=args.nationality,
        dob=args.dob,
        resume_dir=args.resume,
        stage=args.stage,
        treatment_backend=args.treatment_backend,
        treatment_model=args.treatment_model,
        judge_model=args.judge_model,
        run_judge=not args.skip_judge,
        runs_dir=args.runs_dir,
        max_therapy_turns=args.max_therapy_turns,
        force=args.force,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
