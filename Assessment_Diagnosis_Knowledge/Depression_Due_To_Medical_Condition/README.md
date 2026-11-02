# Depressive disorder due to another medical condition — adults

Start with the [readable guide](../06_Depression_Due_To_Medical_Condition_Assessment.md). Scope: adults 18+, including older adults.

`knowledge.json` contains 30 concept cards, field descriptions, controlled values, the clinical map and local sequence. `sources.json` contains 18 sources with links, locations, contributions and access notes. `medical_condition_reference.json` separates reference knowledge from patient testimony. The schema defines the output; examples are fictional authored fixtures.

To run only the mechanical checks (requires Python and jsonschema):

```powershell
python validate_package.py
```

Results are saved in `VALIDATION_REPORT.json`. No API key, model call or interview is involved. Passing these checks is not clinical validation. The package is not connected to the agents. Clinical review, final cross-disorder graph, role-specific context selection and live extraction/planning evaluation remain pending. Do not place every file in every LLM prompt; later integration should provide role-relevant content and preserve patient history/provenance.
