# 07 — Other specified depressive disorder: adult assessment knowledge

Version: 1.0.1-source-reviewed. Research date: 2 November 2026. Revised after visual source audit.

This package explains the category, named example presentations, information to collect, concept-specific evidence output and remaining professional-review questions. It is assessment knowledge and a proposed data contract, not a validated interview or automatic diagnostic classifier. Markdown is the readable explanation; JSON contains the corresponding concepts, fields, values and references for later integration.

## 1. What this category means

Other specified depressive disorder is used when a clinically significant depressive presentation does not meet another depressive category's full requirements and a clinician communicates the specific reason. Relevant adjustment presentations must also be considered. The category is not an automatic label for ordinary sadness, every low screening score or an incomplete conversation. Distress **or** impairment can establish the burden requirement; both are not mandatory. [DSM_OTHER]

“Specified” means a reason is stated by the clinician. It does not mean the extractor should invent one when information is missing. For example, only extracting three symptoms does not establish that the person has only three qualifying symptoms. A category-level judgment requires adequate assessment of what is present, absent, uncertain and explained by alternatives. [DSM_OTHER]

Our project covers adults 18 and above, including older adults with no upper cutoff. That is our implementation boundary, not a claim that the clinical category begins at 18. Adapt communication and physical/cognitive context to the person; do not interpret late-life low mood as normal ageing. [NIMH_DEP; VA_2022]

## 2. Category, examples, severity and uncertainty

The manual supplies **examples**, not a complete closed list of peer disorders. The four named examples below remain within other specified depressive disorder. They are not MDD specifiers. Do not assume that every presentation in this category is mild or short-lived; substantial burden and safety concerns still require attention. [DSM_OTHER; MAIER_1994]

“Subthreshold,” “minor depression,” “subsyndromal depression,” “residual symptoms” and “other specified” are not interchangeable diagnostic labels. A person with established MDD who now has fewer symptoms may need a course/remission assessment of MDD rather than reassignment to a never-had-another-disorder example. Lifetime review is therefore essential. [DSM_OTHER; VA_2022]

Other specified differs from **unspecified depressive disorder**, where the clinician does not state the specific reason, including some settings with insufficient information. Neither category is a code the application should automatically issue when a conversation stops. We will build the unspecified category separately. [DSM_OTHER, adjacent category text]

## 3. Source/version decisions

The foundation is the 2022 DSM-5-TR text, read together with the official September 2025 supplement. The inspected APA update index lists September 2025 as its latest posted update. Two example names now use “depressive-like.” This naming signals resemblance with an unmet requirement; it does not create a new validated screening method. [DSM_OTHER; APA_2025; APA_UPDATE_INDEX]

The supplement retains a four-day inconsistency: the short-duration heading includes four days, while the body requires longer than four days. We record that conflict and do not implement an automatic decision for exactly four days. Visual audit confirms that two other clauses are deleted, not retained: example 2's former recurrent-brief-depression exclusion and example 3's former mixed-anxiety/depressive exclusion. The active reference excludes those deleted clauses. [APA_2025, II.B]

These limitations belong in the knowledge itself so a model cannot claim a precision the inspected source does not provide. The output preserves the person's exact duration and actual anxiety symptoms even when classification needs clarification.

## 4. The four named examples

### 4.1 Recurrent brief depression

The reference pattern includes depressed mood plus at least four other depressive symptoms occurring together for 2–13 days, at least monthly for at least 12 consecutive months. It is not associated with the menstrual cycle. The named example excludes a lifetime presentation meeting another depressive/bipolar disorder and a current active/residual psychotic disorder. The category's clinical-burden requirements still apply. [DSM_OTHER]

Information needed: an individual spell's boundaries; actual co-occurring symptom domains and within-spell frequency; recurrence across every relevant month; exceptions/uncertain months; symptoms between spells; menstrual relationship when applicable; lifetime longer/chronic depression and activation; psychotic history; medical/exposure/stressor explanations; burden and safety.

Twelve selected spells are not proof of twelve consecutive symptomatic months. “Every few weeks” and “most months” require clarification. A three-day low period with only sleep difficulty and poor concentration does not establish the required symptom pattern. A month-like recurrence interval does not prove a menstrual relationship. Do not apply the PMDD pattern merely because spells recur monthly.

### 4.2 Short-duration depressive-like episodes

This example concerns depressed affect with at least four other major-episode symptom domains and significant burden, with insufficient duration for a full major depressive episode. Review the published short-duration range and unresolved exact-four-day boundary. Lifetime other depressive/bipolar history and current active/residual psychotic conditions remain relevant exclusions. The 2025 revision removes the former recurrent-brief-depression exclusion; recurrence information remains useful without applying that deleted rule. [DSM_OTHER; APA_2025]

Information needed: actual start/end or ongoing status, duration, same-period symptom overlap, degree of burden, recurrence pattern and lifetime/alternative explanations. A period that is still ongoing may later reach a longer duration; do not predetermine its final length. A single short episode is different from a recurring pattern across a year. We store information rather than infer that an example applies from duration alone.

### 4.3 Depressive-like episode with insufficient symptoms

The reference example describes depressed affect with at least one other major-episode symptom domain for at least two weeks and clinically significant burden, without full criteria for another depressive category. The first-three-examples lifetime and current-psychotic exclusions still matter. The 2025 revision deletes the former mixed-anxiety/depressive exclusion; anxiety remains clinically relevant but that deleted clause must not be used as a diagnostic gate. [DSM_OTHER; APA_2025]

Do not convert this into a rigid “exactly two symptoms” rule: at least one additional symptom is a minimum, while the overall category requires that another full disorder is not met. Do not substitute loss of interest alone for the depressed-affect requirement of this named example. That example-specific requirement must not be generalized to every possible other-specified presentation.

Information needed: mood, each supported associated symptom, adequate review of missing domains, two-week-or-longer course, burden, lifetime depression/bipolar history, psychosis context, anxiety experiences and other explanations. An unasked symptom is not absent; a count of extracted records is not a count of qualifying criteria.

### 4.4 Major depressive episode superimposed on specified psychotic disorders

This example concerns a full major depressive episode superimposed on schizophrenia, schizophreniform disorder, delusional disorder, or another specified/unspecified schizophrenia-spectrum or other psychotic disorder. A major depressive episode within schizoaffective disorder does **not** merit an additional other-specified depressive diagnosis. This is a specialist differential assessment, not a catch-all for any unusual thought or perception. [DSM_OTHER]

This fourth example is why the current-psychosis exclusion from examples 1–3 cannot be applied to the entire category. Need: reported psychotic diagnosis and source; actual mood episode requirements; timing of psychosis during and outside mood periods; overall course; medicines/substances/medical context; safety; and specialist formulation. Our agents must not diagnose schizophrenia or schizoaffective disorder from a short chat.

### Full major depressive episode reference

A full episode requires at least five of nine symptom groups within the same two-week period, including depressed mood or interest/pleasure loss, with a change from baseline and the appropriate frequency, burden and exclusion review. The nine groups are mood; interest/pleasure; appetite/weight; sleep; psychomotor change; energy; worthlessness/guilt; concentration/decisions; and death/suicidal thoughts or behaviour. Appetite/weight share a group. Individual symptom thresholds and causal/psychotic context need professional interpretation. [VA_2022; DSM_OTHER]

Use the [MDD information guide](02_MDD_Assessment_Information_Requirements.md) for the detailed episode domains. Do not count every alternative word as a separate group, combine symptoms from different periods, assume all physical symptoms are psychiatric, or assume a patient-reported presence satisfies every criterion.

## 5. Concept cards and evidence requirements

Clinical domains are sourced; identifiers, optional field names, controlled values, examples and priorities are project designs. The symptom cards preserve an MDD group reference where useful, without automatically counting criterion satisfaction. Other cards organize course, lifetime exclusions and unresolved information. Not every concept needs the same fields.

### Depressed mood — `depressed_mood`

Reported low, sad or empty mood.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** A sad day alone does not establish the domain threshold or MDD.

### Interest and pleasure — `interest_pleasure`

Reduced desire for activities and/or reduced enjoyment.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** One retained hobby does not negate all symptoms; not doing an activity may reflect lack of opportunity.

### Appetite change — `appetite_change`

Change in desire for food.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** Do not invent weight change from appetite; shares one count group with weight.

### Weight change — `weight_change`

Reported change in body weight.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `direction` | Weight direction. | gain / loss / variable / unclear |
| `amount` | Amount with original units; no guessing. | Supported text; preserve actual timing, units and uncertainty |
| `interval` | Period over which weight changed. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_weight` | Earlier weight if supplied. | Supported text; preserve actual timing, units and uncertainty |
| `measurement` | Measured versus estimated account. | measured_report / estimate / unclear |
| `intentionality` | Whether intentional. | intentional / unintentional / mixed / unclear |

**Example question:** Have you noticed a change in your weight during this period?

**Follow-up focus:** Amount, interval and intentionality when relevant.

**Interpretation limit:** No automatic percent calculation without compatible stated weights and dates; never double-count appetite.

### Sleep disturbance — `sleep_disturbance`

Difficulty sleeping or excessive sleep.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** Insomnia while tired is not reduced sleep need; insufficient opportunity is not automatically insomnia.

### Psychomotor change — `psychomotor_change`

Noticeable motor/speech slowing or agitation.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** Text response speed and feeling restless alone do not establish observable psychomotor change.

### Energy and fatigue — `energy_fatigue`

Unusual tiredness or reduced energy.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** Do not automatically attribute fatigue to depression or infer it from short sleep.

### Worthlessness and guilt — `worthlessness_guilt`

Low self-worth or excessive/inappropriate guilt.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** Ordinary regret, low confidence and guilt about illness are not automatically qualifying guilt.

### Concentration and decisions — `cognition_decisions`

Reported thinking, attention or decision difficulty.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** Do not label dementia, ADHD or depression from this alone.

### Death/suicide-related reports — `death_suicide`

Death-related thoughts, suicidal thoughts, plans or attempts.

Sources: [ASQ_BSSA; NICE_225].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

### Episode timeline — `episode_timeline`

Period linking symptoms and changes.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve actual timing, units and uncertainty |
| `course` | Continuity, fluctuation or change over the relevant period. | Supported text; preserve actual timing, units and uncertainty |
| `overlap` | Whether symptoms occurred together. | Supported text; preserve actual timing, units and uncertainty |
| `intervals` | Earlier periods, recovery and residual symptoms. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** When did these changes begin?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text; preserve actual timing, units and uncertainty |
| `examples` | Concrete difficulty or distress. | Supported text; preserve actual timing, units and uncertainty |
| `baseline` | Usual functioning. | Supported text; preserve actual timing, units and uncertainty |
| `supports` | Assistance helping preserve functioning. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How have these changes affected your daily life?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Activation history — `activation_history`

Possible distinct elevated/overactive periods requiring review.

Sources: [NIMH_BIPOLAR; NICE_185; DSM_OTHER].

| Optional field | Meaning | Values/form |
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

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Medical context — `medical_context`

Relevant reported medical history and symptoms.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `conditions` | Reported conditions; distinguish reported diagnosis from confirmation. | Supported text; preserve actual timing, units and uncertainty |
| `timeline` | Relationship to symptoms. | Supported text; preserve actual timing, units and uncertainty |
| `investigations` | Results only if actually supplied. | Supported text; preserve actual timing, units and uncertainty |
| `clinician_review` | Known professional assessment or unresolved need. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Are there health conditions that might be relevant to these changes?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Medicines and substances — `exposure_context`

Relevant treatment/substance exposure account.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `name` | Named exposure. | Supported text; preserve actual timing, units and uncertainty |
| `dose_use` | Reported amount/use; never recommend a dose. | Supported text; preserve actual timing, units and uncertainty |
| `start_change_stop` | Timing of changes. | Supported text; preserve actual timing, units and uncertainty |
| `symptom_timing` | Reported temporal relationship. | Supported text; preserve actual timing, units and uncertainty |
| `source_kind` | Medicine, alcohol, other substance or unclear. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have any medicines or substance-use patterns changed around this time?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Psychotic experiences — `psychotic_experience`

Reported experiences requiring specialist interpretation.

Sources: [DSM_OTHER; VA_2022].

| Optional field | Meaning | Values/form |
|---|---|---|
| `kind` | Experience as described, not an automatic diagnosis. | Supported text; preserve actual timing, units and uncertainty |
| `content` | Brief relevant content without affirming beliefs. | Supported text; preserve actual timing, units and uncertainty |
| `mood_relationship` | During versus outside mood episodes. | Supported text; preserve actual timing, units and uncertainty |
| `conviction_context` | Reported belief/context and uncertainty. | Supported text; preserve actual timing, units and uncertainty |
| `safety_concerns` | Any reported urgent implications. | Supported text; preserve actual timing, units and uncertainty |
| `reported_mood_congruence` | Professional mood-congruence description if actually supplied; do not invent it. | congruent / incongruent_or_mixed / unclear |

**Example question:** Have you had experiences that other people do not seem to share?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text; preserve actual timing, units and uncertainty |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text; preserve actual timing, units and uncertainty |
| `period` | When and for which symptoms. | Supported text; preserve actual timing, units and uncertainty |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text; preserve actual timing, units and uncertainty |
| `use` | Actual use and barriers as reported. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you received help for something similar before?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Family history — `family_history`

Relevant family mood/psychiatric history.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `relative` | Relationship, without unnecessary identifying details. | Supported text; preserve actual timing, units and uncertainty |
| `reported_condition` | Condition as reported. | Supported text; preserve actual timing, units and uncertainty |
| `certainty` | How the person knows; unknown remains unknown. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Is there relevant mental-health history in your family?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Life context — `life_context`

Relevant stress, loss, trauma and support.

Sources: [VA_2022; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `events` | Events relevant to symptom timeline. | Supported text; preserve actual timing, units and uncertainty |
| `timing` | Temporal relationship. | Supported text; preserve actual timing, units and uncertainty |
| `support` | Current supports. | Supported text; preserve actual timing, units and uncertainty |
| `barriers` | Practical barriers. | Supported text; preserve actual timing, units and uncertainty |
| `meaning` | Person's interpretation of the context. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Has anything important been happening around the time these changes began?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Interpretation limit:** A contextual association is not a confirmed causal explanation.

### Individual brief depressive period — `brief_period_details`

One reported period, with actual boundaries and simultaneous symptoms; brevity alone does not establish a disorder.

Sources: [DSM_OTHER].

| Optional field | Meaning | Values/form |
|---|---|---|
| `start` | Reported beginning, including uncertainty. | Supported text; preserve actual timing, units and uncertainty |
| `end_or_ongoing` | Reported ending or whether still continuing. | Supported text; preserve actual timing, units and uncertainty |
| `duration` | Reported duration in its actual units; not guessed from the next interview date. | Supported text; preserve actual timing, units and uncertainty |
| `depressed_affect` | Reported low mood specifically; interest loss alone must not silently replace it in these named examples. | Supported text; preserve actual timing, units and uncertainty |
| `cooccurring_symptoms` | Symptoms actually present in the same period, each needing its own supporting detail. | Supported text; preserve actual timing, units and uncertainty |
| `within_period_frequency` | How often and how much of the day symptoms occurred during this period. | Supported text; preserve actual timing, units and uncertainty |
| `baseline_change` | Difference from usual functioning/experience. | Supported text; preserve actual timing, units and uncertainty |
| `recall_limit` | Unclear boundaries or uncertainty. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Could you describe one recent low period, from when it began until it ended?

**Follow-up focus:** Clarify actual duration and overlap; an ongoing brief period may later last longer.

**Interpretation limit:** Do not count symptoms from different episodes together or diagnose from duration alone.

### Recurrence across months — `recurrence_pattern`

Pattern of distinct low periods over an observation interval, separate from an individual period's duration.

Sources: [DSM_OTHER; ANGST_1990].

| Optional field | Meaning | Values/form |
|---|---|---|
| `observation_interval` | Calendar span described, not merely number of episodes. | Supported text; preserve actual timing, units and uncertainty |
| `episodes_per_month` | Reported recurrence within months; preserve uncertainty and variable frequency. | Supported text; preserve actual timing, units and uncertainty |
| `consecutive_months` | Whether every month is covered, not only the number of selected symptomatic months. | Supported text; preserve actual timing, units and uncertainty |
| `exceptions` | Months without episodes, uncertain recall or longer episodes. | Supported text; preserve actual timing, units and uncertainty |
| `period_variability` | Differences in duration or symptoms across reported periods. | Supported text; preserve actual timing, units and uncertainty |
| `source_of_pattern` | Recall, contemporaneous records or other identified source; no implied verification. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Over what period has this been happening, and have there been months without a low spell?

**Follow-up focus:** Clarify continuous month coverage rather than assuming 12 episodes means 12 consecutive months.

**Interpretation limit:** A few short episodes do not establish recurrent brief depression; unclear months remain unclear.

### Symptoms between low periods — `between_period_course`

Whether symptoms remit, remain subthreshold or continue between apparently separate low spells.

Sources: [DSM_OTHER; VA_2022].

| Optional field | Meaning | Values/form |
|---|---|---|
| `mood_between` | Actual mood between periods. | Supported text; preserve actual timing, units and uncertainty |
| `other_symptoms_between` | Residual or continuing symptoms, if reported. | Supported text; preserve actual timing, units and uncertainty |
| `return_to_baseline` | Whether usual function/experience returns, with concrete examples. | Supported text; preserve actual timing, units and uncertainty |
| `symptom_free_intervals` | Reported intervals and limitations; do not infer full remission. | Supported text; preserve actual timing, units and uncertainty |
| `longer_low_periods` | Periods that may actually meet another disorder's duration requirements. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** How do you feel between those low spells?

**Follow-up focus:** Review ongoing background symptoms and lifetime MDD/PDD rather than treating every fluctuation as a new episode.

**Interpretation limit:** Feeling somewhat better is not necessarily symptom-free or formal remission.

### Lifetime threshold and previous diagnostic history — `lifetime_threshold_history`

Earlier depressive, bipolar and psychotic presentations relevant to example-specific exclusions.

Sources: [DSM_OTHER; NIMH_BIPOLAR].

| Optional field | Meaning | Values/form |
|---|---|---|
| `previous_depressive_periods` | Earlier symptoms, duration and impact, not just diagnostic labels. | Supported text; preserve actual timing, units and uncertainty |
| `reported_diagnoses` | Reported professional diagnoses with certainty/attribution. | Supported text; preserve actual timing, units and uncertainty |
| `prior_full_episode_review` | Information suggesting prior full episodes or missing information about them. | Supported text; preserve actual timing, units and uncertainty |
| `activation_periods` | Reported elevated/overactive periods needing bipolar assessment. | Supported text; preserve actual timing, units and uncertainty |
| `psychotic_history` | Reported psychotic condition and current active/residual status, not chatbot confirmation. | Supported text; preserve actual timing, units and uncertainty |
| `uncertainty` | Incomplete history or unclear prior diagnosis. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have you ever had a longer period like this, or received a mood or psychotic-disorder diagnosis?

**Follow-up focus:** Follow up an endorsed history rather than treating no remembered diagnosis as no lifetime disorder.

**Interpretation limit:** Examples 1–3 have lifetime/history exclusions; they cannot be inferred satisfied from an opening interview.

### Menstrual-cycle relationship when relevant — `menstrual_relationship`

Whether brief recurring mood periods are linked to a menstrual cycle, without assuming applicability.

Sources: [DSM_OTHER].

| Optional field | Meaning | Values/form |
|---|---|---|
| `applicability` | Relevant reported menstrual context. | menstrual_context_reported / no_relevant_cycle_reported / unclear |
| `relationship` | Reported linkage or absence of linkage; unasked is unknown. | Supported text; preserve actual timing, units and uncertainty |
| `timing` | Onset/improvement relative to bleeding and rest-of-cycle symptoms as actually described. | Supported text; preserve actual timing, units and uncertainty |
| `tracking` | Actual records or recall limits. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** If relevant to you, have you noticed whether these spells are linked to your menstrual cycle?

**Follow-up focus:** Use the PMDD module if a cycle relationship is reported; do not infer from monthly timing alone.

**Interpretation limit:** Recurrent brief depression's named example is not menstrual-associated; no relationship must not be invented.

### Stressors and adjustment-related alternatives — `stressor_adjustment_review`

Relation to identifiable stressors plus symptom pattern and course; an adjustment diagnosis needs its own review.

Sources: [DSM_OTHER; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `stressor` | Actual event or continuing stressor. | Supported text; preserve actual timing, units and uncertainty |
| `timing` | Symptoms relative to the stressor. | Supported text; preserve actual timing, units and uncertainty |
| `meaning` | How the person understands the change. | Supported text; preserve actual timing, units and uncertainty |
| `course` | Persistence, recovery and burden. | Supported text; preserve actual timing, units and uncertainty |
| `other_explanations` | Mood, medical, treatment or other alternatives requiring review. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** What was happening in your life around the time this started?

**Follow-up focus:** Review adjustment-related possibilities without assuming any stressor determines the diagnosis.

**Interpretation limit:** The category definition excludes qualifying adjustment presentations; an ordinary stressful event does not by itself establish adjustment disorder.

### Mood episode alongside a reported psychotic disorder — `psychosis_mood_relationship`

Specialist timeline information for the fourth named example, which differs from the first three.

Sources: [DSM_OTHER].

| Optional field | Meaning | Values/form |
|---|---|---|
| `reported_condition` | Named psychotic disorder and diagnostic source as reported. | Supported text; preserve actual timing, units and uncertainty |
| `psychosis_timeline` | Reported psychotic symptoms during and outside mood periods. | Supported text; preserve actual timing, units and uncertainty |
| `mood_timeline` | Actual full-episode information or gaps; no assumed major depressive episode. | Supported text; preserve actual timing, units and uncertainty |
| `overlap` | Temporal overlap of the two presentations. | Supported text; preserve actual timing, units and uncertainty |
| `reported_schizoaffective_review` | Any reported specialist formulation, with uncertainty. | Supported text; preserve actual timing, units and uncertainty |
| `specialist_care` | Current service and unmet review needs. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have those experiences also happened when your mood was not low?

**Follow-up focus:** Collect a careful timeline only as appropriate and route interpretation to specialist review.

**Interpretation limit:** The fourth example is not the first-three-examples psychosis exclusion applied universally; an episode within schizoaffective disorder does not merit this extra label.

### Anxiety alongside depressive symptoms — `anxiety_depression_overlap`

Actual anxiety and depressive experiences, kept separate from terminology in other classifications.

Sources: [DSM_OTHER; APA_2025; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `anxiety_experiences` | Reported worries, tension, fear or other actual symptoms. | Supported text; preserve actual timing, units and uncertainty |
| `timing_overlap` | Relation to low mood periods. | Supported text; preserve actual timing, units and uncertainty |
| `impact` | Reported burden. | Supported text; preserve actual timing, units and uncertainty |
| `reported_formulation` | Any attributed professional explanation. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Have anxiety or worries also been part of these periods?

**Follow-up focus:** Gather actual experiences and seek review of mixed presentations; do not invent another category.

**Interpretation limit:** Anxiety may coexist; the former example-3 anxiety/depression exclusion was deleted by the 2025 revision. Do not invent a DSM category from an ICD label.

### Reported professional explanation of an unmet requirement — `reported_diagnostic_reason`

A clinician's stated reason for an other-specified formulation, if reported; not a diagnosis generated by the extractor.

Sources: [DSM_OTHER].

| Optional field | Meaning | Values/form |
|---|---|---|
| `speaker` | Reported clinician/service. | Supported text; preserve actual timing, units and uncertainty |
| `reason_as_reported` | Exact attributed explanation, preserving uncertainty. | Supported text; preserve actual timing, units and uncertainty |
| `requirement_discussed` | Requirement reportedly discussed; not an independent criterion judgment. | duration / symptom_pattern / recurrence / other_stated_reason / unclear |
| `review_plan` | Reported further review or follow-up. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** Has a clinician explained how they understand these symptoms or what remains uncertain?

**Follow-up focus:** Distinguish a reported clinical reason from an unanswered assessment question.

**Interpretation limit:** Missing data is not evidence of a missing diagnostic requirement, and the extractor must not invent a specified reason.

### Unanswered or uncertain information — `assessment_information_gaps`

Explicit limits in the available history; a gap is not an absent symptom or confirmed subthreshold presentation.

Sources: [DSM_OTHER; NICE_222].

| Optional field | Meaning | Values/form |
|---|---|---|
| `target` | Specific unknown information relevant to interpretation. | Supported text; preserve actual timing, units and uncertainty |
| `basis` | Reason information remains unavailable. | not_asked / cannot_recall / ambiguous_answer / declined / conflicting_reports / other_reported_limit |
| `partial_information` | What is actually known. | Supported text; preserve actual timing, units and uncertainty |
| `next_clarification` | A focused question/review need; not a fabricated answer. | Supported text; preserve actual timing, units and uncertainty |

**Example question:** What parts of the timing are you able to remember?

**Follow-up focus:** Ask only high-value remaining targets, acknowledge uncertainty and respect declines.

**Interpretation limit:** Do not turn a five-minute incomplete interview into other specified depression because only two symptoms were extracted.

## 6. Assessment structure and follow-ups

This is a semi-structured **project policy**, not a validated question sequence or an implemented cross-disorder graph. Sources support the clinical domains; they do not establish that this exact order is optimal. The conversation agent asks a selected target naturally; the extractor reviews the history and stores supported facts; the planner chooses a useful unresolved target. Clinical interpretation remains separate from extraction.

1. **Safety and opening:** Check current safety concerns as indicated and invite an open account.
2. **Current period:** Clarify one current/recent period: start, end/ongoing, low mood, other symptoms and impact.
3. **Same period overlap:** Review concurrent symptom details without combining unrelated periods or counting unknowns as absent.
4. **Recurrence and baseline:** If brief spells recur, review consecutive months, variability and symptoms between spells.
5. **Lifetime and alternatives:** Review prior longer/chronic depression, activation, psychosis, relevant menstrual pattern, medical/exposure and stressor context.
6. **Focused gaps:** Clarify only targets that remain unresolved and change interpretation; respect uncertainty/declines.
7. **Professional review handoff:** Summarize supported information and remaining classification questions; no automatic residual diagnosis.


Follow up when a gap changes interpretation: current versus historical period; an ended versus ongoing spell; symptom overlap versus symptoms in different months; recurrence in every month versus most months; current low mood versus partial recovery after an earlier full episode; reported diagnosis versus no prior assessment. Ask one manageable question at a time.

Do not repeat an answered item simply because it was not the selected target. If a reply gives duration, sleep difficulty and missed work, extract all three with their quotations. If the person says “yes” to an earlier target, resolve the meaning through the preceding question; do not treat the word as affirmation of a diagnosis or every unanswered symptom.

An unrelated but clinically useful answer still matters. If asked about duration and the person mentions work difficulty, preserve function, acknowledge it and gently return: “That sounds difficult. Do you remember how long that particular low spell lasted?” If they cannot remember, store unknown. If they decline, respect the choice and retain the unresolved target. Do not pressure them until a plausible answer appears.

If the latest spell was first described as three days and then explicitly corrected to four, preserve the correction and earlier provenance. Do not silently leave the old duration active, average the durations, or propagate the latest length to all historical spells. Actual unresolved conflicts need notes and review. Source ambiguity at four days is separate from uncertainty about what the patient said.

## 7. Alternative pathways and coexistence

| Pathway | Information required | Common error to avoid |
|---|---|---|
| MDD, including partial remission/residual symptoms | Earlier full episodes, current course and recurrence | Relabelling a known lifetime MDD history solely because fewer symptoms are present now |
| PDD | Longstanding background symptoms and intervals | Treating fluctuations on chronic low mood as automatically separate brief episodes |
| Bipolar spectrum | Lifetime activation and longitudinal course | Assuming short depression excludes bipolar illness |
| PMDD/cycle-related worsening | Actual menstrual applicability and full-cycle timing | Calling any monthly recurrence either PMDD or recurrent brief depression |
| Medical/substance/medication effects | Relevant histories, actual exposure and chronology | Treating temporal association as causation or ignoring physical causes |
| Adjustment-related distress | Stressor, timing, symptom pattern, burden and alternatives | Diagnosing adjustment disorder from the existence of a stressor |
| Psychotic disorders/schizoaffective presentation | Specialist diagnosis and psychosis/mood timeline | Applying the first-three-examples exclusion universally, or adding this category automatically within schizoaffective disorder |
| Anxiety/depression overlap | Actual experiences, timing and burden | Importing a different classification's label without an explicit map |
| Grief or contextual sadness | Meaning, pattern, functioning and full differential | Assuming grief excludes depression or every sad experience is a disorder |
| Unspecified category or unresolved assessment | What is known and why classification remains unresolved | Treating missing evidence as a confirmed shortfall in diagnostic criteria |

The named examples' exclusions are not a license to infer lifetime absence from “I have never been diagnosed.” Ask about actual earlier experiences and attributed assessment. If earlier six-week low mood is reported, review it; do not diagnose that historical period automatically, but do not ignore it when considering a never-met-another-disorder example. [DSM_OTHER; VA_2022; NIMH_BIPOLAR]

## 8. Screening, tracking and symptom counting

PHQ-2/PHQ-9 may be useful in the wider screening/measurement pathway using verified versions, administration and scoring. Their fixed recall periods do not by themselves describe the full course of a three-day spell or demonstrate monthly recurrence over a year. A score cannot assign one of these named examples or establish lifetime exclusions. The original validation studies do not validate our reworded conversation. [PHQ2_2003; PHQ9_2001]

A prospective record can help document spell dates, symptoms, burden and between-spell status, but this module does not claim a new validated diary or require a year of new observation before support. Preserve whether pattern information comes from recall or contemporaneous records and whether coverage is incomplete. A convenient sample of positive days is not full longitudinal coverage. The recurrence requirement belongs to a particular named example, not to every assessment or every other-specified presentation. [DSM_OTHER]

Known versus unknown fields describe information availability. They are project states, not clinical severity scales. A symptom may be reported present while its frequency or duration remains unknown. A negative answer about one period does not deny the same symptom in every earlier period. No universal yes-count or extracted-record count implements the diagnostic requirements.

## 9. What the research contributes

Angst and colleagues used a prospective Zurich community cohort of young adults to examine recurrent brief depression's manifestations, burden, family history and course. They found similarities with major depression despite shorter duration. We use it as historical support for collecting recurrence and impact alongside duration. It is not the source of a new question order, a current universal threshold or a validated LLM benchmark; its definitions and population must remain labelled. [ANGST_1990]

Maier and colleagues examined recurrent brief depression in 300 general-practice participants from a WHO study. The abstract describes substantial psychosocial impairment and suicide-related findings. We use it to avoid dismissing brief presentations as harmless, not to assign an individual's predicted risk or infer exact prevalence in our users. The older study's RBD definition does not override current DSM example exclusions, and it supplies no validated prompt. [MAIER_1994]

Judd and colleagues proposed a historical subsyndromal symptomatic depression construct involving symptoms and social dysfunction. This is useful chiefly as a terminology warning: research may define “subthreshold” differently. We do not substitute its definition for current DSM other-specified requirements or create an additional peer diagnosis. Its dataset, questionnaire or raw patient records are not included. [JUDD_1994]

These sources were consulted at the stated access level. No benchmark dataset was downloaded, model trained, published accuracy inherited or live agent evaluated by writing this module. Public abstracts are accessible; unrestricted full-paper/tool access must not be assumed from a PubMed link.

## 10. Safety, patient choice and handoff

Short duration or a low symptom count does not justify skipping current suicide-related concerns. Preserve current/historical thoughts and behaviours separately; distinguish death thoughts, suicidal intent and nonsuicidal self-harm rather than inferring one from another. Unmentioned intent is unknown. Use the implemented human-review pathway when indicated, independent of whether a named depressive example can be classified. [ASQ_BSSA; NICE_225]

The NIMH adult brief safety-assessment guide is for trained clinicians after a positive ASQ screen; citing it does not turn this chat into a validated ASQ service. NICE advises against predictive scales or global low/medium/high labels for suicide prediction or care decisions. Our safety fields are workflow flags and unresolved concerns, not risk predictions or proof that someone was contacted. [ASQ_BSSA; NICE_225]

Respect pauses, declines and uncertain recall. Urgent concerns interrupt ordinary checklist completion. Do not advise waiting for a spell to reach two weeks, or waiting twelve months for classification, before seeking appropriate support. The system does not independently confirm diagnoses, prescribe, manage psychosis or claim an emergency response was delivered.

The professional handoff should include the actual symptom pattern, timing and burden; separate spells and recurrence coverage; between-spell baseline; relevant lifetime/alternative information; reported clinical formulations; source or patient uncertainties; safety concerns and actual review status; and the precise questions still needing clarification. Use “brief depressive spells reported; classification unresolved” when that reflects the evidence.

## 11. Evidence output: shared fields and flexible details

| Field | Meaning |
|---|---|
| `module_id`, `schema_version` | Fixed application contract identifiers |
| `concept_id` | Allowlisted information domain from the cards |
| `episode_key` | Application-owned period/pattern key; does not itself establish a formal episode |
| `subject` | Patient in this contract; do not assign third-party symptoms to them |
| `finding_status` | Reported presence, explicit absence, ambiguity or conflict |
| `temporal_status`, `time_reference` | Current/historical/unclear context and actual time wording |
| `attributes` | Only the optional details allowed for that concept |
| `evidence` | Exact patient quote, source message, earlier context and supported fields |
| `uncertainty_notes` | Recall, contradiction or interpretation limits |
| `semantic_check_status` | Whether interpretation appears supported or needs review; cannot be proven by schema validation |
| `question_tracking` | Target/status and unresolved target; includes partial answers and declines |
| `safety_handoff` | Review-need flag, reported concerns and remaining questions; no claim of real-world delivery |

The model does not generate evidence UUIDs. Code supplies message/period IDs and manages the unique snapshot key `(concept_id, episode_key, subject)`. Update a matching record with newly supported information while preserving evidence; use separate keys for different periods and the overall pattern. Keep contradictory accounts visible until resolved.

Every known detail needs a value and an evidence link. Unknown has no value. Not-applicable needs a reason and is not equivalent to not asked. Omitted fields do not mean absent symptoms. All field names, identifiers and states are project implementation choices; clinical sources supply the domains and criteria, not these JSON names.

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


Exact source quotes must be substrings of patient messages. Context references must precede the source answer. A quoted “yes” may be meaningful only through the previous question. Those mechanical constraints help traceability but cannot establish that an LLM interpreted a sentence correctly. The schema does not permit a free-form confirmed diagnosis, criterion count or assigned presentation in the extractor output.

Category definitions and example requirements live in `classification_reference.json`; they are not patient evidence. A reported clinician's reason can be extracted as attributed testimony. The planner may flag a gap, but it cannot change “unknown whether criterion met” into “criterion not met.” Professional-review conclusions need a separately governed output rather than hidden assertions in patient-evidence fields.

## 12. Fictional example and expected result

The fixture describes brief low spells with sadness, sleep difficulty, concentration problems and missed work. The person reports “most months” but cannot remember two months; later they describe an earlier six-week low period, answer a baseline question with a contextual “yes,” and correct the latest spell from roughly three days to exactly four.

Expected behaviour: retain the reported symptoms and work burden; keep recurrence gaps unknown; preserve the older low period separately; resolve the short answer using earlier context; and update only the corrected latest period, retaining provenance. Do not infer all remaining symptoms absent, twelve consecutive qualifying months, a never-had-MDD history or a definitive named example. Even before the four-day source ambiguity is considered, important symptom/history information remains unresolved. Safety is unassessed in this short example.

`examples.json` contains both snapshots and their source messages. They are authored fixtures, not live model outputs. Mechanical tests exercise schema/provenance and these desired storage behaviours; clinical and semantic performance still need evaluation.

## 13. Files and what remains

- `knowledge.json`: concept cards, flexible fields, value definitions, category safeguards and local interview policy.
- `classification_reference.json`: four named examples, distinctions, exclusions and explicit source ambiguities; no automatic classifier.
- `sources.json`: links, locations, contributions, access notes and check date.
- `evidence_output.schema.json`: proposed patient-evidence output contract.
- `examples.json`: fictional history-aware snapshots and expected interpretation.
- `validate_package.py` / `VALIDATION_REPORT.json`: mechanical checks and actual results.

Remaining work: qualified clinical review, resolution of the flagged wording issues before any automated threshold decisions, final cross-disorder graph, role-specific context selection, runtime connection and evaluation on diverse fictional cases. Existing agents/prompts are unchanged. Passing the checks is not clinical validation, diagnostic accuracy evidence or proof that every residual presentation is covered by a fixed rule.

The source-linked category content and evidence contract are ready for that review/integration stage. Copyrighted manuals, licensed interview item sets, real patient records and API keys are not bundled. Other specified does not replace a careful assessment when criteria are uncertain.

## 14. Source register

Manual requirements, guidance, historical research and project implementation are labelled separately. Page numbers distinguish printed pages from PDF-viewer pages. Official updates are applied only to the relevant revised passages; empirical research is not treated as a new diagnostic authority.


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

### DSM_OTHER

[APA DSM-5-TR (2022), Other Specified Depressive Disorder](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders)

**Location:** Printed pp.209–210; PDF viewer pp.340–341; MDD episode reference in same chapter

**Used for:** Category definition, four non-exhaustive examples and example-specific exclusions

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror. Publisher full text blocked. No manual or licensed questionnaire bundled; redistribution permission not inferred.

### APA_2025

[APA DSM-5-TR cumulative update, September 2025](https://www.psychiatry.org/getmedia/b68a5776-f88c-45c7-9535-fd219d7aa5cb/APA-DSM5TR-Update-September-2025.pdf)

**Location:** II.B, printed supplement p.7 / PDF viewer p.7; revised text read with visual revision marks

**Used for:** Revised names and removal of obsolete exclusions in examples 2/3; four-day heading/body discrepancy remains for review

**Access:** Official page rendered and visually reviewed during 2 November audit. Red strikethrough is deleted text, not a retained criterion. Selected revisions only; supplement does not replace manual.

### APA_UPDATE_INDEX

[APA, Updates to DSM-5-TR Criteria and Text](https://www.psychiatry.org/psychiatrists/practice/dsm/updates-to-dsm/updates-to-dsm-5-tr-criteria-text/)

**Location:** September 2025 Updates and earlier-update list

**Used for:** Version verification; September 2025 is the latest update listed on the inspected page

**Access:** Official page inspected on the recorded research date; future changes require rechecking.

### ANGST_1990

[Angst, Merikangas, Scheidegger & Wicki (1990), Recurrent brief depression: a new subtype of affective disorder](https://pubmed.ncbi.nlm.nih.gov/2142703/)

**Location:** J Affect Disord 19(2):87–98; Abstract; DOI 10.1016/0165-0327(90)90013-X

**Used for:** Historical prospective Zurich cohort research: importance of duration, recurrence and burden; not current DSM criteria

**Access:** Primary abstract/indexed material inspected; no full-text or reuse rights inferred

### MAIER_1994

[Maier et al. (1994), Recurrent brief depression in general practice](https://pubmed.ncbi.nlm.nih.gov/7888417/)

**Location:** Eur Arch Psychiatry Clin Neurosci 244(4):196–204; Abstract; DOI 10.1007/BF02190398

**Used for:** Primary-care study in 300 patients: clinical burden and need to assess suicide-related concerns despite brief episodes

**Access:** Primary abstract/indexed material inspected; no full-text or reuse rights inferred

### JUDD_1994

[Judd et al. (1994), Subsyndromal symptomatic depression: a new mood disorder?](https://pubmed.ncbi.nlm.nih.gov/8077164/)

**Location:** Abstract: proposed SSD definition and social dysfunction

**Used for:** Historical research terminology differs from current DSM other-specified examples; do not merge definitions

**Access:** Primary abstract/indexed material inspected; no full-text or reuse rights inferred
