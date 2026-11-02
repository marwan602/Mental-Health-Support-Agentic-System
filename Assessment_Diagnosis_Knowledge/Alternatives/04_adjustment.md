# Adjustment disorder and ordinary stress responses

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Examine symptoms linked to a stressor without treating every stress reaction as MDD or adjustment disorder.

## Benefit for our system

Record stressor timing and continuing consequences, burden and competing full syndromes; avoid an automatic residual-depression label.

## Scope and interpretation

Focused adjustment assessment, especially depressed-mood and mixed anxiety/depressed-mood presentations; no full conduct-disorder management.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- Reference onset is within three months of an identifiable stressor. Clinical significance involves disproportionate distress in context and/or functional impairment; ordinary understandable upset alone is not the diagnosis.
- The particular stress-related symptoms are not better explained by another disorder or merely exacerbation of an existing one. Normal bereavement and PGD require differentiation.
- Symptoms do not persist more than six additional months after the stressor or its consequences have ended. This is not a universal six-month-from-onset limit: ongoing stressors/consequences can support a persistent course.
- Adjustment and another disorder may coexist when each is independently justified and the other disorder does not explain those particular stress-linked symptoms; do not make the categories universally exclusive.

Sources for these distinctions: [DSM_ADJUST; NICE_222].

## When and how to explore

Explore when a clear stressor is reported or symptoms are tightly linked to a change in circumstances.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Identify the actual stressor and onset.
2. Clarify symptoms, burden and contextual meaning.
3. Ask if the stressor or consequences continue.
4. Review full depressive/trauma or other explanations before a residual formulation.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

### Stressor-linked response — `stressor_response`

An identifiable stressor, its consequences and symptom timing/meaning, with full mood and trauma alternatives reviewed.

Sources: [DSM_ADJUST].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `stressor` | Specific reported event or continuing circumstance. | Supported text; preserve timing/units and uncertainty |
| `stressor_onset` | When it began. | Supported text; preserve timing/units and uncertainty |
| `symptom_onset` | When emotional/behavioural symptoms started relative to it. | Supported text; preserve timing/units and uncertainty |
| `continuing_consequences` | Whether stressor or consequences continue and actual ending if known. | Supported text; preserve timing/units and uncertainty |
| `response` | Actual emotional/behavioural pattern and contextual meaning. | Supported text; preserve timing/units and uncertainty |
| `burden` | Distress/interference and relevant cultural context. | Supported text; preserve timing/units and uncertainty |
| `previous_pattern` | Whether this is new or an exacerbation of earlier symptoms. | Supported text; preserve timing/units and uncertainty |

**Example question:** What changed around the time this began, and is that situation or its impact still ongoing?

**Follow-up:** Clarify response, timeline and alternatives without judging whether distress is legitimate.

**Do not infer:** A stressor does not automatically establish adjustment disorder or exclude MDD.

### Depressed mood — `depressed_mood`

Reported low, sad or empty mood.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `description` | The person's account of this experience, without adding a diagnosis. | Supported text; preserve timing/units and uncertainty |
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve timing/units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve timing/units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve timing/units and uncertainty |
| `days_per_week` | Stated days affected; keep units and wording instead of imposing a diagnostic cutoff. | Supported text; preserve timing/units and uncertainty |
| `proportion_of_day` | Reported share of an affected day; most of the day is already useful. | Supported text; preserve timing/units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve timing/units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve timing/units and uncertainty |

**Example question:** How has your mood been during this period?

**Follow-up:** Meaning, persistence and episode timing if unclear.

**Do not infer:** A sad day alone does not establish the domain threshold or MDD.

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text; preserve timing/units and uncertainty |
| `examples` | Concrete difficulty or distress. | Supported text; preserve timing/units and uncertainty |
| `baseline` | Usual functioning. | Supported text; preserve timing/units and uncertainty |
| `supports` | Assistance helping preserve functioning. | Supported text; preserve timing/units and uncertainty |

**Example question:** How have these changes affected your daily life?

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

### Life context — `life_context`

Relevant stress, loss, trauma and support.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `events` | Events relevant to symptom timeline. | Supported text; preserve timing/units and uncertainty |
| `timing` | Temporal relationship. | Supported text; preserve timing/units and uncertainty |
| `support` | Current supports. | Supported text; preserve timing/units and uncertainty |
| `barriers` | Practical barriers. | Supported text; preserve timing/units and uncertainty |
| `meaning` | Person's interpretation of the context. | Supported text; preserve timing/units and uncertainty |

**Example question:** Has anything important been happening around the time these changes began?

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

- A breakup, illness or job loss does not automatically establish adjustment disorder.
- Do not judge cultural expectations from ethnicity or minimize legitimate distress.
- The six-month reference does not mean wait six months before help.

## Professional review and handoff

Professional assessment determines whether the pattern is a disorder and which formulation applies; safety needs are assessed separately from the label.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### DSM_ADJUST

[APA DSM-5-TR (2022), Adjustment Disorders](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed pp.319–320 / PDF viewer pp.477–478; differential/comorbidity p.322 / PDF p.481

**Contribution:** Stressor timing, burden, continuing consequences and alternatives

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.

### NICE_222

[NICE NG222, Depression in adults](https://www.nice.org.uk/guidance/ng222/chapter/Recommendations)

**Location:** 1.2.1–1.2.9; Definitions of depression/severity; 1.12.1

**Contribution:** Comprehensive assessment, communication, safety and specialist review

**Access:** Official search-indexed recommendation extracts inspected; direct retrieval intermittently 403

### VA_2022

[VA/DoD MDD Clinical Practice Guideline, 2022](https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/MH/mdd/VADODMDDCPGFinal508.pdf)

**Location:** p.19 Sidebars 1–2; pp.140–141 Appendix K; Appendix I pp.127–131

**Contribution:** Episode foundation, work-up and measurement context; sidebar is abbreviated DSM-5-era material

**Access:** Public primary-source material inspected

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
