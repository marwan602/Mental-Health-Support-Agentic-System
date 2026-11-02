# Adult MDD module

Version: 1.0.1-source-reviewed. Adults 18+. Assessment/provisional professional review only.

Start with the parent file `02_MDD_Assessment_Information_Requirements.md` for the readable explanation.

| File | Purpose |
|---|---|
| knowledge.json | Sourced concepts, relevant attributes, examples, boundaries and project state definitions |
| sources.json | Source links, exact locations and access limitations |
| evidence_output.schema.json | Proposed output contract; concept-specific attributes, not identical forms |
| examples.json | Fictional dialogue and two valid snapshots showing memory across turns |
| validate_package.py | Mechanical validation and negative-fixture checks |
| VALIDATION_REPORT.json | Results of the latest local checks; not clinical validation |

Clinical definitions are source-based; software fields and conversational examples are project designs. No book PDF is bundled. This module is not connected to existing agents. Do not replace their schema without an explicit migration.

To validate, install `jsonschema>=4.18,<5` if needed, then run `python validate_package.py` in this folder. No API key is needed.

The full schema is for application validation, not a recommendation to paste every branch into every model request. Agent integration should supply the appropriate knowledge cards and a compact role-specific contract while preserving conversation context. That integration is not implemented here.

Audit migration: the Desktop MDD evidence contract is now version 1.0.1 and requires `module_id: adult_mdd`. Older snapshots without a module identifier require explicit migration; existing runtime files are unchanged. This prevents confusion with similarly named concepts in another module.
