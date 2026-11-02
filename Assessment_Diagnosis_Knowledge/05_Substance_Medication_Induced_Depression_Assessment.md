# 05 — Substance/medication-induced depressive disorder: adult assessment knowledge

Version: 1.0.0-source-reviewed. Research date: 2 November 2026.

This package describes what to assess, what evidence to preserve and what needs professional review. It is an adult assessment knowledge module, not a prescribing guide, automatic diagnostic engine or validated interview. The Markdown explains the knowledge; the JSON files represent the same domains and proposed output contract for later agent integration.

## 1. Meaning and age applicability

A person can develop a clinically important depressive presentation in connection with a substance or medication. Establishing that relationship requires more than learning that the person takes a drug. A clinician considers the symptom pattern, timing, what the particular agent can produce, competing explanations and observed course. A prescribed medicine can be relevant even when taken as prescribed; a substance use disorder is not a prerequisite. [DSM_INDUCED]

Our implementation covers adults from 18 upward, without a fixed upper age limit. That boundary is project scope, not a diagnostic minimum age in the source. Ask in a way appropriate to cognition, hearing, language, disability and current capacity. Older adults may have several medicines, physical conditions and cognitive concerns; preserve actual context rather than explaining depression as normal ageing. Acute cognitive change requires particular attention. [NIMH_DEP; VA_2022; NICE_103]

## 2. Criteria-information map and important boundaries

The DSM-5-TR information requirements can be summarized as follows. This is a paraphrase, not the original instrument or a diagnostic decision by our agents. [DSM_INDUCED]

| Domain | Information required for professional review |
|---|---|
| A: presentation | Predominant, persistent depressed mood or marked loss of interest/pleasure in all or almost all activities; extent of the change |
| B: exposure relationship | Appropriate intoxication/withdrawal/medication timing AND evidence that the involved agent can produce the presentation |
| C: independence | Whether an independent depressive disorder better explains the presentation |
| D: delirium | Whether symptoms occur exclusively during delirium |
| E: burden | Clinically significant distress OR impairment |

Do not import MDD's five-of-nine symptom threshold or two-week minimum as mandatory criteria here. The depressive presentation must warrant separate attention rather than merely being an expected transient feature of intoxication or withdrawal. The manual gives persistence around a month after acute effects as one possible clue to independence, alongside pre-exposure symptoms and independent recurrence. It is an example for clinical interpretation, not an automatic cutoff, guaranteed clearance time or instruction to postpone help. [DSM_INDUCED]

## 3. What our agents must distinguish

1. **Patient evidence:** “I started it three weeks ago”; “I felt down a week later.” These are reported events and symptoms.
2. **Reference knowledge:** a classification or current drug label describes possible psychiatric effects. This comes from a source, not a patient quotation.
3. **Case interpretation:** whether this exposure caused this person's depressive disorder. This requires professional judgment and cannot be filled in merely by matching the first two.

The extractor records the first category. A separately reviewed capability reference supports the second. The planner identifies missing information and review needs. A later synthesis component can summarize possibilities with uncertainty; it must not present an automatically confirmed diagnosis. These responsibility boundaries are project design choices.

## 4. Concept cards and concept-specific evidence details

The clinical domains below are sourced; identifiers, optional fields, controlled values and example questions are our implementation design. They are not claimed to be clinical terminologies or validated interview items. Each concept has its own fields. Known facts need quotations; missing facts are not fabricated to complete a form. Supporting symptoms help describe burden and alternatives without changing this disorder into MDD.

### Depressed mood — `depressed_mood`

Reported low, sad or empty mood.

Role: primary_mood_domain. Sources: [VA_2022; NICE_222; DSM_INDUCED].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `description` | The person's account of this experience, without adding a diagnosis. | Supported text; preserve the actual units, timing and uncertainty |
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `days_per_week` | Stated days affected; keep units and wording instead of imposing a diagnostic cutoff. | Supported text; preserve the actual units, timing and uncertainty |
| `proportion_of_day` | Reported share of an affected day; most of the day is already useful. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve the actual units, timing and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** How has your mood been during this period?

**Follow-up:** Meaning, persistence and episode timing if unclear.

**Interpretation limit:** A sad day alone does not establish the domain threshold or MDD.

### Interest and pleasure — `interest_pleasure`

Reduced desire for activities and/or reduced enjoyment.

Role: primary_mood_domain. Sources: [VA_2022; NICE_222; DSM_INDUCED].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `days_per_week` | Stated days affected; keep units and wording instead of imposing a diagnostic cutoff. | Supported text; preserve the actual units, timing and uncertainty |
| `proportion_of_day` | Reported share of an affected day; most of the day is already useful. | Supported text; preserve the actual units, timing and uncertainty |
| `interest` | Reported wanting or motivation to engage. | Supported text; preserve the actual units, timing and uncertainty |
| `pleasure` | Enjoyment when engaged. | Supported text; preserve the actual units, timing and uncertainty |
| `activities` | Affected activities and retained interests. | Supported text; preserve the actual units, timing and uncertainty |
| `breadth` | How broadly activities are affected. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Have your interest or enjoyment in your usual activities changed?

**Follow-up:** Separate wanting from enjoying; establish breadth if relevant.

**Interpretation limit:** One retained hobby does not negate all symptoms; not doing an activity may reflect lack of opportunity.

### Appetite change — `appetite_change`

Change in desire for food.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve the actual units, timing and uncertainty |
| `direction` | Reported appetite direction. | increased / decreased / variable / unclear |
| `appetite_vs_intake` | Distinguish hunger/desire from actual eating. | Supported text; preserve the actual units, timing and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Has your appetite changed compared with usual?

**Follow-up:** Direction, persistence and appetite versus eating.

**Interpretation limit:** Do not infer weight change from appetite. This is supporting symptom information, not a separate induced-disorder count threshold.

### Weight change — `weight_change`

Reported change in body weight.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `direction` | Weight direction. | gain / loss / variable / unclear |
| `amount` | Amount with original units; no guessing. | Supported text; preserve the actual units, timing and uncertainty |
| `interval` | Period over which weight changed. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_weight` | Earlier weight if supplied. | Supported text; preserve the actual units, timing and uncertainty |
| `measurement` | Measured versus estimated account. | measured_report / estimate / unclear |
| `intentionality` | Whether intentional. | intentional / unintentional / mixed / unclear |

**Example question:** Have you noticed a change in your weight during this period?

**Follow-up:** Amount, interval and intentionality when relevant.

**Interpretation limit:** Do not calculate a percentage without compatible stated weights/dates. Do not infer appetite change from weight alone.

### Sleep disturbance — `sleep_disturbance`

Difficulty sleeping or excessive sleep.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve the actual units, timing and uncertainty |
| `pattern` | Reported sleep complaint. | onset_difficulty / maintenance_difficulty / early_waking / excessive_sleep / mixed / unclear |
| `latency` | Time taken to fall asleep. | Supported text; preserve the actual units, timing and uncertainty |
| `awakenings` | Waking during sleep and return-to-sleep account. | Supported text; preserve the actual units, timing and uncertainty |
| `wake_timing` | Actual versus intended/usual waking. | Supported text; preserve the actual units, timing and uncertainty |
| `total_sleep` | Reported sleep hours with period. | Supported text; preserve the actual units, timing and uncertainty |
| `sleep_opportunity` | Opportunity and external interruptions. | Supported text; preserve the actual units, timing and uncertainty |
| `daytime_effect` | Sleepiness, exhaustion or other reported effects. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** How has your sleep changed from what is usual for you?

**Follow-up:** Identify complaint before asking subtype-specific details.

**Interpretation limit:** Insomnia while tired is not reduced sleep need; insufficient opportunity is not automatically insomnia.

### Psychomotor change — `psychomotor_change`

Noticeable motor/speech slowing or agitation.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `direction` | Reported observable change. | slowing / agitation / both / unclear |
| `examples` | Concrete speech/movement behaviour. | Supported text; preserve the actual units, timing and uncertainty |
| `observer` | Who noticed it; self-report about another observer remains patient report. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve the actual units, timing and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Have you or other people noticed changes in how quickly you move or speak?

**Follow-up:** Observable examples and reporter, rather than restlessness alone.

**Interpretation limit:** Text response speed and feeling restless alone do not establish observable psychomotor change.

### Energy and fatigue — `energy_fatigue`

Unusual tiredness or reduced energy.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve the actual units, timing and uncertainty |
| `experience` | Fatigue, low energy or both. | Supported text; preserve the actual units, timing and uncertainty |
| `sleepiness` | Reported sleepiness if distinguished. | Supported text; preserve the actual units, timing and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** How has your energy been compared with usual?

**Follow-up:** Examples and timing; separate sleepiness if ambiguous.

**Interpretation limit:** Do not automatically attribute fatigue to depression or infer it from short sleep.

### Worthlessness and guilt — `worthlessness_guilt`

Low self-worth or excessive/inappropriate guilt.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `content` | Actual self-evaluation or guilt account. | Supported text; preserve the actual units, timing and uncertainty |
| `kind` | Reported experience. | worthlessness / guilt / both / unclear |
| `context` | What the thought concerns; retain uncertainty about proportionality. | Supported text; preserve the actual units, timing and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** How have you been thinking about yourself during this period?

**Follow-up:** Actual thought content; clarify without endorsing it.

**Interpretation limit:** Ordinary regret, low confidence and guilt about illness are not automatically qualifying guilt.

### Concentration and decisions — `cognition_decisions`

Reported thinking, attention or decision difficulty.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve the actual units, timing and uncertainty |
| `kind` | Reported difficulty. | concentration / thinking / indecision / mixed / unclear |
| `tasks` | Concrete affected tasks. | Supported text; preserve the actual units, timing and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Have concentrating or making decisions become harder than usual?

**Follow-up:** Task examples and change from baseline.

**Interpretation limit:** Do not label dementia, ADHD or depression from this alone.

### Death/suicide-related reports — `death_suicide`

Death-related thoughts, suicidal thoughts, plans or attempts.

Role: supporting_assessment. Sources: [ASQ_BSSA; NICE_225].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `experience` | Preserve distinctions. | death_thoughts / wish_not_alive / suicidal_thoughts / suicide_plan / suicide_attempt / unclear |
| `recency` | When last/current; do not infer resolution. | Supported text; preserve the actual units, timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `intent` | Intent as reported. | Supported text; preserve the actual units, timing and uncertainty |
| `plan_present` | Whether a plan was explicitly reported or denied. | reported / denied / unclear |
| `access` | Access to means as reported, without generating procedural details. | Supported text; preserve the actual units, timing and uncertainty |
| `past_behaviour` | Historical self-injury/attempt account, intent and timing. | Supported text; preserve the actual units, timing and uncertainty |
| `support` | Available support as reported. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Have you had thoughts about ending your life?

**Follow-up:** Use dedicated safety pathway; preserve current versus historical information.

**Interpretation limit:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text; preserve the actual units, timing and uncertainty |
| `examples` | Concrete difficulty or distress. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline` | Usual functioning. | Supported text; preserve the actual units, timing and uncertainty |
| `supports` | Assistance helping preserve functioning. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** How have these changes affected your daily life?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Activation history — `activation_history`

Possible distinct elevated/overactive periods requiring review.

Role: supporting_assessment. Sources: [NIMH_BIPOLAR; DSM_INDUCED].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `period` | Current/historical time. | Supported text; preserve the actual units, timing and uncertainty |
| `mood` | Elevated, expansive or irritable mood as reported. | Supported text; preserve the actual units, timing and uncertainty |
| `energy_activity` | Change in energy/activity. | Supported text; preserve the actual units, timing and uncertainty |
| `sleep_need` | Sleep need and tiredness, not just sleep hours. | Supported text; preserve the actual units, timing and uncertainty |
| `other_changes` | Associated speech, thoughts, confidence or risky behaviour. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | Duration of that period. | Supported text; preserve the actual units, timing and uncertainty |
| `impact` | Consequences or other observers. | Supported text; preserve the actual units, timing and uncertainty |
| `exposure_context` | Medicines/substances/medical context. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Have you had a distinct period of unusually increased energy or activity?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Medical context — `medical_context`

Relevant reported medical history and symptoms.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `conditions` | Reported conditions; distinguish reported diagnosis from confirmation. | Supported text; preserve the actual units, timing and uncertainty |
| `timeline` | Relationship to symptoms. | Supported text; preserve the actual units, timing and uncertainty |
| `investigations` | Results only if actually supplied. | Supported text; preserve the actual units, timing and uncertainty |
| `clinician_review` | Known professional assessment or unresolved need. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Are there health conditions that might be relevant to these changes?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Psychotic experiences — `psychotic_experience`

Reported experiences requiring specialist interpretation.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `kind` | Experience as described, not an automatic diagnosis. | Supported text; preserve the actual units, timing and uncertainty |
| `content` | Brief relevant content without affirming beliefs. | Supported text; preserve the actual units, timing and uncertainty |
| `mood_relationship` | During versus outside mood episodes. | Supported text; preserve the actual units, timing and uncertainty |
| `conviction_context` | Reported belief/context and uncertainty. | Supported text; preserve the actual units, timing and uncertainty |
| `safety_concerns` | Any reported urgent implications. | Supported text; preserve the actual units, timing and uncertainty |
| `reported_mood_congruence` | Professional mood-congruence description if actually supplied; do not invent it. | congruent / incongruent_or_mixed / unclear |

**Example question:** Have you had experiences that other people do not seem to share?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text; preserve the actual units, timing and uncertainty |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text; preserve the actual units, timing and uncertainty |
| `period` | When and for which symptoms. | Supported text; preserve the actual units, timing and uncertainty |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text; preserve the actual units, timing and uncertainty |
| `use` | Actual use and barriers as reported. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Have you received help for something similar before?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Family history — `family_history`

Relevant family mood/psychiatric history.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `relative` | Relationship, without unnecessary identifying details. | Supported text; preserve the actual units, timing and uncertainty |
| `reported_condition` | Condition as reported. | Supported text; preserve the actual units, timing and uncertainty |
| `certainty` | How the person knows; unknown remains unknown. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Is there relevant mental-health history in your family?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Life context — `life_context`

Relevant stress, loss, trauma and support.

Role: supporting_assessment. Sources: [VA_2022; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `events` | Events relevant to symptom timeline. | Supported text; preserve the actual units, timing and uncertainty |
| `timing` | Temporal relationship. | Supported text; preserve the actual units, timing and uncertainty |
| `support` | Current supports. | Supported text; preserve the actual units, timing and uncertainty |
| `barriers` | Practical barriers. | Supported text; preserve the actual units, timing and uncertainty |
| `meaning` | Person's interpretation of the context. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Has anything important been happening around the time these changes began?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Overall depressive presentation — `syndrome_course`

Whether depressive symptoms predominate, persist and warrant attention beyond usual transient exposure effects.

Role: supporting_assessment. Sources: [DSM_INDUCED; TIP42].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `onset` | Actual start of the mood change, including uncertain dates. | Supported text; preserve the actual units, timing and uncertainty |
| `duration` | Reported duration; no universal two-week requirement in this module. | Supported text; preserve the actual units, timing and uncertainty |
| `course` | Continuous, fluctuating, improving or worsening course in the person's words. | Supported text; preserve the actual units, timing and uncertainty |
| `predominance` | What is most troubling; professional review decides syndrome predominance. | Supported text; preserve the actual units, timing and uncertainty |
| `related_symptoms` | Other simultaneous symptoms with their own source support. | Supported text; preserve the actual units, timing and uncertainty |
| `clinical_attention` | Reported reason for seeking care or clinician concern. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** When did this change in your mood first begin?

**Follow-up:** Clarify baseline, continuity and burden before collecting redundant details.

**Interpretation limit:** A temporary unpleasant feeling is not automatically a separate depressive disorder.

### Medicine/substance identification and use — `exposure_details`

A reported exposure, recorded separately for each agent without assuming its contents or effects.

Role: supporting_assessment. Sources: [VA_2022; DSM_INDUCED; TIP42].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `name_as_reported` | Name or description exactly as identified; preserve uncertainty about street products. | Supported text; preserve the actual units, timing and uncertainty |
| `kind` | Reported source category; prescribed use does not establish misuse. | prescribed_medicine / nonprescribed_medicine / alcohol / other_substance / supplement / unknown |
| `formulation` | Tablet, liquid or other reported preparation; unknown strength stays unknown. | Supported text; preserve the actual units, timing and uncertainty |
| `route` | Reported route; do not infer from product name. | Supported text; preserve the actual units, timing and uncertainty |
| `dose_or_amount` | Reported amount with units/strength where known; no guessed conversion. | Supported text; preserve the actual units, timing and uncertainty |
| `pattern` | How often and for how long used; distinguish prescribed instructions from actual use. | Supported text; preserve the actual units, timing and uncertainty |
| `indication` | Why the medicine was started, if known. | Supported text; preserve the actual units, timing and uncertainty |
| `prescriber` | Reported prescribing/review professional, if any. | Supported text; preserve the actual units, timing and uncertainty |
| `certainty` | Limits of identification or recall. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** What medicines, supplements, alcohol or other substances have you been using recently?

**Follow-up:** Follow up one relevant agent at a time: actual name, use and changes.

**Interpretation limit:** Do not infer a substance use disorder, a dose, or a causal agent.

### Exposure changes and last use — `exposure_events`

Chronology of starting, changing, missing, stopping or resuming a particular exposure.

Role: supporting_assessment. Sources: [DSM_INDUCED; NICE_215; NICE_222].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `event` | Reported event, not an instruction. | started / increased / decreased / missed_doses / stopped / resumed / last_use / unchanged_use / unclear |
| `event_time` | Date/interval as reported; do not turn relative dates into exact dates without a reference. | Supported text; preserve the actual units, timing and uncertainty |
| `previous_use` | Pattern/dose before this event. | Supported text; preserve the actual units, timing and uncertainty |
| `subsequent_use` | Pattern/dose after this event. | Supported text; preserve the actual units, timing and uncertainty |
| `event_sequence` | Additional events in chronological narrative when more than one is reported. | Supported text; preserve the actual units, timing and uncertainty |
| `supervision` | Whether a clinician was involved as reported. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Was there any change in how you were taking or using it around that time?

**Follow-up:** Resolve which agent and which change before asking for precise timing.

**Interpretation limit:** No instruction to stop, restart, increase or taper for diagnostic testing.

### Mood relative to exposure — `exposure_mood_timing`

Reported temporal relationship; causation remains a separate professional judgment.

Role: supporting_assessment. Sources: [DSM_INDUCED; TIP42].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `relation` | Relative chronology established by the account. | before_exposure / during_use / after_start_or_increase / after_reduction_or_stopping / no_clear_relationship / unclear |
| `interval` | Actual reported gap between event and symptom onset/change. | Supported text; preserve the actual units, timing and uncertainty |
| `symptom_change` | Specific mood/symptom change linked in the account. | Supported text; preserve the actual units, timing and uncertainty |
| `baseline_before_event` | How the person felt before this event. | Supported text; preserve the actual units, timing and uncertainty |
| `patient_explanation` | The person's own belief about cause, explicitly labelled as a belief. | Supported text; preserve the actual units, timing and uncertainty |
| `other_changes` | Other simultaneous events that could affect interpretation. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** How did the timing of the mood change compare with starting or changing it?

**Follow-up:** Clarify before/after and interval; resolve ambiguous pronouns with earlier messages.

**Interpretation limit:** After does not mean caused by; a yes about timing is not a confirmed induced disorder.

### Depression outside the exposure period — `independent_depression_history`

Prior or persistent depressive symptoms that may support an independent explanation.

Role: supporting_assessment. Sources: [DSM_INDUCED; SAMET_2013; TIP42].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `earlier_period` | Earlier low-mood or loss-of-interest period, kept separate from current symptoms. | Supported text; preserve the actual units, timing and uncertainty |
| `exposure_context_then` | Use/nonuse at that time, only if actually described. | Supported text; preserve the actual units, timing and uncertainty |
| `onset_before_use` | Reported chronology before exposure began. | Supported text; preserve the actual units, timing and uncertainty |
| `recurrence` | Reported repeated periods and intervening recovery. | Supported text; preserve the actual units, timing and uncertainty |
| `previous_diagnosis` | Reported clinician diagnosis, not our confirmation. | Supported text; preserve the actual units, timing and uncertainty |
| `certainty` | Unclear dates, exposure coverage or symptom recollection. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Have you had a similar period before, including times before you used this medicine or substance?

**Follow-up:** Keep historical symptoms and their exposure context together.

**Interpretation limit:** An earlier episode does not automatically rule out a current induced episode or prove MDD.

### Course after an exposure change — `post_exposure_course`

Observed/reportable course after a change that already occurred, with continued uncertainty.

Role: supporting_assessment. Sources: [DSM_INDUCED; TIP42; ABSTINENCE_2021].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `observation_interval` | Time since the reported change; not an enforced waiting period. | Supported text; preserve the actual units, timing and uncertainty |
| `mood_course` | Improvement, persistence, worsening or fluctuation in actual words. | Supported text; preserve the actual units, timing and uncertainty |
| `other_symptom_course` | Physical or cognitive changes with their own timing. | Supported text; preserve the actual units, timing and uncertainty |
| `ongoing_exposures` | Other continued use or treatment that affects interpretation. | Supported text; preserve the actual units, timing and uncertainty |
| `followup_available` | Whether follow-up observations exist. | Supported text; preserve the actual units, timing and uncertainty |
| `professional_review` | Reported clinician interpretation, attributed as such. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Since that change happened, what has happened to your mood?

**Follow-up:** Compare actual observations with earlier reports; ask about alternative changes.

**Interpretation limit:** Do not require one month without help, assume recovery, or propose a deliberate rechallenge.

### Possible intoxication/withdrawal context — `intoxication_withdrawal_context`

Reported symptoms or professional assessments around use or reduction; not a chat diagnosis.

Role: supporting_assessment. Sources: [TIP42; NICE_215; NICE_100].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `reported_state` | Label used in the account. | intoxication / withdrawal / neither_reported / unclear |
| `symptoms` | Actual physical/mental changes, their timing and severity. | Supported text; preserve the actual units, timing and uncertainty |
| `assessment_basis` | How the state is known. | patient_description / reported_clinician_assessment / unclear |
| `timing` | Relative to actual use/reduction/cessation. | Supported text; preserve the actual units, timing and uncertainty |
| `past_complications` | Reported previous seizure, delirium or severe withdrawal. | Supported text; preserve the actual units, timing and uncertainty |
| `current_medical_concern` | Current acute concerns needing professional assessment. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** What other changes did you notice around the time you reduced or stopped it?

**Follow-up:** Acute confusion, seizure or serious physical deterioration interrupts ordinary questioning.

**Interpretation limit:** Tolerance, dependence or withdrawal alone does not establish a substance use disorder.

### Acute confusion and attention changes — `acute_cognitive_change`

Recent or fluctuating change in attention, awareness or thinking that requires medical assessment.

Role: supporting_assessment. Sources: [DSM_INDUCED; NICE_103].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `change` | What changed from baseline, as reported. | Supported text; preserve the actual units, timing and uncertainty |
| `onset` | Hours/days versus longstanding pattern, if known. | Supported text; preserve the actual units, timing and uncertainty |
| `fluctuation` | Changes over the day as described. | Supported text; preserve the actual units, timing and uncertainty |
| `observer` | Patient or identified collateral observer. | Supported text; preserve the actual units, timing and uncertainty |
| `medical_context` | Concurrent illness, exposure or withdrawal context. | Supported text; preserve the actual units, timing and uncertainty |
| `review_status` | Reported assessment or unresolved need. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Have you or someone with you noticed any sudden change in confusion or ability to pay attention?

**Follow-up:** Use appropriate urgent clinical review when acute changes are reported; do not continue a diagnostic checklist.

**Interpretation limit:** Depressive symptoms occurring exclusively during delirium do not establish this induced depressive disorder.

### Illness, treatment and competing explanations — `medical_indication_confounding`

The illness being treated, its course and other medical factors may also explain symptoms.

Role: supporting_assessment. Sources: [DSM_INDUCED; VA_2022].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `illness` | Reported underlying illness or reason for treatment. | Supported text; preserve the actual units, timing and uncertainty |
| `illness_timeline` | Illness changes relative to medicine and mood changes. | Supported text; preserve the actual units, timing and uncertainty |
| `symptoms_before_treatment` | Symptoms that existed before treatment. | Supported text; preserve the actual units, timing and uncertainty |
| `other_explanations` | Reported medical, psychosocial or concurrent exposure concerns. | Supported text; preserve the actual units, timing and uncertainty |
| `records_available` | Reported clinician records or investigations; their interpretation remains professional. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** What was happening with the condition being treated when your mood changed?

**Follow-up:** Separate illness onset, treatment onset and mood onset.

**Interpretation limit:** Medicine use for an illness does not distinguish medicine effects from effects of the illness.

### Reported tests and professional findings — `reported_tests_review`

Patient report of tests or clinical interpretation, explicitly attributed and not treated as verified laboratory data.

Role: supporting_assessment. Sources: [DSM_INDUCED; TIP42].

| Output detail | Meaning | Permitted value/form |
|---|---|---|
| `test_or_assessment` | What test or review was reported. | Supported text; preserve the actual units, timing and uncertainty |
| `reported_result` | Result exactly as reported, with uncertainty. | Supported text; preserve the actual units, timing and uncertainty |
| `timing` | When specimen/test occurred relative to exposure and symptoms. | Supported text; preserve the actual units, timing and uncertainty |
| `report_available` | Whether the actual report is available. | Supported text; preserve the actual units, timing and uncertainty |
| `professional_interpretation` | Attributed clinician explanation, if supplied. | Supported text; preserve the actual units, timing and uncertainty |

**Example question:** Has a clinician assessed these changes or discussed any relevant test results with you?

**Follow-up:** Obtain the actual report through authorized professional workflows if needed.

**Interpretation limit:** Positive toxicology indicates exposure, not individual causation; negative testing does not exclude past exposure.

## 5. Exposure capability and onset reference

The separate `capability_reference.json` records the pinned classification table and a few medication-evidence examples. It is not a complete pharmacology database. Do not interpret a substance-class entry as proof about every product, amount or individual. If a product is not identified, preserve that uncertainty. Unknown composition is not a licence to invent an active ingredient. [DSM_INDUCED]

| Class in DSM-5-TR Table 1 | Listed depressive-disorder onset context |
|---|---|
| Alcohol | Intoxication or withdrawal |
| Phencyclidine | Intoxication |
| Other hallucinogens | Intoxication |
| Inhalants | Intoxication |
| Opioids | Intoxication or withdrawal |
| Sedative/hypnotic/anxiolytic | Intoxication or withdrawal |
| Stimulants, including amphetamine-type/cocaine | Intoxication or withdrawal |
| Other/unknown substance | Intoxication or withdrawal |

Caffeine, cannabis and tobacco have no depressive-disorder entry in this particular table. That is a classification boundary, not a statement that these exposures cannot affect mood or are harmless. Do not relabel them “other” simply to force the diagnosis. The medication route also needs agent-specific evidence rather than extrapolation from this substance table. [DSM_INDUCED]

The onset descriptions distinguish symptoms arising with intoxication, with withdrawal, or after medication use/change/withdrawal. Intoxication and withdrawal labels require assessment of the relevant state, not merely a patient's casual use of the word. We preserve the person's description and any attributed clinician assessment; the LLM does not independently certify the syndrome. [DSM_INDUCED; TIP42]

For a medication review, identify the actual agent, formulation if relevant, reported dose/use, indication, co-medications and changes. Link the current label or primary evidence with its date/version and location. Have a qualified reviewer assess the applicability. This package supplies no complete dose-response table, pharmacokinetic calculator or adverse-reaction causality score. [VA_2022; NICE_215]

### Why a simple list of “depression-causing medicines” would be misleading

Prednisone's official label describes psychiatric disturbances including severe depression, along with other possible presentations. That warning justifies attention to symptoms and professional medication review; it does not establish the cause in an individual. It also means activation/psychotic symptoms should not be ignored because the person initially reported sadness. [PREDNISONE_LABEL]

A randomized-trial meta-analysis did not support a general increased-depression rule for beta-blockers; the record includes a linked correction. The isotretinoin meta-analysis likewise did not find increased overall psychiatric risk at population level. Neither result establishes that an individual's new symptoms are irrelevant. Evidence design, underlying illness and individual context matter. These examples are included to prevent blanket causal rules, not to recommend either medicine or declare a patient's medication safe. [BETA_2021; ISOTRETINOIN_2024]

## 6. Differential information to collect

| Possibility | What distinguishes the assessment question | Boundary |
|---|---|---|
| Independent MDD/PDD | Earlier symptoms before the exposure, recurrence, chronicity, periods without relevant use | Use the dedicated module to review its requirements; prior low mood alone is not MDD |
| Substance/medication-induced presentation | Particular exposure, relevant timing, capability evidence and alternatives | Timing is necessary information, not sufficient causation |
| Ordinary intoxication/withdrawal symptoms | Broader expected syndrome, severity and separate clinical attention | Do not label every withdrawal low mood as a separate depressive disorder |
| Antidepressant withdrawal versus relapse | Actual missed/reduced/stopped doses, rapidity, physical/mental symptoms and prior course | Requires clinician review; no LLM medication adjustment |
| Underlying physical illness | Illness onset/course, mood before treatment, clinician findings | An illness and its medicine may both be relevant |
| Bipolar-spectrum/activation presentation | Distinct elevated/irritable mood, increased activity, reduced need for sleep and lifetime course | Insomnia with exhaustion is not reduced sleep need |
| Delirium | Recent/fluctuating attention, awareness/cognitive change and medical setting | Acute assessment; symptoms exclusively within delirium do not establish this diagnosis |
| Substance use disorder | Separate pattern of problems requiring dedicated assessment | Exposure, dependence or withdrawal alone do not confirm it |
| Psychosocial/contextual distress | Life events, loss, stressors, meaning and impact | Do not erase them because an exposure exists |

These are focused alternative pathways, not full treatment modules for every condition. Multiple explanations may coexist. For example, someone can have an independent depressive history and a new exposure-related change. Preserve competing accounts until they can be reviewed. [DSM_INDUCED; TIP42; NIMH_BIPOLAR; NICE_222; NICE_103]

NICE explains that antidepressant withdrawal can follow abrupt stopping, missed doses or dose reduction and can include both mental and physical symptoms. Its timing may differ from relapse. Ask what actually happened and arrange prescriber review rather than automatically labelling either withdrawal or relapse. [NICE_222, 1.4.12–1.4.19]

## 7. Interview structure and when to follow up

This is a **semi-structured project policy**. Sources justify the domains and safeguards; they do not validate this exact conversational order. The final cross-disorder graph still needs to connect this module with the others. Do not describe this as the MINI, SCID or PRISM interview.

1. **Immediate concern:** Attend to acute safety/medical concerns first; use the agreed human-review pathway. Do not claim an emergency response was delivered without confirmation.
2. **Presentation:** Open account of what changed, baseline, onset and impact. Recognize clinically relevant information volunteered outside the current question.
3. **Exposure overview:** Identify recent/current medicines, nonprescribed products, alcohol and other substances. Ask neutrally, without assuming misuse.
4. **Agent timeline:** For each relevant agent clarify actual use and start/change/stop/last-use events. One focused unresolved target at a time; no automatic medication changes.
5. **Mood relationship:** Compare mood onset/change with each exposure event. Temporal relationship and drug capability are separate.
6. **Independent course:** Ask about similar earlier symptoms, unexposed periods and actual post-change course. Preserve different periods; do not enforce abstinence as a prerequisite for care.
7. **Alternatives:** Review medical illness, activation history, delirium and competing explanations. Full treatment of alternative disorders remains outside this module.
8. **Review handoff:** Summarize supported findings, uncertainties and targeted review needs. Patient may pause/decline; missing information is not a negative finding.


At each turn the extractor reviews the transcript and existing evidence before the planner chooses a target. If an answer already gives frequency and duration, store both and do not ask them again just because one was the intended target. If a medicine timeline remains uncertain, clarify that specific gap rather than restarting the whole medication history. A relevant answer to another topic is still evidence; do not discard it as off-topic. These are application rules, not new diagnostic criteria.

**Focused follow-up example:** Person: “I started the tablets three weeks ago, but I was already sad before that.” Store both the exposure and the pre-exposure mood account. Ask how long the low mood had been present beforehand. Do not ask “Did the medicine make you depressed?” as if causation were established.

**Context example:** Assistant: “Did the low mood begin after starting prednisone?” Person: “Yes, about a week later.” The affirmative refers to that named question. Store the timing with earlier context-message references. Do not turn this into affirmation of a diagnosis, apply it to a second medication or infer a dose.

**Two-agent example:** “I stopped A last week and started B yesterday.” Separate the exposure events under application-owned references. Do not merge them into one generic medication record. Symptoms with uncertain attribution remain unassigned rather than attached to whichever drug was mentioned last.

**Correction example:** “Actually I felt low before I started it.” Preserve the earlier statement and explicit correction. Resolve the supported chronology with provenance or mark a genuine unresolved conflict for review. Never retain the earlier chronology silently as a confirmed fact.

**Off-topic example:** If asked about timing and the person discusses university difficulty, record the functional information. Then acknowledge it and explain: “That sounds hard. To understand the timing, do you remember whether the low mood started before or after the tablets?” If they cannot remember, record unknown. If they decline, respect that and record the unresolved target. Do not repeatedly pressure them to answer.

## 8. Longitudinal course and research contribution

SAMHSA stresses that intoxication/withdrawal can resemble depression, that distinguishing induced from independent symptoms can be difficult, and that the interpretation may change with follow-up. Depressive symptoms can persist during early recovery; a single interview does not settle causation. This supports recording actual exposure/symptom courses and preserving uncertainty. It does not justify dismissing distress or withholding care while the explanation remains uncertain. [TIP42]

Samet and colleagues used PRISM-based assessment in prospective research on independent/substance-induced major depression and alcohol, cocaine and heroin dependence outcomes. We use the study to motivate preserving those distinct histories and follow-up information. The study is not a validation of our question wording or schema, and its research diagnostic labels are not automatically substituted for current DSM criteria. PRISM items, training materials and licensing are not included. The PubMed record links free full text. [SAMET_2013]

The early-abstinence study followed depressive symptoms during alcohol/opioid abstinence and observed change over time. Its sample-specific results are a reason to record trajectories, not a rule to wait a month before support or to generalize to every medication. We do not implement its clinical treatment conclusions as a universal policy. [ABSTINENCE_2021]

The beta-blocker and isotretinoin syntheses contribute evidence-quality caution, not assessment datasets or training data. No model was trained, no published benchmark was run and no instrument accuracy was inherited by creating these files. [BETA_2021; ISOTRETINOIN_2024]

## 9. Medical and suicide-related boundaries

Assess suicidal thoughts/behaviour and current support when indicated, separately from causal attribution. Do not assume an exposure explains away suicidal distress. The suicide card preserves current versus historical experiences; unmentioned intent is unknown, not denied. NIMH's adult brief safety-assessment guide is intended for trained clinicians following a positive ASQ screen; our conversational system has not thereby become a validated ASQ service. NICE advises against using scales or low/medium/high labels to predict suicide or determine care. [ASQ_BSSA; NICE_225]

A schema's `safety_handoff.status` is a workflow flag. It is not a predictive risk category, proof of safety, completed clinical assessment or evidence that a professional was contacted. An application must implement and verify its human-review pathway before claiming that escalation was delivered. Acute medical concerns, severe withdrawal symptoms, seizure or rapidly changing confusion must not be absorbed into routine depression questioning. [NICE_100; NICE_103]

Do not recommend stopping alcohol or sedative medicines abruptly as a test of causation. Alcohol withdrawal may require medically supervised assessment; NICE advises against sudden reduction in dependent people outside admission. NG215 addresses clinician-supervised withdrawal decisions for medicines associated with dependence/withdrawal. This module contains no taper, dosing, detoxification or deliberate rechallenge instructions. Any actual decision belongs to the responsible clinician. [NICE_100; NICE_215]

## 10. Evidence output: clear meaning of every shared item

| Item | Meaning and ownership |
|---|---|
| `module_id`, `schema_version` | Fixed application contract identifiers |
| `exposures` | Registry of reported agents; code assigns stable references and links reported names to exact patient text |
| `exposure_ref` | Registry reference when a record is about that agent; null when unassigned/not agent-specific. It does not mean the agent caused the symptom |
| `concept_id` | Allowlisted clinical-information domain from a concept card |
| `episode_key` | Application-owned assessment-period key; does not itself establish a formal depressive episode |
| `subject` | Patient in this contract; third-party symptoms are not assigned to the patient |
| `finding_status` | Reported presence/absence, ambiguity or conflict; not professional confirmation |
| `temporal_status`, `time_reference` | Current/historical/unclear period plus actual reported time text |
| `attributes` | Only the fields allowed for that particular concept; no identical forced form for every symptom |
| `evidence` | Exact patient quotation, source-message ID, earlier context IDs and the claim fields it supports |
| `uncertainty_notes` | Recall, contradiction, attribution or other limitations |
| `semantic_check_status` | Whether meaning appears supported or still needs review; this is not guaranteed by JSON validation |
| `question_tracking` | Application question target/status and remaining target; answers may be partial or declined |
| `safety_handoff` | Current workflow concern flag, reported concerns and unresolved questions; no claim of real-world delivery |

All controlled values are described below and in `knowledge.json`. They are project-defined data states. Unknown is an epistemic state, not a clinical symptom. A known attribute has a value; unknown has no value; not-applicable needs a reason. Absence must be explicitly denied for the relevant subject/period. Omitting a field merely means it was not supplied in that record; it does not mean normal.


### `finding_status`

- `reported_present`: Explicitly described or affirmed in context; not clinical confirmation.
- `reported_absent`: Explicitly denied for this subject/period.
- `unclear`: Meaning or polarity unresolved.
- `conflicting`: Accounts for the same subject/period conflict and are retained.

### `temporal_status`

- `current`: Described as relevant to current period.
- `historical`: An earlier period.
- `unclear`: Timing unresolved.

### `detail_status`

- `known`: A supported value is available.
- `unknown`: Relevant but unresolved; no value asserted.
- `not_applicable`: Inapplicability is explicitly justified; not equivalent to not asked.

### `question_status`

- `not_asked`: No recorded question.
- `answered`: Target addressed.
- `partially_answered`: Some target information supplied.
- `unclear`: Response ambiguous.
- `declined`: Person chose not to answer.

### `semantic_check_status`

- `supported`: Evidence appears to support the claim.
- `needs_review`: Meaning/attribution remains unresolved.

### `safety_handoff_status`

- `not_assessed`: Available conversation has not assessed current safety; no reassuring inference.
- `no_signal_reported_in_available_text`: No concern reported in reviewed text; does not establish safety or predict future behaviour.
- `needs_clinical_review`: An unresolved concern requires clinical review; not a predictive risk category or proof of contact.
- `urgent_review_needed`: Current reported concerns require urgent human/medical review; no claim of response delivery.


### Storage, context and provenance rules

There is no model-generated evidence UUID. Code manages message IDs, exposure references and period keys. The snapshot key is `(concept_id, episode_key, subject, exposure_ref)`: update that record with supported new details, preserving its evidence. Distinct agents and periods stay separate. Multiple events within one period may be retained in the event-sequence narrative and quotations; a future normalized event-log extension needs its own contract.

Every known attribute and finding status needs an explicit evidence link. A short “yes” needs earlier conversational context to identify what was affirmed. Source quotes remain exact substrings of patient messages; earlier context must actually precede the answer. The validator can enforce these structural rules but cannot prove that the quoted words semantically support a claim. Human review and purpose-built extraction evaluation remain necessary.

Patient testimony about a positive test is stored as **reported** test information. No verified laboratory-results import is implemented here. Drug-label knowledge belongs in the capability reference, not in a fabricated patient quotation. A professional causal opinion, if reported by the person, must remain attributed; it is not independently verified by our system.

## 11. Fictional example and expected interpretation

`examples.json` contains an opening snapshot and a later snapshot of the same fictional conversation. The person reports current low mood, prednisone started three weeks ago, an incompletely identified second medicine, mood beginning about a week after prednisone, and a low period last year before ever taking prednisone. Later they report missed doses of Medicine B while prednisone is unchanged.

Expected result: retain separate agent timelines; resolve the contextual “yes”; preserve the earlier depressive history; do not copy three weeks of medicine use into mood duration; do not manufacture a dose, withdrawal syndrome, MDD or induced diagnosis. The earlier episode is a clue needing review, not a guaranteed independent diagnosis. Safety is unassessed in this short fixture. The snapshots demonstrate the proposed contract, not outputs from a live LLM.

The full example output is available in `examples.json`; the schema is `evidence_output.schema.json`. These files contain no API key, real patient information or model call.

## 12. Measures, tests and professional handoff

PHQ-2/PHQ-9 may belong in the shared depression pathway as screening/symptom-burden measures using the original verified version and scoring. A score does not identify a pharmacological cause, distinguish withdrawal from relapse or replace the differential. This module does not reproduce a questionnaire, infer answers from free text or implement a score. Its proposed sequence is not itself a validated tool. [VA_2022; NICE_222]

There is no universal laboratory panel or toxicology requirement for every conversation. A clinician decides investigations from the history, examination and context. A toxicology finding alone cannot establish that a substance caused the depressive syndrome; timing, assay limitations and other explanations remain relevant. [DSM_INDUCED; VA_2022]

The professional handoff should contain: predominant symptoms and burden; actual agent identities and unknowns; symptom/exposure chronology; relevant prior independent periods; competing explanations; acute concerns and actual escalation status; capability-source review status; and unresolved targeted questions. Use “possible exposure-related contribution; attribution unresolved” when that reflects the evidence. Do not assert a confirmed diagnosis, causal certainty or billing code.

## 13. Files, checks and remaining work

`knowledge.json` holds concept cards, fields, criteria-information map, values and interview policy. `sources.json` holds source links, locations, contribution and access notes. `capability_reference.json` keeps clinical reference material separate from patient evidence. The schema defines the output contract. The examples are fictional. `validate_package.py` checks the contract, references and deliberately invalid cases; `VALIDATION_REPORT.json` records the results.

Mechanical validation is not clinical validation, an LLM accuracy benchmark or proof of completeness for every drug and presentation. Remaining work includes qualified clinical review, further agent-specific capability review, final cross-disorder question graph, runtime integration and evaluation on varied fictional cases (polysubstance use, ambiguous chronology, corrections, cognitive changes and safety handoffs). Existing agents have not been connected to this Desktop package by creating these files.

The knowledge content and contract are ready for that next review/integration stage. Medication prescribing/withdrawal management, full SUD diagnosis/treatment and child pathways remain outside this module's implementation scope. No copyrighted DSM/PRISM manuals or original questionnaire items are bundled.

## 14. Source register: links, exact locations and what we used

Page numbers refer to printed pages unless explicitly marked PDF viewer pages. Research uses are labelled separately from diagnostic authority. Access limitations are recorded rather than implying all books or instruments are free.


### NICE_222

[NICE NG222, Depression in adults](https://www.nice.org.uk/guidance/ng222/chapter/Recommendations)

**Location:** 1.2.1–1.2.9; Definitions of depression/severity; 1.12.1; 1.4.12–1.4.19, antidepressant withdrawal

**Used for:** Comprehensive assessment, communication, safety and specialist review; withdrawal versus relapse and prescriber review

**Access:** Official search-indexed recommendation extracts inspected; direct retrieval intermittently 403

### NICE_225

[NICE NG225, Self-harm](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)

**Location:** 1.6.1–1.6.6

**Used for:** No predictive low/medium/high stratification; needs-focused assessment

**Access:** Public primary-source material inspected

### ASQ_BSSA

[NIMH Adult Outpatient Brief Suicide Safety Assessment Guide](https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials/adult-outpatient/adult-outpatient-brief-suicide-safety-assessment-guide)

**Location:** Intended users; thoughts, plan, past behaviour, supports and disposition sections

**Used for:** Safety information domains; clinician guide following positive ASQ, not autonomous LLM validation

**Access:** Public primary-source material inspected

### VA_2022

[VA/DoD MDD Clinical Practice Guideline, 2022](https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/MH/mdd/VADODMDDCPGFinal508.pdf)

**Location:** p.19 Sidebars 1–2; pp.140–141 Appendix K; Appendix I pp.127–131

**Used for:** Episode foundation, work-up and measurement context; sidebar is abbreviated DSM-5-era material

**Access:** Public primary-source material inspected

### NIMH_BIPOLAR

[NIMH, Bipolar Disorder](https://www.nimh.nih.gov/health/publications/bipolar-disorder)

**Location:** Types; symptom comparison; diagnosis

**Used for:** Activation history, reduced sleep need and bipolar uncertainty

**Access:** Public primary-source material inspected

### NIMH_DEP

[NIMH, Depression](https://www.nimh.nih.gov/health/publications/depression)

**Location:** Signs/symptoms; diagnosis; age-presentation paragraphs

**Used for:** Plain-language symptom domains and adult context

**Access:** Public primary-source material inspected

### DSM_INDUCED

[APA DSM-5-TR (2022), Substance/Medication-Induced Depressive Disorder](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders)

**Location:** Printed pp.201–206; substance-class Table 1 pp.545–546; PDF viewer pp.330–336 and 755–756

**Used for:** Criteria-information map, onset descriptions, differential and substance-class reference

**Access:** Original APA text inspected through public psychiatry.ru mirror; publisher full text blocked; no redistribution rights inferred and no book bundled.

### TIP42

[SAMHSA TIP 42 (2020), Chapter 4](https://www.ncbi.nlm.nih.gov/books/NBK571021/)

**Location:** Substance-Induced Mental Disorders; Substance-Induced Depressive Disorders; Exhibits 4.16–4.18

**Used for:** Longitudinal assessment, independent/induced distinction and co-occurring conditions

**Access:** Public primary-source material; relevant sections inspected

### NICE_215

[NICE NG215, medicines associated with dependence or withdrawal symptoms](https://www.nice.org.uk/guidance/ng215/chapter/Recommendations)

**Location:** 1.5.6; 1.5.15–1.5.17

**Used for:** Withdrawal assessment and prescriber review; no abrupt-stop experiments

**Access:** Public primary-source material; relevant sections inspected

### NICE_100

[NICE CG100, alcohol-use disorders: physical complications](https://www.nice.org.uk/guidance/cg100/chapter/recommendations)

**Location:** 1.1.1 acute withdrawal assessment/admission and warning against sudden reduction

**Used for:** Alcohol withdrawal safety boundary; no home detoxification protocol

**Access:** Public primary-source material; relevant sections inspected

### NICE_103

[NICE CG103, delirium](https://www.nice.org.uk/guidance/cg103/chapter/Recommendations)

**Location:** 1.3.1 and 1.6.1–1.6.3

**Used for:** Acute/fluctuating changes in attention/cognition need assessment; hospital/long-term-care guideline context

**Access:** Public primary-source material; relevant sections inspected

### PREDNISONE_LABEL

[DailyMed: predniSONE Tablets, USP; A-S Medication Solutions](https://www.dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=aaaa3460-0239-4203-857f-0ada303c2108&type=display)

**Location:** Precautions, Neuro-Psychiatric; set ID in URL

**Used for:** Example of an official psychiatric-effects warning, not an individual causation finding

**Access:** Public primary-source material; relevant sections inspected

### SAMET_2013

[Samet et al. (2013), independent and substance-induced major depression and remission/relapse](https://pubmed.ncbi.nlm.nih.gov/22775406/)

**Location:** Addiction 108(1):115–123; Abstract, Methods/Findings; DOI 10.1111/j.1360-0443.2012.04010.x

**Used for:** PRISM-based prospective research supports retaining independent/induced course distinctions

**Access:** Primary abstract inspected; free full text linked as PMC3767419. No PRISM questionnaire or scoring implemented.

### ABSTINENCE_2021

[Depressive symptoms in early alcohol or opioid abstinence: course & correlates (2021)](https://pubmed.ncbi.nlm.nih.gov/33983108/)

**Location:** Abstract, methods/results/conclusions

**Used for:** Example of change over early abstinence; cohort-specific, not a universal waiting rule

**Access:** Primary indexed abstract inspected; no full-text access or generalizability claim inferred.

### BETA_2021

[Riemer et al. (2021), Do beta-Blockers Cause Depression?](https://pubmed.ncbi.nlm.nih.gov/33719510/)

**Location:** Hypertension; DOI 10.1161/HYPERTENSIONAHA.120.16590; abstract/conclusion; linked 2022 correction PMID35138874

**Used for:** RCT meta-analysis challenges blanket beta-blocker causation assumptions

**Access:** Primary abstract and author-institution summary inspected; no effect sizes transcribed.

### ISOTRETINOIN_2024

[Tan et al. (2024), Risk of Suicide and Psychiatric Disorders Among Isotretinoin Users: A Meta-Analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC10687715/)

**Location:** JAMA Dermatology 160(1):54–62; Key Points, Results, Discussion/Limitations

**Used for:** Population findings versus individual assessment; avoid a causal medication blacklist

**Access:** Public primary-source material; relevant sections inspected
