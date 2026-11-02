# 02 — Adult MDD assessment knowledge and evidence output

Version: 1.0.1-source-reviewed. Research date: 2 November 2026. Population: adults 18+, including older adults.

This module covers the project's **assessment and provisional diagnostic-review needs** for major depressive disorder (MDD). It includes clinical domains, course, specifiers, focused differential information, evidence output and proposed follow-ups. It does not cover every treatment, prescribing decision or medical examination. It is source-reviewed but **not clinically validated**, and is not yet connected to the agents.

## How to read the material

- **Clinical content** is paraphrased and linked to source IDs below. It is not a verbatim copy of a manual.
- **Project design** includes our fields, state labels, example questions, review states and routing suggestions. A citation to a domain does not mean a source mandates our exact field.
- The JSON files in `MDD` encode the proposed knowledge and output contract; they do not themselves run an interview or diagnose anyone.
- The full 2022 MDD criteria/specifier sections were inspected through a public mirror after publisher access failed. Official APA fact sheets and cumulative updates were checked. Public availability is not permission to redistribute the manual; no book PDF is included.

## 1. Episode versus disorder

A major depressive episode describes a symptom period. MDD requires episode-level assessment plus the disorder-level history/exclusion review. Depressive episodes can occur in bipolar illness. A symptom score cannot settle that distinction. [VA_2022; NIMH_BIPOLAR; APA_MDD]

The episode foundation is five of nine symptom groups in one two-week period, including depressed mood or reduced interest/pleasure, with change from baseline and significant distress or impairment. Evaluate relevant physiological causes. [VA_2022; SAMHSA_2020]

For MDD, additionally review lifetime mania/hypomania, including substance/medical exceptions, and the current psychotic-disorder exclusion. APA's 2022 clarification concerns at least one episode not better explained by schizoaffective disorder or superimposed on the specified psychotic disorders. This is a professional diagnostic judgment. [APA_MDD; SAMHSA_2020]

**Do not count reported concepts mechanically as criteria.** Appetite plus weight count within one group; the same applies to interest/pleasure, sleep subtypes, energy/fatigue, worthlessness/guilt and concentration/decisions. Historical and current findings cannot be pooled into an invented episode. [SAMHSA_2020]

### Timing and frequency

Mood and interest/pleasure have most-of-day and near-daily qualifiers; the other daily symptom formulations need their corresponding persistence. Weight change and death/suicide-related formulations differ. The weight example is over 5% within a month; appetite is a separate route within that same group. Store actual values and windows rather than converting “often” into a threshold. No source establishes our own days-per-week cutoff. [SAMHSA_2020]

## 2. Concept cards: meaning, details and follow-up

Each field below is optional on an individual report. If relevant but unknown, record that state or leave it as an unresolved gap; never invent a value. Fields are project proposals attached to sourced clinical domains. Example questions are original conversational examples, not standardized test items. Their sequence is adaptive and not a validated script.

### Depressed mood — `depressed_mood`

Reported low, sad or empty mood.

Clinical sources: [NIMH_DEP; VA_2022; SAMHSA_2020]. Count group: `mood`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `description` | The person's account of this experience, without adding a diagnosis. | Supported text in the person’s terms |
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `days_per_week` | Stated days affected; keep units and wording instead of imposing a diagnostic cutoff. | Supported text in the person’s terms |
| `proportion_of_day` | Reported share of an affected day; most of the day is already useful. | Supported text in the person’s terms |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text in the person’s terms |
| `impact` | Concrete reported consequences of this experience. | Supported text in the person’s terms |

**Example question:** How has your mood been during this period?

**Follow-up focus:** Meaning, persistence and episode timing if unclear.

**Interpretation boundary:** A sad day alone does not establish the domain threshold or MDD.

**Clinical review note:** Review most-of-day and near-daily persistence within the shared episode period. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Interest and pleasure — `interest_pleasure`

Reduced desire for activities and/or reduced enjoyment.

Clinical sources: [NIMH_DEP; VA_2022]. Count group: `interest_pleasure`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `days_per_week` | Stated days affected; keep units and wording instead of imposing a diagnostic cutoff. | Supported text in the person’s terms |
| `proportion_of_day` | Reported share of an affected day; most of the day is already useful. | Supported text in the person’s terms |
| `interest` | Reported wanting or motivation to engage. | Supported text in the person’s terms |
| `pleasure` | Enjoyment when engaged. | Supported text in the person’s terms |
| `activities` | Affected activities and retained interests. | Supported text in the person’s terms |
| `breadth` | How broadly activities are affected. | Supported text in the person’s terms |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text in the person’s terms |

**Example question:** Have your interest or enjoyment in your usual activities changed?

**Follow-up focus:** Separate wanting from enjoying; establish breadth if relevant.

**Interpretation boundary:** One retained hobby does not negate all symptoms; not doing an activity may reflect lack of opportunity.

**Clinical review note:** The clinical criterion concerns a marked reduction across all or almost all activities, most of the day, nearly daily; one affected hobby alone is insufficient. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Appetite change — `appetite_change`

Change in desire for food.

Clinical sources: [NIMH_DEP; SAMHSA_2020]. Count group: `appetite_weight`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text in the person’s terms |
| `direction` | Reported appetite direction. | increased / decreased / variable / unclear |
| `appetite_vs_intake` | Distinguish hunger/desire from actual eating. | Supported text in the person’s terms |
| `impact` | Concrete reported consequences of this experience. | Supported text in the person’s terms |

**Example question:** Has your appetite changed compared with usual?

**Follow-up focus:** Direction, persistence and appetite versus eating.

**Interpretation boundary:** Do not invent weight change from appetite; shares one count group with weight.

**Clinical review note:** Appetite increase/decrease has a near-daily qualifier; actual intake is not interchangeable with appetite. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Weight change — `weight_change`

Reported change in body weight.

Clinical sources: [SAMHSA_2020]. Count group: `appetite_weight`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `direction` | Weight direction. | gain / loss / variable / unclear |
| `amount` | Amount with original units; no guessing. | Supported text in the person’s terms |
| `interval` | Period over which weight changed. | Supported text in the person’s terms |
| `baseline_weight` | Earlier weight if supplied. | Supported text in the person’s terms |
| `measurement` | Measured versus estimated account. | measured_report / estimate / unclear |
| `intentionality` | Whether intentional. | intentional / unintentional / mixed / unclear |

**Example question:** Have you noticed a change in your weight during this period?

**Follow-up focus:** Amount, interval and intentionality when relevant.

**Interpretation boundary:** No automatic percent calculation without compatible stated weights and dates; never double-count appetite.

**Clinical review note:** Significant non-dieting weight change has its own amount/time formulation; an amount alone without interval cannot establish it. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Sleep disturbance — `sleep_disturbance`

Difficulty sleeping or excessive sleep.

Clinical sources: [NIMH_DEP; SAMHSA_2020; NIMH_BIPOLAR]. Count group: `sleep`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text in the person’s terms |
| `pattern` | Reported sleep complaint. | onset_difficulty / maintenance_difficulty / early_waking / excessive_sleep / mixed / unclear |
| `latency` | Time taken to fall asleep. | Supported text in the person’s terms |
| `awakenings` | Waking during sleep and return-to-sleep account. | Supported text in the person’s terms |
| `wake_timing` | Actual versus intended/usual waking. | Supported text in the person’s terms |
| `total_sleep` | Reported sleep hours with period. | Supported text in the person’s terms |
| `sleep_opportunity` | Opportunity and external interruptions. | Supported text in the person’s terms |
| `daytime_effect` | Sleepiness, exhaustion or other reported effects. | Supported text in the person’s terms |

**Example question:** How has your sleep changed from what is usual for you?

**Follow-up focus:** Identify complaint before asking subtype-specific details.

**Interpretation boundary:** Insomnia while tired is not reduced sleep need; insufficient opportunity is not automatically insomnia.

**Clinical review note:** Review near-daily insomnia/hypersomnia rather than assuming all short sleep is insomnia. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Psychomotor change — `psychomotor_change`

Noticeable motor/speech slowing or agitation.

Clinical sources: [SAMHSA_2020; VA_2022]. Count group: `psychomotor`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `direction` | Reported observable change. | slowing / agitation / both / unclear |
| `examples` | Concrete speech/movement behaviour. | Supported text in the person’s terms |
| `observer` | Who noticed it; self-report about another observer remains patient report. | Supported text in the person’s terms |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text in the person’s terms |
| `impact` | Concrete reported consequences of this experience. | Supported text in the person’s terms |

**Example question:** Have you or other people noticed changes in how quickly you move or speak?

**Follow-up focus:** Observable examples and reporter, rather than restlessness alone.

**Interpretation boundary:** Text response speed and feeling restless alone do not establish observable psychomotor change.

**Clinical review note:** Requires observable agitation/slowing, not solely a subjective sense of restlessness/slowness. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Energy and fatigue — `energy_fatigue`

Unusual tiredness or reduced energy.

Clinical sources: [NIMH_DEP; VA_2022]. Count group: `energy`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text in the person’s terms |
| `experience` | Fatigue, low energy or both. | Supported text in the person’s terms |
| `sleepiness` | Reported sleepiness if distinguished. | Supported text in the person’s terms |
| `impact` | Concrete reported consequences of this experience. | Supported text in the person’s terms |

**Example question:** How has your energy been compared with usual?

**Follow-up focus:** Examples and timing; separate sleepiness if ambiguous.

**Interpretation boundary:** Do not automatically attribute fatigue to depression or infer it from short sleep.

**Clinical review note:** Review near-daily fatigue/loss of energy; cause still requires contextual assessment. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Worthlessness and guilt — `worthlessness_guilt`

Low self-worth or excessive/inappropriate guilt.

Clinical sources: [NIMH_DEP; SAMHSA_2020]. Count group: `worthlessness_guilt`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `content` | Actual self-evaluation or guilt account. | Supported text in the person’s terms |
| `kind` | Reported experience. | worthlessness / guilt / both / unclear |
| `context` | What the thought concerns; retain uncertainty about proportionality. | Supported text in the person’s terms |
| `impact` | Concrete reported consequences of this experience. | Supported text in the person’s terms |

**Example question:** How have you been thinking about yourself during this period?

**Follow-up focus:** Actual thought content; clarify without endorsing it.

**Interpretation boundary:** Ordinary regret, low confidence and guilt about illness are not automatically qualifying guilt.

**Clinical review note:** Review near-daily worthlessness or excessive/inappropriate guilt; illness-related self-reproach alone is insufficient. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Concentration and decisions — `cognition_decisions`

Reported thinking, attention or decision difficulty.

Clinical sources: [NIMH_DEP; VA_2022]. Count group: `cognition`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text in the person’s terms |
| `kind` | Reported difficulty. | concentration / thinking / indecision / mixed / unclear |
| `tasks` | Concrete affected tasks. | Supported text in the person’s terms |
| `impact` | Concrete reported consequences of this experience. | Supported text in the person’s terms |

**Example question:** Have concentrating or making decisions become harder than usual?

**Follow-up focus:** Task examples and change from baseline.

**Interpretation boundary:** Do not label dementia, ADHD or depression from this alone.

**Clinical review note:** Review near-daily thinking/concentration/decision difficulty and change from baseline. [SAMHSA_2020]. This is not an extractor declaration that the criterion is met.

### Death/suicide-related reports — `death_suicide`

Death-related thoughts, suicidal thoughts, plans or attempts.

Clinical sources: [APA_UPDATES; ASQ_BSSA; NICE_222]. Count group: `death_suicide`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `experience` | Preserve distinctions. | death_thoughts / wish_not_alive / suicidal_thoughts / suicide_plan / suicide_attempt / unclear |
| `recency` | When last/current; do not infer resolution. | Supported text in the person’s terms |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text in the person’s terms |
| `intent` | Intent as reported. | Supported text in the person’s terms |
| `plan_present` | Whether a plan was explicitly reported or denied. | reported / denied / unclear |
| `access` | Access to means as reported, without generating procedural details. | Supported text in the person’s terms |
| `past_behaviour` | Historical self-injury/attempt account, intent and timing. | Supported text in the person’s terms |
| `support` | Available support as reported. | Supported text in the person’s terms |

**Example question:** Have you had thoughts about ending your life?

**Follow-up focus:** Use dedicated safety pathway; preserve current versus historical information.

**Interpretation boundary:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

**Clinical review note:** Distinguish recurrent death thoughts/ideation from a specific plan or attempt; fear of dying alone is different. Use the dedicated safety pathway. [VA_2022; SAMHSA_2020; APA_UPDATES]. This is not an extractor declaration that the criterion is met.

### Episode timeline — `episode_timeline`

Period linking symptoms and changes.

Clinical sources: [VA_2022]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text in the person’s terms |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text in the person’s terms |
| `course` | Continuity, fluctuation or change over the relevant period. | Supported text in the person’s terms |
| `overlap` | Whether symptoms occurred together. | Supported text in the person’s terms |
| `intervals` | Earlier periods, recovery and residual symptoms. | Supported text in the person’s terms |

**Example question:** When did these changes begin?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Clinical sources: [NICE_222]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text in the person’s terms |
| `examples` | Concrete difficulty or distress. | Supported text in the person’s terms |
| `baseline` | Usual functioning. | Supported text in the person’s terms |
| `supports` | Assistance helping preserve functioning. | Supported text in the person’s terms |

**Example question:** How have these changes affected your daily life?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Activation history — `activation_history`

Possible distinct elevated/overactive periods requiring review.

Clinical sources: [NICE_185; NIMH_BIPOLAR]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `period` | Current/historical time. | Supported text in the person’s terms |
| `mood` | Elevated, expansive or irritable mood as reported. | Supported text in the person’s terms |
| `energy_activity` | Change in energy/activity. | Supported text in the person’s terms |
| `sleep_need` | Sleep need and tiredness, not just sleep hours. | Supported text in the person’s terms |
| `other_changes` | Associated speech, thoughts, confidence or risky behaviour. | Supported text in the person’s terms |
| `duration` | Duration of that period. | Supported text in the person’s terms |
| `impact` | Consequences or other observers. | Supported text in the person’s terms |
| `exposure_context` | Medicines/substances/medical context. | Supported text in the person’s terms |

**Example question:** Have you had a distinct period of unusually increased energy or activity?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Medical context — `medical_context`

Relevant reported medical history and symptoms.

Clinical sources: [VA_2022; NICE_222]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `conditions` | Reported conditions; distinguish reported diagnosis from confirmation. | Supported text in the person’s terms |
| `timeline` | Relationship to symptoms. | Supported text in the person’s terms |
| `investigations` | Results only if actually supplied. | Supported text in the person’s terms |
| `clinician_review` | Known professional assessment or unresolved need. | Supported text in the person’s terms |

**Example question:** Are there health conditions that might be relevant to these changes?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Medicines and substances — `exposure_context`

Relevant treatment/substance exposure account.

Clinical sources: [NICE_222; VA_2022]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `name` | Named exposure. | Supported text in the person’s terms |
| `dose_use` | Reported amount/use; never recommend a dose. | Supported text in the person’s terms |
| `start_change_stop` | Timing of changes. | Supported text in the person’s terms |
| `symptom_timing` | Reported temporal relationship. | Supported text in the person’s terms |
| `source_kind` | Medicine, alcohol, other substance or unclear. | Supported text in the person’s terms |

**Example question:** Have any medicines or substance-use patterns changed around this time?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Psychotic experiences — `psychotic_experience`

Reported experiences requiring specialist interpretation.

Clinical sources: [APA_MDD; NICE_222]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `kind` | Experience as described, not an automatic diagnosis. | Supported text in the person’s terms |
| `content` | Brief relevant content without affirming beliefs. | Supported text in the person’s terms |
| `mood_relationship` | During versus outside mood episodes. | Supported text in the person’s terms |
| `conviction_context` | Reported belief/context and uncertainty. | Supported text in the person’s terms |
| `safety_concerns` | Any reported urgent implications. | Supported text in the person’s terms |
| `reported_mood_congruence` | Professional mood-congruence description if actually supplied; do not invent it. | congruent / incongruent_or_mixed / unclear |

**Example question:** Have you had experiences that other people do not seem to share?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Clinical sources: [NICE_222]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text in the person’s terms |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text in the person’s terms |
| `period` | When and for which symptoms. | Supported text in the person’s terms |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text in the person’s terms |
| `use` | Actual use and barriers as reported. | Supported text in the person’s terms |

**Example question:** Have you received help for something similar before?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Family history — `family_history`

Relevant family mood/psychiatric history.

Clinical sources: [VA_2022]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `relative` | Relationship, without unnecessary identifying details. | Supported text in the person’s terms |
| `reported_condition` | Condition as reported. | Supported text in the person’s terms |
| `certainty` | How the person knows; unknown remains unknown. | Supported text in the person’s terms |

**Example question:** Is there relevant mental-health history in your family?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Life context — `life_context`

Relevant stress, loss, trauma and support.

Clinical sources: [NICE_222; APA_GRIEF]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `events` | Events relevant to symptom timeline. | Supported text in the person’s terms |
| `timing` | Temporal relationship. | Supported text in the person’s terms |
| `support` | Current supports. | Supported text in the person’s terms |
| `barriers` | Practical barriers. | Supported text in the person’s terms |
| `meaning` | Person's interpretation of the context. | Supported text in the person’s terms |

**Example question:** Has anything important been happening around the time these changes began?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation boundary:** A contextual association is not a confirmed causal explanation.

### Anxious distress — `anxious_distress`

At least two anxiety features on most episode days; anxious-distress severity is distinct from overall MDD severity.

Clinical sources: [ANXIOUS_STUDY; DSM_TR]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `tension` | Feeling keyed up or tense during the relevant episode. | Supported text in the person’s terms |
| `unusual_restlessness` | Restlessness beyond the person's usual state; separate from observed motor agitation. | Supported text in the person’s terms |
| `worry_affecting_concentration` | Difficulty focusing specifically because of worry. | Supported text in the person’s terms |
| `fear_of_awful_event` | Fear that something awful may happen. | Supported text in the person’s terms |
| `fear_of_losing_control` | Fear of losing control of oneself, as described by the person. | Supported text in the person’s terms |
| `episode_overlap` | Relation to the current or most recent episode. | Supported text in the person’s terms |
| `timing_frequency` | Relevant timing/frequency of the pattern. | Supported text in the person’s terms |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text in the person’s terms |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** The five feature labels refer to tension, restlessness, worry-related concentration difficulty and the two specified fears.

**Interpretation boundary:** Clarify episode overlap and actual experience; do not substitute a generic anxiety score.

### Mixed features — `mixed_features`

At least three activation features on most episode days, changed from usual and observable; full mania/hypomania changes the bipolar formulation.

Clinical sources: [MIXED_STUDY; DSM_TR; NIMH_BIPOLAR]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `elevated_expansive_mood` | Unusually elevated or expansive mood; ordinary happiness is insufficient. | Supported text in the person’s terms |
| `grandiosity` | Unusual inflated self-esteem or grandiose beliefs compared with baseline. | Supported text in the person’s terms |
| `increased_talkativeness` | More talkative than usual or feeling pressure to keep talking. | Supported text in the person’s terms |
| `racing_thoughts` | Reported fast/racing thoughts or rapid shifts between ideas. | Supported text in the person’s terms |
| `increased_energy_activity` | Unusual increase in energy or purposeful activity. | Supported text in the person’s terms |
| `risky_activity` | Unusual involvement in activities with significant potential adverse consequences. | Supported text in the person’s terms |
| `reduced_sleep_need` | Feeling rested despite less sleep, rather than being unable to sleep while tired. | Supported text in the person’s terms |
| `episode_overlap` | Relation to the current or most recent episode. | Supported text in the person’s terms |
| `timing_frequency` | Relevant timing/frequency of the pattern. | Supported text in the person’s terms |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text in the person’s terms |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** Each label means a reported change: expansive mood, inflated self-view, speech, thought speed, energy/activity, consequential risk-taking or less sleep without tiredness.

**Interpretation boundary:** Check exposure effects and professional interpretation. Irritability/agitation alone are not the seven-feature definition.

### Melancholic features — `melancholic_features`

At the episode's worst phase: near-total pleasure loss or little mood response to positive events, plus at least three associated features.

Clinical sources: [CANMAT_2016; DSM_TR]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `near_total_pleasure_loss` | Almost no enjoyment across almost all activities at the worst episode phase. | Supported text in the person’s terms |
| `low_mood_reactivity` | Little or no temporary mood improvement with usually enjoyable events. | Supported text in the person’s terms |
| `distinct_mood_quality` | Qualitatively distinct despair/despondency/empty mood; severity alone is insufficient. | Supported text in the person’s terms |
| `morning_worsening` | A regular pattern of worse depression in the morning. | Supported text in the person’s terms |
| `early_waking` | Waking earlier than usual; record the actual difference before evaluating the two-hour feature. | Supported text in the person’s terms |
| `marked_motor_change` | Pronounced observable slowing or agitation; retain reporter and uncertainty. | Supported text in the person’s terms |
| `appetite_weight_loss` | Significant appetite/weight loss, with appetite and weight kept distinct. | Supported text in the person’s terms |
| `excessive_guilt` | Reported excessive/inappropriate guilt; proportionality requires clinical interpretation. | Supported text in the person’s terms |
| `episode_overlap` | Relation to the current or most recent episode. | Supported text in the person’s terms |
| `timing_frequency` | Relevant timing/frequency of the pattern. | Supported text in the person’s terms |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text in the person’s terms |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** Associated features are a distinct mood quality, morning worsening, waking at least two hours early, marked motor change, appetite/weight loss and excessive guilt.

**Interpretation boundary:** Mere severity is not distinct mood quality. Preserve observed versus reported motor changes.

### Atypical features — `atypical_features`

Predominant episode pattern: mood brightening with positive events plus at least two associated features; incompatible melancholic/catatonic criteria must be reviewed.

Clinical sources: [CANMAT_2016; DSM_TR]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `mood_reactivity` | Mood improvement in response to actual or anticipated positive events. | Supported text in the person’s terms |
| `appetite_weight_gain` | Significant increased appetite or weight, preserving which is reported. | Supported text in the person’s terms |
| `excessive_sleep` | Reported extended sleep compared with usual; retain actual hours/naps and baseline. | Supported text in the person’s terms |
| `leaden_limbs` | A heavy, weighted-down feeling in arms or legs; not objective paralysis. | Supported text in the person’s terms |
| `longstanding_rejection_sensitivity` | Impairing sensitivity to interpersonal rejection that also exists outside mood episodes. | Supported text in the person’s terms |
| `episode_overlap` | Relation to the current or most recent episode. | Supported text in the person’s terms |
| `timing_frequency` | Relevant timing/frequency of the pattern. | Supported text in the person’s terms |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text in the person’s terms |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** Associated features concern increased appetite/weight, excessive sleep, heavy limbs and longstanding impairing sensitivity to rejection beyond the episode.

**Interpretation boundary:** Feeling better briefly does not rule out depression. Atypical is a technical pattern, not any unusual symptom.

### Seasonal pattern — `seasonal_pattern`

For recurrent MDD: characteristic seasonal onset/remission, a qualifying two-year pattern without nonseasonal episodes, and seasonal predominance across life.

Clinical sources: [SEASONAL; DSM_TR]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `onset_season` | Time of year when actual depressive episodes begin. | Supported text in the person’s terms |
| `remission_season` | Time of year when episodes remit, not merely improve briefly. | Supported text in the person’s terms |
| `two_year_history` | Episode and recovery pattern over the last two years. | Supported text in the person’s terms |
| `nonseasonal_episodes` | Depressive episodes outside the proposed season; include dates. | Supported text in the person’s terms |
| `lifetime_pattern` | Relative lifetime occurrence of seasonal and nonseasonal episodes. | Supported text in the person’s terms |
| `seasonal_stressors` | Season-linked life events that might explain the reported pattern. | Supported text in the person’s terms |
| `episode_overlap` | Relation to the current or most recent episode. | Supported text in the person’s terms |
| `timing_frequency` | Relevant timing/frequency of the pattern. | Supported text in the person’s terms |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text in the person’s terms |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** Record episode dates and recoveries; seasonal work/school stress alone is not this pattern.

**Interpretation boundary:** A single difficult winter does not establish seasonal pattern.

### Peripartum/perinatal context — `peripartum_context`

Formal peripartum onset concerns pregnancy or the first four weeks after delivery; broader perinatal assessment includes the first postpartum year.

Clinical sources: [ACOG_4; DSM_TR]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `pregnancy_delivery_timing` | Pregnancy stage, delivery date or postpartum interval as actually reported. | Supported text in the person’s terms |
| `symptom_onset_timing` | Onset relative to pregnancy and delivery, separately from interview date. | Supported text in the person’s terms |
| `episode_relationship` | Which episode this reproductive context concerns. | Supported text in the person’s terms |
| `parent_infant_functioning` | Reported self-care, caregiving and related functional concerns. | Supported text in the person’s terms |
| `postpartum_psychosis_concerns` | Reported psychotic/confusional/marked activation concerns after delivery requiring urgent professional review. | Supported text in the person’s terms |
| `episode_overlap` | Relation to the current or most recent episode. | Supported text in the person’s terms |
| `timing_frequency` | Relevant timing/frequency of the pattern. | Supported text in the person’s terms |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text in the person’s terms |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** Use actual dates and circumstances, including whether symptoms began before delivery.

**Interpretation boundary:** Later postpartum onset still warrants assessment. Postpartum psychosis requires urgent professional care.

### Catatonic signs — `catatonic_signs`

A syndrome requiring at least three recognized signs and professional examination; not equivalent to fatigue or ordinary motor slowing.

Clinical sources: [UCL_CATATONIA; BAP_2023; DSM_TR]. Count group: `supporting/feature evidence; not an additional core symptom`.

Proposed information fields:

| Field | Meaning | Permitted values |
|---|---|---|
| `stupor` | Markedly reduced movement and responsiveness, requiring clinical observation. | Supported text in the person’s terms |
| `catalepsy` | An examiner-positioned posture maintained against gravity; requires examination. | Supported text in the person’s terms |
| `waxy_flexibility` | Slight even resistance during examiner repositioning; requires examination. | Supported text in the person’s terms |
| `mutism` | Minimal or absent verbal response, requiring appropriate clinical interpretation. | Supported text in the person’s terms |
| `negativism` | Opposition or absent response to instructions/external stimuli in clinical assessment. | Supported text in the person’s terms |
| `posturing` | Spontaneously holding a posture against gravity. | Supported text in the person’s terms |
| `mannerism` | An unusual exaggerated version of an ordinary action. | Supported text in the person’s terms |
| `stereotypy` | Repeated non-goal-directed movements. | Supported text in the person’s terms |
| `unprovoked_agitation` | Agitation not influenced by external stimuli in the clinical formulation. | Supported text in the person’s terms |
| `grimacing` | Unusual sustained/repeated facial expressions. | Supported text in the person’s terms |
| `echolalia` | Imitation of another person's speech. | Supported text in the person’s terms |
| `echopraxia` | Imitation of another person's movements. | Supported text in the person’s terms |
| `episode_overlap` | Relation to the current or most recent episode. | Supported text in the person’s terms |
| `timing_frequency` | Relevant timing/frequency of the pattern. | Supported text in the person’s terms |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text in the person’s terms |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** Signs cover reduced responsiveness/speech, postural/tone abnormalities, resistance, unusual/repeated movements, agitation and echoing speech/actions. Clinical elicitation is essential.

**Interpretation boundary:** Text silence cannot diagnose mutism or stupor; do not instruct a layperson to perform a physical examination.

## 3. Course, severity, remission and specifier interpretation

Recurrent episodes require at least two consecutive months below full episode criteria between episodes. Full remission concerns at least two months without significant signs/symptoms; partial remission covers residual symptoms or a shorter symptom-free interval after an episode. Store the timeline before applying labels. [DSM_TR, pp.184–185,214]

Severity integrates symptom number/intensity and functional disability. Mild means a limited excess of manageable symptoms with minor impairment; severe involves substantially greater burden and marked interference; moderate falls between. A PHQ band and NICE's management grouping are not identical classification labels. [DSM_TR; NICE_222]

Anxious distress has its own severity: two features mild, three moderate, four/five moderate-severe, and four/five with motor agitation severe. This does not replace overall MDD severity. [ANXIOUS_STUDY; DSM_TR]

Melancholic assessment focuses on the worst episode phase; atypical and mixed patterns have their own timing and exclusions. Do not attach every specifier to every depressive disorder or infer it from one symptom. In atypical assessment, rejection sensitivity must extend beyond the episode; in mixed assessment, exposure effects and full mania/hypomania require review. [CANMAT_2016; DSM_TR]

Psychotic features concern hallucinations/delusions during an episode. Mood-congruent content follows depressive themes; incongruent or mixed content needs separate recording. The extractor records experiences, not whether a belief is objectively false or a confirmed psychotic diagnosis. Specialist assessment is needed. [DSM_TR; NICE_222]

Catatonic signs need examination; the syndrome's professional criteria are not a chat checklist. Peripartum context and seasonal history should be explored when indicated, using actual timing and the boundaries in their cards. [UCL_CATATONIA; BAP_2023; ACOG_4; SEASONAL]

## 4. Focused alternatives and limits

This is a depression module, not a full diagnostic system for every psychiatric or medical condition. Keep these review branches:

| Branch | Information purpose | Boundary |
|---|---|---|
| Bipolar | Distinct activation history, duration, sleep need, impact and exposure context | NICE's four-day recognition/referral recommendation is not sufficient bipolar diagnostic criteria. [NICE_185] |
| Medical or substance/medication effects | Conditions, exposures and timing | A coexisting illness or temporal association does not establish causation. [VA_2022] |
| Psychotic disorders | Experiences during and outside mood episodes | Apply the current exclusion through professional assessment. [APA_MDD] |
| Grief, adjustment and trauma | Loss/stressor relationship and associated symptoms | Grief and MDD can coexist; prolonged grief is a separate differential. [APA_GRIEF; APA_UPDATES] |
| Anxiety and other coexisting illness | Clinically relevant additional symptoms/history | Do not require a full interview for every disorder. [NICE_222] |
| Persistent depression | Longitudinal course and earlier depressive periods | Do not assume all chronic symptoms are mild or automatically switch labels at two years. [CANMAT_2023] |

Older-adult assessment includes relevant physical illness, medicines and cognitive complaints. Acute confusion or concerning physical changes need appropriate medical review; this module cannot establish delirium, dementia or a physical cause. Communication/cognitive needs may require adapted assessment and collateral information with appropriate consent. [NIMH_DEP; NICE_222]

Do not order a universal laboratory panel or infer a test result. Preserve clinician-provided investigations and unresolved medical-review needs. Pregnancy/postpartum pathways require their own clinical support; postpartum psychosis is an urgent obstetric/psychiatric concern. [VA_2022; ACOG_4]

Medical-review examples in VA/DoD include thyroid illness, vitamin B12 deficiency, pain and chronic disease. These examples are neither an exhaustive differential nor grounds for automatic attribution. [VA_2022]

## 5. Safety information and response boundary

Directly enquire about suicidal thoughts and intent in depression assessment; an ordinary symptom sequence must not delay a needed response. Preserve current thoughts, recency/frequency, plan/intent/access, past behaviour and supports. A past account is not automatically current intent, and a denial of one question does not establish complete safety. [NICE_222; ASQ_BSSA]

The BSSA reference is for trained professionals following a positive ASQ. Its domains inform our record design; this package is not a validated BSSA administration. We do not invent a predictive low/medium/high risk score. NICE warns against that use of risk categories/scales. [ASQ_BSSA; NICE_225]

**Project handoff states:** `not_assessed`, `no_signal_reported_in_available_text`, `needs_clinical_review`, `urgent_review_needed`. These describe assessment/handoff needs, not a probability of suicide. “No signal reported” never means “safe.” Declines/unknowns remain visible. No emergency service is activated by this file, and no local crisis contacts are embedded.

## 6. Screening and symptom measurement

| Tool | Role and values | Limits |
|---|---|---|
| PHQ-2 | Two-week frequency screen, two items scored 0–3; total 0–6. A commonly studied positive threshold is 3. [PHQ2_2003] | Not an MDD diagnosis; positive screens need assessment. Do not use a negative result as an absolute exclusion when concerns persist |
| PHQ-9 | Nine items with two-week responses 0–3; total 0–27. Conventional bands begin at 5,10,15,20. [PHQ9_FORM; PHQ9_2001] | Missing answers are not zeros. Interpret alongside clinical assessment and differential history |
| Other tools | EPDS/perinatal or age/context-specific alternatives may be appropriate [ACOG_4] | Version, language, population and administration need a separate tool policy before adoption |

Original PHQ response labels are “Not at all,” “Several days,” “More than half the days,” “Nearly every day.” These standardized options must remain separate from our free-text evidence attributes. We have not reproduced the item set here. [PHQ9_FORM]

The PHQ-9 screening threshold around 10 is not diagnostic certainty; accuracy depends on reference interview and population. The original validation also used independent professional interviews. Keep instrument scores, DSM criteria review and professional conclusions as distinct records. [PHQ9_META; PHQ9_2001]

For software: store instrument name/version, language, date, timeframe, original item responses, missingness and score provenance. Code should score complete standardized responses. Do not reconstruct an official score from casual dialogue or conversational paraphrases. A relevant suicide-related response prompts further assessment rather than being handled only as a contribution to a total. This is our proposed implementation policy, not a validated conversational adaptation.

## 7. Evidence-output contract: what the extractor returns

Open `MDD/evidence_output.schema.json` for the exact JSON contract and `MDD/examples.json` for valid fictional snapshots. The schema restricts each concept to its own allowed attributes. It does not require every attribute on every finding.

### Shared record fields — project definitions

| Field | Meaning |
|---|---|
| `concept_id` | Which knowledge concept the report concerns |
| `episode_key` | Application-maintained period key; different episodes stay separate |
| `subject` | Patient in this contract; do not turn a relative's symptoms into the patient's |
| `finding_status` | Reported present, explicitly denied, unclear or conflicting; not a confirmed clinical criterion |
| `temporal_status` / `time_reference` | Current, historical or unclear, plus the original timing expression |
| `attributes` | Only concept-appropriate details, each with `known`, `unknown` or justified `not_applicable` |
| `evidence` | Exact patient quotes and message references; earlier contextual messages may explain short answers |
| `uncertainty_notes` | Ambiguity, conflicting reports or interpretation limits |
| `semantic_check_status` | Whether meaning appears supported or still needs review; never a diagnostic confidence percentage |

No model-generated evidence UUID is needed. Message IDs and period keys are maintained by code. A concept label alone is not a reliable evidence key: the same concept can concern several periods and contradictory reports. The proposed unique snapshot key is `(concept_id, episode_key, subject)`; multiple evidence entries remain underneath it.

### Allowed states explained

**`finding_status`**

- `reported_present`: Explicitly described or affirmed in context; not clinical confirmation.
- `reported_absent`: Explicitly denied for this subject/period.
- `unclear`: Meaning or polarity unresolved.
- `conflicting`: Accounts for the same subject/period conflict and are retained.

**`temporal_status`**

- `current`: Described as relevant to current period.
- `historical`: An earlier period.
- `unclear`: Timing unresolved.

**`detail_status`**

- `known`: A supported value is available.
- `unknown`: Relevant but unresolved; no value asserted.
- `not_applicable`: Inapplicability is explicitly justified; not equivalent to not asked.

**`question_status`**

- `not_asked`: No recorded question.
- `answered`: Target addressed.
- `partially_answered`: Some target information supplied.
- `unclear`: Response ambiguous.
- `declined`: Person chose not to answer.

**`semantic_check_status`**

- `supported`: Evidence appears to support the claim.
- `needs_review`: Meaning/attribution remains unresolved.

### Missing information and evidence support

No record means “no extracted report,” not absent. `not_asked` belongs to question tracking. Unknown fields must not carry invented values. Known fields name their supporting evidence using each evidence entry's `supports` list. Unstated context is not inherited from another symptom.

Each quote must occur exactly in the cited patient's message. Context IDs must refer to earlier messages, not the same/future message. A contextual “yes” should preserve the preceding question reference; its quote remains “Yes.” An exact quote can still be semantically misinterpreted, so mechanical checks do not prove clinical correctness.

### Memory and corrections

Maintain a source-preserving snapshot per concept and period. Add new detail to the relevant record; keep earlier sources. Do not overwrite six-week mood duration with two-week sleep duration. If the person corrects an earlier statement, record the correction and retain the earlier quotation in audit history. Conflicting accounts stay `conflicting`/`needs_review` until clarified; different periods need not be contradictions.

The schema describes snapshots. An eventual merge/correction engine still needs implementation and tests; this package does not silently change the current agents' state format.

## 8. Proposed planner and conversation behaviour

This is a design policy derived from clinical information needs, not a universally validated question order:

1. Start with introduction/participation and the person's main concern.
2. Address immediate safety or medical concerns when they arise.
3. Establish the relevant period, baseline, core symptoms and impact.
4. Explore missing symptom groups and focused alternative history, using volunteered information.
5. Follow relevant feature/course branches when clues justify them.
6. Review unresolved contradictions, summaries and remaining professional-review needs.

After **each answer**, first extract everything relevant from the answer in context; update memory; then check whether a proposed target is already answered. Ask a useful missing question, not a fixed field-by-field inventory.

| Situation | Proposed behaviour |
|---|---|
| The person supplies two answers at once | Save both and skip redundant follow-ups |
| A short “yes” follows one clear finding question | Resolve with that question and retain the reference |
| A “yes” follows a compound/ambiguous question | Clarify; do not assign both findings |
| Useful information is off the selected topic | Save it, acknowledge it and return gently if the original gap still matters |
| The answer is unrelated | Briefly acknowledge and explain why a focused question may help; offer a choice to answer/skip |
| A detail is already clear | Accept the person's wording; “most of the day” need not become a numeric percentage |
| The person declines | Record the decline, preserve the gap and avoid pressure; follow the separate safety protocol when relevant |
| Burden rises or the person stops | Summarize collected information and label incomplete areas |

The final question graph, source-specific screening placement, burden limits and clinical stop criteria require a separate reviewed workflow. No fixed number of turns establishes diagnostic completeness.

## 9. Professional-review handoff

Proposed handoff: presenting concern; episode timeline; findings grouped without double-counting; functioning/distress; relevant negatives with time windows; activation/medical/exposure review; feature clues; safety concerns and actions actually taken; earlier care; conflicting/missing information; source-linked provisional explanations and alternatives. Clearly distinguish a patient-reported diagnosis from a professional conclusion.

The extractor does not output a confirmed MDD label or silently infer criterion satisfaction. A later synthesis component may explain evidence for an MDD-like presentation and uncertainty. A complete software contract does not establish clinical sufficiency or readiness for real patients.

## 10. Sources, access and maintenance

Source registry: `MDD/sources.json`. Every clinical card links to registry IDs. Full-text access today improves on the earlier draft's access gap, but does not establish clinical validation or rights to reproduce a proprietary manual. Source summaries and engineering design are kept distinct; no source endorses this system.

| ID | Source and location | What we used / access |
|---|---|---|
| `DSM_TR` | [APA DSM-5-TR (2022), Depressive Disorders](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders); Printed pp.183–185, 210–214; inspected mirror PDF viewer pp.309–311, 342–347 | Current-edition boundaries, episode/course and specifier cross-check. Publisher full chapter blocked. Original APA text inspected in a publicly reachable psychiatry.ru mirror; no claim of verified redistribution/licensing rights; book not bundled |
| `APA_MDD` | [APA DSM-5-TR MDD fact sheet](https://www.psychiatry.org/getmedia/33fc7cdb-6fd8-46a7-9ff2-225ba7862f7f/APA-DSM5TR-MajorDepressiveDisorder.pdf); p.1, Rationale for Change | Psychotic-disorder exclusion clarification. Public primary-source material inspected |
| `APA_UPDATES` | [APA DSM-5-TR cumulative supplement, September 2025](https://www.psychiatry.org/getmedia/b68a5776-f88c-45c7-9535-fd219d7aa5cb/APA-DSM5TR-Update-September-2025.pdf); Included September 2022 update p.7 / cumulative PDF viewer p.43; September 2025 II.B p.7 | Non-stigmatizing suicide wording, prolonged-grief differential, other-specified boundary. Public primary-source material inspected |
| `VA_2022` | [VA/DoD MDD Clinical Practice Guideline, 2022](https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/MH/mdd/VADODMDDCPGFinal508.pdf); p.19 Sidebars 1–2; pp.140–141 Appendix K; Appendix I pp.127–131 | Episode foundation, work-up and measurement context; sidebar is abbreviated DSM-5-era material. Public primary-source material inspected |
| `SAMHSA_2020` | [SAMHSA TIP 42, updated 2020](https://www.ncbi.nlm.nih.gov/sites/books/NBK571020/pdf/Bookshelf_NBK571020.pdf); Exhibit 4.1, body pp.72–73 / PDF viewer pp.102–103 | Symptom qualifiers and grouping; later APA corrections take precedence. Public primary-source material inspected |
| `NICE_222` | [NICE NG222, Depression in adults](https://www.nice.org.uk/guidance/ng222/chapter/Recommendations); 1.2.1–1.2.9; Definitions of depression/severity; 1.12.1 | Comprehensive assessment, communication, safety and specialist review. Official search-indexed recommendation extracts inspected; direct retrieval intermittently 403 |
| `NIMH_DEP` | [NIMH, Depression](https://www.nimh.nih.gov/health/publications/depression); Signs/symptoms; diagnosis; age-presentation paragraphs | Plain-language symptom domains and adult context. Public primary-source material inspected |
| `NIMH_BIPOLAR` | [NIMH, Bipolar Disorder](https://www.nimh.nih.gov/health/publications/bipolar-disorder); Types; symptom comparison; diagnosis | Activation history, reduced sleep need and bipolar uncertainty. Public primary-source material inspected |
| `NICE_185` | [NICE CG185, Bipolar disorder](https://www.nice.org.uk/guidance/cg185/chapter/recommendations); 1.2.1 | Recognition/referral recommendation, not a four-day bipolar diagnostic shortcut. Public primary-source material inspected |
| `CANMAT_2016` | [CANMAT 2016 MDD guideline, Section 1](https://journals.sagepub.com/doi/10.1177/0706743716659416); Table 4, episode specifiers and clinical dimensions | Descriptive melancholic/atypical and other feature map. Indexed table inspected; older guideline, cross-checked against 2022 text |
| `CANMAT_2023` | [CANMAT 2023 update, published 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11351064/); Diagnostic/clinical-presentation discussion; Q.5.a measurement-based care | Professional guideline context and measurement alongside assessment. Indexed text inspected; direct PMC access intermittently blocked |
| `ANXIOUS_STUDY` | [McIntyre et al., 2016, anxious distress in adults with MDD](https://doi.org/10.1177/2040622315627805); Introduction: DSM anxious-distress definition | Five feature domains and majority-of-days context. Primary observational study; indexed text inspected; not validation of our agents |
| `MIXED_STUDY` | [The prevalence and diagnostic classification of mixed features: multicenter study, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6877217/); Methods / DSM-5 mixed-feature assessment | Mixed-feature clinical research context; threshold/definition cross-checked against DSM text. Primary study; indexed material inspected |
| `SEASONAL` | [NIMH, Seasonal Affective Disorder](https://www.nimh.nih.gov/health/publications/seasonal-affective-disorder); Diagnosis section | Seasonal course, repeated years and distinction from seasonal stressors. Public primary-source material inspected |
| `ACOG_4` | [ACOG Clinical Practice Guideline No.4, 2023](https://www.acog.org/clinical/clinical-guidance/clinical-practice-guideline/articles/2023/06/screening-and-diagnosis-of-mental-health-conditions-during-pregnancy-and-postpartum); pp.1232, 1235; Box 1 p.1241 / mirrored PDF pp.1,4,10 | Perinatal assessment, first postpartum year versus formal onset modifier, postpartum psychosis. ACOG guideline inspected through Illinois Perinatal Quality Collaborative institutional PDF mirror |
| `UCL_CATATONIA` | [UCL, Catatonia diagnosis](https://www.ucl.ac.uk/brain-sciences/psychiatry/research/epidemiology-and-applied-clinical-research-department/research-projects-groups/catatonia/diagnosis); DSM-5-TR criteria and examination table | Named signs and need for observation/examination. Public primary-source material inspected |
| `BAP_2023` | [BAP evidence-based catatonia consensus guideline, 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10101189/); Diagnosis; assessment; medical aetiology recommendations | Professional assessment and medical differential; not an online self-diagnostic test. Indexed guideline extracts inspected |
| `ASQ_BSSA` | [NIMH Adult Outpatient Brief Suicide Safety Assessment Guide](https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials/adult-outpatient/adult-outpatient-brief-suicide-safety-assessment-guide); Intended users; thoughts, plan, past behaviour, supports and disposition sections | Safety information domains; clinician guide following positive ASQ, not autonomous LLM validation. Public primary-source material inspected |
| `NICE_225` | [NICE NG225, Self-harm](https://www.nice.org.uk/guidance/ng225/chapter/recommendations); 1.6.1–1.6.6 | No predictive low/medium/high stratification; needs-focused assessment. Public primary-source material inspected |
| `PHQ9_2001` | [Kroenke et al., 2001, PHQ-9 validity](https://pmc.ncbi.nlm.nih.gov/articles/PMC1495268/); Abstract; Methods; diagnostic-status comparison | Original validation of symptom/severity measure versus independent interview. Public primary-source material inspected |
| `PHQ2_2003` | [Kroenke et al., 2003, PHQ-2 validity](https://pubmed.ncbi.nlm.nih.gov/14583691/); Abstract, Methods and Results | Two-week screen, scoring range and screening threshold; abstract only. Primary-study abstract inspected; full paper not accessed |
| `PHQ9_FORM` | [PHQ-9 form hosted by AHRQ](https://integrationacademy.ahrq.gov/sites/default/files/2020-07/PHQ-9.pdf); pp.1–2 | Original response categories and scoring; form not reproduced here. Public primary-source material inspected |
| `PHQ9_META` | [PHQ-9 updated individual-participant-data meta-analysis, BMJ 2021](https://www.bmj.com/content/375/bmj.n2183); Abstract / What this study adds | Screening accuracy depends on reference standard/population; cutoff is not diagnostic certainty. Indexed primary meta-analysis text inspected; direct page 403 |
| `APA_GRIEF` | [APA, What Is Depression?](https://www.psychiatry.org/patients-families/depression/what-is-depression); Grief versus depression discussion | Loss context and possible coexistence. Public primary-source material inspected |

## 11. Validation and remaining boundaries

Run `python validate_package.py` from the MDD folder. It checks schema structure, source references, concept-specific fields, exact quotes, context order, evidence support links, episode separation and rejection of invalid fixtures. It makes no model/API calls and proves no clinical sensitivity/specificity.

The package covers the assessment domains and evidence contract for this project. Still required before clinical use: expert review; an operational local safety pathway; validated language/instrument choices; the final question graph; agent integration; semantic extraction and conversation evaluation; and prospective clinical evaluation. Treatment selection/prescribing, a full medical work-up and comprehensive diagnosis of every alternative are outside this module.

Keep this module version-pinned. Future APA/guideline updates require an explicit source/change audit. Existing runtime files have not been modified and cannot be assumed to load this package.
