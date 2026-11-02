# Adult substance/medication-induced depression knowledge

Start with [the readable guide](../05_Substance_Medication_Induced_Depression_Assessment.md). Adult scope: 18+, no upper cutoff.

- `knowledge.json`: 27 concept cards, optional fields, values, clinical map and semi-structured project policy.
- `sources.json`: 16 clinical/research sources, with links, locations and uses.
- `capability_reference.json`: pinned substance-class reference and limited medication examples; not a causal whitelist.
- `evidence_output.schema.json`: proposed concept-specific patient-evidence contract.
- `examples.json`: fictional history-aware, two-agent snapshots; no live-model output.
- `validate_package.py` and `VALIDATION_REPORT.json`: mechanical checks and results.

Run from this folder with Python and jsonschema installed:

```powershell
python validate_package.py
```

No API key is needed. This does not start an interview. Clinical review, runtime integration and the final cross-disorder graph remain pending. Avoid placing the entire reference package in every prompt; later integration should select role-relevant source-linked context while preserving conversation/evidence history. Do not treat the project's storage enums or wording as validated clinical instrument items.
