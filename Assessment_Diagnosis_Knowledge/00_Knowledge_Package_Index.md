# Adult assessment knowledge — package index

Adults aged 18 and older, including older adults. See [the technical overview](README.md) for integration, verification and current boundaries. The seven depressive-category packages and focused alternatives are source-linked research references, not independently clinically validated diagnostic implementations.

| Package | Readable guide | Structured package | Latest mechanical checks |
|---|---|---|---|
| Major depressive disorder | [Guide](02_MDD_Assessment_Information_Requirements.md) | [README](MDD/README.md) | 19 passed |
| Persistent depressive disorder | [Guide](03_PDD_Assessment_Information_Requirements.md) | [README](PDD/README.md) | 23 passed |
| Premenstrual dysphoric disorder | [Guide](04_PMDD_Assessment_Information_Requirements.md) | [README](PMDD/README.md) | 28 passed |
| Substance/medication-induced depressive disorder | [Guide](05_Substance_Medication_Induced_Depression_Assessment.md) | [README](Substance_Medication_Induced_Depression/README.md) | 36 passed |
| Depressive disorder due to another medical condition | [Guide](06_Depression_Due_To_Medical_Condition_Assessment.md) | [README](Depression_Due_To_Medical_Condition/README.md) | 46 passed |
| Other specified depressive disorder | [Guide](07_Other_Specified_Depressive_Disorder_Assessment.md) | [README](Other_Specified_Depressive_Disorder/README.md) | 45 passed |
| Unspecified depressive disorder | [Guide](08_Unspecified_Depressive_Disorder_Assessment.md) | [README](Unspecified_Depressive_Disorder/README.md) | 43 passed |
| Focused alternatives and coexisting-condition pathways | [Guide](09_Alternative_Assessment_Pathways_and_Sources.md) | [README](Alternatives/README.md) | 53 passed |

## What to use

- Readable Markdown: clinical and technical explanation of domains, questions, sources and limits.
- `knowledge.json`: module-specific concepts, fields, states and project policies for later role-specific loading.
- `sources.json`: citation locations, contribution and access limits.
- Evidence schema: application output validation; not diagnostic accuracy validation.
- Examples and validators: reproducible fictional fixtures and mechanical checks.
- Clinical/classification/capability reference files: relevant additional source-linked context.
- Alternatives: numbered readable guides, with canonical pathway records only in `Alternatives/knowledge.json`; redundant standalone JSON copies were removed.

Repeated concepts are module-qualified and require reviewed mappings, rather than a flat global concept list. MDD contract is now 1.0.1 and requires its module ID. Older snapshots need explicit migration; existing runtime files are unchanged.

The shared research interview graph and conditional routing overlay are available; integrate and evaluate agents using their explicit review gates. Clinical sign-off, instrument/language decisions and operational safety/referral design remain pending. The [coverage map](01_Adult_Depression_Coverage_and_Sources.md) records current scope.

<!-- session-map-design -->
## New workflow design draft

Open [the overall session and care-journey map](10_Overall_Session_Map.md). It includes the assessment conversation loop and the proposed therapy-state boundary. This is newly authored project design, not a completed clinical workflow or a change to the audited agents/knowledge contracts.

<!-- main-assessment-route-design -->

Open [the main adult depression assessment route](11_Main_Adult_Depression_Assessment_Route.md) for the proposed semi-structured modules, follow-up/coverage rules and source register. This new design is not runtime integration or part of the earlier clinical-source audit sign-off.

<!-- detailed-interview-graph-design -->

Open [the detailed interview graph and conversation rules](12_Adult_Depression_Interview_Graph_and_Rules.md) for source-linked targets, conditional follow-ups, unanswered-reply handling, diagrams and offline routing checks. This is new research design, not runtime integration or clinical validation.

<!-- full-graph-atlas -->

Open [the full numbered assessment graph](13_Full_Numbered_Assessment_Graph.md) for all route/response diagrams, all branch sequences and the complete optional follow-up catalog. It is a visual reading view of the current research design, not a runtime or clinical-validation change.

<!-- optional-measurement-knowledge -->

Open [screening, measurement and scoring](14_Screening_Measurement_and_Scoring.md) for instrument selection, optional early offer/M8 checkpoint, narrative-versus-scale rules and the offline arithmetic reference. Clinical/language/mode review and agent integration remain pending.
