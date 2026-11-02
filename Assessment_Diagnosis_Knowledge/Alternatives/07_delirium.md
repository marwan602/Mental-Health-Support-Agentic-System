# Delirium and acute medical/cognitive change

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Recognize acute/fluctuating attention or awareness changes that should interrupt routine psychiatric questioning.

## Benefit for our system

Avoid treating a potentially urgent medical syndrome as ordinary depressive poor concentration or lack of engagement.

## Scope and interpretation

Focused recognition and medical handoff. NICE CG103 is a hospital/long-term-care guideline; this chat does not implement a validated delirium screen.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- Recent change over hours/days, fluctuation, reduced attention/awareness and altered thinking can indicate delirium; quiet withdrawal/lethargy may occur as well as agitation.
- Known dementia does not exclude delirium superimposed on it. Where difficult to distinguish, NICE prioritizes delirium management.
- The 2023 NICE update specifies assessment by a competent practitioner using 4AT where appropriate, with CAM-ICU/ICDSC in critical care/recovery and a final diagnosis by a professional with relevant expertise. This is not a script for the LLM to administer or score.

Sources for these distinctions: [NICE_103].

## When and how to explore

Pause routine questioning if current sudden confusion, altered attention/awareness or marked fluctuation is reported.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Clarify briefly what changed, when and who observed it, only as feasible.
2. Prioritize medical assessment and communication/support needs.
3. Record actual escalation/contact status rather than continue until all fields are filled.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

### Acute/fluctuating cognitive change — `acute_attention_change`

New change over hours/days in attention, awareness or thinking, possibly hypoactive rather than agitated.

Sources: [NICE_103].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `baseline` | Usual cognition/behaviour. | Supported text; preserve timing/units and uncertainty |
| `onset` | Reported start and speed of change. | Supported text; preserve timing/units and uncertainty |
| `fluctuation` | Changes across the day. | Supported text; preserve timing/units and uncertainty |
| `attention_awareness` | Actual difficulty attending or altered awareness. | Supported text; preserve timing/units and uncertainty |
| `other_changes` | Reported lethargy/agitation, perception or sleep-wake changes. | Supported text; preserve timing/units and uncertainty |
| `medical_exposures` | Recent illness, treatment or withdrawal context. | Supported text; preserve timing/units and uncertainty |
| `source` | Who noticed, as reported. | Supported text; preserve timing/units and uncertainty |

**Example question:** Has there been a sudden change in confusion or ability to pay attention compared with usual?

**Follow-up:** Current acute change takes priority over the routine depression interview and needs medical assessment.

**Do not infer:** Do not rule out delirium because the person is quiet or has known dementia; chat is not a 4AT assessment.

### Medical context — `medical_context`

Relevant reported medical history and symptoms.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `conditions` | Reported conditions; distinguish reported diagnosis from confirmation. | Supported text; preserve timing/units and uncertainty |
| `timeline` | Relationship to symptoms. | Supported text; preserve timing/units and uncertainty |
| `investigations` | Results only if actually supplied. | Supported text; preserve timing/units and uncertainty |
| `clinician_review` | Known professional assessment or unresolved need. | Supported text; preserve timing/units and uncertainty |

**Example question:** Are there health conditions that might be relevant to these changes?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Medicines and substances — `exposure_context`

Relevant treatment/substance exposure account.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `name` | Named exposure. | Supported text; preserve timing/units and uncertainty |
| `dose_use` | Reported amount/use; never recommend a dose. | Supported text; preserve timing/units and uncertainty |
| `start_change_stop` | Timing of changes. | Supported text; preserve timing/units and uncertainty |
| `symptom_timing` | Reported temporal relationship. | Supported text; preserve timing/units and uncertainty |
| `source_kind` | Medicine, alcohol, other substance or unclear. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have any medicines or substance-use patterns changed around this time?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Assessment participation and limits — `assessment_limits`

Reported inability to recall, decline, uncertainty or communication difficulty; not symptom absence.

Sources: [NICE_222; VA_2022].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `target` | Specific unresolved topic. | Supported text; preserve timing/units and uncertainty |
| `limit` | Reported limitation. | cannot_recall / declined / ambiguous / communication_difficulty / conflicting_reports / other_reported_limit |
| `known_part` | Actual partial information. | Supported text; preserve timing/units and uncertainty |
| `support_requested` | Actual requested accommodation. | Supported text; preserve timing/units and uncertainty |

**Example question:** Would you prefer that I ask this another way or leave it for now?

**Follow-up:** Respect choice and carry the unresolved target into review.

**Do not infer:** A declined question does not establish a negative differential history.

## Interpretation limits

- No agitation or hallucinations does not rule out delirium.
- Poor concentration alone is not delirium.
- Do not claim a chat or JSON flag has delivered medical care.

## Professional review and handoff

Current acute cognitive/awareness change needs timely medical assessment, often urgent; the exact response depends on setting and current condition, through the implemented care pathway.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### NICE_103

[NICE CG103, delirium](https://www.nice.org.uk/guidance/cg103/chapter/Recommendations)

**Location:** 1.3.1, 1.5 and 1.6.1–1.6.3; 2023 assessment update: competent practitioner/4AT and final clinical diagnosis

**Contribution:** Acute/fluctuating changes in attention/cognition need assessment; hospital/long-term-care guideline context

**Access:** Public primary-source material; relevant sections inspected

### VA_2022

[VA/DoD MDD Clinical Practice Guideline, 2022](https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/MH/mdd/VADODMDDCPGFinal508.pdf)

**Location:** p.19 Sidebars 1–2; pp.140–141 Appendix K; Appendix I pp.127–131

**Contribution:** Episode foundation, work-up and measurement context; sidebar is abbreviated DSM-5-era material

**Access:** Public primary-source material inspected

### NICE_222

[NICE NG222, Depression in adults](https://www.nice.org.uk/guidance/ng222/chapter/Recommendations)

**Location:** 1.2.1–1.2.9; Definitions of depression/severity; 1.12.1

**Contribution:** Comprehensive assessment, communication, safety and specialist review

**Access:** Official search-indexed recommendation extracts inspected; direct retrieval intermittently 403
