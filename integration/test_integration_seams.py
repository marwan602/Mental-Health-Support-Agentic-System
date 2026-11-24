"""Integration seam, schema, controller, and real NICE PDF RAG tests."""
import copy
import gc
import json
import tempfile
import unittest
from pathlib import Path

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
    ClinicalSessionController,
    DeliveryGuide,
    HomeworkUpdate,
    InterventionStep,
    SESSION_TRACKER,
    StatePatch,
    SymptomUpdate,
    TherapyDecision,
    TherapyItemUpdate,
    apply_state_patch,
    load_therapy_libraries,
    make_session_plan_schema,
    pause_intervention,
    repair_plan_deterministic,
    resume_intervention,
    retrieve_candidates,
    validate_plan_rules,
)
from integration.treatment_runner import (
    ClinicalPlanEvaluation,
    _extract_text,
    build_plan_header,
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
        SESSION_TRACKER.active_controller = ctrl

        # Complete CHECK_IN and EXPLAIN_AGENDA
        for _ in range(2):
            obj = ctrl.current_objective()
            ctrl.turns_in_obj += 1
            d = TherapyDecision(selected_action="explore", goal="Check in", objective_complete=True)
            ctrl.verify_criterion(d)
            ctrl.enforce_turn(d, obj)
            self.assertTrue(ctrl.advance_if_satisfied(obj))

        # WORK objective: start intervention, test pause/resume tools, verify focus update
        work_obj = ctrl.current_objective()
        ctrl.turns_in_obj += 1
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

        pause_res = pause_intervention.invoke({"reason": "Patient overwhelmed"})
        self.assertIn("PAUSED", pause_res)
        self.assertEqual(ctrl.active_intervention["status"], "PAUSED")  # type: ignore[index]

        resume_res = resume_intervention.invoke({})
        self.assertIn("RESUMED", resume_res)
        self.assertEqual(ctrl.active_intervention["status"], "ACTIVE")  # type: ignore[index]

        # Test 6-turn budget cap forces advance cleanly
        ctrl.turns_in_obj = 6
        d_incomplete = TherapyDecision(selected_action="explore", goal="Keep working", objective_complete=False)
        ctrl.enforce_turn(d_incomplete, work_obj)
        self.assertTrue(ctrl.advance_if_satisfied(work_obj))
        self.assertIsNone(ctrl.active_intervention)

        # Complete CLOSING -> ENDED
        close_obj = ctrl.current_objective()
        ctrl.turns_in_obj += 1
        d_close = TherapyDecision(selected_action="plan", goal="Confirm homework", objective_complete=True)
        ctrl.enforce_turn(d_close, close_obj)
        self.assertTrue(ctrl.advance_if_satisfied(close_obj))
        self.assertEqual(ctrl.status, "ENDED")


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
