# Adult depression assessment knowledge

Source-linked knowledge for conversational assessment, evidence extraction, assessment planning and provisional diagnostic synthesis. Scope: adults aged 18 and older, including older adults.

## Contents

- [Clinical package index](00_Knowledge_Package_Index.md): depressive categories, alternatives and clinical guides.
- Files 01–09: classification, clinical concepts, assessment information and source references.
- Files 10–13: proposed session structure, interview rules and numbered question graph.
- [Measurement guide](14_Screening_Measurement_and_Scoring.md): optional standardized tools and scoring boundaries.
- [Integration contracts](Integration/agent_contracts.json): agent inputs, outputs and application responsibilities.
- [Evidence-to-state rules](Integration/EVIDENCE_TO_STATE_RULES.md): context, history, coverage, corrections and branching.
- [Agent prompts](Integration/AGENT_PROMPTS.txt): conversation, extraction, planning and provisional synthesis.
- [Routing index](Integration/route_completion.json): 219 concept entries and 1,428 attribute targets, with scheduled or conditional routes.
- [Fictional input/output examples](Integration/example_input_output.json): original evidence contracts and example role outputs.

Each clinical module supplies `knowledge.json`, `sources.json`, `evidence_output.schema.json`, fictional examples and a validator. Source registers distinguish clinical authorities, research contributions and engineering design. Preserve source paths with their identifiers; identifiers alone are not globally unique.

## Integration

The application loads relevant knowledge using `Integration/knowledge_access.py` and supplies it in actual model requests. A prompt mentioning a file does not give the model disk access. Use the original per-module schemas for evidence validation. Full schema definitions can remain application-side; select relevant cards within the provider's actual context and rate limits.

Preserve message and episode identifiers, exact patient quotations and earlier question context. Retain source-linked revisions instead of silently overwriting earlier reports. Same-label concepts in different modules require semantic and period checks before reuse. Conditional targets are not a mandatory questionnaire.

```python
from Integration.knowledge_access import get_context

context = get_context("conversation", ["detail/MDD/depressed_mood/duration"])
```

## Verification

Run from this knowledge directory:

```powershell
python -m pip install -r Integration/requirements.txt
python Integration/verify_package.py
```

The verifier checks file integrity, clinical-module fixtures, annotated-state routing, measurement arithmetic and integration contracts. It isolates validator report writes in a temporary copy. `SHA256SUMS.json` records this repository edition; regenerate it intentionally after modifying package files.

## Status and boundaries

This is source-informed research knowledge for agent integration and fictional evaluation. Existing agents are not automatically connected by adding this folder. Clinical review, semantic extraction-to-coverage evaluation, model evaluation and locally configured safety/referral delivery remain separate requirements. Clinical content and engineering rules are distinguishable; a passing schema or routing test does not establish clinical accuracy.

Diagnostic synthesis remains provisional and for professional review. Scores do not independently diagnose depression or predict suicide. Documented source ambiguity, including the exactly-four-day other-specified duration boundary, must be preserved rather than resolved by an invented cutoff. No licensed MINI/SCID item bank or operational emergency service is supplied.
