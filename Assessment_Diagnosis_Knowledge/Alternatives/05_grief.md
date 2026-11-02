# Ordinary grief and prolonged grief disorder

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Understand a bereavement response, identify loss-specific persistent difficulties and assess possible coexisting depression.

## Benefit for our system

Avoid pathologizing normal grief, missing PGD or treating all bereavement-related sadness as one depressive diagnosis.

## Scope and interpretation

Adult DSM-5-TR PGD differential plus ordinary grief context; ICD-11 timing/requirements are not merged into DSM.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- Adult DSM-5-TR reference requires the death of a close person at least twelve months earlier, a persistent longing/preoccupation response and clinically significant burden; time alone is insufficient.
- At least one core separation-distress experience and at least three additional symptom groups are reviewed: identity disruption, disbelief, avoidance, emotional pain, reintegration difficulty, numbness, meaninglessness and loneliness.
- Symptoms must have the required most-day/near-daily recent-month pattern, exceed expected social/cultural/religious norms in context, and not be better explained by another disorder, substance or medical condition.
- Loss-focused longing and broader pervasive depression can be distinct and coexist. Neither an enjoyable moment nor bereavement excludes MDD. Acute grief can be very painful without PGD.

Sources for these distinctions: [DSM_PGD; APA_PGD; APA_GRIEF; PG13R_2021].

## When and how to explore

Explore when a death is reported or the account is strongly loss-focused; do not assume every loss is bereavement after a death.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Ask about the relationship and time since death sensitively.
2. Explore the person's actual grief experiences and cultural meaning.
3. Clarify recent frequency, burden and life engagement.
4. Review broader depression, trauma, support and safety separately.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

### Bereavement and cultural context — `bereavement_context`

Death of a close person, loss timing, relationship, cultural expectations and support without treating normal grief as illness.

Sources: [DSM_PGD; APA_GRIEF].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `relationship` | Who died and closeness as reported. | Supported text; preserve timing/units and uncertainty |
| `death_time` | Actual time since death, preserving uncertainty. | Supported text; preserve timing/units and uncertainty |
| `cultural_context` | Meaning, rituals and norms described by the person, not guessed from identity. | Supported text; preserve timing/units and uncertainty |
| `course` | Waves/triggers, persistence and change since loss. | Supported text; preserve timing/units and uncertainty |
| `functioning` | Actual engagement and difficulties. | Supported text; preserve timing/units and uncertainty |
| `support` | Relevant support and barriers. | Supported text; preserve timing/units and uncertainty |

**Example question:** Would you like to tell me about the loss and how it has affected you?

**Follow-up:** Respect grief without a fixed recovery timetable; ask only meaningful remaining details.

**Do not infer:** Time since death alone does not establish PGD, and grief does not exclude MDD.

### Grief-specific experiences — `grief_specific_experiences`

Longing/preoccupation and other loss-linked experiences, distinguished from generalized depressive symptoms.

Sources: [DSM_PGD].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `longing_preoccupation` | Actual yearning or preoccupation with the deceased. | Supported text; preserve timing/units and uncertainty |
| `identity_disbelief` | Reported identity disruption or disbelief. | Supported text; preserve timing/units and uncertainty |
| `avoidance` | Avoidance of reminders that the person died. | Supported text; preserve timing/units and uncertainty |
| `pain` | Loss-linked emotional pain. | Supported text; preserve timing/units and uncertainty |
| `reintegration` | Difficulty engaging in relationships/activities or future plans. | Supported text; preserve timing/units and uncertainty |
| `numbness_meaning_loneliness` | Actual numbness, meaninglessness or loneliness; preserve which is reported. | Supported text; preserve timing/units and uncertainty |
| `recent_frequency` | Most-day/nearly-daily pattern over the last month as actually described. | Supported text; preserve timing/units and uncertainty |
| `burden_context` | Distress/interference and cultural-context interpretation needs. | Supported text; preserve timing/units and uncertainty |

**Example question:** What has been hardest about the grief recently?

**Follow-up:** Clarify loss-specific experiences and current frequency; do not count alternatives as separate criteria without evidence.

**Do not infer:** Yearning, broad depression and suicidal thoughts are distinct; any wish to die needs direct clarification rather than an assumed grief explanation.

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

### Interest and pleasure — `interest_pleasure`

Reduced desire for activities and/or reduced enjoyment.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve timing/units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve timing/units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve timing/units and uncertainty |
| `days_per_week` | Stated days affected; keep units and wording instead of imposing a diagnostic cutoff. | Supported text; preserve timing/units and uncertainty |
| `proportion_of_day` | Reported share of an affected day; most of the day is already useful. | Supported text; preserve timing/units and uncertainty |
| `interest` | Reported wanting or motivation to engage. | Supported text; preserve timing/units and uncertainty |
| `pleasure` | Enjoyment when engaged. | Supported text; preserve timing/units and uncertainty |
| `activities` | Affected activities and retained interests. | Supported text; preserve timing/units and uncertainty |
| `breadth` | How broadly activities are affected. | Supported text; preserve timing/units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have your interest or enjoyment in your usual activities changed?

**Follow-up:** Separate wanting from enjoying; establish breadth if relevant.

**Do not infer:** One retained hobby does not negate all symptoms; not doing an activity may reflect lack of opportunity.

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

- Do not diagnose solely because twelve months have passed.
- Do not withhold support before the diagnostic time window.
- DSM adult twelve-month and ICD-11 timing are different frameworks.
- A wish to be reunited with the deceased requires careful direct safety clarification; it is not automatically intent or automatically harmless.
- PG-13-R is a research/measurement reference; no items, scoring or inherited accuracy are implemented.

## Professional review and handoff

Seek qualified review for persistent impairing grief or coexisting disorders; address safety and support needs regardless of time since death.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### DSM_PGD

[APA DSM-5-TR (2022), Prolonged Grief Disorder](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed pp.322–323 / PDF viewer pp.481–482

**Contribution:** Adult bereavement interval, core/additional symptoms, culture and differential

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.

### APA_PGD

[APA, Prolonged Grief Disorder fact sheet](https://www.psychiatry.org/getContentAsset/2a667a19-80ac-4aaf-8751-9ed240619757/dfc3d011-8f63-43f6-9ed8-4b444333a1d0/APA-DSM5TR-ProlongedGriefDisorder.pdf?language=en)

**Location:** p.1: description and adult/child timing

**Contribution:** Official overview; not a complete diagnostic interview

**Access:** Official primary guidance/indexed recommendation text inspected

### APA_GRIEF

[APA, What Is Depression?](https://www.psychiatry.org/patients-families/depression/what-is-depression)

**Location:** Grief versus depression discussion

**Contribution:** Loss context and possible coexistence

**Access:** Public primary-source material inspected

### PG13R_2021

[Prigerson et al. (2021), Validation of DSM-5-TR PGD criteria and PG-13-Revised](https://pmc.ncbi.nlm.nih.gov/articles/PMC7801836/)

**Location:** World Psychiatry 20:96–106; objectives, Table 1 and validation results

**Contribution:** Primary validation study supports grief-specific measurement; does not validate our wording or predict an individual

**Access:** Primary indexed article excerpts inspected; direct PMC text encountered a browser check. No raw data or scale items bundled.

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
