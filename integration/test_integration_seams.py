"""Integration seam, schema, controller, and real NICE PDF RAG tests."""
import copy
import gc
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from integration import REPO_ROOT
from integration.patient_record import (
    build_previous_session_summary,
    build_treatment_input,
    create_record,
    format_reported_findings,
    format_therapy_brief,
    format_therapy_profile,
    load_record,
    save_record,
)
from integration.pipeline import check_clinical_gate
from integration.therapy_runner import (
    MODALITY_PATTERNS,
    ClinicalSessionController,
    DeliveryGuide,
    HomeworkUpdate,
    InterventionStep,
    SessionStateTracker,
    StatePatch,
    SymptomUpdate,
    TherapyDecision,
    TherapyItemUpdate,
    TherapySession,
    _parse_structured_json,
    apply_state_patch,
    build_clinical_tools,
    call_structured,
    expand_clinical_query,
    load_therapy_libraries,
    make_session_plan_schema,
    repair_plan_deterministic,
    retrieve_candidates,
    validate_plan_rules,
    validate_replan_rules,
)
from integration.treatment_runner import (
    DEFAULT_GEMINI_MODEL,
    DEFAULT_NVIDIA_MODEL,
    ClinicalPlanEvaluation,
    _extract_text,
    _invoke_gemini_with_retry,
    build_guideline_query,
    build_plan_header,
    generate_treatment_plan,
    load_guideline_retriever,
    parse_evaluation_json,
    parse_treatment_plan,
    retrieve_guideline_context,
)


def _sample_handoff() -> dict:
    return {
        "schema_version": "0.3.0",
        "source": {
            "protocol": "adult-semi-structured-no-kb-v7-interactive-1",
            "run_id": "run123",
            "case_id": "case123",
            "interview_finished_at": "2026-11-24T10:15:00+00:00",
            "stop_reason": "planner_finish",
        },
        "presenting_concerns": [{"text": "Feeling low for three weeks.", "finding_ids": ["f0001"]}],
        "functioning_baseline": [{"text": "Missed a shift due to poor concentration.", "finding_ids": ["f0003"]}],
        "evidence": [
            {
                "finding_id": "f0001",
                "topic": "low mood",
                "status": "reported_present",
                "time_reference": "3 weeks",
                "attributes": {},
                "quote": "I've felt low for three weeks.",
                "message_id": "m0002",
                "context_message_ids": [],
                "related_finding_id": None,
            },
            {
                "finding_id": "f0002",
                "topic": "alcohol use",
                "status": "reported_absent",
                "time_reference": None,
                "attributes": {},
                "quote": "No, I never drink alcohol.",
                "message_id": "m0004",
                "context_message_ids": [],
                "related_finding_id": None,
            },
            {
                "finding_id": "f0003",
                "topic": "work impact",
                "status": "reported_present",
                "time_reference": None,
                "attributes": {},
                "quote": "I missed a shift because I couldn't concentrate.",
                "message_id": "m0006",
                "context_message_ids": [],
                "related_finding_id": None,
            },
            {
                "finding_id": "f0004",
                "topic": "low mood",
                "status": "reported_present",
                "time_reference": "about 2 months",
                "attributes": {},
                "quote": "Actually it started closer to two months ago.",
                "message_id": "m0008",
                "context_message_ids": ["m0002"],
                "related_finding_id": "f0001",
            },
            {
                "finding_id": "f0005",
                "topic": "elevated mood",
                "status": "unclear",
                "time_reference": None,
                "attributes": {},
                "quote": "Maybe once, I am not sure.",
                "message_id": "m0010",
                "context_message_ids": [],
                "related_finding_id": None,
            },
            {
                "finding_id": "f0006",
                "topic": "work impact",
                "status": "reported_absent",
                "time_reference": None,
                "attributes": {},
                "quote": "Wait, I actually made that shift, it was an earlier week I called off.",
                "message_id": "m0012",
                "context_message_ids": ["m0006"],
                "related_finding_id": "f0003",
            },
        ],
        "assessment": {
            "review_status": "provisional_for_review",
            "primary_label": "MDD_SINGLE",
            "primary_label_display": "Major depressive disorder, single episode",
            "supporting_finding_ids": ["f0001", "f0004"],
            "alternatives": [],
            "interpretation_limits": ["Alcohol timing only partially explored."],
        },
        "planning_context": {
            "reason_for_seeking_help": {"status": "not_documented", "statements": []},
            "goals": {
                "status": "reported",
                "statements": [{"text": "Sleep better and feel steadier at work.", "source": {"message_id": "m0014", "quote": "Sleep better and feel steadier at work."}}],
            },
            "preferences": {"status": "not_documented", "statements": []},
            "barriers": {"status": "not_documented", "statements": []},
            "strengths_and_supports": {"status": "not_documented", "statements": []},
            "current_support_and_care": {"status": "not_documented", "statements": []},
            "previous_care_and_response": {"status": "not_documented", "statements": []},
            "coping_strategies": {"status": "not_documented", "statements": []},
        },
        "open_questions": [],
        "next_step_preference": {
            "status": "wants_to_discuss",
            "source": {"message_id": "m0014", "quote": "Yes, I would like to discuss support."},
        },
    }


class PatientRecordTests(unittest.TestCase):
    def test_create_record_validation_and_therapy_specific_parameters(self):
        with self.assertRaises(ValueError):
            create_record(name="Alex", age=17)
        with self.assertRaises(ValueError):
            create_record(name="Alex", age=True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            create_record(name="   ", age=25)

        rec = create_record(name="Alex", age=30)
        tsp = rec["therapy_state"]["therapy_specific_parameters"]
        self.assertEqual(tsp["homework"], [])
        self.assertEqual(set(tsp["CBT"].keys()), {"core_beliefs", "intermediate_beliefs", "automatic_thoughts"})
        self.assertEqual(set(tsp["BA"].keys()), {"avoidance_patterns", "target_activities"})
        self.assertEqual(set(tsp["IPT"].keys()), {"grief", "role_disputes", "role_transitions", "interpersonal_deficits"})

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "patient_record.json"
            rec = create_record(name="Nour", age=34, gender="female", nationality="Egyptian")
            rec["assessment_handoff"] = _sample_handoff()
            save_record(path, rec)
            loaded = load_record(path)
            self.assertEqual(loaded, rec)

    def test_build_treatment_input_preserves_full_evidence(self):
        rec = create_record(name="Alex", age=30)
        with self.assertRaises(ValueError):
            build_treatment_input(rec)

        rec["assessment_handoff"] = _sample_handoff()
        ti = build_treatment_input(rec)
        self.assertEqual(ti["name"], "Alex")
        self.assertEqual(ti["age"], 30)
        self.assertEqual(ti["date"], "2026-11-24")
        self.assertEqual(ti["diagnosis"], "Major depressive disorder, single episode (MDD_SINGLE)")
        self.assertEqual(len(ti["evidence"]), 6)
        statuses = {e["status"] for e in ti["evidence"]}
        self.assertEqual(statuses, {"reported_present", "reported_absent", "unclear"})

    def test_format_reported_findings_filters_denials_and_keeps_updates_and_retractions(self):
        lines = format_reported_findings(_sample_handoff())
        joined = "\n".join(lines)
        self.assertIn('[f0001] low mood (3 weeks): "I\'ve felt low for three weeks."', joined)
        self.assertIn('[f0004, updates f0001] low mood (about 2 months):', joined)
        self.assertIn('[f0006, updates f0003, reported_absent] work impact:', joined)
        # Standalone reported_absent (f0002) and standalone unclear (f0005) are omitted
        self.assertNotIn("f0002", joined)
        self.assertNotIn("f0005", joined)

    def test_profile_brief_and_previous_summary_handle_empty_goals_and_session2(self):
        rec = create_record(name="Alex", age=30)
        handoff = _sample_handoff()
        handoff["planning_context"]["goals"] = {"status": "not_documented", "statements": []}
        rec["assessment_handoff"] = handoff

        self.assertEqual(build_previous_session_summary(rec), "")
        prof = format_therapy_profile(rec)
        self.assertIn("['Not documented yet']", prof)
        self.assertIn("Reported Findings (from assessment, verbatim):", prof)

        rec["therapy_state"]["symptoms"].append({"name": "insomnia", "severity": "moderate", "duration": "unspecified", "description": ""})
        rec["therapy_state"]["therapy_specific_parameters"]["homework"].append({"task": "Morning walk", "status": "assigned"})
        rec["sessions"].append({"goal": "Build morning routine", "delivered_interventions": ["BA-01"], "assigned_homework": ["Morning walk"]})

        prof2 = format_therapy_profile(rec)
        brief2 = format_therapy_brief(rec)
        prev2 = build_previous_session_summary(rec)
        self.assertIn("insomnia (moderate)", prof2)
        self.assertIn("Morning walk", prof2)
        self.assertIn("insomnia (moderate)", brief2)
        self.assertIn("Session 1: Goal=Build morning routine", prev2)
        self.assertNotIn("Deferred to next session", prev2)

    def test_state_patch_descriptions_and_deferred_topics_continuity(self):
        schema = StatePatch.model_json_schema()
        props = schema["properties"]
        for field in ("homework_updates", "symptom_updates", "next_session_topics"):
            self.assertTrue(props[field].get("description", "").strip(), f"Missing description for {field}")
        hw_props = schema["$defs"]["HomeworkUpdate"]["properties"]
        sym_props = schema["$defs"]["SymptomUpdate"]["properties"]
        self.assertTrue(hw_props["task"].get("description", "").strip())
        self.assertTrue(sym_props["name"].get("description", "").strip())

        patch = StatePatch(
            homework_updates=[HomeworkUpdate(task="1 AM screen timer", status="assigned")],
            symptom_updates=[SymptomUpdate(name="low mood", severity="moderate", description="Baseline 4/10")],
            next_session_topics=["Explore detachment at work"],
        )
        self.assertEqual(patch.next_session_topics, ["Explore detachment at work"])

        rec = create_record(name="Alex", age=30)
        rec["sessions"].append({
            "goal": "Week 1 plan",
            "delivered_interventions": ["ba_activity_scheduling_and_structuring"],
            "assigned_homework": ["1 AM screen timer"],
            "next_session_topics": patch.next_session_topics,
        })
        summary = build_previous_session_summary(rec)
        self.assertIn("Deferred to next session=['Explore detachment at work']", summary)

    def test_planning_context_session2_and_no_dangling_update_tag(self):
        rec = create_record(name="Alex", age=30)
        handoff = _sample_handoff()
        handoff["evidence"].extend(
            [
                {
                    "finding_id": "f0099",
                    "topic": "sleep",
                    "status": "unclear",
                    "time_reference": None,
                    "attributes": {},
                    "quote": "Not sure when the early waking began.",
                    "message_id": "m0099",
                    "context_message_ids": [],
                    "related_finding_id": None,
                },
                {
                    "finding_id": "f0100",
                    "topic": "sleep",
                    "status": "reported_present",
                    "time_reference": "2 weeks",
                    "attributes": {},
                    "quote": "Definitely waking at 4am every morning.",
                    "message_id": "m0100",
                    "context_message_ids": ["m0099"],
                    "related_finding_id": "f0099",
                },
            ]
        )
        handoff["planning_context"]["preferences"] = {
            "status": "reported",
            "statements": [{"text": "Prefers practical between-session exercises."}],
        }
        handoff["planning_context"]["barriers"] = {
            "status": "reported",
            "statements": [{"text": "Late work shifts make evening sessions hard."}],
        }
        handoff["open_questions"] = [{"question": "Clarify onset of morning waking.", "topic": "sleep"}]
        rec["assessment_handoff"] = handoff

        findings_text = "\n".join(format_reported_findings(handoff))
        self.assertIn("[f0100] sleep (2 weeks):", findings_text)
        self.assertNotIn("updates f0099", findings_text)

        rec["therapy_state"]["therapy_specific_parameters"]["CBT"]["automatic_thoughts"].append(
            {"thought": "I always fail at work", "status": "examined"}
        )
        rec["therapy_state"]["coping_strategies"].append("Box breathing")
        rec["therapy_state"]["risk_history_notes"].append("Denied intent in session 1")

        profile = format_therapy_profile(rec)
        self.assertIn("Documented Context (from assessment):", profile)
        self.assertIn("- Preferences: Prefers practical between-session exercises.", profile)
        self.assertIn("- Barriers: Late work shifts make evening sessions hard.", profile)
        self.assertIn("Open Questions (from assessment):", profile)
        self.assertIn("- Clarify onset of morning waking.", profile)
        self.assertIn("Prior Therapy Notes:", profile)
        self.assertIn("CBT automatic thoughts: I always fail at work (examined)", profile)
        self.assertIn("Session Coping Strategies: Box breathing", profile)
        self.assertIn("Session Risk Notes: Denied intent in session 1", profile)


class TreatmentRunnerTests(unittest.TestCase):
    def test_extract_text_header_and_parsers(self):
        self.assertEqual(_extract_text("<think>internal</think>Final answer"), "Final answer")
        blocks = [{"type": "thinking", "thinking": "hidden"}, {"type": "text", "text": "Visible text"}]
        self.assertEqual(_extract_text(blocks), "Visible text")

        rec = create_record(name="Alex", age=30)
        rec["assessment_handoff"] = _sample_handoff()
        ti = build_treatment_input(rec)
        header = build_plan_header(ti)
        self.assertIn("Client Name: Alex", header)
        self.assertIn("Age: 30", header)
        self.assertIn("Date: 2026-11-24", header)
        self.assertIn("Diagnosis: Major depressive disorder, single episode (MDD_SINGLE)", header)

        self.assertEqual(parse_treatment_plan("preamble\n<treatment_plan>\nPlan body\n</treatment_plan>"), "Plan body")
        with self.assertRaises(ValueError):
            parse_treatment_plan("No tags here")

        eval_raw = """<evaluation_json>
        {
          "guideline_grounding": {"score": 5, "justification": "Grounded."},
          "safety_and_boundaries": {"score": 5, "justification": "Safe."},
          "timeline_continuity": {"score": 4, "justification": "Sequential."},
          "individualization": {"score": 4, "justification": "Tailored."},
          "critical_safety_violation": false,
          "overall_score": 4.5,
          "summary_feedback": "Solid provisional plan."
        }
        </evaluation_json>"""
        parsed = parse_evaluation_json(eval_raw)
        self.assertIsInstance(parsed, ClinicalPlanEvaluation)
        assert parsed is not None
        self.assertEqual(parsed.overall_score, 4.5)
        self.assertFalse(parsed.critical_safety_violation)

    def test_parse_treatment_plan_fallback_and_diagnostics(self):
        with self.assertRaises(ValueError) as ctx1:
            parse_treatment_plan("No tags here")
        self.assertIn("len=12", str(ctx1.exception))
        self.assertIn("No tags here", str(ctx1.exception))

        with self.assertRaises(ValueError):
            parse_treatment_plan("No tags here", allow_fallback=True)

        valid_body = (
            "Provisional Psychotherapy Treatment Plan (for clinician review)\n\n"
            "Goals: Restore morning energy and work engagement.\n\n"
            "Phase 1 — Week 1: CBT psychoeducation and Behavioral Activation monitoring.\n"
            "Phase 2 — Week 2: Graded activity scheduling intervention and thought records.\n"
            "Final Phase — Week 12: Relapse prevention planning and early warning signs."
        )
        with self.assertRaises(ValueError):
            parse_treatment_plan("<treatment_plan>\n" + valid_body)
        self.assertEqual(parse_treatment_plan("<treatment_plan>\n" + valid_body, allow_fallback=True), valid_body)

        with self.assertRaises(ValueError):
            parse_treatment_plan(valid_body)
        self.assertEqual(parse_treatment_plan("```\n" + valid_body + "\n```", allow_fallback=True), valid_body)

    def test_real_nice_pdf_rag_and_persistence(self):
        rec = create_record(name="Alex", age=30)
        rec["assessment_handoff"] = _sample_handoff()
        ti = build_treatment_input(rec)

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            chroma_dir = Path(tmp) / "chroma_nice"
            retriever = load_guideline_retriever(
                guideline_dir=REPO_ROOT / "Treatment Planning",
                persist_dir=chroma_dir,
            )
            ctx = retrieve_guideline_context(ti, retriever)
            for tag in ("[G1]", "[G2]", "[G3]", "[G4]", "[G5]"):
                self.assertIn(tag, ctx)
            self.assertIn("Source: NICE_Guidelines.pdf, page ", ctx)
            self.assertNotIn("\\NICE_Guidelines.pdf", ctx)
            self.assertTrue(any(chroma_dir.iterdir()))

            # Reuse persisted Chroma index even without re-reading the PDF directory
            cached_retriever = load_guideline_retriever(
                guideline_dir=Path(tmp) / "nonexistent_dir",
                persist_dir=chroma_dir,
            )
            ctx2 = retrieve_guideline_context(ti, cached_retriever)
            self.assertIn("Source: NICE_Guidelines.pdf, page ", ctx2)
            del retriever, cached_retriever
            gc.collect()

    def test_guideline_query_fits_minilm_256_tokens(self):
        os.environ.setdefault("USE_TF", "0")
        from transformers import AutoTokenizer

        rec = create_record(name="Alex", age=30)
        rec["assessment_handoff"] = _sample_handoff()
        ti = build_treatment_input(rec)
        q = build_guideline_query(ti)
        self.assertLessEqual(len(q), 850)
        self.assertIn("Major depressive disorder, single episode", q)
        self.assertIn("I've felt low for three weeks.", q)
        self.assertIn("Sleep better and feel steadier at work.", q)

        tok = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2", local_files_only=True)
        token_ids = tok.encode(q, add_special_tokens=True)
        self.assertLessEqual(len(token_ids), 256)

    def test_chroma_cache_invalidation_on_pdf_change(self):
        rec = create_record(name="Alex", age=30)
        rec["assessment_handoff"] = _sample_handoff()
        ti = build_treatment_input(rec)

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            g_dir = Path(tmp) / "guidelines"
            g_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / "Treatment Planning" / "NICE_Guidelines.pdf", g_dir / "NICE_Guidelines.pdf")
            chroma_dir = Path(tmp) / "chroma_nice"

            r1 = load_guideline_retriever(guideline_dir=g_dir, persist_dir=chroma_dir)
            meta_path = chroma_dir / "index_meta.json"
            self.assertTrue(meta_path.is_file())
            saved = json.loads(meta_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["pdfs"][0]["name"], "NICE_Guidelines.pdf")
            orig_size = saved["pdfs"][0]["size"]
            self.assertGreater(orig_size, 0)
            del r1
            gc.collect()

            saved["pdfs"][0]["size"] = 0
            meta_path.write_text(json.dumps(saved), encoding="utf-8")

            r2 = load_guideline_retriever(guideline_dir=g_dir, persist_dir=chroma_dir)
            rebuilt = json.loads(meta_path.read_text(encoding="utf-8"))
            self.assertEqual(rebuilt["pdfs"][0]["size"], orig_size)
            ctx = retrieve_guideline_context(ti, r2)
            for tag in ("[G1]", "[G2]", "[G3]", "[G4]", "[G5]"):
                self.assertIn(tag, ctx)
            del r2
            gc.collect()

    def test_runtime_env_model_override(self):
        rec = create_record(name="Alex", age=30)
        rec["assessment_handoff"] = _sample_handoff()
        ti = build_treatment_input(rec)

        with (
            patch("integration.treatment_runner.load_guideline_retriever", return_value=object()),
            patch("integration.treatment_runner.retrieve_guideline_context", return_value="[G1] Source: NICE.pdf, page 1\nTest"),
            patch("integration.treatment_runner._generate_plan_gemini", return_value=("Mock plan", None, None)) as mock_gen,
        ):
            with patch.dict(
                os.environ,
                {
                    "TREATMENT_GEMINI_MODEL": "gemini-custom-gen",
                    "TREATMENT_JUDGE_GEMINI_MODEL": "gemini-custom-judge",
                },
                clear=False,
            ):
                out = generate_treatment_plan(ti, backend="gemini")
                self.assertEqual(out["generator_model"], "gemini-custom-gen")
                self.assertEqual(out["judge_model"], "gemini-custom-judge")
                self.assertEqual(mock_gen.call_args.kwargs["generator_model"], "gemini-custom-gen")
                self.assertEqual(mock_gen.call_args.kwargs["judge_model"], "gemini-custom-judge")

            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop("TREATMENT_GEMINI_MODEL", None)
                os.environ.pop("TREATMENT_JUDGE_GEMINI_MODEL", None)
                out_default = generate_treatment_plan(ti, backend="gemini")
                self.assertEqual(out_default["generator_model"], DEFAULT_GEMINI_MODEL)
                self.assertEqual(out_default["judge_model"], DEFAULT_GEMINI_MODEL)

    def test_invoke_gemini_fails_fast_on_404_not_found(self):
        class _StubNotFoundLLM:
            def __init__(self):
                self.calls = 0

            def invoke(self, _messages):
                self.calls += 1
                raise RuntimeError("404 NOT_FOUND: models/missing-model not found")

        stub = _StubNotFoundLLM()
        with self.assertRaises(RuntimeError):
            _invoke_gemini_with_retry(stub, [], retries=3)
        self.assertEqual(stub.calls, 1)

    def test_nvidia_backend_env_override_and_wiring(self):
        rec = create_record(name="Alex", age=30)
        rec["assessment_handoff"] = _sample_handoff()
        ti = build_treatment_input(rec)

        with (
            patch("integration.treatment_runner.load_guideline_retriever", return_value=object()),
            patch("integration.treatment_runner.retrieve_guideline_context", return_value="[G1] Source: NICE.pdf, page 1\nTest"),
            patch("integration.treatment_runner._generate_plan_nvidia", return_value=("Mock NVIDIA plan", None, None)) as mock_nv,
        ):
            with patch.dict(
                os.environ,
                {
                    "TREATMENT_NVIDIA_MODEL": "nv-custom-gen",
                    "TREATMENT_JUDGE_NVIDIA_MODEL": "nv-custom-judge",
                },
                clear=False,
            ):
                out = generate_treatment_plan(ti, backend="nvidia")
                self.assertEqual(out["backend"], "nvidia")
                self.assertEqual(out["generator_model"], "nv-custom-gen")
                self.assertEqual(out["judge_model"], "nv-custom-judge")
                self.assertEqual(mock_nv.call_args.kwargs["generator_model"], "nv-custom-gen")
                self.assertEqual(mock_nv.call_args.kwargs["judge_model"], "nv-custom-judge")

            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop("TREATMENT_NVIDIA_MODEL", None)
                os.environ.pop("TREATMENT_JUDGE_NVIDIA_MODEL", None)
                out_default = generate_treatment_plan(ti, backend="nvidia")
                self.assertEqual(DEFAULT_NVIDIA_MODEL, "nvidia/nemotron-3.5-lightning-30b-a3b")
                self.assertEqual(out_default["generator_model"], DEFAULT_NVIDIA_MODEL)
                self.assertEqual(out_default["judge_model"], DEFAULT_NVIDIA_MODEL)


class TherapyRunnerTests(unittest.TestCase):
    def test_libraries_and_bm25_with_empty_goals(self):
        libs = load_therapy_libraries()
        self.assertEqual(len(libs["interventions_all"]), 45)
        self.assertEqual(len(libs["psychoeducation_cards"]), 52)
        plan = "Major depressive disorder plan using CBT cognitive restructuring and Behavioral Activation (BA) activity scheduling."
        candidates = retrieve_candidates(plan, [], limit=6, libs=libs)
        self.assertGreater(len(candidates), 0)
        mods = {c["therapy_id"].lower() for c in candidates}
        self.assertIn("cbt", mods)
        self.assertIn("ba", mods)

    def test_apply_state_patch_session1_and_session2_keeps_handoff_immutable(self):
        rec = create_record(name="Alex", age=30)
        rec["assessment_handoff"] = _sample_handoff()
        handoff_before = copy.deepcopy(rec["assessment_handoff"])

        patch1 = StatePatch(
            symptom_updates=[SymptomUpdate(name="insomnia", severity="moderate", description="Wakes at 4am")],
            homework_updates=[HomeworkUpdate(task="10-minute morning walk", status="assigned")],
            therapy_updates=[
                TherapyItemUpdate(
                    therapy="BA",
                    category="target_activities",
                    text="Morning walk outside",
                    status="in_progress",
                )
            ],
            new_goals=["Walk three mornings per week"],
            new_coping_strategies=["Deep breathing before bed"],
            risk_history_note="No acute risk reported during session 1.",
        )
        ts1 = apply_state_patch(rec["therapy_state"], patch1)
        self.assertEqual(len(ts1["symptoms"]), 1)
        self.assertEqual(ts1["symptoms"][0]["name"], "insomnia")
        self.assertEqual(ts1["symptoms"][0]["severity"], "moderate")
        self.assertEqual(ts1["therapy_specific_parameters"]["homework"][0]["status"], "assigned")
        self.assertEqual(ts1["therapy_specific_parameters"]["BA"]["target_activities"][0]["activity"], "Morning walk outside")
        self.assertEqual(ts1["goals"], ["Walk three mornings per week"])
        self.assertEqual(ts1["coping_strategies"], ["Deep breathing before bed"])
        self.assertEqual(ts1["risk_history_notes"], ["No acute risk reported during session 1."])
        self.assertEqual(rec["assessment_handoff"], handoff_before)

        patch2 = StatePatch(
            symptom_updates=[SymptomUpdate(name="insomnia", severity="mild")],
            homework_updates=[HomeworkUpdate(task="morning walk", status="completed")],
        )
        ts2 = apply_state_patch(ts1, patch2)
        self.assertEqual(len(ts2["symptoms"]), 1)
        self.assertEqual(ts2["symptoms"][0]["severity"], "mild")
        self.assertEqual(ts2["therapy_specific_parameters"]["homework"][0]["status"], "completed")

    def test_controller_intervention_tracker_and_turn_cap(self):
        libs = load_therapy_libraries()
        cid = libs["interventions_all"][0]["intervention_id"]
        PlanSchema = make_session_plan_schema([cid])
        plan = PlanSchema(
            session_goal="Practice grounding and activity scheduling.",
            session_objectives=[
                {"phase": "CHECK_IN", "title": "Mood check", "task": "Check mood.", "criterion": "Shares mood", "intervention": "NONE"},
                {"phase": "EXPLAIN_AGENDA", "title": "Agree agenda", "task": "Set focus.", "criterion": "Agrees", "intervention": "NONE"},
                {"phase": "WORK", "title": "Core exercise", "task": "Run intervention.", "criterion": "Picks step", "intervention": cid},
                {"phase": "CLOSING", "title": "Wrap up", "task": "Agree homework.", "criterion": "Confirms plan", "intervention": "NONE"},
            ],
        )
        self.assertEqual(validate_plan_rules(plan), [])
        repair_plan_deterministic(plan)

        guides = {
            cid: DeliveryGuide(
                structure="sequential",
                steps=[
                    InterventionStep(step_number=1, instruction="Step 1", done_when="Done 1"),
                    InterventionStep(step_number=2, instruction="Step 2", done_when="Done 2"),
                ],
                completion_condition="Agreed on step.",
            )
        }
        ctrl = ClinicalSessionController(plan, guides)
        tracker = SessionStateTracker()
        tracker.active_controller = ctrl
        tools = {t.name: t for t in build_clinical_tools(tracker)}

        # Complete CHECK_IN and EXPLAIN_AGENDA
        for t in (1, 2):
            obj = ctrl.current_objective()
            ctrl.turns_in_obj += 1
            ctrl.current_turn = t
            d = TherapyDecision(selected_action="explore", goal="Check in", objective_complete=True)
            ctrl.enforce_turn(d, obj)
            self.assertTrue(ctrl.advance_if_satisfied(obj))

        # WORK objective: start intervention, test pause/resume tools, verify exact 1-based event turns
        work_obj = ctrl.current_objective()
        ctrl.turns_in_obj += 1
        ctrl.current_turn = 3
        d_start = TherapyDecision(
            selected_action="intervene",
            goal="Start step 1",
            intervention_id=cid,
            recommended_focus=1,
            objective_complete=False,
        )
        ctrl.enforce_turn(d_start, work_obj)
        self.assertIsNotNone(ctrl.active_intervention)
        self.assertEqual(ctrl.active_intervention["step"], 1)  # type: ignore[index]
        self.assertEqual(ctrl.intervention_events[0]["event"], "STARTED")
        self.assertEqual(ctrl.intervention_events[0]["turn"], 3)

        pause_res = tools["pause_intervention"].invoke({"reason": "Patient overwhelmed"})
        self.assertIn("PAUSED", pause_res)
        self.assertEqual(ctrl.active_intervention["status"], "PAUSED")  # type: ignore[index]

        resume_res = tools["resume_intervention"].invoke({})
        self.assertIn("RESUMED", resume_res)
        self.assertEqual(ctrl.active_intervention["status"], "ACTIVE")  # type: ignore[index]

        # Test 6-turn budget cap forces advance cleanly
        ctrl.turns_in_obj = 6
        ctrl.current_turn = 8
        d_incomplete = TherapyDecision(selected_action="explore", goal="Keep working", objective_complete=False)
        ctrl.enforce_turn(d_incomplete, work_obj)
        self.assertTrue(ctrl.advance_if_satisfied(work_obj))
        self.assertIsNone(ctrl.active_intervention)
        self.assertEqual(ctrl.intervention_events[-1]["event"], "CLOSED_ON_ADVANCE")
        self.assertEqual(ctrl.intervention_events[-1]["turn"], 8)

        # Complete CLOSING -> ENDED
        close_obj = ctrl.current_objective()
        ctrl.turns_in_obj += 1
        d_close = TherapyDecision(selected_action="plan", goal="Confirm homework", objective_complete=True)
        ctrl.enforce_turn(d_close, close_obj)
        self.assertTrue(ctrl.advance_if_satisfied(close_obj))
        self.assertEqual(ctrl.status, "ENDED")

    def test_modality_regex_avoids_false_positives_and_matches_full_names(self):
        matched_cbt = {m for m, pat in MODALITY_PATTERNS.items() if pat.search("evidence-based CBT plan with description".lower())}
        self.assertEqual(matched_cbt, {"cbt"})

        matched_full = {
            m for m, pat in MODALITY_PATTERNS.items() if pat.search("behavioural activation and interpersonal psychotherapy".lower())
        }
        self.assertEqual(matched_full, {"ba", "ipt"})

    def test_retrieve_candidates_preserves_missing_modality_within_limit(self):
        libs = load_therapy_libraries()
        plan = "CBT cognitive restructuring thought record automatic thoughts core beliefs and Interpersonal Psychotherapy (IPT)"
        raw_top6 = libs["bm25_index"].search(expand_clinical_query(plan), top_k=6)
        self.assertEqual(len(raw_top6), 6)
        self.assertNotIn("ipt", {r["therapy_id"].lower() for r in raw_top6})

        candidates = retrieve_candidates(plan, [], limit=6, libs=libs)
        self.assertEqual(len(candidates), 6)
        mods = {c["therapy_id"].lower() for c in candidates}
        self.assertIn("cbt", mods)
        self.assertIn("ipt", mods)

    def test_replan_validator_allows_remaining_phases_only(self):
        libs = load_therapy_libraries()
        cid = libs["interventions_all"][0]["intervention_id"]
        PlanSchema = make_session_plan_schema([cid])
        replan = PlanSchema(
            session_goal="Focus on patient's work stress concern.",
            session_objectives=[
                {"phase": "WORK", "title": "Core exercise", "task": "Explore stressor.", "criterion": "Shares example", "intervention": cid},
                {"phase": "CLOSING", "title": "Wrap up", "task": "Agree homework.", "criterion": "Confirms plan", "intervention": "NONE"},
            ],
        )
        self.assertEqual(validate_replan_rules(replan, {"CHECK_IN", "EXPLAIN_AGENDA"}), [])

        bad_plan = PlanSchema(
            session_goal="Invalid replan.",
            session_objectives=[
                {"phase": "CHECK_IN", "title": "Mood check", "task": "Check mood.", "criterion": "Shares mood", "intervention": "NONE"},
                {"phase": "WORK", "title": "Core exercise", "task": "Explore stressor.", "criterion": "Shares example", "intervention": cid},
                {"phase": "CLOSING", "title": "Wrap up", "task": "Agree homework.", "criterion": "Confirms plan", "intervention": "NONE"},
            ],
        )
        errs = validate_replan_rules(bad_plan, {"CHECK_IN"})
        self.assertTrue(any("CHECK_IN" in e for e in errs))

    def test_zero_turn_finish_does_not_append_session(self):
        libs = load_therapy_libraries()
        cid = libs["interventions_all"][0]["intervention_id"]
        PlanSchema = make_session_plan_schema([cid])
        plan = PlanSchema(
            session_goal="Minimal plan",
            session_objectives=[
                {"phase": "CHECK_IN", "title": "Mood check", "task": "Check mood.", "criterion": "Shares mood", "intervention": "NONE"},
                {"phase": "EXPLAIN_AGENDA", "title": "Agree agenda", "task": "Set focus.", "criterion": "Agrees", "intervention": "NONE"},
                {"phase": "WORK", "title": "Core exercise", "task": "Run intervention.", "criterion": "Picks step", "intervention": cid},
                {"phase": "CLOSING", "title": "Wrap up", "task": "Agree homework.", "criterion": "Confirms plan", "intervention": "NONE"},
            ],
        )
        guides = {
            cid: DeliveryGuide(
                structure="sequential",
                steps=[InterventionStep(step_number=1, instruction="Step 1", done_when="Done 1")],
                completion_condition="Agreed on step.",
            )
        }
        rec = create_record(name="Alex", age=30)
        rec["assessment_handoff"] = _sample_handoff()
        rec["treatment_plan"] = "Use CBT for depression."

        sess = TherapySession(rec)
        sess.session_plan = plan
        sess.controller = ClinicalSessionController(plan, guides)
        res = sess.finish()
        self.assertIsNone(res["session_archive"])
        self.assertEqual(res["state_patch"], {})
        self.assertEqual(res["record"]["sessions"], [])

    def test_call_structured_uses_json_schema_then_falls_back_to_json_object(self):
        fenced_reply = '<think>plan reasoning</think>\n```json\n{"selected_action": "explore", "goal": "Explore sleep habits", "objective_complete": false}\n```'
        parsed = _parse_structured_json(fenced_reply, TherapyDecision)
        self.assertIsInstance(parsed, TherapyDecision)
        self.assertEqual(parsed.selected_action, "explore")
        self.assertEqual(parsed.goal, "Explore sleep habits")

        class _FakeResp:
            def __init__(self, content: str):
                self.content = content
                self.response_metadata = {"finish_reason": "stop"}
                self.additional_kwargs = {}

        class _FakeBoundLLM:
            def __init__(self, rf: dict, fail_json_schema: bool, seen: list):
                self.rf = rf
                self.fail_json_schema = fail_json_schema
                self.seen = seen

            def invoke(self, messages):
                self.seen.append((self.rf, messages))
                if self.fail_json_schema and self.rf.get("type") == "json_schema":
                    raise RuntimeError("[400] invalid schema")
                return _FakeResp('{"selected_action": "validate", "goal": "Validate feeling", "objective_complete": true}')

        class _FakeNvidiaClient:
            def __init__(self, fail_json_schema: bool):
                self.fail_json_schema = fail_json_schema
                self.seen: list = []

            def bind(self, **kwargs):
                self.seen.append(("bind_keys", tuple(sorted(kwargs.keys()))))
                return _FakeBoundLLM(kwargs["response_format"], self.fail_json_schema, self.seen)

            def with_structured_output(self, _schema):
                raise AssertionError("with_structured_output (guided_json) must not be called for NVIDIA roles")

        primary_client = _FakeNvidiaClient(fail_json_schema=False)
        with patch("integration.therapy_runner._get_nvidia_client", return_value=primary_client):
            out1 = call_structured("planner", TherapyDecision, "sys", "usr")
        self.assertIsInstance(out1, TherapyDecision)
        self.assertEqual(out1.selected_action, "validate")
        invoked_rf_1 = [item[0]["type"] for item in primary_client.seen if isinstance(item[0], dict)]
        self.assertEqual(invoked_rf_1, ["json_schema"])
        self.assertFalse(any("guided_json" in keys for tag, keys in primary_client.seen if tag == "bind_keys"))

        fallback_client = _FakeNvidiaClient(fail_json_schema=True)
        with patch("integration.therapy_runner._get_nvidia_client", return_value=fallback_client):
            out2 = call_structured("reasoning", TherapyDecision, "sys", "usr")
        self.assertIsInstance(out2, TherapyDecision)
        self.assertTrue(out2.objective_complete)
        invoked_items_2 = [item for item in fallback_client.seen if isinstance(item[0], dict)]
        self.assertEqual([rf["type"] for rf, _ in invoked_items_2], ["json_schema", "json_object"])
        self.assertIn("Return ONLY one valid JSON object", invoked_items_2[1][1][1].content)
        self.assertFalse(any("guided_json" in keys for tag, keys in fallback_client.seen if tag == "bind_keys"))


class PipelineGateTests(unittest.TestCase):
    def test_clinical_gate_conditions(self):
        clean = _sample_handoff()
        self.assertEqual(check_clinical_gate(clean), [])

        stopped = copy.deepcopy(clean)
        stopped["source"]["stop_reason"] = "patient_stop"
        self.assertEqual(len(check_clinical_gate(stopped)), 1)

        no_dis = copy.deepcopy(clean)
        no_dis["assessment"]["primary_label"] = "NO_DISORDER"
        self.assertEqual(len(check_clinical_gate(no_dis)), 1)

        insuff = copy.deepcopy(clean)
        insuff["assessment"]["primary_label"] = "INSUFFICIENT_INFORMATION"
        self.assertEqual(len(check_clinical_gate(insuff)), 1)

        declined = copy.deepcopy(clean)
        declined["next_step_preference"]["status"] = "declined"
        self.assertEqual(len(check_clinical_gate(declined)), 1)


if __name__ == "__main__":
    unittest.main()
