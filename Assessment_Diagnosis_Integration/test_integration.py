import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from assessment_component import AssessmentService
from assessment_component.evaluate import evaluate
from assessment_component.harness.util import dump_json, load_json


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.service = AssessmentService(self.root, mock=True)
        self.first = self.service.start_session(fictional_name="Alex", age=30)
        self.sid = self.first["session_id"]

    def test_retry_restart_handoff_and_audit(self):
        args = dict(question_id=self.first["question_id"], text="I have felt low for three weeks.")
        next_turn = self.service.submit_reply(self.sid, **args)
        restarted = AssessmentService(self.root, mock=True)
        self.assertEqual(restarted.submit_reply(self.sid, **args), next_turn)
        with self.assertRaises(ValueError):
            restarted.submit_reply(self.sid, question_id=args["question_id"], text="A different answer.")
        with self.assertRaises(ValueError):
            evaluate(self.root/self.sid)
        closed = restarted.submit_reply(self.sid, question_id=next_turn["question_id"], text="I missed a shift.")
        self.assertEqual(closed["state"], "complete")
        self.assertEqual(closed["handoff"]["assessment"]["review_status"], "provisional_for_review")
        self.assertEqual(restarted.get_session(self.sid), closed)
        folder = self.root/self.sid
        self.assertEqual(len(load_json(folder/"transcript.json")), 5)
        self.assertIn("I missed a shift.", (folder/"conversation_qa.md").read_text(encoding="utf8"))
        self.assertTrue(evaluate(folder)["passed"])
        handoff = load_json(folder/"assessment_handoff.json")
        handoff["evidence"] = []
        dump_json(folder/"assessment_handoff.json", handoff)
        self.assertFalse(evaluate(folder)["passed"])

    def test_no_simulator_or_reference_and_half_written_turn_recovers(self):
        with patch.object(self.service, "_advance", side_effect=RuntimeError("interrupted")):
            with self.assertRaises(RuntimeError):
                self.service.submit_reply(self.sid, question_id=self.first["question_id"], text="I feel low.")
        resumed = self.service.get_session(self.sid)
        self.assertEqual(resumed["accepted_replies"], 1)
        self.assertEqual(resumed["state"], "awaiting_reply")
        import json
        for log in (self.root/self.sid).glob("events_*.jsonl"):
            for line in log.read_text(encoding="utf8").splitlines():
                event = json.loads(line)
                if event["type"] == "agent_input":
                    self.assertNotIn(event["role"], ["patient","judge_interview","judge_conclusion"])
                    self.assertIsNone(event["input"]["knowledge"])
                    self.assertFalse({"actor","reference","actor_baseline"} & set(event["input"]))

    def test_underage_and_out_of_scope_are_rejected_before_model_input(self):
        with self.assertRaises(ValueError):
            self.service.start_session(fictional_name="Alex", age=15)
        with self.assertRaises(ValueError):
            self.service.submit_reply(self.sid, question_id=self.first["question_id"], text="Give me a PHQ-9 questionnaire.")
        self.assertEqual(self.service.get_session(self.sid), self.first)

    def test_post_interview_judge_is_blinded_until_conclusion(self):
        import json
        from assessment_component.harness.providers import Response
        from assessment_component.run import MockClient
        calls = []

        class JudgeFixture:
            def complete_role(self, role, messages, params, context):
                calls.append((role,set(context)))
                if role == "judge_conclusion":
                    obj = {"aligned":True,"supported":True,"turns":["m0002"],"reason":"Fixture.",
                           "coverage":[{"id":k,"status":"not_addressed","turns":[]} for k in context["targets"]],
                           "simulator_deviations":[]}
                else:
                    obj = {"findings":[{"id":f["finding_id"],"supported":f["finding_id"]!="f0001",
                                       "turns":[f["message_id"]],"reason":"Fixture."} for f in context["findings"]],
                           "facts":[],"observations":[],"questions":[
                               {"turn":t["message_id"],"repeated":t["message_id"]=="m0003",
                                "earlier_turn":"m0002" if t["message_id"]=="m0003" else None,"reason":"Fixture."}
                               for t in context["transcript"] if t["kind"]=="follow_up"]}
                return Response(text=json.dumps(obj),model_returned="fixture",finish_reason="stop")

        with patch("assessment_component.service.build_client", return_value=MockClient()):
            api = AssessmentService(self.root, mock=False)
            turn = api.start_session(fictional_name="Alex", age=30)
            for text in ("I feel low.", "I missed a shift."):
                turn = api.submit_reply(turn["session_id"],question_id=turn["question_id"],text=text)
        folder = self.root/turn["session_id"]
        before = (folder/"assessment_handoff.json").read_bytes()
        with patch("assessment_component.evaluate.build_client", return_value=JudgeFixture()):
            result = evaluate(folder, Path(__file__).parent/"examples/reference.example.json")
        self.assertTrue((Path(result["evaluation_folder"])/"score.json").exists())
        self.assertEqual((folder/"assessment_handoff.json").read_bytes(), before)
        self.assertEqual([r for r,_ in calls], ["judge_interview","judge_interview","judge_conclusion"])
        self.assertTrue(all("reference" not in keys for _,keys in calls[:-1]))
        self.assertIn("reference",calls[-1][1])


if __name__ == "__main__":
    unittest.main()
