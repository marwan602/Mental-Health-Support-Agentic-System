# Assessment and diagnosis integration

This is the English-language assessment component for the graduation project's fictional adult interviews. It adapts the semi-structured v7 experiment to accept replies from the host application. The conversation, extraction, planning and reasoning roles use the NVIDIA assessment model. The reasoner delivers a provisional summary and a structured handoff for treatment or therapy. This version uses the no-knowledge experiment configuration. It handles neither real-patient care nor crisis response.

## 1. Try one complete interview

From the unpacked folder, using Python 3.10 or later:

```bash
python -m pip install .
python demo.py
python -m unittest discover -v
```

In Ubuntu use `python3` if needed. The default demo uses two fictional answers and local test responses. It prints the directory containing the conversation, findings and handoff. For a live role-play run `python demo.py --live` and enter the NVIDIA key at the hidden prompt, or set `NVIDIA_API_KEY` on the backend. The model is `nvidia/nemotron-3-ultra-550b-a55b`. The patient reply comes from your app or a simulator you control. No Gemini key is required by this component.

## 2. Connect the full system

Create one service for the backend process. Give it a private, writable directory. Route each user to their own session through your backend's identity and access controls. Use a worker for a turn if your UI cannot wait synchronously for model calls.

```python
from assessment_component import AssessmentService

service = AssessmentService("private/assessment_sessions", mock=False)
turn = service.start_session(fictional_name="Alex", age=30)
# Display turn["text"]. Store turn["session_id"] and turn["question_id"].

# When the app receives the user's answer:
turn = service.submit_reply(
    turn["session_id"], question_id=turn["question_id"], text="I feel low most mornings."
)
# Display turn["text"]. Repeat submit_reply while state == "awaiting_reply".
if turn["state"] == "complete":
    assessment_handoff = turn["handoff"]
```

| Host event | What the host does |
|---|---|
| Opens a fictional assessment | Call `start_session` with a name and integer age of 18 or older. Display the opening. |
| Receives typed or spoken input | Submit one finalized text reply for the displayed question ID. The host provides speech transcription for audio or video and handles playback. |
| Gets `awaiting_reply` | Show the returned interviewer text. The handoff is null. |
| Gets `complete` | Show the returned text. The handoff is available internally. Read `end_reason` and `next_step_preference` before offering the next stage. A stop request calls for ending the interaction. |
| Connection drops or a provider fails | Retry the same question ID with the same text, or call `get_session(session_id)`. Stored answers and model responses allow recovery. A conflicting second answer for an accepted question is rejected. A busy session can be retried. |

The returned object includes `session_id`, `state`, `question_id`, `text`, `accepted_replies`, `end_reason` and `handoff`. The final question ID is null. Only the text is meant to be spoken or displayed. Use the same package version, prompt files, storage directory and mock/live mode for an ongoing session. This file-backed implementation is designed for one host with shared local storage. A distributed deployment would need shared session persistence and locking.

## 3. What treatment and therapy receive

Read `assessment_handoff.json` or use the identical object in the final response. The machine-readable contract is `assessment_component/assessment_handoff.schema.json`. Open `examples/assessment_handoff.mock.json` to see a complete example.

| Field | Meaning for the receiving team |
|---|---|
| `assessment` | Provisional primary label, alternatives, supporting finding IDs and limits. `INSUFFICIENT_INFORMATION` is a valid result. |
| `presenting_concerns`, `functioning_baseline`, `evidence` | What the person reported and how daily life was affected, with references to the interview. |
| `planning_context` | Reason for seeking help, goals, preferences, barriers, supports, coping strategies and past or current care when actually disclosed. `not_documented` means the receiving agent may need to ask. |
| `open_questions` | Material gaps kept by the final review and why answering them could matter. An empty list can reflect a missed gap. |
| `source`, `schema_version`, `next_step_preference` | Origin, stop reason, contract version and any explicit preference about discussing support. Even an expressed wish to discuss support does not constitute consent to a specific treatment. |

Keep assessment evidence and later therapy observations in their own records. For example, later therapy homework can refer back to the person's original goal without changing their recorded interview answers. The host decides when to offer the next stage. The handoff does not prescribe treatment.

## 4. Evaluate the component

**Use automated file checks at integration time and a separate AI review for research comparisons.** Neither produces a patient-facing score. The diagnosis agent has no access to the case answer key, evaluation targets or judge feedback.

1. **Check a completed handoff locally.** Run `python -m assessment_component.evaluate PATH_TO_SESSION`. It checks the JSON contract, the transfer of evidence, patient quote matches and primary evidence references. The result is saved in `integration_audit.json`. A pass verifies those properties. A quote can still be interpreted incorrectly.
2. **Grade a completed live fictional benchmark session.** Set the backend's `NVIDIA_API_KEY`. Run `python -m assessment_component.evaluate PATH_TO_SESSION --reference PATH_TO_MATCHED_REFERENCE_JSON`. Supply the same actor card, evaluator key and targets used for that particular case. The format is shown in `examples/reference.example.json`. That example belongs only to the illustrative Alex scenario. Store real benchmark reference files in the evaluation environment, outside the assessment inputs.
3. **Read the two reviews separately.** After a calibration fixture, the Mistral judge reviews the conversation and findings without the key. A second request reviews the conclusion against the key and disclosed evidence and flags invented or contradictory simulator facts. A failed calibration or incomplete review must be reported as unevaluated. Mock interviews are for integration checks only.

| Research question | What to report from evaluated cases |
|---|---|
| Did the system identify a supported provisional explanation? | Count cases with both `aligned` and `supported` in `judge_conclusion.json`, divided by fully judged cases. Report completed and judged totals separately. |
| Did extraction preserve what the person said? | Supported findings / extracted findings, and captured disclosed facts / disclosed facts. Inspect cited turns for changes in meaning. |
| Were the interviews focused? | Repeated follow-ups / follow-ups and fully disclosed targets / reference targets. Review missed follow-ups and partial or declined targets alongside the rates. |
| Did the simulator follow its case? | Review `simulator_deviations` separately so invented background details are attributed to the simulator. |

Use counts from `score.json` only after both reviews succeed. Sum numerators and denominators across cases for the extraction, repetition and coverage rates. A zero denominator is unavailable. These scores describe this synthetic benchmark and the judge's judgments. They do not establish clinical accuracy.

## 5. Files and current limits

Each session saves `conversation_qa.md`, `transcript.json`, `evidence.json`, `coverage.json`, `planner_decisions.json` once the planner acts, `synthesis.json`, `assessment_handoff.json` at completion, and status and internal model logs. Internal logs and caches contain full prompts and conversation text. Keep those backend-only. Installation includes the role prompts and label options in `assessment_component/prompts` and `config.json`.

The integration adapter was tested with offline model responses. In the source v7 development interviews, the interviewer sometimes changed a patient's meaning, skipped a useful follow-up, or left an important gap out of the handoff. Review those behaviors when comparing versions. The package does not include the separate disease knowledge base, benchmark answer keys, or any claim of suitability for real patients. Text is the supported interface; speech, video and Arabic evaluation belong to the host project.
