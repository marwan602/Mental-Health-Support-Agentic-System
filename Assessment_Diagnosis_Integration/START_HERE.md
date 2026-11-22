# What’s inside the assessment and diagnosis package?

This package gives the graduation project a Python component that can conduct a semi-structured interview with a fictional adult in English. Your app sends one reply at a time. The component returns the next question or, when the interview ends, a closing message and a structured record for the treatment or therapy module.

It uses the **v7 experiment without the external disease knowledge base**. It includes the interview topics, prompts and possible conclusions used in that version. The separate disease knowledge base and the 60-case patient simulator are separate project resources. This prototype is intended for fictional interviews.

## Three files to open first

| Open this file | What you’ll find |
|---|---|
| `demo.py` | A complete example showing how to start a session, send replies, display the interviewer’s questions and receive the handoff. The default demo runs locally without an API key. |
| `examples/assessment_handoff.mock.json` | An example of the actual JSON structure the treatment module will receive. The values come from the offline demo. |
| `README.md` | Installation commands, the Python integration example, instructions for a live fictional interview, and how to run evaluation. |

## How one interview works

1. **Start.** Your app calls `start_session` with the fictional person’s name and age (18 or older). It receives the welcome message, a session ID and a question ID.
2. **Listen.** Your app calls `submit_reply` with the session ID, question ID and reply text. The **evidence extractor** reads the conversation and records what the person reported, with quotes and message IDs.
3. **Choose and ask.** The **planner** checks what has been answered, what is still relevant and whether another question would help. The **conversation agent** turns the selected topic into a question for the person. This repeats while the state is `awaiting_reply`.
4. **Summarize and hand over.** The **reasoning agent** weighs the evidence and writes a provisional explanation. The care-context and final-review steps prepare the handoff and check the closing wording. When the state is `complete`, display the returned `text` and pass the `handoff` object internally.

**Example.** If someone says, “I missed a shift because I couldn’t concentrate,” the extractor can record a concrete effect on work. The planner can ask when that difficulty began if the person has not already said. The treatment module can later read the work impact from the handoff. A goal such as “get back to work” belongs there only if the person actually expressed it.

## What your part of the full system connects to

| If you are working on… | Use this |
|---|---|
| **The app or backend** | `assessment_component/service.py` exposes `AssessmentService` with `start_session`, `submit_reply` and `get_session`. Keep the session and question IDs. If you support voice or video, send the finalized transcript as text. |
| **The interview agents** | `assessment_component/prompts/` holds the instructions for each role. `coverage.py` defines the interview topics, `run.py` coordinates the turns, and `config.json` lists the models and allowed conclusions. Live assessment uses NVIDIA Nemotron Ultra. |
| **Treatment or therapy** | Read the final `handoff`. It includes the provisional conclusion, alternatives, supporting evidence, daily functioning, unanswered questions, and any reported goals, preferences, barriers or supports. `assessment_component/assessment_handoff.schema.json` defines each field. Check the stop reason and the person’s stated preference before offering a next step. |
| **Reviewing a finished session** | Open `conversation_qa.md` for the questions and answers, `evidence.json` for the findings, `planner_decisions.json` for the planner’s choices, `synthesis.json` for the conclusion and `assessment_handoff.json` for the final handoff. These files are generated in the session folder when you run the component. |

## What evaluation is included?

**For integration testing**, `assessment_component/evaluate.py` can check a completed session locally. It verifies the handoff’s structure, the transfer of evidence and whether cited quotes appear in the patient’s messages. A passing result tells you the files fit together. Whether a quote was interpreted correctly is a separate question.

**For research comparisons**, an optional Mistral AI judge reviews the saved fictional interview after it ends. It examines repeated questions, missed follow-ups, extraction quality, and whether the conclusion fits both the conversation and the fictional case. Only the evaluation step receives the matched case reference. `examples/reference.example.json` shows the format using the demo character, Alex.

**First integration check:** Unzip the package, open a terminal in the folder containing `demo.py`, then run the commands below. The demo prints the session folder. Open its `conversation_qa.md` and `assessment_handoff.json` to see both sides of the integration.

```bash
python -m pip install .
python demo.py
```
