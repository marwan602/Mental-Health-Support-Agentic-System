# Integrated Pipeline (`Assessment -> Treatment Planning -> Therapy`)

This folder wires the three completed AI modules together cleanly without modifying `Assessment_Diagnosis_Integration/` or `Treatment Planning/`.

## Folder Structure

```text
integration/
  ├── __init__.py               # Repo root + Assessment_Diagnosis_Integration path setup
  ├── patient_record.py         # Unified patient_record.json contract & prompt helpers
  ├── treatment_runner.py       # NICE PDF RAG + Gemini (default) / local 4-bit MedGemma+Qwen
  ├── therapy_runner.py         # Turn-by-turn TherapySession (fixed Therapy System 2.0)
  ├── pipeline.py               # Composable orchestrator & CLI (python -m integration.pipeline)
  ├── test_integration_seams.py # Seam, schema, controller, and real NICE PDF RAG tests
  └── README.md
```

## Data Flow & `patient_record.json`

Every pipeline run stores all outputs in `pipeline_runs/<run_id>/`:

```text
Stage 1: AssessmentService (NVIDIA API)
  └─► writes 01_assessment_handoff.json (immutable clinical quotes + provisional label)
  └─► updates patient_record.json["assessment_handoff"] + ["assessment_meta"]

Stage 2: treatment_runner (NICE_Guidelines.pdf Chroma RAG + Gemini / local GPU)
  └─► reads build_treatment_input(record)  [keeps full evidence[], including denials/unclear]
  └─► writes 02_treatment_plan.txt, 02_treatment_audit.json, 02_guideline_context.txt
  └─► updates patient_record.json["treatment_plan"] + ["treatment_audit"]

Stage 3: TherapySession (NVIDIA Nemotron + Google Gemma 4)
  └─► reads record["treatment_plan"], format_therapy_profile(record), record["therapy_state"]
  └─► runs conversational session + StatePatch updater
  └─► writes 03_therapy_session_<N>.json
  └─► updates ONLY record["therapy_state"] (preserving therapy_specific_parameters) and record["sessions"]
```

Why `assessment_handoff` stays separate from `therapy_state`:
- Assessment records raw, verified patient quotes and never scores symptom severity or risk history.
- Keeping `assessment_handoff` immutable prevents translation/LLM hallucinations on intake data while letting `therapy_state` track ongoing `homework`, `CBT`/`BA`/`IPT` parameters, and session-observed symptoms cleanly across sessions.

## Required Environment Variables

- `NVIDIA_API_KEY`: used by **Assessment** (`nvidia/nemotron-3-ultra-550b-a55b`) and **Therapy** infrastructure agents (`nvidia/nemotron-3.5-lightning-30b-a3b`).
- `GOOGLE_API_KEY` (or `GEMINI_API_KEY`): used by **Treatment Planning** (default `gemini-2.5-flash`) and **Therapy** Therapist Agent (`gemma-4-26b-a4b-it`).

Optional overrides:
- `TREATMENT_GEMINI_MODEL` / `TREATMENT_JUDGE_GEMINI_MODEL`: override default Gemini models for Treatment Planning.
- `HF_TOKEN`: only needed if running Treatment Planning with `--treatment-backend local` (`google/medgemma-27b-text-it`).

## Running the Integrated Pipeline

### Full A-Z Run (Interactive)

```powershell
$env:NVIDIA_API_KEY = "nvapi-..."
$env:GOOGLE_API_KEY = "AIza..."
python -m integration.pipeline --name "Alex" --age 30
```

### Resume an Existing Run (e.g., Skip Stage 1 or Start Session 2 of Therapy)

```powershell
python -m integration.pipeline --resume pipeline_runs\<run_id>
```

### Re-run a Single Stage

```powershell
python -m integration.pipeline --resume pipeline_runs\<run_id> --stage treatment
python -m integration.pipeline --resume pipeline_runs\<run_id> --stage therapy
```

### Use Local GPU Backend for Treatment Planning

```powershell
python -m integration.pipeline --resume pipeline_runs\<run_id> --stage treatment --treatment-backend local
```

## Future Hook: Post-Session Block (Block 4)

When the Post-session Block comes online, it only needs to read `pipeline_runs/<run_id>/patient_record.json` (plus the latest `03_therapy_session_<N>.json`), write updated trajectory/reflection updates to `record["therapy_state"]`, and optionally trigger `run_treatment_stage(...)` if treatment modifications are indicated.

## Running Verification Tests

```powershell
python -m unittest discover -s Assessment_Diagnosis_Integration -v
python -m unittest discover -s integration -v
```
