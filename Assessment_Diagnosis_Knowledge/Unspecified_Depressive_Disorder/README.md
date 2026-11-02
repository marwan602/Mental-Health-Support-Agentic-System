# Unspecified depressive disorder — adults

Start with the [readable guide](../08_Unspecified_Depressive_Disorder_Assessment.md). Adults 18+, including older adults.

The package contains 27 concept cards and 14 sources. `knowledge.json` describes domains, fields and project policy. `classification_reference.json` explains the residual category and distinctions; no classifier is implemented. The schema defines patient evidence and the examples are authored fictional fixtures.

Run only the mechanical checks from this folder (Python and jsonschema required):

```powershell
python validate_package.py
```

Results: `VALIDATION_REPORT.json`. No API key/model call/interview is involved. Incomplete assessment is not a diagnosis. Clinical review, final shared question graph, role-specific context selection and agent integration remain pending. Avoid sending the whole package to every role on every turn; later integration should select source-linked relevant knowledge while retaining history and provenance.
