# Adult PMDD package

Read the parent `04_PMDD_Assessment_Information_Requirements.md` first.

| File | Purpose |
|---|---|
| knowledge.json | Clinical-reference map, concept-specific fields and engineering states |
| sources.json | Source links, exact locations and access limitations |
| evidence_output.schema.json | Conversation-evidence snapshot contract |
| examples.json | Fictional conversation and two snapshots |
| diary_input.schema.json | Separate original-DRSP-response storage contract |
| diary_examples.json | Two partial fictional days, not prospective diagnostic confirmation |
| validate_package.py | Mechanical checks, no model/API calls |
| VALIDATION_REPORT.json | Actual check results and limitations |

Source-reviewed design, not clinical validation. No manual or complete instrument item set is bundled. Tools need verified versions, language and permissions before administration. No agent integration or C-PASS scorer is implemented. Do not paste the whole schema/reference into every model request; use role-relevant cards and an explicit interface migration.

To validate: install jsonschema>=4.18,<5 if needed and run `python validate_package.py` here. No API key is needed.
