# 08 — Unspecified depressive disorder: adult assessment knowledge

Version: 1.0.0-source-reviewed. Research date: 2 November 2026.

This package explains the category, information needed for assessment, differential boundaries and a proposed evidence-output contract. It contains no automated diagnostic classifier. Markdown is the readable clinical/design explanation; JSON holds the corresponding concepts, field definitions, controlled values and sources for later integration. Source review and mechanical checks are not clinical validation.

## 1. Meaning and clinical use

Unspecified depressive disorder concerns a predominant depressive presentation with clinically significant distress or impairment, without a more specific depressive category established for that presentation. A clinician does not specify the reason the requirements of a particular category are not met. The definition includes some settings with insufficient information for a more specific diagnosis, such as emergency assessments. Qualifying adjustment presentations must also be considered. [DSM_UNSPECIFIED, printed p.210]

This is a clinical diagnostic category, not a rule saying “the interview is unfinished, so the diagnosis is unspecified depression.” There still has to be a clinically meaningful depressive presentation and professional interpretation. The system must not use this label for a model error, missing duration, unanswered question, stopped conversation or low screening score. Those are information/workflow states, not diagnoses.

The clinical definition includes uncertainty; it does not require the AI to falsely certify that every alternative has been ruled out before a professional can ever use the category. Record what has and has not been assessed. A professional formulation may remain broad while appropriate further evaluation proceeds. Our prototype supplies evidence and questions for that review rather than independently assigning the diagnosis. [DSM_UNSPECIFIED]

## 2. Age and scope

Our implementation covers adults 18+, including older adults, without a fixed upper age cutoff. That is project scope, not a clinical minimum age for the category. Children/adolescents need a separately designed pathway. Adapt assessment to language, sensory, physical and cognitive needs; depression is not assumed to be normal ageing. A person's inability to use chat is not a symptom denial. [NIMH_DEP; VA_2022]

This package supports assessment and provisional explanations for professional review. It does not prescribe, independently diagnose other medical/psychiatric conditions, interpret clinical records as verified merely because they were mentioned, or claim an emergency-response service. Medical/substance causes and bipolar/psychotic presentations require relevant review even when the current depressive category is uncertain.

## 3. The category's information requirements

| Clinical issue | What must be understood | What must not be inferred |
|---|---|---|
| Depressive presentation | Actual mood/interest experiences and associated reported changes | A diagnostic label from the word “sad” alone |
| Predominance | What is most prominent in the clinical picture | That the last symptom mentioned is the primary disorder |
| Clinical burden | Distress OR impairment, with actual examples | That absence of visible disability means no distress |
| Specificity | What supports or remains unknown about more specific categories | That unasked criteria are absent |
| Adjustment alternatives | Stressors, timing, pattern and burden | That every stressor proves adjustment disorder |
| Non-specification | The professional does not state the particular reason | That the model should invent a reason |
| Insufficient-information context | What the assessment could and could not establish | That limited information alone establishes the diagnosis |

The manual does not supply a separate fixed symptom count or minimum number of days for this residual category. Do not manufacture a five-symptom/two-week rule for the category itself. Equally, the lack of a category-specific numerical rule does not mean any sadness qualifies or that symptom duration/breadth is unimportant. Those details help determine whether another explanation is more appropriate. [DSM_UNSPECIFIED]

There is no unique biological test, medication response, PHQ cutoff or characteristic symptom that independently confirms this category. Do not create a severity, recurrence or feature algorithm by copying every MDD specifier into it. Collect the actual features and leave classification to professional review. The output schema below deliberately contains patient evidence rather than a confirmed diagnosis.

## 4. Terms that must remain distinct

| Term | Meaning in this project |
|---|---|
| Unspecified depressive disorder | A clinical category in which a particular reason is not specified; insufficient-information presentations are included |
| Other specified depressive disorder | The clinician communicates the particular reason another depressive category's requirements are not met |
| Incomplete assessment | Application status describing missing information; not a diagnosis |
| MDD with unspecified severity/course | A descriptor within an MDD formulation; different from unspecified depressive disorder |
| Unspecified mood disorder | A separate category when choosing between bipolar and depressive classes is difficult; not a synonym |
| Reported/provisional diagnosis | Attribution or certainty of a formulation; not interchangeable with unspecified depressive disorder |

These diagnostic distinctions follow the manual; the application status is our design. Do not turn the plain-language phrase “depression, not sure which kind” into a verified clinical code. The code printed with the manual's category is not permission to auto-code a patient; jurisdiction/version and professional documentation require their own review. [DSM_UNSPECIFIED]

“Unspecified” also does not mean mild, harmless, fabricated, untreatable or guaranteed to become MDD later. The label alone does not tell us severity, safety needs, cause or prognosis. Improvement or later clarification may change the formulation, but it is not a promise of any particular diagnosis. Clinical help and review should address the actual presentation and burden, not wait for a more precise label.

## 5. Concepts, definitions, flexible evidence and follow-ups

There is no special symptom set unique to unspecified depression. These cards deliberately reuse the common depressive assessment domains and add reported-formulation, uncertainty and follow-up context. Clinical domains are sourced; JSON names, optional fields, controlled states and example wording are project designs, not a validated interview or a new clinical vocabulary. Field requirements vary by concept and by what the person actually reports.

### Depressed mood — `depressed_mood`

Reported low, sad or empty mood.

Sources: [VA_2022; NICE_222].

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

**Follow-up:** Meaning, persistence and episode timing if unclear.

**Interpretation limit:** A sad day alone does not establish the domain threshold or MDD.

### Interest and pleasure — `interest_pleasure`

Reduced desire for activities and/or reduced enjoyment.

Sources: [VA_2022; NICE_222].

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

**Follow-up:** Separate wanting from enjoying; establish breadth if relevant.

**Interpretation limit:** One retained hobby does not negate all symptoms; not doing an activity may reflect lack of opportunity.

### Appetite change — `appetite_change`

Change in desire for food.

Sources: [VA_2022; NICE_222].

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

**Follow-up:** Direction, persistence and appetite versus eating.

**Interpretation limit:** Do not infer weight change from appetite. No category-specific symptom count is established by this record.

### Weight change — `weight_change`

Reported change in body weight.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `direction` | Weight direction. | gain / loss / variable / unclear |
| `amount` | Amount with original units; no guessing. | Supported text; preserve actual timing, units and uncertainty |
| `interval` | Period over which weight changed. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_weight` | Earlier weight if supplied. | Supported text; preserve actual timing, units and uncertainty |
| `measurement` | Measured versus estimated account. | measured_report / estimate / unclear |
| `intentionality` | Whether intentional. | intentional / unintentional / mixed / unclear |

**Example question:** Have you noticed a change in your weight during this period?

**Follow-up:** Amount, interval and intentionality when relevant.

**Interpretation limit:** Do not calculate percentages without compatible reported measurements or infer appetite from weight alone.

### Sleep disturbance — `sleep_disturbance`

Difficulty sleeping or excessive sleep.

Sources: [VA_2022; NICE_222].

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

**Follow-up:** Identify complaint before asking subtype-specific details.

**Interpretation limit:** Insomnia while tired is not reduced sleep need; insufficient opportunity is not automatically insomnia.

### Psychomotor change — `psychomotor_change`

Noticeable motor/speech slowing or agitation.

Sources: [VA_2022; NICE_222].

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

**Follow-up:** Observable examples and reporter, rather than restlessness alone.

**Interpretation limit:** Text response speed and feeling restless alone do not establish observable psychomotor change.

### Energy and fatigue — `energy_fatigue`

Unusual tiredness or reduced energy.

Sources: [VA_2022; NICE_222].

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

**Follow-up:** Examples and timing; separate sleepiness if ambiguous.

**Interpretation limit:** Do not automatically attribute fatigue to depression or infer it from short sleep.

### Worthlessness and guilt — `worthlessness_guilt`

Low self-worth or excessive/inappropriate guilt.

Sources: [VA_2022; NICE_222].

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

**Follow-up:** Actual thought content; clarify without endorsing it.

**Interpretation limit:** Ordinary regret, low confidence and guilt about illness are not automatically qualifying guilt.

### Concentration and decisions — `cognition_decisions`

Reported thinking, attention or decision difficulty.

Sources: [VA_2022; NICE_222].

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

**Follow-up:** Task examples and change from baseline.

**Interpretation limit:** Do not label dementia, ADHD or depression from this alone.

### Death/suicide-related reports — `death_suicide`

Death-related thoughts, suicidal thoughts, plans or attempts.

Sources: [ASQ_BSSA; NICE_225].

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

**Follow-up:** Use dedicated safety pathway; preserve current versus historical information.

**Interpretation limit:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

### Episode timeline — `episode_timeline`

Period linking symptoms and changes.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `course` | Continuity, fluctuation or change over the relevant period. | Supported text; preserve actual timing, units and uncertainty |
| `overlap` | Whether symptoms occurred together. | Supported text; preserve actual timing, units and uncertainty |
| `intervals` | Earlier periods, recovery and residual symptoms. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** When did these changes begin?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text; preserve actual timing, units and uncertainty |
| `examples` | Concrete difficulty or distress. | Supported text; preserve actual timing, units and uncertainty |
| `baseline` | Usual functioning. | Supported text; preserve actual timing, units and uncertainty |
| `supports` | Assistance helping preserve functioning. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How have these changes affected your daily life?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Activation history — `activation_history`

Possible distinct elevated/overactive periods requiring review.

Sources: [NIMH_BIPOLAR; NICE_185].

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

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Medical context — `medical_context`

Relevant reported medical history and symptoms.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `conditions` | Reported conditions; distinguish reported diagnosis from confirmation. | Supported text; preserve actual timing, units and uncertainty |
| `timeline` | Relationship to symptoms. | Supported text; preserve actual timing, units and uncertainty |
| `investigations` | Results only if actually supplied. | Supported text; preserve actual timing, units and uncertainty |
| `clinician_review` | Known professional assessment or unresolved need. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Are there health conditions that might be relevant to these changes?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Medicines and substances — `exposure_context`

Relevant treatment/substance exposure account.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `name` | Named exposure. | Supported text; preserve actual timing, units and uncertainty |
| `dose_use` | Reported amount/use; never recommend a dose. | Supported text; preserve actual timing, units and uncertainty |
| `start_change_stop` | Timing of changes. | Supported text; preserve actual timing, units and uncertainty |
| `symptom_timing` | Reported temporal relationship. | Supported text; preserve actual timing, units and uncertainty |
| `source_kind` | Medicine, alcohol, other substance or unclear. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have any medicines or substance-use patterns changed around this time?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Psychotic experiences — `psychotic_experience`

Reported experiences requiring specialist interpretation.

Sources: [VA_2022; DSM_UNSPECIFIED].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `kind` | Experience as described, not an automatic diagnosis. | Supported text; preserve actual timing, units and uncertainty |
| `content` | Brief relevant content without affirming beliefs. | Supported text; preserve actual timing, units and uncertainty |
| `mood_relationship` | During versus outside mood episodes. | Supported text; preserve actual timing, units and uncertainty |
| `conviction_context` | Reported belief/context and uncertainty. | Supported text; preserve actual timing, units and uncertainty |
| `safety_concerns` | Any reported urgent implications. | Supported text; preserve actual timing, units and uncertainty |
| `reported_mood_congruence` | Professional mood-congruence description if actually supplied; do not invent it. | congruent / incongruent_or_mixed / unclear |

**Example question:** Have you had experiences that other people do not seem to share?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text; preserve actual timing, units and uncertainty |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text; preserve actual timing, units and uncertainty |
| `period` | When and for which symptoms. | Supported text; preserve actual timing, units and uncertainty |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text; preserve actual timing, units and uncertainty |
| `use` | Actual use and barriers as reported. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you received help for something similar before?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Family history — `family_history`

Relevant family mood/psychiatric history.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `relative` | Relationship, without unnecessary identifying details. | Supported text; preserve actual timing, units and uncertainty |
| `reported_condition` | Condition as reported. | Supported text; preserve actual timing, units and uncertainty |
| `certainty` | How the person knows; unknown remains unknown. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Is there relevant mental-health history in your family?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Life context — `life_context`

Relevant stress, loss, trauma and support.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `events` | Events relevant to symptom timeline. | Supported text; preserve actual timing, units and uncertainty |
| `timing` | Temporal relationship. | Supported text; preserve actual timing, units and uncertainty |
| `support` | Current supports. | Supported text; preserve actual timing, units and uncertainty |
| `barriers` | Practical barriers. | Supported text; preserve actual timing, units and uncertainty |
| `meaning` | Person's interpretation of the context. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Has anything important been happening around the time these changes began?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Stressors and adjustment-related alternatives — `stressor_adjustment_review`

Relation to identifiable stressors plus symptom pattern and course; an adjustment diagnosis needs its own review.

Sources: [DSM_UNSPECIFIED; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `stressor` | Actual event or continuing stressor. | Supported text; preserve actual timing, units and uncertainty |
| `timing` | Symptoms relative to the stressor. | Supported text; preserve actual timing, units and uncertainty |
| `meaning` | How the person understands the change. | Supported text; preserve actual timing, units and uncertainty |
| `course` | Persistence, recovery and burden. | Supported text; preserve actual timing, units and uncertainty |
| `other_explanations` | Mood, medical, treatment or other alternatives requiring review. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** What was happening in your life around the time this started?

**Follow-up:** Review adjustment-related possibilities without assuming any stressor determines the diagnosis.

**Interpretation limit:** The category definition excludes qualifying adjustment presentations; an ordinary stressful event does not by itself establish adjustment disorder.

### Symptoms between low periods — `between_period_course`

Whether symptoms remit, remain subthreshold or continue between apparently separate low spells.

Sources: [DSM_UNSPECIFIED; VA_2022].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `mood_between` | Actual mood between periods. | Supported text; preserve actual timing, units and uncertainty |
| `other_symptoms_between` | Residual or continuing symptoms, if reported. | Supported text; preserve actual timing, units and uncertainty |
| `return_to_baseline` | Whether usual function/experience returns, with concrete examples. | Supported text; preserve actual timing, units and uncertainty |
| `symptom_free_intervals` | Reported intervals and limitations; do not infer full remission. | Supported text; preserve actual timing, units and uncertainty |
| `longer_low_periods` | Periods that may actually meet another disorder's duration requirements. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How do you feel between those low spells?

**Follow-up:** Review ongoing background symptoms and lifetime MDD/PDD rather than treating every fluctuation as a new episode.

**Interpretation limit:** Feeling somewhat better is not necessarily symptom-free or formal remission.

### Lifetime threshold and previous diagnostic history — `lifetime_threshold_history`

Earlier mood, activation and psychotic experiences relevant to a more specific explanation.

Sources: [DSM_UNSPECIFIED; NIMH_BIPOLAR].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `previous_depressive_periods` | Earlier symptoms, duration and impact, not just diagnostic labels. | Supported text; preserve actual timing, units and uncertainty |
| `reported_diagnoses` | Reported professional diagnoses with certainty/attribution. | Supported text; preserve actual timing, units and uncertainty |
| `prior_full_episode_review` | Information suggesting prior full episodes or missing information about them. | Supported text; preserve actual timing, units and uncertainty |
| `activation_periods` | Reported elevated/overactive periods needing bipolar assessment. | Supported text; preserve actual timing, units and uncertainty |
| `psychotic_history` | Reported psychotic condition and current active/residual status, not chatbot confirmation. | Supported text; preserve actual timing, units and uncertainty |
| `uncertainty` | Incomplete history or unclear prior diagnosis. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you ever had a longer period like this, or received a mood or psychotic-disorder diagnosis?

**Follow-up:** Follow up an endorsed history rather than treating no remembered diagnosis as no lifetime disorder.

**Interpretation limit:** Never diagnosed does not mean no earlier disorder. A reported prior diagnosis is not independent confirmation.

### Anxiety alongside depressive symptoms — `anxiety_depression_overlap`

Actual anxiety and depressive experiences, kept separate from terminology in other classifications.

Sources: [DSM_UNSPECIFIED; NICE_222; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `anxiety_experiences` | Reported worries, tension, fear or other actual symptoms. | Supported text; preserve actual timing, units and uncertainty |
| `timing_overlap` | Relation to low mood periods. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Reported burden. | Supported text; preserve actual timing, units and uncertainty |
| `reported_formulation` | Any attributed professional explanation. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have anxiety or worries also been part of these periods?

**Follow-up:** Gather actual experiences and seek review of mixed presentations; do not invent another category.

**Interpretation limit:** Assess actual experiences; do not translate a mixed presentation automatically into a different classification or unspecified mood disorder.

### Current depressive presentation and burden — `presentation_description`

What the person means by feeling depressed or low, its predominant experiences and clinically relevant consequences.

Sources: [DSM_UNSPECIFIED; VA_2022].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `experience` | Actual feelings/changes, without assigning a diagnosis. | Supported text; preserve actual timing, units and uncertainty |
| `predominant_concern` | What is most prominent or troubling in the account, not proof of clinical predominance. | Supported text; preserve actual timing, units and uncertainty |
| `intensity_as_reported` | Severity in the person's words; no invented scale category. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_change` | Difference from usual experience/functioning. | Supported text; preserve actual timing, units and uncertainty |
| `duration_or_uncertainty` | Reported duration or inability to recall it. | Supported text; preserve actual timing, units and uncertainty |
| `burden` | Concrete distress, disability or interference; help from others may mask difficulties. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** What have you noticed, and how has it affected everyday life?

**Follow-up:** Understand the account before forcing it into symptom labels; retain unasked domains as unknown.

**Interpretation limit:** A self-label of depression, ordinary sadness or one questionnaire answer does not by itself establish a depressive disorder.

### Reported clinician diagnosis or formulation — `reported_clinical_formulation`

A diagnosis or explanation attributed to a professional, stored separately from current verified findings.

Sources: [DSM_UNSPECIFIED; VA_2022].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `label_as_reported` | The actual diagnostic term as reported; preserve uncertain wording. | Supported text; preserve actual timing, units and uncertainty |
| `professional` | Reported clinician/service, if identified. | Supported text; preserve actual timing, units and uncertainty |
| `assessment_time` | When the reported assessment occurred; not automatically the current episode. | Supported text; preserve actual timing, units and uncertainty |
| `context` | Circumstances of that assessment as reported. | Supported text; preserve actual timing, units and uncertainty |
| `reason_as_reported` | Any actual reason given; do not require or invent one for unspecified. | Supported text; preserve actual timing, units and uncertainty |
| `certainty` | Limits of recall or wording. | Supported text; preserve actual timing, units and uncertainty |
| `record_availability` | Whether original documentation is reportedly available; no independent verification implied. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Has a professional assessed this before, and what did they explain to you?

**Follow-up:** Distinguish a historical label, an actual current formulation and a patient's interpretation of the label.

**Interpretation limit:** Unspecified does not mean that a reason must be guessed, that the condition is mild, or that MDD is confirmed.

### Reported limits affecting assessment — `assessment_limit`

A reported limitation such as recall uncertainty, decline or difficulty communicating; not an absent symptom.

Sources: [NICE_222; VA_2022].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `target` | Specific question/domain that remains unclear. | Supported text; preserve actual timing, units and uncertainty |
| `reported_limit` | What the person reports is limiting the answer. | cannot_recall / does_not_understand / declines_for_now / communication_difficulty / conflicting_account / other_reported_limit |
| `partial_information` | What was actually supplied, without filling the rest. | Supported text; preserve actual timing, units and uncertainty |
| `help_requested` | Actual requested support, pacing or format relevant to assessment. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Would you like me to ask that another way, or leave it for now?

**Follow-up:** Respect the choice, preserve the unresolved target, and clarify later only when appropriate.

**Interpretation limit:** A refusal is not a denial, poor recall is not proof of a cognitive disorder, and missing information is not a confirmed residual diagnosis.

### Changes reported at reassessment — `followup_change_report`

New observations compared with an earlier period; diagnosis may need review as information changes.

Sources: [VA_2022; NICE_222].

| Optional detail | Meaning | Values/form |
|---|---|---|
| `comparison_period` | Earlier period being compared, only when identifiable. | Supported text; preserve actual timing, units and uncertainty |
| `symptom_change` | Reported improvement, worsening, persistence or fluctuation. | Supported text; preserve actual timing, units and uncertainty |
| `functional_change` | Actual change in daily functioning, not invented improvement. | Supported text; preserve actual timing, units and uncertainty |
| `new_information` | Newly remembered symptoms, dates, treatment or clinical findings. | Supported text; preserve actual timing, units and uncertainty |
| `intervening_events` | Actual changes in medical conditions, medicines, substances or life context. | Supported text; preserve actual timing, units and uncertainty |
| `professional_followup` | Reported follow-up arrangements, without implying that contact occurred. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Since we last discussed this, what has changed or become clearer?

**Follow-up:** Update supported details without overwriting history or treating improvement as proof of a diagnosis.

**Interpretation limit:** Do not convert new evidence into an independently confirmed MDD, bipolar or causal diagnosis.

## 6. What remains unknown, absent or in conflict?

The extractor must distinguish a reported symptom, a denial for a specific period, an unclear account, an unresolved contradiction and no information. These are information states, not severity levels. Unknown information does not satisfy or negate diagnostic requirements. A declined activation-history question does not establish that the person never had hypomania. No recalled diagnosis does not establish that a full depressive episode never occurred.

Every clinically useful fact volunteered in an answer should be considered, even if it was not the last question's target. “I don't know when it started, but I missed two shifts” provides uncertain timing and relevant impairment. Store both appropriately. Do not make the person repeat the work impact simply because the planner initially wanted duration. These extraction/history rules are project design informed by the need for comprehensive assessment.

Record approximations as approximations. “About six weeks” does not become an exact start date; an earlier inability to remember need not remain the active duration once the person provides a supported estimate. Preserve provenance and uncertainty. A genuine unresolved contradiction needs both accounts and review; an explicit correction should update the active interpretation without erasing history.

Not every clinician's use of the category means the information was missing. The definition also allows a clinician to choose not to state the reason. If a patient does not remember an explanation, that does not prove the clinician had no reason, assessed no alternatives or made an error. Keep the patient's account attributed and avoid inventing what happened in the appointment. [DSM_UNSPECIFIED]

## 7. Alternative pathways and clinically relevant history

| Pathway | Information needed | Boundary |
|---|---|---|
| MDD | Same-period mood/interest, associated symptoms, timing, burden, history and exclusions | A low count of extracted facts is not a low count of actual qualifying symptoms |
| PDD | Longstanding course, baseline and gaps | Current fluctuations may be part of chronic symptoms |
| PMDD/cycle pattern | Relevant menstrual context and full-cycle timing | Not assumed from gender or monthly recurrence |
| Substance/medication effects | Actual exposure, start/change/stop and mood chronology | Timing alone is not causation |
| Depression due to medical condition | Actual reported illness, findings and individual physiological relationship | Comorbidity alone is insufficient |
| Other specified depression | Known clinical reason for unmet requirements and example-specific history | Do not invent a specified reason from missing information |
| Bipolar spectrum | Lifetime elevation/activation, energy/activity and reduced sleep need | Unasked or declined activation history is not negative history |
| Psychotic/schizoaffective presentation | Actual experiences, diagnosis source and mood/psychosis timeline | Specialist interpretation; do not assume MDD or a residual category |
| Adjustment, grief or other contextual response | Stressor, loss, meaning, timing and symptom pattern | Stress or grief does not automatically determine or exclude a diagnosis |
| Anxiety or another predominant presentation | Actual symptoms, overlap, burden and course | Do not call every mixed account unspecified mood disorder |
| Cognitive/delirium or acute medical concern | Baseline and current changes, source and medical context | Appropriate medical assessment takes priority; chat cannot establish the cause |

The dedicated completed packages contain detailed depressive-category information. This module coordinates unresolved classification; it does not replace those requirements or implement full management of every alternative. Reported previous diagnoses need attribution, and earlier symptoms may need reassessment even when no one diagnosed them at the time. [DSM_UNSPECIFIED; VA_2022; NIMH_BIPOLAR]

NICE supports comprehensive assessment of symptoms, course, history, functioning and context rather than a count alone, including relevant mood elevation and physical/exposure history. We use those domains to select meaningful gaps. The guideline does not validate our exact conversation order, prescribe these JSON fields or establish an automatic unspecified-category algorithm. [NICE_222, 1.2.6–1.2.7]

## 8. Interview structure and follow-up policy

This is a semi-structured project policy, not a validated diagnostic instrument or the final cross-disorder graph. It aims to make uncertainty visible and collect useful information without forcing a conclusion. All stages remain subject to the person's participation, communication needs and immediate concerns.

1. **Safety and open account:** Attend to urgent concerns and invite the person's account without promising a diagnosis.
2. **Presentation and burden:** Clarify actual mood/interest experiences, associated symptoms, timing and daily consequences.
3. **History and alternatives:** Review prior mood/activation, relevant psychotic symptoms, medical/exposure and stressor context.
4. **Focused remaining gaps:** Ask the most useful unresolved target, using the whole conversation and respecting limits.
5. **Supported summary:** Summarize evidence, explicitly unknown items and review needs without a forced diagnostic conclusion.
6. **Professional reassessment:** Preserve new information and appropriate review arrangements; revise the evidence as it becomes clearer.


Before selecting the next question, inspect the transcript and existing records. Ask about an important remaining uncertainty, not an item already answered elsewhere. If mood, duration and impact are supplied together, retain all three. If information is only partial, ask about the missing part instead of repeating the original broad question. An answer can address several earlier targets.

Use context for short answers. If asked whether mood began around the start of term and the person says “yes, around then,” link the answer to that earlier question. Do not turn it into an endorsement of MDD or an exact date. If the reference is unclear, clarify it rather than guessing. Pronouns and historical references must remain attached to the correct person and period.

If the person answers a different but relevant issue, acknowledge and retain that information. Then gently return when useful: “That sounds difficult. To understand the timing, do you remember roughly how long this low feeling has been there?” Explain the purpose briefly. Unknown is a valid result. Respect “not now”; do not treat refusal as denial or keep reformulating until an answer is produced.

The conversational agent expresses a selected question naturally. The extractor preserves supported facts and context; the planner chooses a focused gap. An agent's empty plan, provider error, token limit or exhausted turn budget should produce an incomplete-run status, not a patient diagnosis. Diagnostic sufficiency and conversation termination are separate decisions. This is an implementation boundary that the later runtime must enforce.

The interview should end with a supported summary and review needs when appropriate, rather than continue indefinitely until every field is filled. Persistent uncertainty may justify professional review or a supported reassessment plan. Do not automatically demand every possible test or alternative-disorder interview before the person can receive help.

## 9. Measures, research and source hierarchy

PHQ-2/PHQ-9 are candidate screening/measurement tools within the shared pathway. The primary validation papers concern those tools under defined conditions; they do not validate our prompts, identify a cause or assign unspecified depressive disorder. A symptom score does not decide whether a clinician should specify a reason or whether bipolar/medical explanations have been assessed. No questionnaire responses are inferred or scored from the free-text examples here. [PHQ2_2003; PHQ9_2001]

The First and colleagues paper is a primary author account of DSM-5-TR's rationale and revisions, including diagnostic-boundary changes. It helps explain why residual depressive categories are not replacements for a qualifying adjustment presentation. It is not a new dataset, intervention trial or validation of an unspecified-depression interview. We use the manual for the category definition and guidelines for assessment domains, without implying an empirical benchmark result for our system. [DSM_OVERVIEW; DSM_UNSPECIFIED]

The official APA index and September 2025 supplement provide version context. The supplement revises adjacent other-specified examples; it is not presented as a new unspecified-category symptom list. The category definition used here is the inspected DSM-5-TR passage, with source locations recorded. Researching access does not grant permission to redistribute the manual or licensed interview items. [APA_UPDATE_INDEX; APA_2025]

No gold-standard interview, benchmark dataset, live-model run or diagnostic accuracy study was performed by creating this package. The schema and examples make the intended data behaviour reviewable; they cannot supply the clinical validity of an interview. We do not invent a paper or scoring method just to fill a research slot for this category.

## 10. Safety and appropriate review

An unspecified category or uncertain diagnosis is not evidence of low clinical need. Suicide-related concerns should be assessed and acted on through the agreed human-review pathway regardless of diagnostic specificity. Preserve current/historical thoughts and behaviours, reported intent, access, past behaviour and available support. Unmentioned safety information is unknown, and a pause/refusal does not establish safety. [ASQ_BSSA; NICE_225]

The NIMH adult brief safety-assessment guide is intended for trained clinicians after a positive ASQ screen, not evidence that our reworded chat is an ASQ service. NICE discourages predictive scales or global low/medium/high labels to determine suicide risk and care. Our handoff flags indicate a review need; they do not predict outcomes or prove an escalation was delivered. [ASQ_BSSA; NICE_225]

Distress, impairment and immediate concerns deserve attention while the diagnostic explanation remains uncertain. The planner must not tell a person to wait for a fixed symptom duration or a more specific label before seeking appropriate help. Medical deterioration, acute cognitive changes or other urgent concerns interrupt routine depressive-history collection. This package supplies no medication, withdrawal or emergency-treatment instructions.

## 11. Evidence contract and meaning of the output

| Shared item | Meaning |
|---|---|
| `module_id`, `schema_version` | Fixed contract identifiers |
| `concept_id` | Allowlisted information domain, not a confirmed condition |
| `episode_key` | Application-owned period key; does not prove a formal episode occurred |
| `subject` | Patient in this contract; no reassignment of someone else's symptoms |
| `finding_status` | Reported presence/absence, ambiguity or unresolved conflict |
| `temporal_status`, `time_reference` | Current/historical/unclear context and actual reported time wording |
| `attributes` | Optional, concept-specific details; different concepts have different fields |
| `evidence` | Exact patient quotation, source message, earlier context and supported fields |
| `uncertainty_notes` | Recall, chronology, attribution or interpretation limitations |
| `semantic_check_status` | Whether the interpretation appears supported or needs review; not guaranteed by JSON validation |
| `question_tracking` | Application target/status and remaining target; includes partial answers and declines |
| `safety_handoff` | Workflow review-need flag, reported concerns and unresolved questions; no proof of contact |

No LLM-generated evidence UUID is required. Code supplies message and period IDs. The active snapshot key is `(concept_id, episode_key, subject)`. New supported details update that record while retaining provenance; different periods remain separate. A historical reported formulation does not become the diagnosis for the current period.

Each known attribute needs a value and an evidence link. Unknown has no value. Not-applicable needs a reason and must not mean “not asked.” An omitted attribute is not an absent symptom. An assessment-limit record with reported presence means the limitation was reported; it does not mean the symptom targeted by the declined question was present or absent. These controlled states and JSON names are project design choices, not clinical diagnostic criteria.

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


Exact quotations must be substrings of patient messages. Context references must precede the answer they help interpret. A report that a clinician used a term remains patient testimony about the clinician; independently verified records need a separate provenance workflow. The evidence contract rejects a top-level diagnosis, billing code or automatic residual-classification field. Nevertheless, a valid JSON object may still contain a semantically unsupported interpretation; human review and targeted evaluation remain necessary.

## 12. Fictional example and expected interpretation

The authored fixture begins with low mood, exhaustion, missed work and uncertain onset. A later answer provides an approximate six-week duration. The person reports that a doctor used “unspecified depressive disorder” last year, without remembering the explanation, and then declines to discuss lifetime activation.

Expected behaviour: record current symptoms and work impact; update current duration from unknown to an approximate supported value; keep the reported historical label separate; preserve the declined target as unresolved; and avoid inventing absent activation, a specified reason or a current diagnosis. The past appointment's brevity does not prove what was assessed or why the category was used. Safety remains unassessed in the short fixture.

`examples.json` contains the full messages and first/later snapshots. These are authored examples, not actual LLM outputs, validated patient cases or evidence of agent accuracy. Mechanical tests assess the proposed contract and desired information handling. They cannot prove that an agent will reliably perform it.

## 13. What to hand to professional review

Provide the actual mood/interest and associated experiences, burden, duration and course; historical mood/activation and psychosis information; medical/exposure/stressor context; reported diagnoses with source/time; known limitations and declined questions; safety concerns and actual review status; and focused outstanding questions. Clearly distinguish what was not asked from what was denied and what is uncertain.

Example summary: “The person reports low mood and exhaustion for approximately six weeks with missed work. They report a historical unspecified-depression formulation. Lifetime activation history was declined and remains unresolved. The current assessment does not establish a specific diagnosis.” This is a fictional summary of available evidence, not a diagnostic conclusion.

If a clinician later supplies a formulation or additional evidence, preserve who said it, when and with what basis. Reassessment can change the working explanation; do not retain an old broad label as an immutable truth or automatically discard it because one detail became clearer. Clinical review determines how diagnoses are documented.

## 14. Files, checks and remaining work

- `knowledge.json`: common symptom and differential-assessment concepts, field meanings, value sets and local policy.
- `classification_reference.json`: definition, distinctions and explicitly disabled automatic shortcuts.
- `sources.json`: links, locations, use and access notes.
- `evidence_output.schema.json`: proposed patient-evidence contract.
- `examples.json`: fictional, history-aware snapshots.
- `validate_package.py` and `VALIDATION_REPORT.json`: mechanical checks and their results.

These checks cover schema, allowed fields/values, source references, quotations, prior context, duplicate keys and invalid examples. They are not clinical validation, semantic proof or a diagnostic benchmark. Existing agents/prompts are not changed or connected by creating this Desktop package. No API key, medical record or copyrighted manual is included.

This completes the planned **seven adult depressive-category reference packages**. It does not complete clinical review, all age/life-stage refinements, full alternative-disorder pathways, the shared question graph or runtime integration. The next joint stage is to review consistency across modules, then build and test role-specific knowledge access and conversation/extraction/planning behaviour. This module's reference content and proposed contract are ready for that review stage.

## 15. Source register: links, precise parts and contributions

Manuals define the category; guidance informs assessment; primary measurement/revision papers have their own limited roles. Published source requirements are distinguished from project wording, fields and sequencing. Page numbers distinguish printed pages from PDF-viewer pages; access to a public abstract is not assumed to include all tools or full-text rights.


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

### NICE_185

[NICE CG185, Bipolar disorder](https://www.nice.org.uk/guidance/cg185/chapter/recommendations)

**Location:** 1.2.1

**Used for:** Recognition/referral recommendation, not a four-day bipolar diagnostic shortcut

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

### APA_GRIEF

[APA, What Is Depression?](https://www.psychiatry.org/patients-families/depression/what-is-depression)

**Location:** Grief versus depression discussion

**Used for:** Loss context and possible coexistence

**Access:** Public primary-source material inspected

### DSM_UNSPECIFIED

[APA DSM-5-TR (2022), Unspecified Depressive Disorder](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders)

**Location:** Printed p.210 / inspected PDF viewer p.341; adjacent Other Specified Depressive Disorder pp.209–210 and Unspecified Mood Disorder p.210

**Used for:** Category definition, clinically significant burden, adjustment exclusions, non-specification and insufficient-information context; comparison with adjacent categories

**Access:** Original APA text inspected locally through previously obtained public psychiatry.ru mirror. Publisher chapter blocked. No redistribution permission inferred; book not bundled.

### APA_2025

[APA DSM-5-TR cumulative update, September 2025](https://www.psychiatry.org/getmedia/b68a5776-f88c-45c7-9535-fd219d7aa5cb/APA-DSM5TR-Update-September-2025.pdf)

**Location:** II.B, printed supplement p.7 / PDF viewer p.7; revised text read with visual revision marks

**Used for:** Version context and adjacent other-specified revisions; not claimed to supply a replacement definition for unspecified depressive disorder.

**Access:** Official page rendered and visually reviewed during 2 November audit. Red strikethrough is deleted text, not a retained criterion. Selected revisions only; supplement does not replace manual.

### APA_UPDATE_INDEX

[APA, Updates to DSM-5-TR Criteria and Text](https://www.psychiatry.org/psychiatrists/practice/dsm/updates-to-dsm/updates-to-dsm-5-tr-criteria-text/)

**Location:** September 2025 Updates and earlier-update list

**Used for:** Version verification; September 2025 is the latest update listed on the inspected page

**Access:** Official page inspected on the recorded research date; future changes require rechecking.

### DSM_OVERVIEW

[First et al., DSM-5-TR: Rationale, Process, and Overview of Changes](https://pubmed.ncbi.nlm.nih.gov/36510761/)

**Location:** Psychiatric Services 74(8):869–875 (2023); DOI 10.1176/appi.ps.20220334; online 13 December 2022; indexed author discussion of diagnostic changes

**Used for:** Primary account of manual revision; contextual distinction between residual depressive categories and qualifying adjustment presentations; not a validation of our agents

**Access:** Primary bibliographic record and indexed author article passages inspected; direct PubMed retrieval was incomplete. No full instrument or empirical accuracy result inferred.
