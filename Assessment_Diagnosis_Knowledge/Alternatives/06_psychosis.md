# Psychotic experiences, mood disorders with psychosis and schizoaffective alternatives

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Clarify unusual experiences and their relationship to mood episodes, exposures and medical context.

## Benefit for our system

Avoid confusing psychotic depression with a primary psychotic disorder, trauma phenomena, cultural experiences or delirium.

## Scope and interpretation

Focused recognition and specialist handoff for schizophrenia-spectrum/schizoaffective alternatives; not full diagnosis or treatment of all psychotic disorders.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- A hallucination, unusual belief or disorganized account alone does not establish schizophrenia. Review exact experience, cultural/sleep/grief context, medical/exposure factors, function and timeline.
- Psychotic symptoms during a depressive episode may need a psychotic-depression formulation, but a lifetime specialist assessment is needed to determine the relationship.
- Schizoaffective reference includes a full major mood episode with the schizophrenia symptom syndrome, a lifetime interval of at least two weeks of delusions/hallucinations without a major mood episode, and mood episodes during the majority of the total active/residual illness. Those facts and causal exclusions must be considered together.
- A report of psychosis outside low mood is a reason for clarification, not sufficient to assign schizoaffective disorder. The major depressive episode in its schizoaffective criterion must include depressed mood.

Sources for these distinctions: [NICE_178; DSM_PSYCH].

## When and how to explore

Explore when perceptual, belief, disorganization or prior psychotic-diagnosis information is reported; do not infer it from unfamiliar cultural expression.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Ask a neutral description and current distress/safety.
2. Clarify awake/asleep and cultural/medical/exposure context.
3. Compare timing with full mood periods and lifetime course.
4. Preserve the account and seek specialist assessment without debating or validating delusional content.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

### Unusual perceptual or belief experiences — `psychotic_experiences`

Reported perceptions, beliefs or disorganization requiring sensitive contextual and specialist interpretation.

Sources: [NICE_178; DSM_PSYCH].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `experience` | What the person actually experiences; neutral wording, no confirmation of the belief. | Supported text; preserve timing/units and uncertainty |
| `context` | Awake/asleep, bereavement, cultural/spiritual context and other circumstances. | Supported text; preserve timing/units and uncertainty |
| `conviction_distress` | Meaning, certainty and distress as reported. | Supported text; preserve timing/units and uncertainty |
| `frequency_duration` | Actual timing and persistence. | Supported text; preserve timing/units and uncertainty |
| `thought_behaviour_changes` | Reported disorganization or behaviour changes, not inferred from typing. | Supported text; preserve timing/units and uncertainty |
| `safety_content` | Threatening/command content, distress and immediate needs if reported. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have you noticed experiences such as hearing or seeing things that others do not seem to notice?

**Follow-up:** If endorsed, explore neutral description, context and current concerns; arrange appropriate specialist assessment.

**Do not infer:** Do not endorse a delusion as fact, diagnose from a spiritual belief, or treat a hallucination report as schizophrenia by itself.

### Psychosis and mood across time — `psychosis_mood_course`

Relationship between psychotic experiences and full mood periods across the illness, not one isolated answer.

Sources: [DSM_PSYCH].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `mood_periods` | Actual depressive/activation periods and their boundaries. | Supported text; preserve timing/units and uncertainty |
| `outside_mood_periods` | Whether experiences occurred outside major mood periods and how long. | Supported text; preserve timing/units and uncertainty |
| `overall_course` | Proportion/sequence across active and residual illness, if genuinely known. | Supported text; preserve timing/units and uncertainty |
| `reported_diagnoses` | Attributed specialist diagnoses, not confirmation. | Supported text; preserve timing/units and uncertainty |
| `exposure_medical_context` | Concurrent exposures/illness and investigations. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have those experiences also happened at times when you were not having a low or unusually high mood period?

**Follow-up:** Keep uncertainty; a full lifetime timeline may require collateral/records and specialist review.

**Do not infer:** Two weeks of an unusual experience alone does not diagnose schizoaffective disorder.

### Distinct activation period — `activation_mood_energy`

A change in mood AND activity/energy compared with baseline, rather than ordinary happiness or lifelong temperament.

Sources: [DSM_BIPOLAR].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `mood` | Reported unusually elevated, expansive or irritable mood. | Supported text; preserve timing/units and uncertainty |
| `energy_activity` | Change in energy/goal-directed activity. | Supported text; preserve timing/units and uncertainty |
| `onset_duration` | Start, end/ongoing and number of consecutive days. | Supported text; preserve timing/units and uncertainty |
| `within_day_pattern` | How much of the day and how often during that period. | Supported text; preserve timing/units and uncertainty |
| `baseline_change` | Difference from usual; distinguish episodic change from longstanding traits. | Supported text; preserve timing/units and uncertainty |
| `observer` | Who reportedly noticed, preserving source attribution. | Supported text; preserve timing/units and uncertainty |
| `functional_consequences` | Actual work/social/self-care consequences, not severity assigned from enthusiasm. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have there been distinct times when your mood and energy were unusually different from your usual self?

**Follow-up:** If endorsed, clarify one period and actual changes; keep lifetime and current periods separate.

**Do not infer:** Irritability, racing worry or a busy productive day alone does not establish mania/hypomania.

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

## Interpretation limits

- Do not endorse a threatening belief as established fact.
- Typing errors or unusual wording do not prove thought disorder.
- Trauma intrusions, grief experiences and sleep-transition perceptions need context.
- Do not make a diagnosis from the two-week reference alone.

## Professional review and handoff

NICE supports timely specialist assessment for concerning psychotic presentations, including medical/exposure review. Current severe symptoms or safety concerns require the appropriate urgent pathway.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### NICE_178

[NICE CG178, Psychosis and schizophrenia in adults](https://www.nice.org.uk/guidance/cg178/chapter/recommendations)

**Location:** 1.2 recognition/referral; 1.3.3.1–1.3.3.4 multidisciplinary assessment and affective presentations

**Contribution:** Prompt specialist assessment and medical/exposure/cultural/contextual review

**Access:** Official primary guidance/indexed recommendation text inspected

### DSM_PSYCH

[APA DSM-5-TR (2022), Schizoaffective Disorder](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed pp.121–122 / PDF viewer pp.232–233

**Contribution:** Mood/psychosis lifetime relationship; isolated duration is insufficient

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.

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

### DSM_BIPOLAR

[APA DSM-5-TR (2022), Bipolar and Related Disorders](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed pp.140–143,150–154,160 / PDF viewer pp.256–259,268–272,279

**Contribution:** Mania/hypomania, bipolar I/II and adult cyclothymic boundaries

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.
