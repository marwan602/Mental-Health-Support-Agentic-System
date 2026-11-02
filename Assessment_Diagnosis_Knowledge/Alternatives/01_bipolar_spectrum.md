# Bipolar I, bipolar II and cyclothymic/other bipolar-spectrum presentations

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Check whether a depressive presentation belongs to an illness with lifetime mania, hypomania or sustained subthreshold activation.

## Benefit for our system

Avoid summarizing depression as unipolar MDD while relevant activation history is missing; provide an interpretable specialist handoff.

## Scope and interpretation

Focused bipolar differential assessment with detailed episode/course information; not a complete bipolar management or coding package.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- Bipolar I requires a qualifying lifetime manic episode; a depressive episode is common but not required. A reported history needs assessment, not acceptance as a confirmed diagnosis.
- Mania reference: distinct abnormal mood plus increased energy/activity, generally at least one week (or any duration if hospitalization is necessary), with associated changes and marked impairment/hospitalization or psychotic features; medical/exposure and psychotic-disorder alternatives require review.
- Hypomania reference: at least four consecutive days, observable/uncharacteristic change in functioning, and no marked impairment/hospitalization or psychotic features. Associated features need same-period review: grandiosity, reduced sleep need, speech pressure, racing thoughts, distractibility, activity/agitation and consequential behaviour; three are required, or four if mood is only irritable.
- Bipolar II requires a qualifying hypomanic episode and a major depressive episode, with no manic episode; hypomania being less impairing than mania does not mean the overall illness is mild.
- Adult cyclothymic reference: at least two years of numerous subthreshold high/low periods, present at least half the time, with no symptom-free gap longer than two months; full depressive, manic or hypomanic episodes have never been met, and burden/alternative explanations still matter.
- Shorter or otherwise incomplete activation can still need specialist review. Do not force it into bipolar I/II or invent an other-specified bipolar subtype from an incomplete interview.

Sources for these distinctions: [DSM_BIPOLAR; NICE_185; NIMH_BIPOLAR].

## When and how to explore

Lifetime activation is relevant in any depression assessment. Ask focused follow-ups if the account suggests a distinct high/irritable, energetic or disinhibited period, reduced sleep need, or prior bipolar formulation.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Ask about a distinct lifetime change in mood/activity.
2. If endorsed, choose one period and clarify baseline, duration and same-period changes.
3. Clarify restedness after less sleep, observations and consequences.
4. Review hospitalization/psychotic symptoms, treatment/exposures and medical context.
5. Review depressive periods, interepisode course and professional assessment.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

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

### Reduced need for sleep — `reduced_sleep_need`

Less sleep with feeling rested/energetic, distinct from inability to sleep with exhaustion.

Sources: [DSM_BIPOLAR].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `sleep_amount` | Actual amount as reported, no invented baseline. | Supported text; preserve timing/units and uncertainty |
| `restedness` | How the person felt after less sleep. | Supported text; preserve timing/units and uncertainty |
| `usual_sleep` | Usual amount, if supplied. | Supported text; preserve timing/units and uncertainty |
| `duration` | How long this pattern lasted. | Supported text; preserve timing/units and uncertainty |
| `overlap` | Whether it coincided with the same activation period. | Supported text; preserve timing/units and uncertainty |
| `other_reasons` | Opportunity, shift work, substance or medical context. | Supported text; preserve timing/units and uncertainty |

**Example question:** When you slept less during that period, did you feel rested or tired afterwards?

**Follow-up:** Clarify sleep opportunity and same-period energy; do not infer the answer from hours alone.

**Do not infer:** Short sleep plus fatigue is not reduced sleep need.

### Associated activation features — `activation_associated_changes`

Actual same-period changes in self-view, speech, thoughts, attention, activity or consequential behaviour.

Sources: [DSM_BIPOLAR].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `self_view` | Unusual inflated confidence or grandiosity, not ordinary confidence. | Supported text; preserve timing/units and uncertainty |
| `speech` | More/pressured speech as reported, not judged from chat typing. | Supported text; preserve timing/units and uncertainty |
| `thought_speed` | Racing thoughts or rapid shifts, distinguished from repetitive anxious worries. | Supported text; preserve timing/units and uncertainty |
| `attention` | Distractibility against baseline. | Supported text; preserve timing/units and uncertainty |
| `activity` | Purposeful activity or motor agitation as reported. | Supported text; preserve timing/units and uncertainty |
| `consequential_behaviour` | Actual unusual spending, sexual/business or other risky actions without moral judgment. | Supported text; preserve timing/units and uncertainty |
| `overlap` | Which changes occurred together and during which period. | Supported text; preserve timing/units and uncertainty |

**Example question:** What else changed during that same period?

**Follow-up:** Ask about relevant missing features individually rather than a long leading list.

**Do not infer:** Do not count symptoms from different periods together or diagnose from chat style.

### Activation severity and causal context — `activation_severity_context`

Reported marked impairment, hospitalization, psychotic experiences and exposure/medical context.

Sources: [DSM_BIPOLAR; NICE_185].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `impairment` | Actual severity/consequences as reported. | Supported text; preserve timing/units and uncertainty |
| `hospitalization` | Whether/why admission was necessary or occurred, if reported. | Supported text; preserve timing/units and uncertainty |
| `psychotic_experience` | Reported perceptual/belief changes; needs interpretation. | Supported text; preserve timing/units and uncertainty |
| `exposures` | Named medicines/substances and actual changes. | Supported text; preserve timing/units and uncertainty |
| `persistence` | What persisted after an already-occurring exposure change. | Supported text; preserve timing/units and uncertainty |
| `medical_context` | Reported conditions and findings. | Supported text; preserve timing/units and uncertainty |
| `current_concerns` | Immediate concerns and actual available support. | Supported text; preserve timing/units and uncertainty |

**Example question:** Did that period cause serious problems or lead you to need urgent care?

**Follow-up:** Current severe activation or psychotic concerns change review urgency; do not wait for duration thresholds.

**Do not infer:** Do not recommend stopping/restarting treatment to test cause; one or two activation symptoms after medicine are not automatically a bipolar episode.

### Long-term mood fluctuation — `longterm_mood_fluctuation`

Repeated subthreshold high/low experiences across years, with gaps and possible full episodes reviewed separately.

Sources: [DSM_BIPOLAR].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `observation_span` | Actual span described. | Supported text; preserve timing/units and uncertainty |
| `high_periods` | Reported activation symptoms and their duration. | Supported text; preserve timing/units and uncertainty |
| `low_periods` | Reported depressive symptoms and duration. | Supported text; preserve timing/units and uncertainty |
| `proportion_of_time` | How often symptoms were present across the span. | Supported text; preserve timing/units and uncertainty |
| `longest_gap` | Longest symptom-free interval, if actually known. | Supported text; preserve timing/units and uncertainty |
| `full_episode_history` | Earlier periods needing full mania/hypomania/depression review. | Supported text; preserve timing/units and uncertainty |

**Example question:** Over the longer term, how have the higher and lower periods alternated?

**Follow-up:** Clarify sustained course and gaps; do not turn every mood fluctuation into an episode.

**Do not infer:** Mood swings do not automatically establish cyclothymia or bipolar illness.

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

### Family history — `family_history`

Relevant family mood/psychiatric history.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `relative` | Relationship, without unnecessary identifying details. | Supported text; preserve timing/units and uncertainty |
| `reported_condition` | Condition as reported. | Supported text; preserve timing/units and uncertainty |
| `certainty` | How the person knows; unknown remains unknown. | Supported text; preserve timing/units and uncertainty |

**Example question:** Is there relevant mental-health history in your family?

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

- Family history, irritability, ordinary happiness or one medication reaction does not confirm bipolar illness.
- Insomnia with fatigue is not reduced sleep need.
- Do not combine several different high periods into one qualifying episode.
- NICE's four-day primary-care referral prompt is not a diagnostic algorithm or a reason to ignore a shorter concerning period.
- NICE advises against questionnaires to identify bipolar disorder in primary care; no MDQ/HCL scorer is implemented here.

## Professional review and handoff

Possible current mania, severe depression, psychosis or immediate safety concerns change urgency. NICE recommends urgent specialist assessment when mania/severe depression or danger is suspected. Do not delay because a duration threshold is not yet met; the application must implement its human-review pathway.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### DSM_BIPOLAR

[APA DSM-5-TR (2022), Bipolar and Related Disorders](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed pp.140–143,150–154,160 / PDF viewer pp.256–259,268–272,279

**Contribution:** Mania/hypomania, bipolar I/II and adult cyclothymic boundaries

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.

### NICE_185

[NICE CG185, Bipolar disorder](https://www.nice.org.uk/guidance/cg185/chapter/recommendations)

**Location:** 1.2.1–1.2.3; 1.3.1–1.3.3: recognition/referral, assessment and differential

**Contribution:** Depression presentations require lifetime overactivity/disinhibition history; specialist review; questionnaires not used for primary-care bipolar identification

**Access:** Public primary-source material inspected

### NIMH_BIPOLAR

[NIMH, Bipolar Disorder](https://www.nimh.nih.gov/health/publications/bipolar-disorder)

**Location:** Types; symptom comparison; diagnosis

**Contribution:** Activation history, reduced sleep need and bipolar uncertainty

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
