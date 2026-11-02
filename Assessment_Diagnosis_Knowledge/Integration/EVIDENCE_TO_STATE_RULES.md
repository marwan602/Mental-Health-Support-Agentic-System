# Evidence to application state: integration specification

This is an explicit **project adapter specification**, informed by the clinical concept definitions and the interview controller. It is not a validated clinical interview or an automatic text classifier. Implementers must evaluate semantic decisions against annotated fictional cases.

## 1. Identifiers and period registry

The application assigns unique message IDs and creates episode/period IDs. Do not ask a language model to invent evidence UUIDs. Identify clinical records by **module + concept + subject + actual episode/period**, preserving every source-linked revision. `current`, `longterm`, `cycle`, `lifetime` and `contact` are graph binding roles, not interchangeable clinical periods. A historical episode needs its own actual ID. Pregnancy/delivery and menstrual dates may be imprecise; retain that uncertainty.

Original module schemas use `episode_key`; the graph uses `period_id`. Map them explicitly to the same registered actual period when they refer to the same period. Do not put a lifetime exposure history into the presenting episode just because the latest question concerns current symptoms.

## 2. Ordered message interpretation

Retain original questions and patient responses in order. A patient 'Yes' may support the content of a preceding clear question, but only within its scope and period. Cite the patient message as evidence and the earlier question as context. The quoted word does not itself contain a symptom definition. The reference validator checks chronology; a semantic decision still has to verify which question was answered.

If 'yes' could refer to several alternatives or a compound question, classify the meaning as unclear and ask a focused clarification. A question such as 'more or less sleep?' cannot establish direction through 'yes'. Do not interpret quoted statements about another person as the patient's own symptoms. Third-party accounts and uncertain voice transcripts need a separately identified provenance path; do not relabel them as a direct patient report.

## 3. Evidence-to-coverage transition rules

| Evidence/response | State transition | Do not do |
|---|---|---|
| A concept is clearly reported in its defined scope and period | Root coverage may be `supported`, with `finding_status=reported_present`, message pointers and incremented revision | Do not mark every attribute answered |
| A symptom is clearly denied, covering the whole target scope and period | Root coverage may be `supported`, with `finding_status=reported_absent` | Do not extend a present-period denial to lifetime history or another episode |
| A concept combines alternatives and only one part is denied | Preserve the narrower denial; leave whole-target adequacy unresolved | Do not deny the entire interest/pleasure domain from denial of interest loss alone |
| An attribute has a supported `known` value, verified against its definition | Mark its detail target `supported` with the same evidence and period | Do not infer another field merely because its label looks similar |
| A detail is unmentioned or schema `unknown` | Keep `not_asked` or `needs_clarification`, according to whether it was asked | Never convert missing to absent, zero or normal |
| The person explicitly does not know | Classify reply `does_not_know`; offer an optional simpler wording/anchor once, or defer | Do not invent a date, quantity or denial |
| An answer supplies only part of the requested meaning | Retain the supported part; pending reply `partial` for the missing part | Do not repeat the whole question or discard the useful part |
| Mutually inconsistent reports remain unresolved | Preserve both; finding/target needs clarification, with both evidence pointers | Do not select the most recent report just because it is newer |
| An explicit correction identifies an earlier statement as mistaken | Append the correction and its relation to the earlier revision; use the corrected view with history retained | Do not delete the original quote |
| A report describes genuine change over time | Create/update distinct actual time periods and retain both reports | Do not treat every change as a contradiction or correction |
| The person declines a question, concept, module or session | Apply a separate scoped block and retain earlier facts. Mark only outstanding affected coverage declined | Do not equate refusal with absence or force a response |
| A topic is deferred | Record period, reason and unresolved target; skip it unless participation/priorities later change | Do not silently call it answered |
| A field is genuinely inapplicable | Use `not_applicable` with a justified reason matching its clinical meaning | Do not assume inapplicability from gender, age stereotype, missing information or an irrelevant question |

Coverage `supported` means information is present, not that a diagnostic requirement is satisfied. Diagnosis review separately checks whether the value, qualifiers and whole clinical picture meet the relevant requirement.

## 4. One answer can cover several targets

'Around six days a week. On those days, I feel down for most of the day' can support both recurrence and proportion-of-day targets for the same mood period. Extract both supported details. Do not ask 'how much of the day?' again. 'Most days' is useful qualitative frequency but does not justify inventing six days. A value can inform more than one target only after checking the actual semantics and units.

An answer to a sleep question may also report appetite or functioning. Preserve all applicable clinical information, then check whether the original sleep target remains unanswered. Acknowledge the volunteered topic and offer a return without coercion when still useful. Non-diagnostic goals/preferences belong in the separate care context, not a symptom count.

## 5. Cross-module reuse

`same_label_review_candidates` in the routing index is a discovery aid. It is not permission to copy an entire record. For every proposed reuse:

1. Compare the source and destination definitions and the exact field meaning.
2. Confirm patient subject and actual period; distinguish concurrent episode, long-term depressed periods and cycle windows.
3. Check the destination field's value set and original schema. Do not convert a qualitative answer into a numeric category without explicit support.
4. Reuse only supported compatible facts, preserving original evidence. Do not transfer criterion thresholds or diagnostic conclusions.
5. Leave destination-specific qualifiers unresolved and ask only for those missing qualifiers if relevant.

Example: a reported sleep difficulty can inform symptom description in a persistent-depression review. It does not establish that the difficulty occurred during the required long-term depressed periods. A PMDD review still needs its specific cyclical relationship and prospective confirmation. Separate qualified module records can reference the same patient quote after those checks; the patient need not repeat it.

## 6. Branch facts and supplemental requests

Branch status is `open`, `not_indicated` or `unknown`; it is not present/absent diagnosis. A non-unknown branch decision needs evidence and a reason. Unknown does not mean excluded. Preserve unresolved branch applicability in handoff. Relevant activation, medical/exposure, reproductive/cycle and course information can justify additional assessment without confirming an explanation.

A supplemental request must identify a `conditional_supplement` target from `route_completion.json`, a relevant reason, real source message IDs and a requirement reference. The reference wrapper requires an eligible active module before asking. Clinical need and selected priority are still semantic decisions; a large index must not become an obligatory checklist.

## 7. Safety and review delivery

Keep reported current/historical concerns, unresolved information, action needed, and action actually delivered separate. A negative ideation answer, missing item or total questionnaire score does not establish safety clearance. Do not output low/medium/high predictive suicide-risk categories. The service must define human review and urgent response appropriate to its setting. A model flag cannot count as clinician contact or a delivered review.

Reference controller acknowledgement is bound to the safety target, actual period and coverage revision. It does not prove clinical clearance. If new relevant information appears, reassess review needs; do not reuse an old timeless acknowledgement.

## 8. Synthesis and pointer convention

Use application evidence pointers such as `ledger[0].snapshot.records[1]` (zero-based indices) or another explicit application-assigned stable location. The model copies supplied pointers. Source references must be qualified, for example `MDD/sources.json#SAMHSA_2020`. An unassessed requirement has no patient evidence pointer; it still needs a source reference explaining the requirement. A contradicted requirement needs the actual conflicting or negative report, not an invented statement.

The synthesis component reports possible explanations, requirements supported/contradicted/unclear/not_assessed/requiring professional review, alternatives and remaining information. It must not turn route completion or lack of another label into an unspecified-depression diagnosis. The package's clinical source uncertainty and access limitations remain visible in the output when relevant.

## 9. Engineering acceptance

Schema validation checks allowed structure; quote validation checks provenance mechanics; annotated routing tests check programmed selection. None independently verifies clinical interpretation. Before real use, evaluate extraction-to-coverage and synthesis against adjudicated cases, evaluate the whole conversation and obtain appropriate clinical review. For fictional integration, tests must at least cover contextual yes/no, volunteered findings, delayed updates, conflicting reports, explicit corrections, scoped refusal, off-topic replies and period-specific reuse.
