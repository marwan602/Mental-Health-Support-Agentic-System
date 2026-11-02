# 04 — Adult PMDD assessment knowledge, evidence output and diary input

Version: 1.0.0-source-reviewed. Research date: 2 November 2026.

Scope: adult premenstrual dysphoric disorder (PMDD) assessment and provisional explanation for professional review. This is a source-reviewed information/contract package, not clinical validation, a prescribing guide or a connected agent runtime.

## 1. Meaning and applicability

PMDD concerns a recurring menstrual-cycle-linked symptom pattern with significant distress or interference. Our implementation starts at 18+. Assess actual reproductive/menstrual context rather than assuming applicability from gender or assigning a fixed upper age. NHS describes menstrual applicability; unusual absent/irregular bleeding or hormonal contexts may need specialist review. [NHS_PMDD; ISPMD_2011]

The adult scope is ours; ACOG's guideline also addresses adolescents. We are not implementing its adolescent pathway here. ACOG describes a broader premenstrual-disorders spectrum; DSM PMDD is one particular diagnosis, not an alias for every premenstrual problem. [ACOG_7]

## 2. Clinical foundation and criteria-information map

The DSM pattern is at least five of eleven symptom groups, including at least one of four core affective groups and additional symptom group(s), in the final premenstrual week. Symptoms begin improving within days after menses starts and become minimal/absent in the postmenstrual week. The pattern is required in most cycles over the preceding year. [DSM_PMDD]

Significant distress **or** interference is required; do not require both. Review whether this is merely worsening of another disorder and whether medical/substance/treatment effects explain it. Another condition can coexist; it does not automatically exclude PMDD. Prospective daily ratings across at least two symptomatic cycles are needed for confirmation; the manual permits a provisional professional diagnosis beforehand. Our extractor does not issue either as a confirmed diagnosis. [DSM_PMDD]

| Map | Information our system must preserve |
|---|---|
| A | Cycle timing, total symptom pattern and recurrence history |
| B | Required core affective group(s) |
| C | Additional groups reaching the total |
| D | Distress or functional interference |
| E | Underlying disorder versus distinct cyclical pattern |
| F | Actual prospective daily-record coverage and limitations |
| G | Medical, substance/medication and hormone explanations |

The criteria map is a reference for professional review, not an automatic classifier. A day of irritability or a diary's existence alone does not establish PMDD.

## 3. Counting and interpretation safeguards

Core groups: mood lability; irritability/anger/conflict; depressive affect/hopelessness/self-critical thoughts; anxiety/tension. Additional groups: reduced interest; concentration difficulty; low energy; appetite/cravings; sleep; overwhelmed/out-of-control feelings; physical symptoms. These are eleven groups, not the number of separate words mentioned. [ACOG_7; DSM_PMDD]

Multiple alternatives within one group count once. Breast tenderness plus bloating is one physical group. Appetite change plus cravings is one appetite group. Do not count hopelessness separately from depressive affect in this framework. Do not automatically count tearfulness under both lability and depression without supporting distinct information.

PMDD does not require depressed mood specifically if another required core affective group qualifies. Conversely, physical symptoms alone are insufficient. These are source-based assessment distinctions, not an instruction to turn reported presence into criterion satisfaction. [DSM_PMDD]

## 4. Concept cards: meanings, output details and follow-ups

Clinical domains are sourced. All field names, controlled value sets, conversational examples and priorities are project designs, not a validated questionnaire. Every detail is optional on an individual report; do not force all symptoms into an identical form. Sources do not mandate our schema.

### Mood lability — `mood_lability`

Marked mood swings, sudden sadness/tearfulness or rejection sensitivity.

Role: `core_affective`. PMDD count group: `lability`. Sources: [DSM_PMDD; NHS_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `changes` | Actual mood shifts or rejection-related experiences. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** What kinds of mood changes have you noticed around that time?

**Follow-up focus:** Clarify actual shifts and cycle relationship.

**Do not infer:** Tearfulness alone does not automatically establish lability and a separate depressed-mood group.

### Irritability, anger or conflict — `irritability_anger`

Marked irritability/anger or increased interpersonal conflict.

Role: `core_affective`. PMDD count group: `irritability`. Sources: [DSM_PMDD; NHS_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `examples` | Reported irritability, anger or conflict; avoid blaming language. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** Have you noticed changes in irritability or how you get along with others?

**Follow-up focus:** Collect examples and whether the change switches off outside the relevant interval.

**Do not infer:** Anger and conflict are alternatives within one group, not two criteria.

### Depressed mood, hopelessness or self-critical thoughts — `depressed_affect`

Marked depressive affect or the specified negative thoughts.

Role: `core_affective`. PMDD count group: `depressive_affect`. Sources: [DSM_PMDD; NHS_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `content` | Actual mood, future expectations or self-critical thought content. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** How do you feel about yourself and the future during those days?

**Follow-up focus:** Distinguish cyclical change from symptoms throughout the month.

**Do not infer:** Do not count hopelessness and depressed mood as two PMDD groups; assess suicide concerns separately.

### Anxiety or tension — `anxiety_tension`

Marked anxiety, tension, or keyed-up/on-edge feelings.

Role: `core_affective`. PMDD count group: `anxiety`. Sources: [DSM_PMDD; NHS_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `experience` | What the anxious/tension experience is like. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** What is anxiety or tension like for you during that time?

**Follow-up focus:** Clarify severity and the rest-of-cycle pattern.

**Do not infer:** Anxiety alone does not establish a separate anxiety disorder or PMDD.

### Reduced interest — `reduced_interest`

Less interest in usual activities.

Role: `additional_symptom`. PMDD count group: `interest`. Sources: [DSM_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `activities` | Usual activities with reduced interest or preserved engagement. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** Does your interest in your usual activities change during those days?

**Follow-up focus:** Distinguish loss of interest from lack of time/opportunity.

**Do not infer:** Do not import MDD's two-week duration requirement into this PMDD group.

### Concentration difficulty — `concentration_difficulty`

Subjective difficulty concentrating.

Role: `additional_symptom`. PMDD count group: `concentration`. Sources: [DSM_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `tasks` | Concrete attention-related tasks affected. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** Do you notice changes in concentration during those days?

**Follow-up focus:** Examples and timing, without assuming a cognitive disorder.

**Do not infer:** An isolated forgotten task is not a clinical threshold.

### Low energy/fatigue — `low_energy`

Lethargy, easy fatigue or marked lack of energy.

Role: `additional_symptom`. PMDD count group: `energy`. Sources: [DSM_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `experience` | Fatigue/low energy versus sleepiness as actually reported. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** How does your energy compare at different points in the month?

**Follow-up focus:** Clarify the cycle pattern and effect on activity.

**Do not infer:** Do not attribute all fatigue to the menstrual cycle or PMDD.

### Appetite, overeating or cravings — `appetite_cravings`

Marked appetite change, overeating or specific food cravings.

Role: `additional_symptom`. PMDD count group: `appetite`. Sources: [DSM_PMDD; NHS_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `pattern` | Reported experience. | appetite_change / overeating / specific_cravings / mixed / unclear |
| `details` | Appetite direction, actual eating or named craving, as supplied. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |

**Example question:** Have you noticed changes in appetite, eating or cravings at that time?

**Follow-up focus:** Preserve which experience was reported.

**Do not infer:** These alternatives count as one group; appetite change does not establish weight change.

### Sleep disturbance — `sleep_disturbance`

Excessive sleep or insomnia.

Role: `additional_symptom`. PMDD count group: `sleep`. Sources: [DSM_PMDD; NIMH_BIPOLAR].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `pattern` | Reported sleep complaint. | onset_difficulty / maintenance_difficulty / early_waking / excessive_sleep / mixed / unclear |
| `sleep_hours` | Reported sleeping time with units/reference period. | Supported text; preserve timing and uncertainty |
| `sleep_opportunity` | Opportunity to sleep and external interruptions. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `latency` | Reported time needed to fall asleep, not months of symptom recurrence. | Supported text; preserve timing and uncertainty |
| `awakenings` | Night waking and return-to-sleep account. | Supported text; preserve timing and uncertainty |
| `wake_timing` | Actual versus usual/intended waking time. | Supported text; preserve timing and uncertainty |
| `daytime_effects` | Reported sleepiness, exhaustion or other daytime effects. | Supported text; preserve timing and uncertainty |

**Example question:** Does your sleep change around that time?

**Follow-up focus:** Identify complaint before subtype-specific follow-ups.

**Do not infer:** Insomnia with fatigue is not reduced sleep need; do not infer cycle timing from another symptom.

### Overwhelmed or out of control — `overwhelmed_control`

Feeling overwhelmed or out of control.

Role: `additional_symptom`. PMDD count group: `overwhelmed`. Sources: [DSM_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `meaning` | What overwhelmed or out of control means to the person. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** Do you feel overwhelmed or out of control during those days?

**Follow-up focus:** Clarify the meaning and timing without interpreting it as psychosis.

**Do not infer:** Do not automatically translate this into dangerous behaviour or a psychotic symptom.

### Physical symptom group — `physical_symptoms`

Breast tenderness/swelling, joint/muscle pain, bloating or reported weight gain.

Role: `additional_symptom`. PMDD count group: `physical`. Sources: [DSM_PMDD; NHS_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `description` | The person's account of this experience; do not add a diagnosis. | Supported text; preserve timing and uncertainty |
| `symptoms` | Actual physical symptoms; multiple symptoms remain one PMDD group. | Supported text; preserve timing and uncertainty |
| `weight_if_reported` | Amount/units/time interval only if actually supplied; distinguish sensation of bloating. | Supported text; preserve timing and uncertainty |
| `onset_relative_to_bleeding` | When this symptom starts relative to a reported period, preserving actual wording. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When this symptom starts to improve; improvement is not necessarily disappearance. | Supported text; preserve timing and uncertainty |
| `postmenstrual_level` | This symptom outside the premenstrual interval; absent, low, persistent or unclear as actually described. | Supported text; preserve timing and uncertainty |
| `duration_within_cycle` | How long this symptom lasts within a cycle; not how many months the recurring pattern has existed. | Supported text; preserve timing and uncertainty |
| `intensity_as_reported` | Reported severity/meaning; do not manufacture an instrument rating. | Supported text; preserve timing and uncertainty |
| `impact` | Concrete consequence of this symptom. | Supported text; preserve timing and uncertainty |

**Example question:** What physical changes, if any, do you notice around that time?

**Follow-up focus:** Identify each report and its own timing; distinguish pain at menses from premenstrual affective pattern.

**Do not infer:** Breast tenderness plus bloating is not two PMDD criteria; bloating is not a measured weight gain.

### Cycle/reproductive context — `cycle_context`

Reported cycles, bleeding and reproductive circumstances relevant to interpretation.

Role: `cycle_context`. PMDD count group: `supporting information; no extra symptom count`. Sources: [ACOG_7; ISPMD_2011].

| Detail | Meaning | Values/form |
|---|---|---|
| `bleeding_pattern` | Reported pattern. | regular / irregular / absent / unclear |
| `recent_periods` | Actual reported onset/offset dates and uncertainty. | Supported text; preserve timing and uncertainty |
| `usual_cycle_length` | Reported length/variability, not assumed 28 days. | Supported text; preserve timing and uncertainty |
| `reproductive_context` | Relevant pregnancy/postpartum/perimenopausal, surgery or other context if supplied. | Supported text; preserve timing and uncertainty |
| `hormonal_context` | Whether a treatment may affect bleeding/ovarian activity. | Supported text; preserve timing and uncertainty |
| `ovulation_information` | Only actual available evidence; no inference from cycle day. | Supported text; preserve timing and uncertainty |

**Example question:** What is your usual pattern of periods, and has it changed recently?

**Follow-up focus:** Establish actual context before interpreting timing.

**Do not infer:** Do not infer ovulation on day 14 or equate no bleeding with no ovarian activity.

### Symptom timing across cycles — `cyclical_timeline`

Reported onset, improvement, low-symptom interval and recurrence across cycles.

Role: `cycle_pattern`. PMDD count group: `supporting information; no extra symptom count`. Sources: [ACOG_7; DSM_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `onset_timing` | When the reported group of symptoms starts relative to bleeding. | Supported text; preserve timing and uncertainty |
| `improvement_timing` | When improvement starts after bleeding begins. | Supported text; preserve timing and uncertainty |
| `postmenstrual_course` | Actual symptoms after menses, not assumed absence. | Supported text; preserve timing and uncertainty |
| `history_duration` | How long the recurring pattern has been noticed; this alone does not establish the proportion of affected cycles. | Supported text; preserve timing and uncertainty |
| `preceding_year_pattern` | Reported recurrence over the preceding year; do not invent percentages. | Supported text; preserve timing and uncertainty |
| `cycles_described` | Which/how many cycles were recalled. | Supported text; preserve timing and uncertainty |
| `symptom_scope` | Which symptoms a shared timing statement explicitly refers to. | Supported text; preserve timing and uncertainty |
| `recall_limits` | Uncertainty, variability or incomplete recall. | Supported text; preserve timing and uncertainty |

**Example question:** What happens to those symptoms after your period starts?

**Follow-up focus:** Clarify onset and switching-off pattern; distinguish prospective data from memory.

**Do not infer:** Two retrospective examples do not establish prospective confirmation or the year-long pattern.

### Symptoms outside the premenstrual interval — `background_symptoms`

The rest-of-cycle symptom pattern, including ongoing illness or distinct cyclical symptoms.

Role: `differential_context`. PMDD count group: `supporting information; no extra symptom count`. Sources: [DSM_PMDD; ISPMD_2011; ACOG_7].

| Detail | Meaning | Values/form |
|---|---|---|
| `symptoms` | What remains present outside the reported premenstrual days. | Supported text; preserve timing and uncertainty |
| `timing` | When and how persistently those symptoms occur. | Supported text; preserve timing and uncertainty |
| `baseline_intensity` | Reported background burden. | Supported text; preserve timing and uncertainty |
| `premenstrual_difference` | What changes premenstrually, including whether symptoms are the same or distinct. | Supported text; preserve timing and uncertainty |

**Example question:** How do you feel at other times in the month?

**Follow-up focus:** Assess symptom-by-symptom pattern rather than ruling in/out from a global answer.

**Do not infer:** Any background condition does not automatically exclude coexisting PMDD; mere worsening of it is not sufficient for PMDD.

### Prospective-record history — `prospective_records`

What diary/rating records exist and what remains unverified.

Role: `measurement_context`. PMDD count group: `supporting information; no extra symptom count`. Sources: [ACOG_7; DRSP_2006; CPASS_2017].

| Detail | Meaning | Values/form |
|---|---|---|
| `availability` | What is reported. | not_collected / reportedly_available / unclear |
| `instrument` | Tool/version/language actually used, if known. | Supported text; preserve timing and uncertainty |
| `coverage` | Actual dates/cycles supplied, not assumed complete. | Supported text; preserve timing and uncertainty |
| `recording_method` | Same-day versus recalled/backfilled entries as reported. | Supported text; preserve timing and uncertainty |
| `missingness` | Reported gaps or incomplete entries. | Supported text; preserve timing and uncertainty |
| `review_history` | Professional review actually reported; not our confirmation. | Supported text; preserve timing and uncertainty |

**Example question:** Have you kept daily symptom ratings across complete cycles?

**Follow-up focus:** Ask about records and obtain the actual data through the application, not reconstructed LLM scores.

**Do not infer:** A statement that a diary exists is not diary verification; retrospective chat never becomes prospective data.

### Hormonal exposure context — `hormone_exposure`

Reported contraception/hormone treatment and relevant changes.

Role: `exposure_context`. PMDD count group: `supporting information; no extra symptom count`. Sources: [DSM_PMDD; ISPMD_2011].

| Detail | Meaning | Values/form |
|---|---|---|
| `treatment` | Name/formulation as supplied; do not infer composition. | Supported text; preserve timing and uncertainty |
| `start_change_stop` | Dates of starting/changing/stopping. | Supported text; preserve timing and uncertainty |
| `regimen` | Continuous/cyclic/unknown as actually reported. | Supported text; preserve timing and uncertainty |
| `bleeding_relationship` | Bleeding changes including possible withdrawal bleeding. | Supported text; preserve timing and uncertainty |
| `symptom_relationship` | Reported temporal association; no causal conclusion. | Supported text; preserve timing and uncertainty |

**Example question:** Have hormonal treatments or contraception changed around the time these symptoms changed?

**Follow-up focus:** Preserve actual exposure and dates for medical review.

**Do not infer:** Do not advise stopping/changing hormones or assume bleeding confirms ovulation.

### Premenstrual exacerbation review — `pme_review`

Possible premenstrual worsening of an underlying condition; not a new diagnosis assigned by the extractor.

Role: `differential_context`. PMDD count group: `supporting information; no extra symptom count`. Sources: [ISPMD_2011; DSM_PMDD].

| Detail | Meaning | Values/form |
|---|---|---|
| `underlying_history` | Reported condition and who diagnosed it. | Supported text; preserve timing and uncertainty |
| `baseline_pattern` | Symptoms outside the premenstrual interval. | Supported text; preserve timing and uncertainty |
| `worsening_pattern` | What becomes worse, when and how much, as reported. | Supported text; preserve timing and uncertainty |
| `distinct_symptoms` | Possible new cyclical symptoms distinct from the underlying pattern. | Supported text; preserve timing and uncertainty |
| `records_needed` | Unresolved cycle-wide symptom information. | Supported text; preserve timing and uncertainty |

**Example question:** Are these the same difficulties you have at other times, or do different symptoms appear?

**Follow-up focus:** Preserve uncertainty until cycle-wide evidence and professional review are available.

**Do not infer:** Do not classify PMDD or PME from one sentence, or force them into a simplistic binary for every case.

### Death/suicide-related reports — `death_suicide`

Death/suicide-related reports requiring separate safety assessment; not an additional PMDD symptom-count group.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [ASQ_BSSA; NICE_222].

| Detail | Meaning | Values/form |
|---|---|---|
| `experience` | Preserve distinctions. | death_thoughts / wish_not_alive / suicidal_thoughts / suicide_plan / suicide_attempt / unclear |
| `recency` | When last/current; do not infer resolution. | Supported text; preserve timing and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve timing and uncertainty |
| `intent` | Intent as reported. | Supported text; preserve timing and uncertainty |
| `plan_present` | Whether a plan was explicitly reported or denied. | reported / denied / unclear |
| `access` | Access to means as reported, without generating procedural details. | Supported text; preserve timing and uncertainty |
| `past_behaviour` | Historical self-injury/attempt account, intent and timing. | Supported text; preserve timing and uncertainty |
| `support` | Available support as reported. | Supported text; preserve timing and uncertainty |

**Example question:** Have you had thoughts about ending your life?

**Follow-up focus:** Use dedicated safety pathway; preserve current versus historical information.

**Do not infer:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [NICE_222].

| Detail | Meaning | Values/form |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text; preserve timing and uncertainty |
| `examples` | Concrete difficulty or distress. | Supported text; preserve timing and uncertainty |
| `baseline` | Usual functioning. | Supported text; preserve timing and uncertainty |
| `supports` | Assistance helping preserve functioning. | Supported text; preserve timing and uncertainty |

**Example question:** How have these changes affected your daily life?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Activation history — `activation_history`

Possible distinct elevated/overactive periods requiring review.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [NIMH_BIPOLAR].

| Detail | Meaning | Values/form |
|---|---|---|
| `period` | Current/historical time. | Supported text; preserve timing and uncertainty |
| `mood` | Elevated, expansive or irritable mood as reported. | Supported text; preserve timing and uncertainty |
| `energy_activity` | Change in energy/activity. | Supported text; preserve timing and uncertainty |
| `sleep_need` | Sleep need and tiredness, not just sleep hours. | Supported text; preserve timing and uncertainty |
| `other_changes` | Associated speech, thoughts, confidence or risky behaviour. | Supported text; preserve timing and uncertainty |
| `duration` | Duration of that period. | Supported text; preserve timing and uncertainty |
| `impact` | Consequences or other observers. | Supported text; preserve timing and uncertainty |
| `exposure_context` | Medicines/substances/medical context. | Supported text; preserve timing and uncertainty |

**Example question:** Have you had a distinct period of unusually increased energy or activity?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Medical context — `medical_context`

Relevant reported medical history and symptoms.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [VA_2022; NICE_222].

| Detail | Meaning | Values/form |
|---|---|---|
| `conditions` | Reported conditions; distinguish reported diagnosis from confirmation. | Supported text; preserve timing and uncertainty |
| `timeline` | Relationship to symptoms. | Supported text; preserve timing and uncertainty |
| `investigations` | Results only if actually supplied. | Supported text; preserve timing and uncertainty |
| `clinician_review` | Known professional assessment or unresolved need. | Supported text; preserve timing and uncertainty |

**Example question:** Are there health conditions that might be relevant to these changes?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Medicines and substances — `exposure_context`

Relevant treatment/substance exposure account.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [NICE_222; VA_2022].

| Detail | Meaning | Values/form |
|---|---|---|
| `name` | Named exposure. | Supported text; preserve timing and uncertainty |
| `dose_use` | Reported amount/use; never recommend a dose. | Supported text; preserve timing and uncertainty |
| `start_change_stop` | Timing of changes. | Supported text; preserve timing and uncertainty |
| `symptom_timing` | Reported temporal relationship. | Supported text; preserve timing and uncertainty |
| `source_kind` | Medicine, alcohol, other substance or unclear. | Supported text; preserve timing and uncertainty |

**Example question:** Have any medicines or substance-use patterns changed around this time?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Psychotic experiences — `psychotic_experience`

Reported experiences requiring specialist interpretation.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [DSM_PMDD; NICE_222].

| Detail | Meaning | Values/form |
|---|---|---|
| `kind` | Experience as described, not an automatic diagnosis. | Supported text; preserve timing and uncertainty |
| `content` | Brief relevant content without affirming beliefs. | Supported text; preserve timing and uncertainty |
| `mood_relationship` | During versus outside mood episodes. | Supported text; preserve timing and uncertainty |
| `conviction_context` | Reported belief/context and uncertainty. | Supported text; preserve timing and uncertainty |
| `safety_concerns` | Any reported urgent implications. | Supported text; preserve timing and uncertainty |
| `reported_mood_congruence` | Professional mood-congruence description if actually supplied; do not invent it. | congruent / incongruent_or_mixed / unclear |

**Example question:** Have you had experiences that other people do not seem to share?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [NICE_222].

| Detail | Meaning | Values/form |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text; preserve timing and uncertainty |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text; preserve timing and uncertainty |
| `period` | When and for which symptoms. | Supported text; preserve timing and uncertainty |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text; preserve timing and uncertainty |
| `use` | Actual use and barriers as reported. | Supported text; preserve timing and uncertainty |

**Example question:** Have you received help for something similar before?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Family history — `family_history`

Relevant family mood/psychiatric history.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [VA_2022].

| Detail | Meaning | Values/form |
|---|---|---|
| `relative` | Relationship, without unnecessary identifying details. | Supported text; preserve timing and uncertainty |
| `reported_condition` | Condition as reported. | Supported text; preserve timing and uncertainty |
| `certainty` | How the person knows; unknown remains unknown. | Supported text; preserve timing and uncertainty |

**Example question:** Is there relevant mental-health history in your family?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Life context — `life_context`

Relevant stress, loss, trauma and support.

Role: `supporting_review`. PMDD count group: `supporting information; no extra symptom count`. Sources: [NICE_222; APA_GRIEF].

| Detail | Meaning | Values/form |
|---|---|---|
| `events` | Events relevant to symptom timeline. | Supported text; preserve timing and uncertainty |
| `timing` | Temporal relationship. | Supported text; preserve timing and uncertainty |
| `support` | Current supports. | Supported text; preserve timing and uncertainty |
| `barriers` | Practical barriers. | Supported text; preserve timing and uncertainty |
| `meaning` | Person's interpretation of the context. | Supported text; preserve timing and uncertainty |

**Example question:** Has anything important been happening around the time these changes began?

**Follow-up focus:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

## 5. Cycle timing: what the data must show

Record actual bleeding dates/type, symptom onset, improvement, postmenstrual levels, rest-of-cycle symptoms and variability. A shared timing statement can cover several symptoms only when the person explicitly refers to them together. Do not copy timing by proximity. A calendar date is not proof of ovulation or a biological phase.

ISPMD distinguishes core PMD from variants, including exacerbation of an underlying disorder and hormone-related/absent-bleeding contexts. Ovarian activity may continue despite absent bleeding in some situations. These are specialist-review contexts, not extra DSM PMDD diagnoses our agent assigns. [ISPMD_2011]

Do not assume a 28-day cycle or day-14 ovulation. Preserve irregularity, possible withdrawal bleeding, treatment changes and uncertainty. Persistent low mood all month requires a different review from a symptom that switches on/off; distinct symptoms may have different patterns. Treatment effects or pregnancy/postpartum/perimenopausal concerns need appropriate medical context rather than a forced PMDD label. [ISPMD_2011; DSM_PMDD]

## 6. PMDD, PMS, PME and other explanations

| Explanation | What we need | Boundary |
|---|---|---|
| PMDD-like pattern | Affective/additional symptoms, cycle-wide timing, burden and prospective data | Retrospective description is not confirmation |
| PMS / broader PMD | Symptoms, burden and timing without assuming DSM PMDD count/core requirements | Do not automatically label every non-PMDD case PMS |
| Premenstrual exacerbation (PME) | Existing symptoms throughout the cycle with premenstrual worsening | Mere exacerbation is insufficient for PMDD; distinct coexisting symptoms still require review |
| MDD/PDD/anxiety/bipolar illness | Background symptoms, lifetime course and activation history | Cycle worsening does not erase the underlying condition |
| Dysmenorrhea or another gynecological concern | Pain and its timing, associated symptoms and medical history | Pain at menstruation is not itself PMDD |
| Medicine/hormone/substance effects or medical illness | Exposures, changes and symptom timing; relevant clinician findings | Temporal association alone is not causation; do not advise medication withdrawal |

These boundaries come from DSM/ACOG/ISPMD discussion, with different frameworks kept labelled. We collect focused clues and professional-review needs, not full management of every alternative. Normal laboratory values do not establish PMDD; examinations/tests may address other explanations when clinically indicated. Do not invent a universal hormone panel. [DSM_PMDD; ACOG_7; ISPMD_2011]

## 7. Prospective symptom records

ACOG recommends prospective cycle-wide recording, commonly over two consecutive cycles, to reduce recall bias and distinguish patterns. This practical recommendation is separately labelled from DSM's at-least-two-symptomatic-cycles wording. ISPMD recommends another cycle when the first two are inconsistent; it is not permission to select only convenient positive days. [ACOG_7; ISPMD_2011]

Use the full cycle, including less symptomatic days, and preserve missingness. Two dates are not two cycles. Two cycles with inadequate entries are not automatically sufficient. A historical conversation cannot be relabelled prospective; a claim that tracking occurred is not verification of the actual records. Necessary clinical help must not be delayed merely to finish a diary.

### Candidate measures and what each contributes

| Measure | Role | Limits |
|---|---|---|
| DRSP [DRSP_2006] | Daily symptom/interference measure; original six-point scale | Version, language and administration need verification; no item set bundled |
| PSST [PSST_2003] | Retrospective premenstrual symptom screening | Does not replace prospective confirmation; no scoring implementation here |
| C-PASS [CPASS_2017] | Published scoring operationalization using daily DRSP data | Research method, not a DSM-mandated universal percentage or an implemented classifier here |
| PHQ or other general symptom measures | May inform another condition's current burden | Do not establish cyclical PMDD timing |

The DRSP paper describes 21 symptom items representing the clinical groups plus three interference items, scored 1–6 (not 0–3). Keep original item identifiers and responses separate from our concept summaries. Do not reuse PHQ scoring or translate a narrative severity word into an official rating. [DRSP_2006]

C-PASS evaluates relative change, absolute premenstrual severity, postmenstrual clearance and duration using specified windows. Its published windows include days −7 to −1 and +4 to +10 relative to menstrual onset, with protocol-specific completeness rules. These are research operationalizations, not permission to infer phase from a generic cycle day. The development sample involved naturally cycling adults with regular cycles and important exclusions; accuracy cannot be assumed for every hormonal/clinical context. This package does not implement the algorithm or reproduce its formulas. [CPASS_2017]

## 8. Structured diary input: separate from extracted conversation

`PMDD/diary_input.schema.json` defines a proposed storage format for original, version-verified DRSP responses. It is not a new validated questionnaire. The example file contains only two fictional partial days with unverified metadata and cannot establish PMDD.

| Item | Meaning |
|---|---|
| `instrument_id` | DRSP only for this contract; a project diary with another scale needs a different labelled contract |
| `instrument_version`, `language` | Actual source/version/language; schema validity does not verify them |
| `cycles` | Application cycle references with actual or unknown onset dates |
| `bleeding_events` | Reported menses, spotting, withdrawal bleeding or unclear events |
| `observation_date` | Day the rating concerns |
| `recorded_at` | Actual timestamp, or null when unavailable; do not manufacture one |
| `observation_utc_offset` | Actual offset for the observation calendar, used to compare dates correctly; unknown for unverified imports when unavailable |
| `collection_mode` | Prospective daily, retrospective entry or unverified import, supplied from provenance rather than guessed by the LLM |
| `item_id`, `rating` | Original item identifier 1–24 and rating 1–6, or null if missing |
| `missing_reason` | Reason for an explicit missing value; missing is not zero |
| `cycle_ref` | Supplied known cycle reference or null; does not prove ovarian phase |

The application must retain provenance and corrections. Duplicate day/item entries require explicit resolution rather than silent averaging. Timestamp/date consistency can be checked, but timestamps alone cannot prove that a person did not recall or backfill symptoms. No automatic imputation, cycle-phase calculator or C-PASS diagnosis is included.

## 9. Conversation evidence output

`PMDD/evidence_output.schema.json` is a proposed snapshot contract. `examples.json` shows valid fictional first/later snapshots. Message and assessment-period keys are application-supplied; there is no model-generated evidence UUID.

| Shared record item | Meaning |
|---|---|
| `concept_id` | Sourced domain or supporting-review concept |
| `episode_key` | Application assessment-period key; can represent a reported cycle pattern or a specific period |
| `subject` | Patient, not a relative's symptoms |
| `finding_status` | Explicit report, denial, unclear or conflicting account; not a clinically satisfied criterion |
| `temporal_status` / `time_reference` | Current/historical/unclear plus original timing expression |
| `attributes` | Only the concept's optional, meaningful fields |
| `evidence` | Exact patient quotations, source IDs, earlier context IDs and supported fields |
| `uncertainty_notes` | Attribution, recall, missing-data or contradictory-report limitations |
| `semantic_check_status` | A declaration of support/review need, not proof of correctness |

Absence of a record is not denial. Known details need linked supporting quotations; unknown details cannot carry invented values; inapplicable details need a reason. Exact quotations can still be clinically misinterpreted. Preserve corrections and separate periods rather than overwriting the whole patient's history.

### State values — project definitions

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

**`prospective_review_status`**

- `not_evaluated`: No assessment of actual supplied diary data.
- `no_diary_supplied`: No actual diary data supplied; reported existence is separate.
- `incomplete_or_unverified`: Some data available, but completeness/provenance or interpretation unresolved.
- `requires_professional_review`: Available information needs professional interpretation; not diagnostic confirmation.

The top-level `prospective_review` states deliberately contain no confirmed-diagnosis value. An available diary needs its actual completeness, provenance and clinical interpretation checked. `safety_handoff` uses the same non-predictive project states as the earlier modules; “no signal reported” never means safe.

### What the fictional example demonstrates

Irritability, mood swings and physical complaints initially describe three clinical groups, even though breast pain and bloating are both mentioned. The person reports about a year of noticing the pattern; the exact proportion of affected cycles remains unknown. Later information adds improvement timing and postmenstrual course. Persistent low mood outside that interval prompts further review; it does not automatically confirm PME or exclude distinct coexisting PMDD. A statement that no diary was kept stays separate from prospective confirmation. No diagnosis is assigned.

## 10. Adaptive follow-ups and safety

Proposed order: understand the concern and relevant menstrual context; address immediate safety/medical needs; establish symptom-by-symptom timing and burden; review the rest of the cycle and relevant alternatives; inspect existing records or prepare an appropriately supported tracking pathway; summarize missing information and professional-review needs. This is a project design, not a validated universal interview sequence.

After every answer, extract relevant clinical information across topics, update context-preserving memory, and ask only a meaningful unanswered target. A short yes/no needs its preceding question; ambiguous compound questions need clarification. Useful off-topic answers are saved. Explain a return to an important gap gently, respect declines and avoid repeating already supplied details.

Safety assessment is not limited to premenstrual days or postponed until two cycles are recorded. Preserve reported current thoughts, intent, past behaviour, supports and needs; follow a separately designed professional response pathway. No predictive low/medium/high label is used. The BSSA is a trained-clinician guide, not validation of an autonomous LLM. [ASQ_BSSA; NICE_225; ACOG_7]

## 11. Handoff and module boundaries

Proposed handoff: symptom groups and exact evidence; actual cycle/bleeding context; onset/improvement/rest-of-cycle pattern; distress/interference; preceding-year recurrence account; actual diary coverage and limitations; possible underlying/alternative explanations; medicines/hormones; previous care; safety concerns/actions actually taken; declined/uncertain/conflicting information; professional-review questions.

Unlike MDD, PMDD does not use a two-week episode threshold, and unlike PDD it does not use a two-year persistent-mood threshold. Do not copy MDD specifiers, remission rules or severity bands into PMDD. Record burden and course without inventing a PMDD severity instrument or a universal score cutoff. This module is DSM-oriented; an ICD-specific mapping is separate work.

## 12. Sources and exact parts used

| ID | Source / inspected location | Use and access limits |
|---|---|---|
| `NICE_222` | [NICE NG222, Depression in adults](https://www.nice.org.uk/guidance/ng222/chapter/Recommendations); 1.2.1–1.2.9; Definitions of depression/severity; 1.12.1 | Comprehensive assessment, communication, safety and specialist review. Official search-indexed recommendation extracts inspected; direct retrieval intermittently 403 |
| `NICE_225` | [NICE NG225, Self-harm](https://www.nice.org.uk/guidance/ng225/chapter/recommendations); 1.6.1–1.6.6 | No predictive low/medium/high stratification; needs-focused assessment. Public primary-source material inspected |
| `ASQ_BSSA` | [NIMH Adult Outpatient Brief Suicide Safety Assessment Guide](https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials/adult-outpatient/adult-outpatient-brief-suicide-safety-assessment-guide); Intended users; thoughts, plan, past behaviour, supports and disposition sections | Safety information domains; clinician guide following positive ASQ, not autonomous LLM validation. Public primary-source material inspected |
| `NIMH_BIPOLAR` | [NIMH, Bipolar Disorder](https://www.nimh.nih.gov/health/publications/bipolar-disorder); Types; symptom comparison; diagnosis | Activation history, reduced sleep need and bipolar uncertainty. Public primary-source material inspected |
| `NIMH_DEP` | [NIMH, Depression](https://www.nimh.nih.gov/health/publications/depression); Signs/symptoms; diagnosis; age-presentation paragraphs | Plain-language symptom domains and adult context. Public primary-source material inspected |
| `VA_2022` | [VA/DoD MDD Clinical Practice Guideline, 2022](https://www.healthquality.va.gov/HEALTHQUALITY/guidelines/MH/mdd/VADODMDDCPGFinal508.pdf); p.19 Sidebars 1–2; pp.140–141 Appendix K; Appendix I pp.127–131 | Episode foundation, work-up and measurement context; sidebar is abbreviated DSM-5-era material. Public primary-source material inspected |
| `APA_GRIEF` | [APA, What Is Depression?](https://www.psychiatry.org/patients-families/depression/what-is-depression); Grief versus depression discussion | Loss context and possible coexistence. Public primary-source material inspected |
| `DSM_PMDD` | [APA DSM-5-TR, Depressive Disorders (2022)](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders); Printed pp.197–201 / inspected mirror PDF viewer pp.325–330 | PMDD criteria, recording procedures, course and differential. Original APA text inspected through public psychiatry.ru mirror after publisher access failed; reuse permission not inferred; no manual PDF bundled. |
| `ACOG_7` | [ACOG Clinical Practice Guideline No.7, Management of Premenstrual Disorders (2023)](https://pubmed.ncbi.nlm.nih.gov/37973069/); Diagnostic Evaluation p.1520 / PDF p.5; Box 1 p.1521 / PDF p.6 | Symptom assessment, prospective records, distress/functioning and differential. Publisher page returned 402; ACOG-authored PDF inspected through DocRed-hosted mirror. Treatment recommendations are outside this module. |
| `ISPMD_2011` | [O’Brien et al., ISPMD Montreal consensus (2011)](https://doi.org/10.1007/s00737-010-0201-3); Table 1 and classification; Methods of measurement; consensus recommendations; PDF pp.4,7–8 | Core/variant PMD, PME, cycle-wide assessment and repeat-cycle review. Original consensus PDF inspected through public Asarina-hosted mirror; distinct framework, not substituted for DSM PMDD. |
| `DRSP_2006` | [Endicott, Nee & Harrison, DRSP reliability and validity (2006)](https://pubmed.ncbi.nlm.nih.gov/16172836/); pp.41–42 and Table 1 / inspected article PDF pp.1–3 | Prospective daily measurement, item structure and 1–6 scale. Primary paper inspected through PMDD research-site mirror. Original DSM-IV-era validation; item wording and tool not bundled. |
| `CPASS_2017` | [Eisenlohr-Moul et al., Carolina Premenstrual Assessment Scoring System (2017; online 2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5205545/); Tables 1–3; Development of the C-PASS; Participants and Procedure; Limitations | Research operationalization of cycle timing, symptom dimensions, missing data and DSM symptom grouping. Primary validation paper inspected via full/indexed PMC text; no implementation or universal accuracy claim adopted. |
| `PSST_2003` | [Steiner, Macdougall & Brown, Premenstrual Symptoms Screening Tool (2003)](https://pubmed.ncbi.nlm.nih.gov/12920618/); Abstract; development study | Retrospective screening-tool role, separate from prospective confirmation. Primary abstract/indexed material inspected; full questionnaire and scoring not reproduced or implemented. |
| `NHS_PMDD` | [NHS, PMDD](https://www.nhs.uk/conditions/pmdd-premenstrual-dysphoric-disorder/); Introduction; Symptoms; How PMDD is diagnosed | Plain-language symptom explanation and menstrual applicability. Free public guidance; simplified diagnostic summary does not replace formal criteria. |
| `RCOG_48` | [RCOG Green-top Guideline No.48, PMS management](https://www.rcog.org.uk/guidance/browse-all-guidance/green-top-guidelines/premenstrual-syndrome-management-green-top-guideline-no-48/); Guideline status page: 2016 edition, reviewed 2023, update in development | Version/access context; not treated as a new PMDD classification. Official status page/indexed guideline recommendation on prospective records inspected; no claim of completed newer edition. |

## 13. Coverage, checks and remaining work

Documented: adult applicability; criteria A–G; eleven groups with four affective core groups; grouping safeguards; actual cycle history; prospective versus retrospective evidence; PMS/PME and other focused alternatives; hormonal/medical context; burden and safety; tools/research limits; concept-specific evidence; diary input and fictional examples.

Run `python validate_package.py` in the PMDD folder. Checks cover contracts, sources, exact quotes, context order, grouping, diary value/date constraints and rejection of invalid fixtures. They do not establish semantic accuracy, diagnostic validity or safe real-patient use.

Remaining external/implementation work: expert clinical review; final cross-disorder interview graph; verified instrument versions/languages/permissions; an operational safety and tracking workflow; agent integration; diary analysis/C-PASS implementation if selected; model and clinical evaluation. Treatment selection, medication/hormone changes and full management of every alternative are outside this assessment module. Earlier modules' pending clinical review is not closed by adding PMDD.
