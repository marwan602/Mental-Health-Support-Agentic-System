# 06 — Depressive disorder due to another medical condition

Version: 1.0.0-source-reviewed. Research date: 2 November 2026.

This document explains the clinical information needed for an adult assessment, the evidence our agents should preserve and the limits of causal interpretation. The accompanying JSON represents these concepts and a proposed output contract. It is source-linked assessment knowledge, not an independently confirmed diagnosis, a medical work-up service or clinical validation of an AI interview.

## 1. Meaning, scope and age

This category concerns a depressive presentation judged to arise from the **direct physiological effects of a medical condition**. It is different from the broad observation that depression and a physical illness occur together. Establishing the medical condition and judging the physiological relationship require clinical evidence and professional interpretation. A distressing diagnosis can also be a psychological stressor, and treatment can have separate mood effects. These explanations must be considered rather than collapsed into one label. [DSM_MEDICAL]

Our implementation includes adults aged 18 and above, including older adults, without a fixed upper cutoff. Age 18 is the project's boundary, not a clinical minimum age for the disorder. Late recognition of depression, several medicines, cognitive symptoms or disability are reasons to understand the individual context, not automatic evidence of a particular cause. Depression is not treated as normal ageing. [NIMH_DEP; VA_2022]

The system's purpose is to collect and organize information for professional assessment. It does not diagnose thyroid disease, cancer, stroke or another physical illness from a conversation, interpret imaging independently, order investigations or prescribe treatment. Its questions should help identify what is reported, what is unknown and what needs professional review.

## 2. Criteria-information map

The following is a paraphrase of DSM-5-TR's information requirements, not reproduced diagnostic wording or an automatic checklist decision. [DSM_MEDICAL, printed pp.206–209]

| Domain | Information needed |
|---|---|
| A | Predominant, persistent depressed mood or marked reduction of interest/pleasure in all or almost all activities |
| B | History, examination or laboratory evidence supporting a direct physiological relationship to a medical condition |
| C | Whether another mental disorder better explains the presentation, including an adjustment response to illness |
| D | Whether symptoms occur exclusively during delirium |
| E | Clinically significant distress OR impairment in important functioning |

The base category does not universally require the full MDD symptom-count and duration threshold. That threshold matters for the **major depressive-like episode** specifier below. Do not equate having a physical diagnosis with meeting domain B, and do not treat an abnormal test as proof of the mood's cause. The clinician integrates the individual history, relevant findings and condition-specific literature. There is no infallible single attribution test. [DSM_MEDICAL]

## 3. This disorder's descriptive specifiers

These are descriptions within this category, not three new disorders. Our extractor collects the features; it does not select a confirmed specifier. [DSM_MEDICAL]

| Specifier | Meaning for our assessment |
|---|---|
| With depressive features | A depressive presentation that does not meet full major depressive episode criteria |
| With major depressive-like episode | Major depressive episode requirements are met except the episode exclusion concerning a physiological medical cause; this is not independent MDD |
| With mixed features | Manic/hypomanic symptoms also occur but do not dominate the clinical presentation |

The mixed description here must not be silently replaced by MDD's separate mixed-features algorithm. Clarify actual activation symptoms, their overlap, baseline change and medical/treatment context. Predominant mania or hypomania needs another diagnostic pathway. Do not automatically attach the entire set of MDD features, patterns or billing codes to this category. Professional coding also requires naming the medical condition correctly; coding automation is outside this package.

### Major depressive-like episode: what extra information is needed

Review at least five of nine symptom groups occurring within the same period of at least two weeks, including depressed mood or loss of interest/pleasure, with a change from previous functioning. The groups are mood; interest/pleasure; appetite/weight; sleep; psychomotor change; energy/fatigue; worthlessness/inappropriate guilt; concentration/decisions; and death/suicidal thoughts or behaviour. Appetite and weight share one group. The full episode's symptom-specific frequency, clinical significance and differential requirements still need review; its physiological-attribution exclusion is the stated exception for this specifier. [DSM_MEDICAL; VA_2022]

Many episode symptoms require most-day/nearly-every-day information, but do not impose one identical frequency question on every group: weight and death/suicide information have different forms, for example. The symptom cards preserve the relevant details. A `reported_present` field is not evidence that every threshold is met. The dedicated [MDD information guide](02_MDD_Assessment_Information_Requirements.md) explains the full episode requirements; here we reuse the episode description without concluding independent MDD or importing all MDD specifiers.

If the full episode requirements are not established, preserve what is missing. Do not automatically choose the depressive-features specifier from an incomplete interview, or treat unknown as evidence that a threshold was not met. Specifier selection belongs to professional review. [DSM_MEDICAL]

## 4. Three evidence layers kept separate

**Patient evidence:** what the person reports about symptoms, diagnoses, tests, treatment and clinicians' comments. A quote can support “the patient reports a diagnosis”; it cannot independently verify the diagnosis or its cause.

**Clinical reference knowledge:** what a manual, guideline or primary study says about a condition and possible depressive presentations. This belongs in a referenced knowledge file, not a fabricated patient statement.

**Professional attribution:** a clinical judgment integrating the actual medical evidence and alternatives. This is not generated automatically by matching an illness name to low mood. A reported clinician opinion remains attributed to its speaker until the appropriate workflow verifies it.

These boundaries are our implementation design. They preserve the difference between knowing a word, knowing an association and establishing what happened in an individual case.

## 5. Concept cards: definitions, output items and follow-ups

Every card below gives the meaning, optional concept-specific details, example question, follow-up focus and interpretation limits. Clinical domains are linked to sources. Field names, controlled values and conversational wording are project choices, not a validated interview or internationally standardized vocabulary. A field can be absent from a turn when nothing relevant was supplied. The extractor must not fill it merely to make a uniform output.

### Depressed mood — `depressed_mood`

Reported low, sad or empty mood.

Sources: [VA_2022; NICE_222; DSM_MEDICAL]. Role: primary_mood_domain.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience, without adding a diagnosis. | Supported text; preserve actual timing, units and uncertainty |
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `days_per_week` | Stated days affected; keep units and wording instead of imposing a diagnostic cutoff. | Supported text; preserve actual timing, units and uncertainty |
| `proportion_of_day` | Reported share of an affected day; most of the day is already useful. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How has your mood been during this period?

**Follow-up focus:** Meaning, persistence and episode timing if unclear.

**Do not infer:** A sad day alone does not establish the domain threshold or MDD.

### Interest and pleasure — `interest_pleasure`

Reduced desire for activities and/or reduced enjoyment.

Sources: [VA_2022; NICE_222; DSM_MEDICAL]. Role: primary_mood_domain.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `days_per_week` | Stated days affected; keep units and wording instead of imposing a diagnostic cutoff. | Supported text; preserve actual timing, units and uncertainty |
| `proportion_of_day` | Reported share of an affected day; most of the day is already useful. | Supported text; preserve actual timing, units and uncertainty |
| `interest` | Reported wanting or motivation to engage. | Supported text; preserve actual timing, units and uncertainty |
| `pleasure` | Enjoyment when engaged. | Supported text; preserve actual timing, units and uncertainty |
| `activities` | Affected activities and retained interests. | Supported text; preserve actual timing, units and uncertainty |
| `breadth` | How broadly activities are affected. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have your interest or enjoyment in your usual activities changed?

**Follow-up focus:** Separate wanting from enjoying; establish breadth if relevant.

**Do not infer:** One retained hobby does not negate all symptoms; not doing an activity may reflect lack of opportunity.

### Appetite change — `appetite_change`

Change in desire for food.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve actual timing, units and uncertainty |
| `direction` | Reported appetite direction. | increased / decreased / variable / unclear |
| `appetite_vs_intake` | Distinguish hunger/desire from actual eating. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Has your appetite changed compared with usual?

**Follow-up focus:** Direction, persistence and appetite versus eating.

**Do not infer:** Do not infer weight change from appetite. This is supporting symptom information, not a separate induced-disorder count threshold.

### Weight change — `weight_change`

Reported change in body weight.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `direction` | Weight direction. | gain / loss / variable / unclear |
| `amount` | Amount with original units; no guessing. | Supported text; preserve actual timing, units and uncertainty |
| `interval` | Period over which weight changed. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_weight` | Earlier weight if supplied. | Supported text; preserve actual timing, units and uncertainty |
| `measurement` | Measured versus estimated account. | measured_report / estimate / unclear |
| `intentionality` | Whether intentional. | intentional / unintentional / mixed / unclear |

**Example question:** Have you noticed a change in your weight during this period?

**Follow-up focus:** Amount, interval and intentionality when relevant.

**Do not infer:** Do not calculate a percentage without compatible stated weights/dates. Do not infer appetite change from weight alone.

### Sleep disturbance — `sleep_disturbance`

Difficulty sleeping or excessive sleep.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve actual timing, units and uncertainty |
| `pattern` | Reported sleep complaint. | onset_difficulty / maintenance_difficulty / early_waking / excessive_sleep / mixed / unclear |
| `latency` | Time taken to fall asleep. | Supported text; preserve actual timing, units and uncertainty |
| `awakenings` | Waking during sleep and return-to-sleep account. | Supported text; preserve actual timing, units and uncertainty |
| `wake_timing` | Actual versus intended/usual waking. | Supported text; preserve actual timing, units and uncertainty |
| `total_sleep` | Reported sleep hours with period. | Supported text; preserve actual timing, units and uncertainty |
| `sleep_opportunity` | Opportunity and external interruptions. | Supported text; preserve actual timing, units and uncertainty |
| `daytime_effect` | Sleepiness, exhaustion or other reported effects. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How has your sleep changed from what is usual for you?

**Follow-up focus:** Identify complaint before asking subtype-specific details.

**Do not infer:** Insomnia while tired is not reduced sleep need; insufficient opportunity is not automatically insomnia.

### Psychomotor change — `psychomotor_change`

Noticeable motor/speech slowing or agitation.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `direction` | Reported observable change. | slowing / agitation / both / unclear |
| `examples` | Concrete speech/movement behaviour. | Supported text; preserve actual timing, units and uncertainty |
| `observer` | Who noticed it; self-report about another observer remains patient report. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you or other people noticed changes in how quickly you move or speak?

**Follow-up focus:** Observable examples and reporter, rather than restlessness alone.

**Do not infer:** Text response speed and feeling restless alone do not establish observable psychomotor change.

### Energy and fatigue — `energy_fatigue`

Unusual tiredness or reduced energy.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve actual timing, units and uncertainty |
| `experience` | Fatigue, low energy or both. | Supported text; preserve actual timing, units and uncertainty |
| `sleepiness` | Reported sleepiness if distinguished. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How has your energy been compared with usual?

**Follow-up focus:** Examples and timing; separate sleepiness if ambiguous.

**Do not infer:** Do not automatically attribute fatigue to depression or infer it from short sleep.

### Worthlessness and guilt — `worthlessness_guilt`

Low self-worth or excessive/inappropriate guilt.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `content` | Actual self-evaluation or guilt account. | Supported text; preserve actual timing, units and uncertainty |
| `kind` | Reported experience. | worthlessness / guilt / both / unclear |
| `context` | What the thought concerns; retain uncertainty about proportionality. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How have you been thinking about yourself during this period?

**Follow-up focus:** Actual thought content; clarify without endorsing it.

**Do not infer:** Ordinary regret, low confidence and guilt about illness are not automatically qualifying guilt.

### Concentration and decisions — `cognition_decisions`

Reported thinking, attention or decision difficulty.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve actual timing, units and uncertainty |
| `kind` | Reported difficulty. | concentration / thinking / indecision / mixed / unclear |
| `tasks` | Concrete affected tasks. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have concentrating or making decisions become harder than usual?

**Follow-up focus:** Task examples and change from baseline.

**Do not infer:** Do not label dementia, ADHD or depression from this alone.

### Death/suicide-related reports — `death_suicide`

Death-related thoughts, suicidal thoughts, plans or attempts.

Sources: [ASQ_BSSA; NICE_225]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `experience` | Preserve distinctions. | death_thoughts / wish_not_alive / suicidal_thoughts / suicide_plan / suicide_attempt / unclear |
| `recency` | When last/current; do not infer resolution. | Supported text; preserve actual timing, units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve actual timing, units and uncertainty |
| `intent` | Intent as reported. | Supported text; preserve actual timing, units and uncertainty |
| `plan_present` | Whether a plan was explicitly reported or denied. | reported / denied / unclear |
| `access` | Access to means as reported, without generating procedural details. | Supported text; preserve actual timing, units and uncertainty |
| `past_behaviour` | Historical self-injury/attempt account, intent and timing. | Supported text; preserve actual timing, units and uncertainty |
| `support` | Available support as reported. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you had thoughts about ending your life?

**Follow-up focus:** Use dedicated safety pathway; preserve current versus historical information.

**Do not infer:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text; preserve actual timing, units and uncertainty |
| `examples` | Concrete difficulty or distress. | Supported text; preserve actual timing, units and uncertainty |
| `baseline` | Usual functioning. | Supported text; preserve actual timing, units and uncertainty |
| `supports` | Assistance helping preserve functioning. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How have these changes affected your daily life?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Activation history — `activation_history`

Possible distinct elevated/overactive periods requiring review.

Sources: [NIMH_BIPOLAR; DSM_MEDICAL]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `period` | Current/historical time. | Supported text; preserve actual timing, units and uncertainty |
| `mood` | Elevated, expansive or irritable mood as reported. | Supported text; preserve actual timing, units and uncertainty |
| `energy_activity` | Change in energy/activity. | Supported text; preserve actual timing, units and uncertainty |
| `sleep_need` | Sleep need and tiredness, not just sleep hours. | Supported text; preserve actual timing, units and uncertainty |
| `other_changes` | Associated speech, thoughts, confidence or risky behaviour. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | Duration of that period. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Consequences or other observers. | Supported text; preserve actual timing, units and uncertainty |
| `exposure_context` | Medicines/substances/medical context. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you had a distinct period of unusually increased energy or activity?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Psychotic experiences — `psychotic_experience`

Reported experiences requiring specialist interpretation.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `kind` | Experience as described, not an automatic diagnosis. | Supported text; preserve actual timing, units and uncertainty |
| `content` | Brief relevant content without affirming beliefs. | Supported text; preserve actual timing, units and uncertainty |
| `mood_relationship` | During versus outside mood episodes. | Supported text; preserve actual timing, units and uncertainty |
| `conviction_context` | Reported belief/context and uncertainty. | Supported text; preserve actual timing, units and uncertainty |
| `safety_concerns` | Any reported urgent implications. | Supported text; preserve actual timing, units and uncertainty |
| `reported_mood_congruence` | Professional mood-congruence description if actually supplied; do not invent it. | congruent / incongruent_or_mixed / unclear |

**Example question:** Have you had experiences that other people do not seem to share?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text; preserve actual timing, units and uncertainty |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text; preserve actual timing, units and uncertainty |
| `period` | When and for which symptoms. | Supported text; preserve actual timing, units and uncertainty |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text; preserve actual timing, units and uncertainty |
| `use` | Actual use and barriers as reported. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you received help for something similar before?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Family history — `family_history`

Relevant family mood/psychiatric history.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `relative` | Relationship, without unnecessary identifying details. | Supported text; preserve actual timing, units and uncertainty |
| `reported_condition` | Condition as reported. | Supported text; preserve actual timing, units and uncertainty |
| `certainty` | How the person knows; unknown remains unknown. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Is there relevant mental-health history in your family?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Life context — `life_context`

Relevant stress, loss, trauma and support.

Sources: [VA_2022; NICE_222]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `events` | Events relevant to symptom timeline. | Supported text; preserve actual timing, units and uncertainty |
| `timing` | Temporal relationship. | Supported text; preserve actual timing, units and uncertainty |
| `support` | Current supports. | Supported text; preserve actual timing, units and uncertainty |
| `barriers` | Practical barriers. | Supported text; preserve actual timing, units and uncertainty |
| `meaning` | Person's interpretation of the context. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Has anything important been happening around the time these changes began?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Overall depressive presentation — `syndrome_course`

Predominance, persistence and actual course of the depressive presentation.

Sources: [DSM_MEDICAL; VA_2022]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | Actual start of the mood change, including uncertain dates. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | Reported duration; no universal two-week requirement in this module. | Supported text; preserve actual timing, units and uncertainty |
| `course` | Continuous, fluctuating, improving or worsening course in the person's words. | Supported text; preserve actual timing, units and uncertainty |
| `predominance` | What is most troubling; professional review decides syndrome predominance. | Supported text; preserve actual timing, units and uncertainty |
| `related_symptoms` | Other simultaneous symptoms with their own source support. | Supported text; preserve actual timing, units and uncertainty |
| `clinical_attention` | Reported reason for seeking care or clinician concern. | Supported text; preserve actual timing, units and uncertainty |
| `intensity_as_reported` | Severity in the person's own words; not an invented scale score or automatically assigned clinical severity. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** When did this change in your mood first begin?

**Follow-up focus:** Clarify baseline, continuity and burden before collecting redundant details.

**Do not infer:** The base medical-condition category does not universally require a full major depressive episode; its major-depressive-like specifier does.

### Acute confusion and attention changes — `acute_cognitive_change`

Recent or fluctuating change in attention, awareness or thinking that requires medical assessment.

Sources: [DSM_MEDICAL; NICE_103]. Role: supporting_assessment.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `change` | What changed from baseline, as reported. | Supported text; preserve actual timing, units and uncertainty |
| `onset` | Hours/days versus longstanding pattern, if known. | Supported text; preserve actual timing, units and uncertainty |
| `fluctuation` | Changes over the day as described. | Supported text; preserve actual timing, units and uncertainty |
| `observer` | Patient or identified collateral observer. | Supported text; preserve actual timing, units and uncertainty |
| `medical_context` | Concurrent illness, exposure or withdrawal context. | Supported text; preserve actual timing, units and uncertainty |
| `review_status` | Reported assessment or unresolved need. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you or someone with you noticed any sudden change in confusion or ability to pay attention?

**Follow-up focus:** Use appropriate urgent clinical review when acute changes are reported; do not continue a diagnostic checklist.

**Do not infer:** Symptoms exclusively during delirium do not establish this depressive disorder; a neurocognitive disorder is not an automatic exclusion.

### Reported medical condition and diagnostic basis — `condition_identification`

What illness is reported and how its identification is known; patient report is distinct from verified medical documentation.

Sources: [DSM_MEDICAL; VA_2022]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `name_as_reported` | The medical condition or concern in the person's own account; do not supply a diagnosis from symptoms. | Supported text; preserve actual timing, units and uncertainty |
| `diagnosis_basis` | How the person describes its identification. | reported_clinician_diagnosis / reported_under_investigation / self_suspected / unclear |
| `diagnosing_professional` | Reported professional/service, if identified. | Supported text; preserve actual timing, units and uncertainty |
| `diagnosis_time` | When it was recognized or diagnosed, distinct from when physical symptoms began. | Supported text; preserve actual timing, units and uncertainty |
| `reported_subtype` | Clinically meaningful subtype/stage only when actually supplied. | Supported text; preserve actual timing, units and uncertainty |
| `records_available` | Whether clinical documents are reportedly available; not proof of verification. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you been diagnosed with a medical condition, or are any symptoms being investigated?

**Follow-up focus:** Identify the actual condition and source of the information; suspected disease stays suspected.

**Do not infer:** A reported physical diagnosis does not confirm it or establish that it caused depression.

### Medical illness chronology and course — `medical_condition_course`

Onset, recognition, changes and current state of each condition, kept distinct from mood chronology.

Sources: [DSM_MEDICAL; VA_2022]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `symptom_onset` | When physical/neurological symptoms began, including an uncertain period. | Supported text; preserve actual timing, units and uncertainty |
| `recognition_time` | When the condition was recognized; diagnosis may follow biological onset. | Supported text; preserve actual timing, units and uncertainty |
| `recent_change` | Reported worsening, improvement, acute event or stable period. | Supported text; preserve actual timing, units and uncertainty |
| `course` | Reported progression, recurrence or recovery; not a stage assigned by the agent. | Supported text; preserve actual timing, units and uncertainty |
| `current_burden` | Current physical/cognitive symptoms and practical consequences. | Supported text; preserve actual timing, units and uncertainty |
| `treatment_events` | Actual treatment start/change and timing, linked in narrative to the named condition. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** When did the physical symptoms begin, and what has changed since then?

**Follow-up focus:** Distinguish symptoms, diagnosis and treatment dates rather than treating them as the same event.

**Do not infer:** Mood before the diagnosis date does not automatically mean mood before the disease.

### Relationship of mood and medical course — `mood_medical_timing`

Reported timing of mood changes relative to illness onset, exacerbation, improvement or treatment.

Sources: [DSM_MEDICAL]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `relationship` | Chronology in the account; not a causal verdict. | mood_before_reported_illness_onset / mood_after_reported_illness_onset / mood_before_diagnosis_onset_uncertain / mood_changes_with_illness_course / no_clear_relationship / unclear |
| `mood_onset` | Actual reported start of mood change. | Supported text; preserve actual timing, units and uncertainty |
| `medical_event` | Specific illness event used for comparison. | Supported text; preserve actual timing, units and uncertainty |
| `interval` | Reported gap; do not invent dates or apply a fixed post-event window. | Supported text; preserve actual timing, units and uncertainty |
| `course_comparison` | Reported similarities/differences across improving or worsening periods. | Supported text; preserve actual timing, units and uncertainty |
| `patient_explanation` | The person's belief about the relationship, labelled as a belief. | Supported text; preserve actual timing, units and uncertainty |
| `uncertainty` | Uncertain disease onset, recall or competing events. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How did the timing of your mood change compare with the illness or its treatment?

**Follow-up focus:** Ask which event the person means; physiological onset may differ from diagnosis.

**Do not infer:** Temporal association, simultaneous improvement or a plausible story is not proof of a direct physiological cause.

### Reported examination and investigation findings — `reported_investigation`

What the patient says an examination, test or scan showed, with its limits and attributed interpretation.

Sources: [DSM_MEDICAL; VA_2022; NICE_145; NICE_239]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `investigation` | Name of the test/examination as reported. | Supported text; preserve actual timing, units and uncertainty |
| `reported_result` | Exact reported result or wording; preserve units and any uncertainty. | Supported text; preserve actual timing, units and uncertainty |
| `test_time` | When it was done relative to illness and mood changes. | Supported text; preserve actual timing, units and uncertainty |
| `reported_reference_range` | Reference range only if supplied; no invented cutoffs. | Supported text; preserve actual timing, units and uncertainty |
| `clinician_interpretation` | What a clinician reportedly said it means, attributed to them. | Supported text; preserve actual timing, units and uncertainty |
| `document_status` | Availability of original documentation. | not_available / reportedly_available_not_reviewed / unclear |
| `review_need` | What needs professional verification or explanation. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have any tests or examinations been done, and what did your clinician tell you about the results?

**Follow-up focus:** Separate the numerical result, reported interpretation and unresolved questions.

**Do not infer:** The transcript is not a verified lab record. An abnormal test alone does not establish depression or its cause.

### Reported professional view of the relationship — `reported_professional_opinion`

An explicitly attributed clinician statement about whether a medical condition could explain the mood presentation.

Sources: [DSM_MEDICAL; VA_2022]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `speaker` | Reported clinician/service, if known. | Supported text; preserve actual timing, units and uncertainty |
| `opinion` | What they reportedly said, preserving possibility versus certainty. | Supported text; preserve actual timing, units and uncertainty |
| `opinion_time` | When this assessment occurred. | Supported text; preserve actual timing, units and uncertainty |
| `reported_reasoning` | Reasoning or evidence the patient reports; no inferred mechanism. | Supported text; preserve actual timing, units and uncertainty |
| `review_plan` | Reported follow-up or uncertainty. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Has a clinician discussed whether the condition, its treatment or something else may be affecting your mood?

**Follow-up focus:** Ask what was said and what remains uncertain; do not upgrade it to independent verification.

**Do not infer:** A patient's account of a causal opinion remains attributed testimony, not the system's causal conclusion.

### Earlier depressive periods and baseline — `prior_depressive_course`

Lifetime mood information relevant to an independent depressive explanation, without using diagnosis date as disease onset.

Sources: [DSM_MEDICAL; VA_2022]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `earlier_period` | Specific earlier low mood or interest/pleasure change. | Supported text; preserve actual timing, units and uncertainty |
| `duration_course` | Reported duration, recurrence and recovery. | Supported text; preserve actual timing, units and uncertainty |
| `medical_context_then` | Known/suspected condition status at that time; unknown does not mean disease-free. | Supported text; preserve actual timing, units and uncertainty |
| `treatment_exposure_then` | Relevant medicines/substances then, if supplied. | Supported text; preserve actual timing, units and uncertainty |
| `previous_diagnosis` | Reported earlier mental-health diagnosis, not confirmation. | Supported text; preserve actual timing, units and uncertainty |
| `family_context` | Relevant family history if supplied, without treating its absence as a causal test. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have there been similar periods earlier in your life, and what was happening with your health then?

**Follow-up focus:** Keep historical and present periods separate; review relevant MDD/PDD history.

**Do not infer:** Previous depression is relevant but does not automatically exclude an additional current medical contribution.

### Treatment, medication and substance alternatives — `treatment_exposure_review`

Treatments for an illness may have their own mood effects, independently of the illness.

Sources: [DSM_MEDICAL; VA_2022; NICE_215]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `named_exposures` | Actual named medicines, nonprescribed products, supplements or substances; no assumed agent. | Supported text; preserve actual timing, units and uncertainty |
| `actual_use` | Reported dose/use, with units/strength only if known. | Supported text; preserve actual timing, units and uncertainty |
| `changes` | Starts, dose changes, missed doses, stopping or resumed use. | Supported text; preserve actual timing, units and uncertainty |
| `symptom_relationship` | Mood course relative to named treatment events. | Supported text; preserve actual timing, units and uncertainty |
| `other_changes` | Other treatments/life changes occurring at the same time. | Supported text; preserve actual timing, units and uncertainty |
| `professional_review` | Reported prescriber assessment or unresolved medication review need. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** What treatments or medicines were started or changed around the time your mood changed?

**Follow-up focus:** Use the substance/medication module for detailed agent-specific timelines when indicated.

**Do not infer:** Do not attribute the mood to the illness simply because the medicine was prescribed for it. Do not recommend stopping/restarting treatment to test causation.

### Symptoms with several possible explanations — `overlapping_symptoms`

Fatigue, sleep, appetite, movement or cognitive changes may reflect illness, treatment, depression or more than one factor.

Sources: [VA_2022; NICE_222]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `symptom` | Specific reported experience, not a causal label. | Supported text; preserve actual timing, units and uncertainty |
| `baseline` | What was usual before the relevant changes. | Supported text; preserve actual timing, units and uncertainty |
| `change` | Actual change from that baseline. | Supported text; preserve actual timing, units and uncertainty |
| `contexts` | When it occurs or is different; distinguish ability, opportunity, motivation and enjoyment. | Supported text; preserve actual timing, units and uncertainty |
| `patient_attribution` | Person's own explanation, labelled as theirs. | Supported text; preserve actual timing, units and uncertainty |
| `clinical_uncertainty` | Alternative explanations needing review. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Is this different from your usual experience with the physical condition?

**Follow-up focus:** Clarify the experience and its independent timing; preserve uncertainty.

**Do not infer:** Do not automatically include every physical symptom as depression, or discard it merely because there is a medical illness.

### Response to illness, loss and demoralization — `illness_related_distress`

Meaning, helplessness and emotional response to illness may need care without establishing a physiological depressive disorder.

Sources: [DSM_MEDICAL; NICE_222]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `stressors` | Actual illness-related losses, fears or changes. | Supported text; preserve actual timing, units and uncertainty |
| `emotional_experience` | Reported sadness, hopelessness, helplessness or wish to give up. | Supported text; preserve actual timing, units and uncertainty |
| `pleasure_preserved` | Activities still enjoyed, if explicitly described; not an exclusion by itself. | Supported text; preserve actual timing, units and uncertainty |
| `pervasiveness` | Whether feelings are tied to particular situations or broadly present, as reported. | Supported text; preserve actual timing, units and uncertainty |
| `support_needs` | Clinically relevant barriers/support needs and current care. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How has living with the condition affected how you feel about your life?

**Follow-up focus:** Explore meaning without implying that all distress is an expected or trivial reaction.

**Do not infer:** Do not diagnose adjustment disorder or demoralization solely because distress followed an illness. Preserved enjoyment alone does not rule out depression.

### Motivation, mood and involuntary expression — `motivation_emotional_expression`

Clinical clarification when reduced initiation or sudden crying/laughing may differ from sustained sadness or loss of pleasure.

Sources: [STROKE_DEFINITIONS]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `initiation` | Reported difficulty getting started or doing purposeful activities. | Supported text; preserve actual timing, units and uncertainty |
| `felt_mood` | How the person actually feels during the event. | Supported text; preserve actual timing, units and uncertainty |
| `enjoyment` | Reported pleasure when participating, distinct from initiation or motor capacity. | Supported text; preserve actual timing, units and uncertainty |
| `expression` | Reported crying/laughing or other outward expression. | Supported text; preserve actual timing, units and uncertainty |
| `event_duration` | How long an expressive event lasts. | Supported text; preserve actual timing, units and uncertainty |
| `control_triggers` | Reported control, triggers and whether expression matches felt emotion. | Supported text; preserve actual timing, units and uncertainty |
| `neurological_context` | Relevant reported neurological condition and professional review. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** When that happens, how do you feel inside, and does the crying or laughing match that feeling?

**Follow-up focus:** Ask only when the account raises this distinction; obtain specialist interpretation.

**Do not infer:** Do not label crying as depressed mood or reduced initiation as anhedonia without clarifying the experience.

### Communication, cognition and source limitations — `communication_assessment_context`

Requirements for an interpretable assessment; difficulty answering must not become a symptom denial.

Sources: [VA_2022; NICE_222; STROKE_2025]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `barrier` | Reported language, hearing, vision, speech, cognitive or fatigue-related barrier. | Supported text; preserve actual timing, units and uncertainty |
| `adaptation` | Actual support used or requested, such as a slower pace or accessible format. | Supported text; preserve actual timing, units and uncertainty |
| `understanding` | Reported uncertainty about understanding the question. | Supported text; preserve actual timing, units and uncertainty |
| `collateral_available` | Whether another informant/record might help through an authorized workflow. | Supported text; preserve actual timing, units and uncertainty |
| `assessment_limit` | Why an answer, tool or chat may not be interpretable. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Would a slower pace or another way of asking make this easier to answer?

**Follow-up focus:** Respect supported communication and capacity needs; seek an appropriate professional pathway when needed.

**Do not infer:** Aphasia, silence or difficulty using chat is not evidence that a symptom is absent. Patient and collateral accounts must retain separate provenance.

### Concurrent activation features for review — `concurrent_activation`

Possible manic/hypomanic symptoms alongside the depressive presentation; no automatic mixed-features label.

Sources: [DSM_MEDICAL; NIMH_BIPOLAR]. Role: medical_differential_information.

| Optional detail | Meaning | Values/form |
|---|---|---|
| `mood` | Reported unusual elevation/expansiveness or irritability. | Supported text; preserve actual timing, units and uncertainty |
| `energy_activity` | Change in purposeful activity/energy. | Supported text; preserve actual timing, units and uncertainty |
| `sleep_need` | Reduced need for sleep versus insomnia with fatigue. | Supported text; preserve actual timing, units and uncertainty |
| `speech_thoughts` | Reported speech/thought-speed changes. | Supported text; preserve actual timing, units and uncertainty |
| `other_changes` | Grandiosity, risky behaviour or other reported features. | Supported text; preserve actual timing, units and uncertainty |
| `overlap` | Timing relative to the depressive presentation and medical/treatment changes. | Supported text; preserve actual timing, units and uncertainty |
| `predominance` | Which presentation dominates as reported; professional interpretation required. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** During this low period, have there also been times of unusually increased energy or needing much less sleep?

**Follow-up focus:** Clarify one endorsed feature at a time; evaluate lifetime activation and treatment effects.

**Do not infer:** Do not copy the MDD mixed-features three-symptom algorithm onto this disorder's differently described specifier. Predominant mania needs a different pathway.

## 6. Which medical conditions are relevant?

The separate `medical_condition_reference.json` records illustrative conditions discussed in DSM-5-TR, with links to selected condition-specific guidance. The list is not exhaustive. Strength and applicability of causal evidence vary. Do not ask every patient a long checklist of these illnesses or infer them from common symptoms. [DSM_MEDICAL]

| Condition/group | Focus of our information collection |
|---|---|
| cerebrovascular disease or stroke | Neurological course, pre-event mood and separate physical/cognitive limitations; depression after stroke is not an automatic causal diagnosis. [DSM_MEDICAL; STROKE_2025] |
| traumatic brain injury or focal brain lesion | Reported injury/lesion and course, treatment and neurocognitive changes; no inference from lesion location by the chatbot. [DSM_MEDICAL] |
| parkinson disease | Motor/non-motor course and treatment; mood symptoms may precede recognition of the motor disorder. [DSM_MEDICAL; NICE_71] |
| huntington disease | Reported confirmed/suspected condition, neuropsychiatric course and specialist care; do not infer disease from depression/family clues. [DSM_MEDICAL] |
| hypothyroidism | Actual diagnosis/testing context; overt and subclinical presentations must not be merged. [DSM_MEDICAL; NICE_145; TRUST_2021] |
| cushing syndrome | Reported endocrine diagnosis and clinician findings; do not infer it from weight change or depression. [DSM_MEDICAL] |
| pancreatic cancer | A manual example of potential physiological association; mood symptoms do not justify a cancer diagnosis or universal cancer screening. [DSM_MEDICAL] |
| systemic lupus erythematosus | Medical activity, medicines and other explanations require individualized specialist review. [DSM_MEDICAL] |
| vitamin b12 deficiency | Possible psychiatric association; assess reported symptoms/risk context, not depression as a specific deficiency marker. [DSM_MEDICAL; NICE_239] |
| multiple sclerosis | An example of association with variable causal evidence; preserve illness, treatment and psychosocial alternatives. [DSM_MEDICAL] |


“Depression with cancer,” “post-stroke depression” and “depression with heart disease” are broad clinical descriptions. They do not, by those words alone, establish the direct physiological category. Even when a condition is a plausible physiological contributor, stress, disability, medication effects and independent depression may also be relevant. A medical condition not listed here can still need review; no list replaces the assessment. [DSM_MEDICAL]

### Selected guidance and what it adds

NICE NG145 says clinicians should **consider** thyroid testing in people with depression or unexplained anxiety. It also cautions that acute illness can affect results. This supports recording test context and asking about professional interpretation; it is not an instruction for the AI to order tests or diagnose hypothyroidism from tiredness. [NICE_145, 1.2.1–1.2.6]

NICE NG239 notes possible depression/anxiety/psychosis with B12 deficiency, nonspecific symptoms and context-dependent testing. Absence of anaemia alone does not exclude deficiency. These are medical-review considerations, not grounds to assume every depressed person has a deficiency or needs supplements. No thresholds or replacement regimen are implemented here. [NICE_239, 1.2.1–1.2.6]

NICE NG71 directs Parkinson-related depression care to the chronic-physical-health depression guideline. We use that referral link rather than inventing a Parkinson-specific causal test or adding a new diagnosis from slow movement. [NICE_71]

## 7. Timelines and causal interpretation

Keep four timelines distinct: the beginning of physical/neurological symptoms, recognition/diagnosis of the condition, treatment changes and the depressive presentation. They may overlap but are not interchangeable. The condition may have existed before it was recognized. Therefore “mood began before diagnosis” does not necessarily mean “mood began before the disease.” Mood symptoms may even precede conspicuous manifestations of some conditions. There is no universal fixed interval after illness onset that our planner should treat as diagnostic. [DSM_MEDICAL]

Collect baseline, onset, duration, persistence, symptom breadth and functional effects. A timeline that seems consistent with a physiological relationship is relevant but insufficient. Prior independent depressive periods, illness-independent fluctuations, treatment effects, psychosocial events and the quality of medical evidence must also be considered. Improvement near medical recovery can be informative without proving a mechanism, especially when several treatments changed together. Absence of family history or an unusual age/course must not become a rule that “proves medical causation.” [DSM_MEDICAL]

Separate the known from the unknown: if the person remembers the thyroid diagnosis date but not the date physical symptoms began, store the diagnosis date and preserve unknown onset. Do not manufacture a disease-free baseline. If two illnesses are present, keep each condition's course under its own reference rather than attaching all mood changes to the most recently named one. These are project provenance rules.

### Fictional examples of correct follow-up

- “I was diagnosed two weeks ago, but the low mood started six weeks ago.” Ask whether physical symptoms or investigations had begun earlier. Do not automatically exclude a medical contribution.
- “The doctor said the thyroid might be part of it.” Record the possible contribution as an attributed clinician opinion. Ask what review is planned; do not change “might” to “is.”
- “My joints stop me drawing, but I enjoy it when I can.” Record physical limitation and preserved enjoyment. Do not extract loss of pleasure solely from reduced activity.
- “It got better after treatment.” Ask what changed and when, including medicines or support. Do not treat improvement as a completed causal experiment.

## 8. Alternatives and coexistence

| Alternative/context | Information we need | Limit |
|---|---|---|
| Independent MDD or PDD | Prior mood periods, chronicity, recurrence and medical context then | Use the relevant disorder module; prior low mood alone is not a diagnosis |
| Substance/medication effect | Actual agent, use, changes and timing | Illness and its treatment can both be relevant; use the exposure module |
| Adjustment response | Illness as a stressor, symptom pattern, burden, pervasiveness and alternatives | Not every distressed response is adjustment disorder |
| Demoralization | Helplessness, meaning, desire to give up and actual enjoyment | Can overlap with depression; preserved pleasure alone does not rule out depression |
| Delirium | Acute/fluctuating attention, awareness and cognition | Exclusive delirium prevents this depressive diagnosis; acute clinical review takes priority |
| Major/mild neurocognitive disorder | Baseline cognition, course and source reliability | Does not automatically exclude a coexisting physiological depressive presentation |
| Apathy or involuntary emotional expression | Initiative, felt mood, enjoyment, triggers/control and event duration | Do not infer depressed mood from crying or anhedonia from reduced initiation |
| Bipolar/activation presentation | Lifetime and concurrent activation, sleep need, energy/activity and medical/treatment course | May require a different primary pathway |
| Physical symptom overlap | Fatigue, sleep, appetite, cognition and motor changes against baseline | Neither automatically count as depression nor discard because of physical illness |

The DSM differential discussion supports distinguishing the physiological category from an independent disorder, medication effects, delirium, neurocognitive presentations and psychological responses to illness. A medical diagnosis can coexist with an independent depressive disorder; not every possible explanation must be forced into one exclusive box by the extractor. [DSM_MEDICAL]

Canadian stroke definitions distinguish apathy and pseudobulbar affect from depression while allowing coexistence. Reduced motivation can occur independently; brief uncontrolled crying/laughing may not match inner mood. This supports asking what the person feels and experiences before interpreting outward behaviour. We do not diagnose these syndromes from text. The stroke definitions' abbreviated depressive threshold is not substituted for the DSM medical-condition category. [STROKE_DEFINITIONS]

## 9. Interview structure and question order

Our sequence is a **semi-structured project policy** informed by clinical domains and safety requirements. No source validates this exact agent sequence. It is not a MINI, SCID or other licensed interview. The final graph connecting all disorders is a later integration artifact; the local sequence below guides this module's information needs.

1. **Acute concerns:** Attend to current suicide-related or acute medical/cognitive concerns before ordinary assessment.
2. **Open presentation:** Understand what changed in mood, interest, baseline and functioning.
3. **Medical context:** Identify actual reported conditions, diagnostic basis and care team; clarify suspicion versus diagnosis.
4. **Parallel timelines:** Compare physical symptoms, diagnosis, treatment changes and mood onset as separate events.
5. **Targeted followup:** Clarify relevant symptom details already missing; review overlaps without assuming attribution.
6. **Alternative explanations:** Review past mood/activation, medication/substance effects, illness-related distress and cognitive changes.
7. **Source and review needs:** Identify reported investigations, accessible records and remaining professional interpretation needs.
8. **Summary handoff:** Summarize supported findings, unresolved causation, burdens, unanswered questions and actual review status.


After every answer: inspect the transcript, extract all supported relevant facts, update the correct concept/period/condition and identify the most useful unresolved target. The planner must not assume that only the last question can be answered. If a person provides duration and impact while answering an onset question, retain both and avoid repeating them.

Use follow-ups when an ambiguity changes interpretation: disease onset versus diagnosis; unable to perform versus unable to enjoy; actual test result versus suspected result; treatment effect versus illness course; short “yes” referring to an earlier question. Ask one manageable target at a time. Use a brief acknowledgement rather than repeatedly restating the same symptom before every question. These are application conversation rules.

If the reply is relevant but answers a different question, preserve the useful information and gently return to the missing target. Example: “That sounds exhausting. To understand the timing, do you remember whether the low mood started before or after those physical symptoms?” If the person does not know, record unknown. If they decline, acknowledge the choice and preserve the unresolved item. Do not pressure them until an answer appears.

If a new urgent concern arises, pause ordinary information collection and follow the implemented human/medical-review pathway. If the person is unable to use the format, stop treating lack of response as evidence and seek an appropriate supported assessment. Neither a token limit nor the end of a checklist establishes diagnostic sufficiency.

## 10. Communication and functional context

CG91 supports comprehensive assessment beyond counts, attention to function and duration, review of physical illness/medicines and adaptations for communication difficulties. It covers depression accompanying chronic physical illness generally; it does not by itself establish the causal disorder described here. Its older DSM-IV definitions are not used to overwrite current module requirements. [NICE_91, 1.1.1 and 1.3.1]

Canadian Stroke Best Practices recommends medically appropriate screening by trained professionals using validated tools and adaptations for communication challenges, followed by expert assessment when indicated. Our chat is not automatically suitable for aphasia or impaired communication. Record actual access needs and avoid equating inability to complete a verbal question with symptom absence. These recommendations support professional assessment access, not a claim that our reworded questions inherit screening validity. [STROKE_2025, 1.1]

This patient-evidence contract does not import collateral reports as direct patient quotations. If an authorized later workflow uses carers or clinical documents, keep source type, speaker, date and provenance separately. A patient's report that a relative observed something remains the patient's account of that observation. No carer/document verification service is implemented here.

## 11. Tests, measurements and research evidence

There is no single blood test, scan or biomarker that confirms this entire depressive diagnosis and causal attribution. Medical investigations address the suspected physical condition and alternatives; the clinician interprets them in context. The chatbot records reported findings and review needs. It must not generate a standard imaging/endocrine/cancer panel for everyone or use an isolated abnormality to assign the cause. [DSM_MEDICAL; VA_2022]

PHQ-2 and PHQ-9 can have a role in the shared depression screening/measurement pathway. Their validation studies concern the specified tools and populations, not physiological causal diagnosis. A score cannot determine whether thyroid disease, stroke, treatment or independent depression explains symptoms. Use verified versions and administration rather than inventing scores from narrative; a separate instrument workflow still needs to be implemented. [PHQ2_2003; PHQ9_2001]

The Wildisen/TRUST ancillary randomized study examined depressive symptom scores after levothyroxine versus placebo in adults aged 65+ with **subclinical** hypothyroidism. It found no benefit for depressive symptom scores at 12 months in its studied population. Baseline symptom scores were generally low, and the findings do not establish the result for younger people, overt hypothyroidism or people with substantial depression. We use this study to avoid treating all thyroid abnormalities as equivalent or promising mood recovery from thyroid treatment. It supplies no training dataset, clinical rule or treatment recommendation for our agents. [TRUST_2021]

No LLM benchmark, diagnostic accuracy study or live patient experiment has been run for this package. Fictional examples and schema tests assess the proposed contract, not inherited performance from the cited research.

## 12. Safety and medical-review boundaries

Suicide-related concerns require their own assessment and support pathway regardless of possible medical cause. Preserve current versus historical thoughts/behaviours, reported intent, access, past behaviour and available support. Unmentioned items are unknown. Do not assume that treating a physical condition eliminates immediate distress or the need for assessment. [ASQ_BSSA; NICE_225]

The NIMH adult brief safety-assessment guide is for trained clinicians after a positive ASQ screen; citing it does not validate our agent. NICE advises against predictive scales or global low/medium/high stratification to predict suicide or determine care. Our output flags concern/review status rather than numerical prediction. [ASQ_BSSA; NICE_225]

Acute confusion and fluctuation in attention/cognition can require medical assessment; do not absorb them into a depression symptom list or continue routine questioning as if they were ordinary poor concentration. NICE CG103's specific recommendations are grounded in hospital/long-term-care settings; we use the acute-change boundary without claiming a validated chat delirium screen. [NICE_103]

The system does not direct people to stop, restart or change medicines to distinguish causes. Treatment and withdrawal decisions require the responsible clinician. No medication doses, endocrine correction regimen, detoxification protocol or deliberate rechallenge is included. [NICE_215]

## 13. Output contract and meaning of each shared field

| Field | Meaning |
|---|---|
| `module_id`, `schema_version` | Fixed contract identifiers |
| `conditions` | Application registry of named reported conditions/concerns, each linked to patient text |
| `condition_ref` | Which reported condition this record concerns; null for unassigned or non-condition-specific facts. It does not assert causation |
| `concept_id` | Allowlisted concept card |
| `episode_key` | Code-supplied period key; not proof that a formal depressive episode occurred |
| `subject` | Patient in this contract; third-party symptoms are not reassigned to the patient |
| `finding_status` | Reported present/absent, unclear or conflicting; not diagnostic confirmation |
| `temporal_status` | Current, historical or unclear time context |
| `time_reference` | Actual reported time wording, or null when absent |
| `attributes` | Optional fields allowed for that particular concept |
| `evidence` | Exact patient quote, source message, earlier context messages and supported claims |
| `uncertainty_notes` | Recall, inconsistency, attribution or other limitations |
| `semantic_check_status` | Meaning appears supported versus needs review; JSON validation cannot establish this automatically |
| `question_tracking` | Question target/status and remaining target; supports partial answers and declines |
| `safety_handoff` | Reported concerns, unresolved questions and review-need flag; no proof of professional contact |

The application assigns condition references and message/period identifiers. The model does not invent evidence UUIDs. Patient-facing conversation never needs to display these identifiers. The unique snapshot key is `(concept_id, episode_key, subject, condition_ref)`. New supported details update that record while preserving earlier evidence; different conditions or periods remain separate. A registry entry itself does not mean a clinically confirmed condition.

Each known attribute has a value and an evidence link. Unknown has no value. Not-applicable requires a reason and must not stand for “not asked.” An omitted field is not a normal finding or symptom denial. The following controlled values are project definitions, not clinical severity categories:


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


### Context, correction and sourcing examples

“Yes” can support a finding only when the earlier question/context identifies what was affirmed. Reference those earlier messages; do not reference the answer itself as its own earlier context. The actual source quotation stays the patient's exact words even if interpretation uses context. The validator enforces exact substrings and earlier-message order, but not semantic truth.

“Actually it began before I was diagnosed” updates chronology. Retain source history and the correction; unresolved contradiction gets a conflict status, notes and review. Do not combine current low mood and a period five years earlier into one continuous duration. Do not copy one condition's timing into another condition unless the person explicitly links them.

The `reported_investigation.document_status` values describe availability, not verification. Patient text cannot establish an independently reviewed document. A verified EHR/laboratory import and clinician attribution record require separate provenance contracts in a future integration. An empty or partial test history must not make the planner conclude the person has no medical cause.

Reference-file facts and patient evidence must remain separate. The schema deliberately rejects a free-form confirmed diagnosis or cause property in the extractor output. Schema validity still cannot prevent a semantically incorrect allowed value: clinical review and extraction evaluation remain necessary.

## 14. Fictional example: expected behaviour

`examples.json` contains a short fictional transcript plus first/later snapshots. It illustrates current low mood, a reported hypothyroidism diagnosis, arthritis, an ambiguous disease-onset date, preserved enjoyment despite physical difficulty drawing, a recent prednisone exposure, a cautious reported clinician opinion and an earlier low period with unknown thyroid status.

Expected behaviour: distinguish the two conditions; preserve current and historical periods; resolve the contextual “yes”; retain unknown biological onset; do not infer anhedonia from physical limitation; record the treatment alternative without attributing causation; and preserve “might contribute” as uncertainty. No definitive MDD, physiological depressive disorder, adjustment disorder or medication-induced diagnosis is established. Safety remains unassessed in this limited fixture.

The snapshots are authored examples, not live LLM outputs or evidence that the agents already perform these tasks. The schema and validator make the desired storage/output behaviour concrete for subsequent implementation.

## 15. What the professional summary should contain

Summarize the main depressive experiences, timing, breadth, burden and relevant associated symptoms. Include reported medical conditions with their diagnostic basis, separate illness/diagnosis/treatment/mood timelines, attributed test findings and professional opinions, prior mood/activation periods, treatment exposures, alternative explanations, communication limitations and unresolved questions. Include safety concerns and the actual status of any review, without implying delivery that has not occurred.

Use language matching the evidence: “The person reports hypothyroidism and low mood; the onset of the thyroid problem is uncertain, and a physiological relationship requires professional review.” Do not substitute “depression caused by hypothyroidism” merely because both are in the record. A professional may ultimately support that interpretation, but the patient's interview data and source list alone are not the whole clinical assessment.

## 16. Files, verification and remaining work

- `knowledge.json`: clinical information map, three descriptive specifiers, concept-specific fields, controlled values and local assessment policy.
- `sources.json`: sources with links, exact parts used, access notes and date checked.
- `medical_condition_reference.json`: illustrative medical contexts and professional-attribution review fields; not a causal classifier.
- `evidence_output.schema.json`: patient-evidence output contract.
- `examples.json`: fictional context-aware multi-condition snapshots.
- `validate_package.py`: mechanical validation and invalid-case checks.
- `VALIDATION_REPORT.json`: actual results and their scope.

Mechanical checks cover schema structure, allowed fields/values, source references, exact quotations, context order, condition references, duplicate keys and deliberately invalid examples. They cannot validate clinical causation, prove symptom interpretation, guarantee completeness for every illness or establish the performance of an LLM.

Qualified clinical review, agent integration, the cross-disorder question graph and evaluation on diverse fictional cases remain pending. This package does not change the existing runtime or agent prompts. It does not include copyrighted manuals, licensed interview content, clinical records or API credentials. We have completed this module's reference content and proposed evidence contract for the next review/integration stage, with the remaining boundaries stated explicitly.

## 17. Source register: links, locations and exact contribution

Printed and PDF-viewer page numbers are labelled separately. Clinical manuals, practice guidelines and primary empirical research serve different roles. Some public guidance concerns depression accompanying illness generally rather than proving this particular causal disorder; that distinction is maintained throughout.


### VA_2022

[VA/DoD MDD Clinical Practice Guideline, 2022](https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/MH/mdd/VADODMDDCPGFinal508.pdf)

**Location:** p.19 Sidebars 1–2; pp.140–141 Appendix K; Appendix I pp.127–131

**Used for:** Episode foundation, work-up and measurement context; sidebar is abbreviated DSM-5-era material

**Access:** Public primary-source material inspected

### NICE_222

[NICE NG222, Depression in adults](https://www.nice.org.uk/guidance/ng222/chapter/Recommendations)

**Location:** 1.2.1–1.2.9; Definitions of depression/severity; 1.12.1

**Used for:** Comprehensive assessment, communication, safety and specialist review

**Access:** Official search-indexed recommendation extracts inspected; direct retrieval intermittently 403

### NIMH_DEP

[NIMH, Depression](https://www.nimh.nih.gov/health/publications/depression)

**Location:** Signs/symptoms; diagnosis; age-presentation paragraphs

**Used for:** Plain-language symptom domains and adult context

**Access:** Public primary-source material inspected

### NIMH_BIPOLAR

[NIMH, Bipolar Disorder](https://www.nimh.nih.gov/health/publications/bipolar-disorder)

**Location:** Types; symptom comparison; diagnosis

**Used for:** Activation history, reduced sleep need and bipolar uncertainty

**Access:** Public primary-source material inspected

### ASQ_BSSA

[NIMH Adult Outpatient Brief Suicide Safety Assessment Guide](https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials/adult-outpatient/adult-outpatient-brief-suicide-safety-assessment-guide)

**Location:** Intended users; thoughts, plan, past behaviour, supports and disposition sections

**Used for:** Safety information domains; clinician guide following positive ASQ, not autonomous LLM validation

**Access:** Public primary-source material inspected

### NICE_225

[NICE NG225, Self-harm](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)

**Location:** 1.6.1–1.6.6

**Used for:** No predictive low/medium/high stratification; needs-focused assessment

**Access:** Public primary-source material inspected

### PHQ9_2001

[Kroenke et al., 2001, PHQ-9 validity](https://pmc.ncbi.nlm.nih.gov/articles/PMC1495268/)

**Location:** Abstract; Methods; diagnostic-status comparison

**Used for:** Original validation of symptom/severity measure versus independent interview

**Access:** Public primary-source material inspected

### PHQ2_2003

[Kroenke et al., 2003, PHQ-2 validity](https://pubmed.ncbi.nlm.nih.gov/14583691/)

**Location:** Abstract, Methods and Results

**Used for:** Two-week screen, scoring range and screening threshold; abstract only

**Access:** Primary-study abstract inspected; full paper not accessed

### NICE_103

[NICE CG103, delirium](https://www.nice.org.uk/guidance/cg103/chapter/Recommendations)

**Location:** 1.3.1 and 1.6.1–1.6.3

**Used for:** Acute/fluctuating changes in attention/cognition need assessment; hospital/long-term-care guideline context

**Access:** Public primary-source material; relevant sections inspected

### NICE_215

[NICE NG215, medicines associated with dependence or withdrawal symptoms](https://www.nice.org.uk/guidance/ng215/chapter/Recommendations)

**Location:** 1.5.6; 1.5.15–1.5.17

**Used for:** Withdrawal assessment and prescriber review; no abrupt-stop experiments

**Access:** Public primary-source material; relevant sections inspected

### DSM_MEDICAL

[APA DSM-5-TR (2022), Depressive Disorder Due to Another Medical Condition](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders)

**Location:** Printed pp.206–209; inspected PDF viewer pp.336–340. Major depressive episode reference: MDD criteria in same chapter.

**Used for:** Criteria A–E, three descriptive specifiers, attribution, medical examples, course and differential

**Access:** Original APA text inspected locally through previously obtained public psychiatry.ru mirror. Publisher full text blocked; licensing/redistribution rights not inferred. No manual bundled.

### NICE_91

[NICE CG91, Depression in adults with a chronic physical health problem](https://www.nice.org.uk/guidance/cg91/chapter/Recommendations)

**Location:** 1.1.1.1–1.1.1.2; 1.3.1.3–1.3.1.5; 1.3.2

**Used for:** Assessment alongside physical illness, function, medicine review and communication; not a causal diagnostic standard

**Access:** Official indexed recommendations inspected; direct page returned 403. Older guideline uses DSM-IV definitions: these are not substituted for DSM-5-TR criteria.

### NICE_145

[NICE NG145, Thyroid disease: assessment and management](https://www.nice.org.uk/guidance/ng145/chapter/Recommendations)

**Location:** 1.2.1–1.2.6; particularly 1.2.3 and 1.2.6

**Used for:** Clinician consideration of thyroid tests with depression and caution about acute illness affecting results

**Access:** Public primary-source recommendations/indexed extracts inspected

### NICE_239

[NICE NG239, Vitamin B12 deficiency in over 16s (2024)](https://www.nice.org.uk/guidance/ng239/chapter/recommendations)

**Location:** 1.2.1–1.2.6; symptom/risk-factor boxes

**Used for:** Possible mental-health associations, nonspecific symptoms and context-based testing

**Access:** Public primary-source recommendations/indexed extracts inspected

### NICE_71

[NICE NG71, Parkinson's disease in adults](https://www.nice.org.uk/guidance/ng71/chapter/Recommendations)

**Location:** Non-motor symptoms: Depression

**Used for:** Parkinson depression assessment links to CG91; not proof of individual causal attribution

**Access:** Public primary-source recommendations/indexed extracts inspected

### STROKE_2025

[Heart & Stroke, Canadian Stroke Best Practices, 7th edition update 2025, Part Three](https://www.strokebestpractices.ca/recommendations/activity-participation-following-stroke/1-mood-and-depression)

**Location:** 1.0 and 1.1, especially communication-accessible screening and expert assessment; PDF p.13 onward

**Used for:** Trained-professional screening, timely diagnostic review and communication adaptations

**Access:** Official recommendation text/indexed PDF inspected. No screening instrument reproduced or validated for this system.

### STROKE_DEFINITIONS

[Canadian Stroke Best Practices, Part Three: Definitions and Descriptions](https://www.strokebestpractices.ca/recommendations/activity-participation-following-stroke/definitions-and-descriptions)

**Location:** Apathy; Pseudobulbar Affect following stroke

**Used for:** Differentiate motivation and involuntary emotional expression from sustained depressive mood

**Access:** Official definitions inspected. Its abbreviated depression threshold is not used to override DSM-5-TR medical-condition specifiers.

### TRUST_2021

[Wildisen et al. (2021), Effect of Levothyroxine Therapy on the Development of Depressive Symptoms in Older Adults With Subclinical Hypothyroidism](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2776099)

**Location:** JAMA Network Open 4(2):e2036645; Methods, Results, Strengths and Limitations; DOI 10.1001/jamanetworkopen.2020.36645; PMID33566107

**Used for:** Primary randomized ancillary study illustrating subgroup-specific evidence and limits of causal/treatment assumptions

**Access:** Open-access primary article/indexed full text and PubMed abstract inspected. GDS-15 responses/scoring not implemented.
