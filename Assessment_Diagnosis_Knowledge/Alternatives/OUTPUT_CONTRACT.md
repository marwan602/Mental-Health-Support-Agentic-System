# Shared alternative-pathway evidence contract

This is a project storage/output design, not a clinical terminology or diagnostic algorithm. It can support the later conversational/extractor/planner integration, which has not been implemented by creating this package.

| Item | Meaning |
|---|---|
| module_id / schema_version | Fixed application contract identifiers |
| concept_id | An allowlisted information domain, not a diagnosis |
| episode_key | Code-owned period/pattern reference; not proof of a formal episode |
| subject | Patient in this contract; third-party symptoms are not reassigned |
| finding_status | Reported presence, explicit denial, unclear or conflicting account |
| temporal_status / time_reference | Current/historical/unclear context and actual reported time wording |
| attributes | Only the optional details allowed for that specific concept |
| evidence | Exact patient quote, source message, earlier context and supported claims |
| uncertainty_notes | Recall, chronology, contradiction or interpretation limits |
| semantic_check_status | Supported interpretation versus needs-review declaration; not guaranteed by JSON validation |
| question_tracking | App question target/status and unresolved target, including partial answers and declines |
| safety_handoff | Workflow review-need flag and unresolved concerns; not risk prediction or delivered contact |

One fact may inform multiple pathways through the knowledge map. Do not make the patient repeat it, copy symptoms into several new independent evidence records or force a single mutually exclusive branch. The unique snapshot key is `(concept_id, episode_key, subject)`. Code assigns message/period IDs; the LLM need not invent evidence UUIDs. Different periods remain separate, and later supported details update the matched record while preserving sources.

A known attribute has a value and explicit quote linkage. Unknown has no value. Not-applicable needs a reason and cannot stand for not asked. Omission is not denial. Reported-presence on an assessment-limit record means the limitation was reported, not that the symptom being discussed was present/absent. A “yes” needs enough earlier context to resolve what was affirmed. Context must precede the answer. Retain corrections or genuine conflicts rather than silently rewriting history.

The schema disallows diagnosis, causal verdict, criterion-count and scoring properties. It checks format, not semantics: a permitted value can still be wrongly attributed. Exact quote matching cannot prove that the quote supports the meaning. Qualified review and direct extraction/planning evaluation remain necessary. Patient reports of clinician opinions or tests are attributed testimony; independently verified records and collateral accounts require separate provenance workflows.

Do not dump all reference files/schema into every prompt. Later integration should select relevant role-specific content while preserving the conversation and accumulated evidence. Local pathway question order is project policy. It is not a licensed interview, a final cross-disorder graph or a validated optimum sequence.

## Project-controlled states

### finding_status

- `reported_present`: Explicitly described or affirmed in context; not clinical confirmation.
- `reported_absent`: Explicitly denied for this subject/period.
- `unclear`: Meaning or polarity unresolved.
- `conflicting`: Accounts for the same subject/period conflict and are retained.

### temporal_status

- `current`: Described as relevant to current period.
- `historical`: An earlier period.
- `unclear`: Timing unresolved.

### detail_status

- `known`: A supported value is available.
- `unknown`: Relevant but unresolved; no value asserted.
- `not_applicable`: Inapplicability is explicitly justified; not equivalent to not asked.

### question_status

- `not_asked`: No recorded question.
- `answered`: Target addressed.
- `partially_answered`: Some target information supplied.
- `unclear`: Response ambiguous.
- `declined`: Person chose not to answer.

### semantic_check_status

- `supported`: Evidence appears to support the claim.
- `needs_review`: Meaning/attribution remains unresolved.

### safety_handoff_status

- `not_assessed`: Available conversation has not assessed current safety; no reassuring inference.
- `no_signal_reported_in_available_text`: No concern reported in reviewed text; does not establish safety or predict future behaviour.
- `needs_clinical_review`: An unresolved concern requires clinical review; not a predictive risk category or proof of contact.
- `urgent_review_needed`: Current reported concerns require urgent human/medical review; no claim of response delivery.

## Safety and completion

NIMH adult BSSA is intended for trained clinicians following a positive ASQ screen; citing it does not validate the chat. NICE NG225 discourages predictive scales or global low/medium/high labels for suicide prediction/care decisions. Current safety, delirium/acute medical, severe activation or psychotic concerns can interrupt routine assessment. A fixed rule based on a single keyword is not a complete safety pathway. Escalation/contact must be implemented and verified before being claimed. No hotline, medication, taper, detoxification or emergency-treatment service is implemented here.

An API/model error, turn budget or empty candidate list is not a patient diagnosis or evidence of clinical completion. Respect pauses/declines. A supported summary with unresolved questions and professional review is a valid research workflow outcome.
