# Alternatives and coexisting conditions in adult depression assessment

Start with [the coverage/purpose guide](../09_Alternative_Assessment_Pathways_and_Sources.md).

There are 11 focused pathways, 33 shared concept cards and 35 sources. Each numbered pathway has Markdown; machine-readable pathway records are stored once in `knowledge.json` under `pathways`. Redundant standalone JSON exports were removed during the audit. Shared sources, evidence schema, fictional examples and [output explanation](OUTPUT_CONTRACT.md) are in this folder. Existing detailed medical/substance packages are linked for reuse.

Run mechanical checks only (Python and jsonschema required):

```powershell
python validate_package.py
```

`VALIDATION_REPORT.json` records the results. This does not run an LLM or require an API key. No full diagnostic/treatment service, final shared question graph, clinician validation or agent connection is implemented. Professional review and actual model evaluation remain pending. Every pathway explicitly states its purpose, benefit, assessment details and limits.
