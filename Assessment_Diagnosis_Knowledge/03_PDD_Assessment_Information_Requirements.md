# 03 — Adult PDD assessment knowledge and evidence output

Version: 1.0.1-source-reviewed. Research date: 2 November 2026. Adults 18+, including older adults. Source-precedence clarification added during audit.

**Scope:** persistent depressive disorder (PDD) assessment and provisional professional review. This package documents the clinical information domains and a proposed evidence contract. It is not a validated clinical interview, a prescribing guide or an autonomous diagnostic system. It is not connected to the current agents.

## 1. What PDD means

PDD is a persistent depressive course and is not necessarily mild. APA removed the older dysthymia parenthesis because current PDD includes a broader range of presentations than historical dysthymic disorder. The two retained symptom-feature specifiers are anxious distress and atypical features. [APA_PDD]

NICE's chronic-depressive-symptoms grouping is broader guideline terminology, not automatic confirmation of DSM PDD. Our age 18+ boundary is project scope; childhood onset can still be relevant to an adult history. [NICE_222]

**Clinical facts versus project design:** sources support symptoms, timing, exclusions and assessment domains. Our JSON keys, value sets, question examples, merge rules and priorities are engineering proposals. A citation does not imply a guideline mandates our schema or validates our agents.

## 2. Adult clinical requirements and what to establish

The adult foundation is low mood most of the day, more days than not, for at least two years, with at least two of six associated groups while depressed. Relevant symptom-absent intervals cannot exceed two months at a time. Distress/impairment and differential exclusions also need review. [SAMHSA_PDD]

The six associated groups are appetite/eating, sleep, energy, self-esteem, concentration/decisions and hopelessness. Alternatives within a group are not separate criteria. Do not impose MDD's nine-domain count or universal near-daily rule here. A symptom report does not by itself establish a qualifying criterion. [SAMHSA_PDD]

The current manual also requires review of manic/hypomanic history, persistent psychotic-disorder explanations and physiological substance/medical causes. Cyclothymic patterns matter in the differential. Full MDE-level illness may coexist with the persistent course rather than excluding it. [DSM_PDD]

| Requirement | Information needed | Meaning for our system |
|---|---|---|
| Mood/duration | Actual long-term mood account and reference period | No duration invented from “always” |
| Associated symptoms | Relevant groups and overlap with depressed periods | No frequency invented or double counting |
| Continuity | Better intervals and whether symptoms actually disappeared | Better is not automatically symptom-free |
| MDE relationship | Current/past episode information | Use MDD knowledge when indicated; do not force exclusive labels |
| Alternatives | Activation, psychotic, medical/exposure history | Focused review, not complete diagnosis of every alternative |
| Burden | Distress and concrete functional consequences | Long duration alone is insufficient |

The detailed criteria-information map is in `PDD/knowledge.json`. Its D entry is explicitly a compatibility note, not an additional symptom requirement or an exclusion.

## 3. Concept cards and concept-specific output details

Each card explains the clinical domain and proposed fields. No card requires every field on every response. Known values need source quotations; unknown values stay unknown. Patient-reported professional history is not our confirmed diagnosis. Questions below are original project examples, not standardized test items.

### Persistent depressed-mood report — `depressed_mood`

Low, sad or empty mood described over a relevant period.

Role: `required_mood`. PDD associated count group: `not one of the six associated groups`. Sources: [APA_PDD; SAMHSA_PDD].

| Output detail | Meaning | Values / form |
|---|---|---|
| `description` | The person's description of this experience, without adding a diagnosis. | Supported text; preserve wording and uncertainty |
| `onset` | When this specific experience began; retain approximate dates or life anchors. | Supported text; preserve wording and uncertainty |
| `duration` | Reported length of this particular experience; do not borrow another symptom's duration. | Supported text; preserve wording and uncertainty |
| `frequency` | Actual recurrence pattern and reference period; no invented days-per-week threshold. | Supported text; preserve wording and uncertainty |
| `proportion_of_day` | How much of an affected day the experience lasts. | Supported text; preserve wording and uncertainty |
| `course` | Continuity, fluctuations and changes within the relevant period. | Supported text; preserve wording and uncertainty |
| `baseline_comparison` | Usual state if recall permits; a clear pre-illness baseline is not always available. | Supported text; preserve wording and uncertainty |
| `recall_limits` | Approximation, uncertainty or difficulty reconstructing history. | Supported text; preserve wording and uncertainty |

**Example question:** When do you remember this longer-lasting low mood beginning?

**Follow-up focus:** Clarify most-of-day experience, more-days-than-not pattern and the long-term window if missing.

**Do not infer:** Always been this way is not a verified duration. Do not impose MDD's nearly-daily rule on PDD.

### Appetite or overeating — `appetite_eating`

Poor appetite or eating more than usual; preserve which was actually reported.

Role: `associated_symptom`. PDD associated count group: `appetite_eating`. Sources: [SAMHSA_PDD].

| Output detail | Meaning | Values / form |
|---|---|---|
| `description` | The person's description of this experience, without adding a diagnosis. | Supported text; preserve wording and uncertainty |
| `onset` | When this specific experience began; retain approximate dates or life anchors. | Supported text; preserve wording and uncertainty |
| `duration` | Reported length of this particular experience; do not borrow another symptom's duration. | Supported text; preserve wording and uncertainty |
| `frequency` | Actual recurrence pattern and reference period; no invented days-per-week threshold. | Supported text; preserve wording and uncertainty |
| `overlap_with_low_mood` | Whether and when this associated experience occurred during low-mood periods. | Supported text; preserve wording and uncertainty |
| `pattern` | Reported experience. | poor_appetite / overeating / both_or_variable / unclear |
| `appetite_vs_intake` | Desire for food versus actual eating; not interchangeable. | Supported text; preserve wording and uncertainty |
| `impact` | Concrete reported consequence of this experience. | Supported text; preserve wording and uncertainty |

**Example question:** During those low-mood periods, what was your appetite or eating like?

**Follow-up focus:** Separate low appetite from overeating; retain relevant timing.

**Do not infer:** Do not require weight change, infer overeating from hunger alone or count appetite and overeating as two groups.

### Sleep disturbance — `sleep_disturbance`

Difficulty sleeping or excessive sleep within the assessed course.

Role: `associated_symptom`. PDD associated count group: `sleep`. Sources: [SAMHSA_PDD; NIMH_BIPOLAR].

| Output detail | Meaning | Values / form |
|---|---|---|
| `onset` | When this specific experience began; retain approximate dates or life anchors. | Supported text; preserve wording and uncertainty |
| `duration` | Reported length of this particular experience; do not borrow another symptom's duration. | Supported text; preserve wording and uncertainty |
| `frequency` | Actual recurrence pattern and reference period; no invented days-per-week threshold. | Supported text; preserve wording and uncertainty |
| `overlap_with_low_mood` | Whether and when this associated experience occurred during low-mood periods. | Supported text; preserve wording and uncertainty |
| `pattern` | Reported complaint. | onset_difficulty / maintenance_difficulty / early_waking / excessive_sleep / mixed / unclear |
| `latency` | Time needed to fall asleep, not weeks/months of the complaint. | Supported text; preserve wording and uncertainty |
| `sleep_hours` | Actual reported sleeping time with units and reference period. | Supported text; preserve wording and uncertainty |
| `opportunity` | Opportunity to sleep and relevant external interruptions. | Supported text; preserve wording and uncertainty |
| `daytime_effects` | Reported sleepiness, exhaustion or other effects. | Supported text; preserve wording and uncertainty |
| `baseline_comparison` | Usual state if recall permits; a clear pre-illness baseline is not always available. | Supported text; preserve wording and uncertainty |

**Example question:** How was your sleep during those periods?

**Follow-up focus:** Identify the complaint before asking subtype-specific details.

**Do not infer:** Short sleep with tiredness is not reduced need for sleep; do not assume the complaint lasted as long as low mood.

### Energy and fatigue — `energy_fatigue`

Low energy or unusual tiredness.

Role: `associated_symptom`. PDD associated count group: `energy`. Sources: [SAMHSA_PDD].

| Output detail | Meaning | Values / form |
|---|---|---|
| `description` | The person's description of this experience, without adding a diagnosis. | Supported text; preserve wording and uncertainty |
| `onset` | When this specific experience began; retain approximate dates or life anchors. | Supported text; preserve wording and uncertainty |
| `duration` | Reported length of this particular experience; do not borrow another symptom's duration. | Supported text; preserve wording and uncertainty |
| `frequency` | Actual recurrence pattern and reference period; no invented days-per-week threshold. | Supported text; preserve wording and uncertainty |
| `overlap_with_low_mood` | Whether and when this associated experience occurred during low-mood periods. | Supported text; preserve wording and uncertainty |
| `baseline_comparison` | Usual state if recall permits; a clear pre-illness baseline is not always available. | Supported text; preserve wording and uncertainty |
| `impact` | Concrete reported consequence of this experience. | Supported text; preserve wording and uncertainty |

**Example question:** What was your energy like during those low-mood periods?

**Follow-up focus:** Collect an example and timing if unclear.

**Do not infer:** Fatigue alone does not establish its cause or a diagnosis.

### Low self-esteem — `low_self_esteem`

Reported low evaluation of oneself or one's worth/capabilities.

Role: `associated_symptom`. PDD associated count group: `self_esteem`. Sources: [SAMHSA_PDD].

| Output detail | Meaning | Values / form |
|---|---|---|
| `description` | The person's description of this experience, without adding a diagnosis. | Supported text; preserve wording and uncertainty |
| `self_evaluation` | Actual thoughts and examples in the person's terms. | Supported text; preserve wording and uncertainty |
| `onset` | When this specific experience began; retain approximate dates or life anchors. | Supported text; preserve wording and uncertainty |
| `duration` | Reported length of this particular experience; do not borrow another symptom's duration. | Supported text; preserve wording and uncertainty |
| `frequency` | Actual recurrence pattern and reference period; no invented days-per-week threshold. | Supported text; preserve wording and uncertainty |
| `overlap_with_low_mood` | Whether and when this associated experience occurred during low-mood periods. | Supported text; preserve wording and uncertainty |
| `context` | Situations in which this evaluation occurs. | Supported text; preserve wording and uncertainty |
| `impact` | Concrete reported consequence of this experience. | Supported text; preserve wording and uncertainty |

**Example question:** How were you thinking about yourself during that time?

**Follow-up focus:** Clarify self-evaluation and persistence, without endorsing negative beliefs.

**Do not infer:** Do not automatically turn low self-esteem into excessive guilt, delusional worthlessness or a personality diagnosis.

### Concentration and decisions — `cognition_decisions`

Poor concentration or difficulty making decisions.

Role: `associated_symptom`. PDD associated count group: `cognition`. Sources: [SAMHSA_PDD].

| Output detail | Meaning | Values / form |
|---|---|---|
| `description` | The person's description of this experience, without adding a diagnosis. | Supported text; preserve wording and uncertainty |
| `kind` | Reported difficulty. | concentration / indecision / both / unclear |
| `tasks` | Concrete affected tasks. | Supported text; preserve wording and uncertainty |
| `onset` | When this specific experience began; retain approximate dates or life anchors. | Supported text; preserve wording and uncertainty |
| `duration` | Reported length of this particular experience; do not borrow another symptom's duration. | Supported text; preserve wording and uncertainty |
| `frequency` | Actual recurrence pattern and reference period; no invented days-per-week threshold. | Supported text; preserve wording and uncertainty |
| `overlap_with_low_mood` | Whether and when this associated experience occurred during low-mood periods. | Supported text; preserve wording and uncertainty |
| `baseline_comparison` | Usual state if recall permits; a clear pre-illness baseline is not always available. | Supported text; preserve wording and uncertainty |
| `impact` | Concrete reported consequence of this experience. | Supported text; preserve wording and uncertainty |

**Example question:** Were concentrating or making decisions difficult during that time?

**Follow-up focus:** Collect examples and distinguish a longstanding difficulty from the mood-related account.

**Do not infer:** Do not diagnose dementia or ADHD from this report.

### Hopelessness — `hopelessness`

Reported negative expectations or lack of hope about the future.

Role: `associated_symptom`. PDD associated count group: `hopelessness`. Sources: [SAMHSA_PDD; ASQ_BSSA].

| Output detail | Meaning | Values / form |
|---|---|---|
| `description` | The person's description of this experience, without adding a diagnosis. | Supported text; preserve wording and uncertainty |
| `future_expectations` | What the person expects or sees as unlikely to improve. | Supported text; preserve wording and uncertainty |
| `onset` | When this specific experience began; retain approximate dates or life anchors. | Supported text; preserve wording and uncertainty |
| `duration` | Reported length of this particular experience; do not borrow another symptom's duration. | Supported text; preserve wording and uncertainty |
| `frequency` | Actual recurrence pattern and reference period; no invented days-per-week threshold. | Supported text; preserve wording and uncertainty |
| `overlap_with_low_mood` | Whether and when this associated experience occurred during low-mood periods. | Supported text; preserve wording and uncertainty |
| `context` | What these expectations concern. | Supported text; preserve wording and uncertainty |
| `impact` | Concrete reported consequence of this experience. | Supported text; preserve wording and uncertainty |

**Example question:** How did the future seem to you during that period?

**Follow-up focus:** Clarify the actual expectation; assess safety separately when needed.

**Do not infer:** Hopelessness is not automatically suicidal intent; future plans do not by themselves prove safety.

### Longitudinal course — `longitudinal_timeline`

The background period and its changes, without a diagnosis inferred from duration alone.

Role: `timeline`. PDD associated count group: `not one of the six associated groups`. Sources: [DSM_PDD; SAMHSA_PDD; PDD_SURVEY_2020].

| Output detail | Meaning | Values / form |
|---|---|---|
| `onset` | When this specific experience began; retain approximate dates or life anchors. | Supported text; preserve wording and uncertainty |
| `duration` | Reported length of this particular experience; do not borrow another symptom's duration. | Supported text; preserve wording and uncertainty |
| `course` | Continuity, fluctuations and changes within the relevant period. | Supported text; preserve wording and uncertainty |
| `recall_limits` | Approximation, uncertainty or difficulty reconstructing history. | Supported text; preserve wording and uncertainty |
| `reference_window` | Which long-term interval is being reconstructed. | Supported text; preserve wording and uncertainty |
| `longest_better_interval` | Longest reported better interval; clarify what better means. | Supported text; preserve wording and uncertainty |
| `symptom_absence_account` | Evidence concerning intervals without relevant symptoms; not mere improvement. | Supported text; preserve wording and uncertainty |
| `life_anchors` | Reported ages/events helping recall timing. | Supported text; preserve wording and uncertainty |
| `associated_symptom_overlap` | Whether associated reports belong to the low-mood periods. | Supported text; preserve wording and uncertainty |
| `intervals` | Reported intervals. Each entry keeps raw dates/duration, degree of change and description; uncertainty is explicit. | Structured interval list; explained below |

**Example question:** Were there stretches when these difficulties went away?

**Follow-up focus:** Distinguish feeling better from absence of the relevant symptoms, and clarify length.

**Do not infer:** Do not convert always into two years, better into remission or eight weeks into two calendar months.

### Age-at-onset history — `onset_history`

Reported age or life period when the persistent course began.

Role: `timeline`. PDD associated count group: `not one of the six associated groups`. Sources: [DSM_PDD].

| Output detail | Meaning | Values / form |
|---|---|---|
| `age_or_period` | Reported age/life period; do not guess a number. | Supported text; preserve wording and uncertainty |
| `approximation` | Precision and uncertainty of recall. | Supported text; preserve wording and uncertainty |
| `continuity_to_adulthood` | Whether the reported course extended into adulthood. | Supported text; preserve wording and uncertainty |

**Example question:** About how old were you when that longer-lasting pattern began?

**Follow-up focus:** Use a life-stage anchor if exact age is not recalled.

**Do not infer:** Before 21 versus 21+ is an onset description, not our adult eligibility rule.

### Major depressive episode history — `mde_history`

Periods needing separate MDE review within or outside the persistent background.

Role: `episode_review`. PDD associated count group: `not one of the six associated groups`. Sources: [DSM_PDD; CANMAT_2023].

| Output detail | Meaning | Values / form |
|---|---|---|
| `period` | Dates/duration of the suspected episode. | Supported text; preserve wording and uncertainty |
| `symptoms` | Reported symptoms requiring full MDD-module assessment. | Supported text; preserve wording and uncertainty |
| `impact` | Reported burden. | Supported text; preserve wording and uncertainty |
| `current_status` | Current versus past presentation, as reported. | Supported text; preserve wording and uncertainty |
| `background_relationship` | Relation to the long-term background. | Supported text; preserve wording and uncertainty |
| `lower_symptom_intervals` | Intervals below a full episode threshold, if actually professionally established; otherwise preserve raw changes. | Supported text; preserve wording and uncertainty |
| `professional_history` | What a professional reportedly diagnosed, not our confirmation. | Supported text; preserve wording and uncertainty |

**Example question:** Were there periods when things became noticeably worse than that usual pattern?

**Follow-up focus:** Open the MDD information pathway when indicated; severity alone is not a qualifying episode.

**Do not infer:** Do not force PDD and MDD to be mutually exclusive, or label full MDE from worse alone.

### Death/suicide-related reports — `death_suicide`

Reported death/suicide-related experiences requiring separate safety assessment; not one of the six PDD associated groups.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [ASQ_BSSA; NICE_222].

| Output detail | Meaning | Values / form |
|---|---|---|
| `experience` | Preserve distinctions. | death_thoughts / wish_not_alive / suicidal_thoughts / suicide_plan / suicide_attempt / unclear |
| `recency` | When last/current; do not infer resolution. | Supported text; preserve wording and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve wording and uncertainty |
| `intent` | Intent as reported. | Supported text; preserve wording and uncertainty |
| `plan_present` | Whether a plan was explicitly reported or denied. | reported / denied / unclear |
| `access` | Access to means as reported, without generating procedural details. | Supported text; preserve wording and uncertainty |
| `past_behaviour` | Historical self-injury/attempt account, intent and timing. | Supported text; preserve wording and uncertainty |
| `support` | Available support as reported. | Supported text; preserve wording and uncertainty |

**Example question:** Have you had thoughts about ending your life?

**Follow-up focus:** Use dedicated safety pathway; preserve current versus historical information.

**Do not infer:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [NICE_222].

| Output detail | Meaning | Values / form |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text; preserve wording and uncertainty |
| `examples` | Concrete difficulty or distress. | Supported text; preserve wording and uncertainty |
| `baseline` | Usual functioning. | Supported text; preserve wording and uncertainty |
| `supports` | Assistance helping preserve functioning. | Supported text; preserve wording and uncertainty |

**Example question:** How have these changes affected your daily life?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Activation history — `activation_history`

Possible distinct elevated/overactive periods requiring review.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [NICE_185; NIMH_BIPOLAR].

| Output detail | Meaning | Values / form |
|---|---|---|
| `period` | Current/historical time. | Supported text; preserve wording and uncertainty |
| `mood` | Elevated, expansive or irritable mood as reported. | Supported text; preserve wording and uncertainty |
| `energy_activity` | Change in energy/activity. | Supported text; preserve wording and uncertainty |
| `sleep_need` | Sleep need and tiredness, not just sleep hours. | Supported text; preserve wording and uncertainty |
| `other_changes` | Associated speech, thoughts, confidence or risky behaviour. | Supported text; preserve wording and uncertainty |
| `duration` | Duration of that period. | Supported text; preserve wording and uncertainty |
| `impact` | Consequences or other observers. | Supported text; preserve wording and uncertainty |
| `exposure_context` | Medicines/substances/medical context. | Supported text; preserve wording and uncertainty |

**Example question:** Have you had a distinct period of unusually increased energy or activity?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Medical context — `medical_context`

Relevant reported medical history and symptoms.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [NICE_222].

| Output detail | Meaning | Values / form |
|---|---|---|
| `conditions` | Reported conditions; distinguish reported diagnosis from confirmation. | Supported text; preserve wording and uncertainty |
| `timeline` | Relationship to symptoms. | Supported text; preserve wording and uncertainty |
| `investigations` | Results only if actually supplied. | Supported text; preserve wording and uncertainty |
| `clinician_review` | Known professional assessment or unresolved need. | Supported text; preserve wording and uncertainty |

**Example question:** Are there health conditions that might be relevant to these changes?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Medicines and substances — `exposure_context`

Relevant treatment/substance exposure account.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [NICE_222].

| Output detail | Meaning | Values / form |
|---|---|---|
| `name` | Named exposure. | Supported text; preserve wording and uncertainty |
| `dose_use` | Reported amount/use; never recommend a dose. | Supported text; preserve wording and uncertainty |
| `start_change_stop` | Timing of changes. | Supported text; preserve wording and uncertainty |
| `symptom_timing` | Reported temporal relationship. | Supported text; preserve wording and uncertainty |
| `source_kind` | Medicine, alcohol, other substance or unclear. | Supported text; preserve wording and uncertainty |

**Example question:** Have any medicines or substance-use patterns changed around this time?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Psychotic experiences — `psychotic_experience`

Reported experiences requiring specialist interpretation.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [DSM_PDD; NICE_222].

| Output detail | Meaning | Values / form |
|---|---|---|
| `kind` | Experience as described, not an automatic diagnosis. | Supported text; preserve wording and uncertainty |
| `content` | Brief relevant content without affirming beliefs. | Supported text; preserve wording and uncertainty |
| `mood_relationship` | During versus outside mood episodes. | Supported text; preserve wording and uncertainty |
| `conviction_context` | Reported belief/context and uncertainty. | Supported text; preserve wording and uncertainty |
| `safety_concerns` | Any reported urgent implications. | Supported text; preserve wording and uncertainty |
| `reported_mood_congruence` | Professional mood-congruence description if actually supplied; do not invent it. | congruent / incongruent_or_mixed / unclear |

**Example question:** Have you had experiences that other people do not seem to share?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [NICE_222].

| Output detail | Meaning | Values / form |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text; preserve wording and uncertainty |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text; preserve wording and uncertainty |
| `period` | When and for which symptoms. | Supported text; preserve wording and uncertainty |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text; preserve wording and uncertainty |
| `use` | Actual use and barriers as reported. | Supported text; preserve wording and uncertainty |

**Example question:** Have you received help for something similar before?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Family history — `family_history`

Relevant family mood/psychiatric history.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [NICE_222].

| Output detail | Meaning | Values / form |
|---|---|---|
| `relative` | Relationship, without unnecessary identifying details. | Supported text; preserve wording and uncertainty |
| `reported_condition` | Condition as reported. | Supported text; preserve wording and uncertainty |
| `certainty` | How the person knows; unknown remains unknown. | Supported text; preserve wording and uncertainty |

**Example question:** Is there relevant mental-health history in your family?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Life context — `life_context`

Relevant stress, loss, trauma and support.

Role: `supporting_review`. PDD associated count group: `not one of the six associated groups`. Sources: [NICE_222; APA_GRIEF].

| Output detail | Meaning | Values / form |
|---|---|---|
| `events` | Events relevant to symptom timeline. | Supported text; preserve wording and uncertainty |
| `timing` | Temporal relationship. | Supported text; preserve wording and uncertainty |
| `support` | Current supports. | Supported text; preserve wording and uncertainty |
| `barriers` | Practical barriers. | Supported text; preserve wording and uncertainty |
| `meaning` | Person's interpretation of the context. | Supported text; preserve wording and uncertainty |

**Example question:** Has anything important been happening around the time these changes began?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Anxious distress — `anxious_distress`

Anxiety features on the majority of symptomatic days of current PDD; at least two specified features need professional review.

Role: `feature_evidence`. PDD associated count group: `not one of the six associated groups`. Sources: [APA_PDD; DSM_PDD; ANXIOUS_STUDY].

| Output detail | Meaning | Values / form |
|---|---|---|
| `tension` | Feeling keyed up or tense during the relevant episode. | Supported text; preserve wording and uncertainty |
| `unusual_restlessness` | Restlessness beyond the person's usual state; separate from observed motor agitation. | Supported text; preserve wording and uncertainty |
| `worry_affecting_concentration` | Difficulty focusing specifically because of worry. | Supported text; preserve wording and uncertainty |
| `fear_of_awful_event` | Fear that something awful may happen. | Supported text; preserve wording and uncertainty |
| `fear_of_losing_control` | Fear of losing control of oneself, as described by the person. | Supported text; preserve wording and uncertainty |
| `timing_frequency` | Frequency of the features during the relevant persistent-depression period. | Supported text; preserve wording and uncertainty |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text; preserve wording and uncertainty |
| `depressed_period_overlap` | Relation to the current PDD symptomatic period, not an assumed discrete MDE. | Supported text; preserve wording and uncertainty |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** The five feature labels refer to tension, restlessness, worry-related concentration difficulty and the two specified fears.

**Do not infer:** Clarify episode overlap and actual experience; do not substitute a generic anxiety score.

### Atypical features — `atypical_features`

Mood reactivity plus at least two of increased appetite/weight, excessive sleep, leaden limbs or longstanding impairing rejection sensitivity, predominant on the majority of symptomatic days of current PDD.

Role: `feature_evidence`. PDD associated count group: `not one of the six associated groups`. Sources: [APA_PDD; DSM_PDD; CANMAT_2016].

| Output detail | Meaning | Values / form |
|---|---|---|
| `mood_reactivity` | Mood improvement in response to actual or anticipated positive events. | Supported text; preserve wording and uncertainty |
| `appetite_weight_gain` | Significant increased appetite or weight, preserving which is reported. | Supported text; preserve wording and uncertainty |
| `excessive_sleep` | Reported extended sleep compared with usual; retain actual hours/naps and baseline. | Supported text; preserve wording and uncertainty |
| `leaden_limbs` | A heavy, weighted-down feeling in arms or legs; not objective paralysis. | Supported text; preserve wording and uncertainty |
| `longstanding_rejection_sensitivity` | Impairing sensitivity to interpersonal rejection that also exists outside mood episodes. | Supported text; preserve wording and uncertainty |
| `timing_frequency` | Frequency of the features during the relevant persistent-depression period. | Supported text; preserve wording and uncertainty |
| `observer` | Reporter/observer; not a substitute for examination. | Supported text; preserve wording and uncertainty |
| `depressed_period_overlap` | Relation to the current PDD symptomatic period, not an assumed discrete MDE. | Supported text; preserve wording and uncertainty |

**Example question:** Ask a focused, neutral question about a relevant feature only.

**Follow-up focus:** Associated features concern increased appetite/weight, excessive sleep, heavy limbs and longstanding impairing sensitivity to rejection beyond the episode.

**Do not infer:** Feeling better briefly does not rule out depression. Atypical is a technical pattern, not any unusual symptom.

## 4. Longitudinal intervals and changing symptoms

The proposed `intervals` detail is a list. Each interval has `start_raw`, `end_raw`, `duration_raw`, `change_kind` and `description`. Missing dates are null, not invented. `change_kind` describes reported partial improvement, absence of relevant symptoms, worsening or an unclear change. It is not a remission diagnosis.

Important distinctions:

- Two years of mood symptoms does not prove two years of every associated symptom.
- Feeling less bad is different from absence of the relevant mood/associated symptoms.
- Falling below full MDE requirements differs from being entirely free of PDD symptoms.
- Eight weeks and two calendar months are different source expressions; retain which was reported and avoid silent conversion.
- A long-established pattern may lack a clear pre-illness baseline. Record that uncertainty rather than forcing an MDD-style new-change requirement onto PDD.

These recordkeeping distinctions are our operational design around the source requirements. When answers conflict, preserve the quotations and clarify instead of averaging dates or erasing earlier history.

## 5. Course, onset, MDD relationship and severity

The manual permits PDD and MDD together when their requirements are met. Record background and superimposed episodes separately. [DSM_PDD]

For the preceding two years, course descriptions distinguish: no full MDE; persistent full MDE; intermittent MDE with a current episode; and intermittent MDE without a current episode. The intermittent/current description has a specific eight-week below-full-MDE condition. Early onset is before 21; late onset is 21+. These are onset descriptions, not adult eligibility limits. [DSM_PDD]

Severity and remission descriptions require professional interpretation of symptoms, intensity, functioning, residual symptoms and timing. We preserve that information and reported professional conclusions; no severity/remission label is generated from symptom silence or a screening score. The shared remission definitions referenced by the PDD criteria use episode-oriented wording, so we do not invent a separate automated PDD remission formula. [DSM_PDD]

For clarity, the referenced shared severity definitions describe mild illness as relatively limited, manageable symptom burden with minor functional impairment; severe illness as substantially greater, unmanageable burden with marked interference; and moderate illness as intermediate. The shared remission text describes partial remission as residual symptoms below full episode requirements or a symptom-free interval shorter than two months after an episode, and full remission as two months without significant signs/symptoms. Applying those labels to a persistent course requires professional review; we do not substitute a new numeric algorithm. [DSM_PDD]

Never describe PDD as necessarily mild or use “high functioning” to negate distress. Preserved functioning may reflect effort or support; collect the person's actual account. [APA_PDD; NICE_222]

## 6. Applicable feature specifiers

Only anxious distress and atypical features are included as PDD symptom-feature branches. Course/onset, severity and remission are different description axes. Do not copy the broader MDD feature list into PDD. [APA_PDD]

Anxious distress concerns the specified tension/restlessness/worry/fear features on most symptomatic days, with at least two present. Its severity descriptors distinguish two features (mild), three (moderate), four/five (moderate-severe), and four/five with motor agitation (severe); these are separate from overall PDD severity. Atypical features require mood reactivity plus at least two of the four additional eating/weight, sleep, heavy-limb or rejection-sensitivity features. Rejection sensitivity is longstanding and impairing outside the depressive period too. Neither ordinary anxiety nor one long sleep is enough. [ANXIOUS_STUDY; CANMAT_2016; DSM_PDD]

Motor agitation used in anxious-distress severity needs clinical interpretation; it is not inferred from text speed. The shared atypical definition excludes concurrent melancholic/catatonic criteria in the same episode; this is not permission to attach all MDD specifiers to PDD. Other serious experiences such as psychosis, catatonia or perinatal concerns can still require assessment even though they are not all PDD symptom-feature specifiers. [DSM_PDD; APA_PDD]

## 7. Alternative review, context and safety

Assess relevant activation history, medical conditions, medicines/substances and psychotic experiences, alongside functioning, previous treatment, family history and life context. NICE recommends this comprehensive approach. [NICE_222]

An MDD-like episode, a cyclothymic/bipolar pattern, medical/substance explanations and other residual depressive categories must not be decided by duration alone. We record clues and uncertainty; a specialist may need to assess the alternative. Do not automatically diagnose a personality disorder because distress has been longstanding. [DSM_PDD]

Older adults remain in scope. Physical/cognitive complaints, medication context and communication needs may affect assessment. A medical assessment can be necessary; this package does not prescribe a universal laboratory panel or establish a medical cause. [NIMH_DEP; NICE_222]

Ask directly about suicidal thoughts and intent rather than treating hopelessness as the answer. Keep current thoughts, past behaviour, intent, access and support distinct. Longstanding illness or a negative answer to one question does not prove safety. NIMH's BSSA domains inform our safety record, but it is a guide for trained clinicians after a positive ASQ, not validation of autonomous LLM use. [NICE_222; ASQ_BSSA]

The handoff states `not_assessed`, `no_signal_reported_in_available_text`, `needs_clinical_review` and `urgent_review_needed` are project workflow states, not predicted suicide probabilities. “No signal reported” is not “safe.” NICE advises against predictive low/medium/high global risk categories. A local operational response pathway remains separate work. [NICE_225]

## 8. How the research papers inform this module

| Paper | What it studied / what we use | What we do not infer |
|---|---|---|
| German clinical/population surveys, 2020 [PDD_SURVEY_2020] | Reconstructed persistent depression using interview history, including long episode duration and dysthymia; illustrates why ascertainment and course matter | Its older DSM-IV-derived operationalization is not our current diagnostic rule; its sample age limits are not our population limits |
| Long-term follow-up study, 2023 [PDD_FOLLOWUP_2023] | Examined persistent depression over follow-up, including residual symptoms and changing trajectories; supports keeping longitudinal residual-symptom information visible | Associations do not establish a patient's diagnosis, an optimal question order or our agents' accuracy |
| CANMAT update, 2024 [CANMAT_2023] | Professional guideline discussion highlights heterogeneity of persistent depressive presentations | We do not turn chronicity into a single treatment or diagnosis shortcut |

Books/classification sources establish definitions; guidelines support assessment domains; research motivates design and evaluation. No AI benchmark supplies PDD diagnostic definitions or validates these prompts.

## 9. Evidence output: structure, values and context

The exact contract is `PDD/evidence_output.schema.json`; examples are in `PDD/examples.json`. This is a proposed snapshot output, not the final integrated agent interface.

| Shared item | Meaning |
|---|---|
| `module_id` | Fixed `adult_pdd`; prevents treating the output as an MDD result |
| `schema_version` | Contract version, independent of clinical classification edition |
| `concept_id` | Concept from this package |
| `episode_key` | Application-supplied assessment-period key; can denote a longstanding background or a separate recent episode |
| `subject` | Patient; relative's symptoms are not patient's evidence |
| `finding_status` | What is reported/denied/unclear/conflicting; not whether a criterion is clinically met |
| `temporal_status` / `time_reference` | Current/historical/unclear and original time expression |
| `attributes` | Concept-specific optional details with explicit knowledge states |
| `evidence` | Exact patient quotations, source messages and earlier contextual references |
| `uncertainty_notes` | Ambiguity, contradictions or limitations |
| `semantic_check_status` | Support declaration or need for review; not proof of correct clinical meaning |

There is no LLM-generated evidence UUID. The application supplies message/period IDs. The proposed record identity is `(concept_id, episode_key, subject)`; new source statements can be retained under that record. Different periods are not silently merged.

### State values — our engineering choices

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

An omitted record means no extracted report, not symptom absence. An omitted detail is not zero or denied. `known` requires an evidence-supported value; `unknown` cannot carry one; `not_applicable` requires a reason. A controlled value `unclear` describes an explicitly ambiguous report, whereas an unknown detail may not have been established at all.

Every evidence entry has `message_id`, `quote`, `context_message_ids` and `supports`. `supports` names finding status and/or the known detail(s) supported. Context references must precede the source answer. A contextual “Yes.” retains that exact quote and the earlier question; the system must not expand it into invented patient wording. Exact quotation alone does not prove correct attribution or clinical interpretation.

### Fictional example and memory behaviour

In `examples.json`, the person first reports three years of low mood and trouble falling asleep. The first snapshot does not copy the mood duration into sleep. A later contextual “Yes.” explicitly answers the sleep-duration question, so that detail can be added.

The person also reports six weeks of feeling better while still low and sleeping badly. That is recorded as partial improvement, not a symptom-free interval or clinical remission. A later hopeless statement remains hopelessness evidence; it does not manufacture suicidal intent.

Corrections need their own retained sources. For a contradiction in the same period, mark `conflicting`/`needs_review` and explain it. The validator checks source structure, not whether a correction semantically resolves the contradiction. A live merge engine is not included.

## 10. Follow-ups and conversational handling

These are proposed project priorities, not a validated fixed interview order:

1. Address immediate safety/medical needs when indicated.
2. Establish the person's long-term concern and reference period.
3. Clarify mood pattern, associated groups and overlap, using existing answers.
4. Explore better intervals and recent worsening without assuming what they mean.
5. Review functioning, relevant alternatives, previous care and applicable features.
6. Summarize what is supported, unclear, declined or still needs professional assessment.

Extract all useful clinical information from each answer before choosing a new target. A useful off-topic answer is still saved. Return gently to an unanswered important target if needed; unrelated responses do not justify pressure. A decline remains a decline. Do not ask for a numeric day percentage when “most of the day” already answers the target.

For each concept, use its card's follow-up focus and only missing relevant details. Do not ask every optional field simply because it exists. The final cross-disorder graph, burden/stop rules and standardized instrument placement remain separate implementation work.

## 11. Screening, measurement and professional handoff

A two-week PHQ measure cannot establish a two-year PDD course. PHQ-9 may inform current symptom burden, with its original administration and clinical interpretation; it cannot automatically establish PDD continuity or remission. Keep scores, symptom evidence and diagnostic conclusions separate. [PHQ9_2001; PHQ9_FORM]

Any tool policy must specify version, validated language/population, timeframe, missing-answer handling and follow-up pathway. Do not reconstruct official scores from freely paraphrased conversation. Instrument selection and placement are not finalized here.

Proposed handoff: persistent-course account; mood and associated groups with quotations; intervals and uncertainties; current/past MDE review; functioning; activation/medical/exposure review; applicable feature clues; safety concerns and actions actually taken; previous care; conflicting/declined/missing information; and professional-review questions. Do not output a confirmed diagnosis from this extractor.

## 12. Source audit: important discrepancies

The older SAMHSA exhibit contains a broader feature-specifier list than APA's 2022 correction. Its persistent-MDE line also says “have not been met throughout,” whereas the checked DSM-5-TR definition says full requirements have been met throughout; its severity list ends in “Major” rather than the current “Severe.” We do not adopt those discrepancies. Primary current text and official correction take precedence. [SAMHSA_PDD; APA_PDD; DSM_PDD]

The NIMH public overview describes PDD as less severe. This simplified wording is not used as a diagnostic severity ceiling: inspected DSM-5-TR text and the APA correction allow persistent full major depressive episodes. The structured source-precedence note records this distinction. NIMH remains useful for accessible domain descriptions. [NIMH_DEP; DSM_PDD; APA_PDD]

The source registry records which material was full text and which was abstract/indexed text. Public mirror access does not establish permission to redistribute a proprietary manual. No manual PDF is included.

| ID | Source and inspected location | Use / access limits |
|---|---|---|
| `NICE_222` | [NICE NG222, Depression in adults](https://www.nice.org.uk/guidance/ng222/chapter/Recommendations); 1.2.1–1.2.9; Definitions of depression/severity; 1.12.1 | Comprehensive assessment, communication, safety and specialist review. Official search-indexed recommendation extracts inspected; direct retrieval intermittently 403 |
| `NIMH_DEP` | [NIMH, Depression](https://www.nimh.nih.gov/health/publications/depression); Signs/symptoms; diagnosis; age-presentation paragraphs | Plain-language symptom domains and adult context. Public primary-source material inspected |
| `NIMH_BIPOLAR` | [NIMH, Bipolar Disorder](https://www.nimh.nih.gov/health/publications/bipolar-disorder); Types; symptom comparison; diagnosis | Activation history, reduced sleep need and bipolar uncertainty. Public primary-source material inspected |
| `NICE_185` | [NICE CG185, Bipolar disorder](https://www.nice.org.uk/guidance/cg185/chapter/recommendations); 1.2.1 | Recognition/referral recommendation, not a four-day bipolar diagnostic shortcut. Public primary-source material inspected |
| `CANMAT_2016` | [CANMAT 2016 MDD guideline, Section 1](https://journals.sagepub.com/doi/10.1177/0706743716659416); Table 4, episode specifiers and clinical dimensions | Descriptive melancholic/atypical and other feature map. Indexed table inspected; older guideline, cross-checked against 2022 text |
| `CANMAT_2023` | [CANMAT 2023 update, published 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11351064/); Diagnostic/clinical-presentation discussion; Q.5.a measurement-based care | Professional guideline context and measurement alongside assessment. Indexed text inspected; direct PMC access intermittently blocked |
| `ANXIOUS_STUDY` | [McIntyre et al., 2016, anxious distress in adults with MDD](https://doi.org/10.1177/2040622315627805); Introduction: DSM anxious-distress definition | Five feature domains and majority-of-days context. Primary observational study; indexed text inspected; not validation of our agents |
| `ASQ_BSSA` | [NIMH Adult Outpatient Brief Suicide Safety Assessment Guide](https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials/adult-outpatient/adult-outpatient-brief-suicide-safety-assessment-guide); Intended users; thoughts, plan, past behaviour, supports and disposition sections | Safety information domains; clinician guide following positive ASQ, not autonomous LLM validation. Public primary-source material inspected |
| `NICE_225` | [NICE NG225, Self-harm](https://www.nice.org.uk/guidance/ng225/chapter/recommendations); 1.6.1–1.6.6 | No predictive low/medium/high stratification; needs-focused assessment. Public primary-source material inspected |
| `PHQ9_2001` | [Kroenke et al., 2001, PHQ-9 validity](https://pmc.ncbi.nlm.nih.gov/articles/PMC1495268/); Abstract; Methods; diagnostic-status comparison | Original validation of symptom/severity measure versus independent interview. Public primary-source material inspected |
| `PHQ9_FORM` | [PHQ-9 form hosted by AHRQ](https://integrationacademy.ahrq.gov/sites/default/files/2020-07/PHQ-9.pdf); pp.1–2 | Original response categories and scoring; form not reproduced here. Public primary-source material inspected |
| `APA_GRIEF` | [APA, What Is Depression?](https://www.psychiatry.org/patients-families/depression/what-is-depression); Grief versus depression discussion | Loss context and possible coexistence. Public primary-source material inspected |
| `DSM_PDD` | [APA DSM-5-TR, Depressive Disorders (2022)](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders); Printed pp.193–196; mirror PDF viewer pp.320–324. Shared specifier definitions pp.210–214 / viewer pp.342–347. | PDD requirements, course/onset, MDD relationship, differential and feature applicability. Original APA text inspected through public psychiatry.ru mirror after publisher access failed. No redistribution permission inferred; no book PDF bundled. |
| `APA_PDD` | [APA DSM-5-TR PDD fact sheet (2022)](https://www.psychiatry.org/getmedia/fd3dfaad-d409-4e94-8605-0350adec5b91/APA-DSM5TR-PersistentDepressive.pdf); p.1, Rationale for Change | Category breadth and removal of extraneous feature specifiers. Free official full fact sheet inspected |
| `SAMHSA_PDD` | [SAMHSA TIP 42 (2020)](https://www.ncbi.nlm.nih.gov/sites/books/NBK571020/pdf/Bookshelf_NBK571020.pdf); Exhibit 4.2, body pp.74–75 / PDF viewer pp.104–105 | Mood, six associated symptom groups and continuity information; current APA text takes precedence. Public government manual inspected. Older specifiers and apparent persistent-MDE/severity wording errors are explicitly not adopted. |
| `PDD_SURVEY_2020` | [Persistent depressive disorder across the adult lifespan: clinical and population surveys in Germany (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7011512/); Methods: Assessment of chronicity; Discussion | Research example of reconstructing chronic course from interview history; definitions depend on ascertainment. Primary study; official indexed Methods extracts inspected. Older DSM-IV-based interviews do not replace current DSM-5-TR requirements. |
| `PDD_FOLLOWUP_2023` | [Koshikawa et al., Characteristics of persistent depression in the long-term (2023)](https://pubmed.ncbi.nlm.nih.gov/37886758/); Abstract and indexed article Results/Discussion; DOI 10.1016/j.heliyon.2023.e20917 | Primary follow-up research motivating residual-symptom and course records, not a diagnostic algorithm. Abstract/indexed primary article excerpts inspected; no treatment recommendation or model-validation claim inferred. |

## 13. Coverage audit and boundaries

The package documents adult scope; clinical requirements; seven primary concepts (mood plus six associated groups); continuity/intervals; MDE relationship; onset/course; applicable feature evidence; relevant context/alternatives; safety domains; concept-specific output and examples. The machine coverage list is in `knowledge.json`.

This is a documentation/contract completion statement for the declared assessment scope, not a claim of all possible PDD knowledge or clinical validity. Remaining external/implementation work: expert clinical review; operational safety response; final question graph; tool/language policy; agent integration; semantic/model evaluation and clinical evaluation. Prescribing, full medical examination and full diagnosis of every alternative are outside this module.

Run `python validate_package.py` from the PDD folder for mechanical checks. These checks do not prove diagnostic accuracy, semantic correctness or safety. Creating this PDD package did not alter the existing runtime. Subsequent Desktop-contract changes are recorded in the shared audit report; clinical review remains pending.
