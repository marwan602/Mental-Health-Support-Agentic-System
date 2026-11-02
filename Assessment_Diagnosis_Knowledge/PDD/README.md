# Adult PDD knowledge package

Start with the parent `03_PDD_Assessment_Information_Requirements.md` for the readable guide.

| File | Purpose |
|---|---|
| knowledge.json | Clinical-reference map, concept-specific details, values and coverage |
| sources.json | Links, exact parts used and access/source discrepancies |
| evidence_output.schema.json | Proposed PDD evidence contract; not identical to MDD |
| examples.json | Fictional first/later snapshots showing context, intervals and new details |
| validate_package.py | Mechanical checks; no API calls |
| VALIDATION_REPORT.json | Actual check results and limitations |

Adults 18+. Source-reviewed project design, not clinical validation. Questions and software fields are our design. Current agents do not load this folder. The MDD and PDD contracts need an explicit shared-interface migration before integration; do not concatenate or swap them blindly.

Use role-relevant knowledge and compact contracts in model requests, rather than pasting the full reference/schema every turn. No model call or merge engine is implemented by these files.

To check locally: install jsonschema>=4.18,<5 if needed, then run `python validate_package.py` here. No API key is required.
