# Substance, medication, intoxication and withdrawal-related presentations

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Clarify actual exposures and changes that may contribute to mood, anxiety, sleep, psychosis or cognition.

## Benefit for our system

Prevent causal assumptions, identify relevant medical withdrawal concerns and separate independent depressive history from exposure timing.

## Scope and interpretation

Reuse the detailed substance/medication-induced depression package. Full substance-use-disorder diagnosis and withdrawal treatment are outside scope.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- Take a neutral history of prescribed/nonprescribed medicines, supplements, alcohol and other substances, with names, actual use and start/change/missed/stop/last-use events.
- Separate each agent's timeline; a positive toxicology result, medicine warning or symptoms occurring afterward do not prove causation in an individual.
- Preserve earlier depressive periods and actual course after already-occurring changes. Do not impose a universal abstinence month before support or independent-depression review.
- Tolerance/dependence or withdrawal alone does not establish a substance use disorder. Intoxication/withdrawal labels need appropriate assessment rather than acceptance of a colloquial label.

Sources for these distinctions: [DSM_INDUCED; TIP42; NICE_215; NICE_100].

## When and how to explore

Exposure history is relevant across assessment; expand when an exposure/change or related symptoms are reported.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Ask neutrally what is used and actual changes.
2. Identify agents separately and compare with symptom onset.
3. Review earlier mood history and current medical/safety concerns.
4. Use the detailed exposure module and appropriate professional review.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

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

### Episode timeline — `episode_timeline`

Period linking symptoms and changes.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve timing/units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve timing/units and uncertainty |
| `course` | Continuity, fluctuation or change over the relevant period. | Supported text; preserve timing/units and uncertainty |
| `overlap` | Whether symptoms occurred together. | Supported text; preserve timing/units and uncertainty |
| `intervals` | Earlier periods, recovery and residual symptoms. | Supported text; preserve timing/units and uncertainty |

**Example question:** When did these changes begin?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text; preserve timing/units and uncertainty |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text; preserve timing/units and uncertainty |
| `period` | When and for which symptoms. | Supported text; preserve timing/units and uncertainty |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text; preserve timing/units and uncertainty |
| `use` | Actual use and barriers as reported. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have you received help for something similar before?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

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

### Death/suicide-related reports — `death_suicide`

Death-related thoughts, suicidal thoughts, plans or attempts.

Sources: [ASQ_BSSA; NICE_225].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `experience` | Preserve distinctions. | death_thoughts / wish_not_alive / suicidal_thoughts / suicide_plan / suicide_attempt / unclear |
| `recency` | When last/current; do not infer resolution. | Supported text; preserve timing/units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve timing/units and uncertainty |
| `intent` | Intent as reported. | Supported text; preserve timing/units and uncertainty |
| `plan_present` | Whether a plan was explicitly reported or denied. | reported / denied / unclear |
| `access` | Access to means as reported, without generating procedural details. | Supported text; preserve timing/units and uncertainty |
| `past_behaviour` | Historical self-injury/attempt account, intent and timing. | Supported text; preserve timing/units and uncertainty |
| `support` | Available support as reported. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have you had thoughts about ending your life?

**Follow-up:** Use dedicated safety pathway; preserve current versus historical information.

**Do not infer:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

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

- No abrupt-stop/restart/taper experiment to test causation.
- Alcohol or sedative withdrawal can require medically supervised assessment; no home detox protocol is supplied.
- Withdrawal low mood is not automatically an independently qualifying induced depressive disorder.

## Professional review and handoff

Current severe withdrawal/medical concerns need appropriate medical review; prescribers manage medication decisions. Depression/safety needs remain important while attribution is uncertain.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Existing detailed knowledge to reuse

- [Substance_Medication_Induced_Depression README](../Substance_Medication_Induced_Depression/README.md)

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### DSM_INDUCED

[APA DSM-5-TR (2022), Substance/Medication-Induced Depressive Disorder](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders)

**Location:** Printed pp.201–206; substance-class Table 1 pp.545–546; PDF viewer pp.330–336 and 755–756

**Contribution:** Criteria-information map, onset descriptions, differential and substance-class reference

**Access:** Original APA text inspected through public psychiatry.ru mirror; publisher full text blocked; no redistribution rights inferred and no book bundled.

### TIP42

[SAMHSA TIP 42 (2020), Chapter 4](https://www.ncbi.nlm.nih.gov/books/NBK571021/)

**Location:** Substance-Induced Mental Disorders; Substance-Induced Depressive Disorders; Exhibits 4.16–4.18

**Contribution:** Longitudinal assessment, independent/induced distinction and co-occurring conditions

**Access:** Public primary-source material; relevant sections inspected

### NICE_215

[NICE NG215, medicines associated with dependence or withdrawal symptoms](https://www.nice.org.uk/guidance/ng215/chapter/Recommendations)

**Location:** 1.5.6; 1.5.15–1.5.17

**Contribution:** Withdrawal assessment and prescriber review; no abrupt-stop experiments

**Access:** Public primary-source material; relevant sections inspected

### NICE_100

[NICE CG100, alcohol-use disorders: physical complications](https://www.nice.org.uk/guidance/cg100/chapter/recommendations)

**Location:** 1.1.1 acute withdrawal assessment/admission and warning against sudden reduction

**Contribution:** Alcohol withdrawal safety boundary; no home detoxification protocol

**Access:** Public primary-source material; relevant sections inspected

### ASQ_BSSA

[NIMH Adult Outpatient Brief Suicide Safety Assessment Guide](https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials/adult-outpatient/adult-outpatient-brief-suicide-safety-assessment-guide)

**Location:** Intended users; thoughts, plan, past behaviour, supports and disposition sections

**Contribution:** Safety information domains; clinician guide following positive ASQ, not autonomous LLM validation

**Access:** Public primary-source material inspected

### NICE_225

[NICE NG225, Self-harm](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)

**Location:** 1.6.1–1.6.6

**Contribution:** No predictive low/medium/high stratification; needs-focused assessment

**Access:** Public primary-source material inspected

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

### NICE_103

[NICE CG103, delirium](https://www.nice.org.uk/guidance/cg103/chapter/Recommendations)

**Location:** 1.3.1, 1.5 and 1.6.1–1.6.3; 2023 assessment update: competent practitioner/4AT and final clinical diagnosis

**Contribution:** Acute/fluctuating changes in attention/cognition need assessment; hospital/long-term-care guideline context

**Access:** Public primary-source material; relevant sections inspected
