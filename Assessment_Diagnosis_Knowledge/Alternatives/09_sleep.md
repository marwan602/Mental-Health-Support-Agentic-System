# Insomnia, sleep-disordered breathing and schedule-related problems

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Determine whether sleep opportunity, insomnia, breathing disruption or schedule mismatch contributes to mood, fatigue and cognition.

## Benefit for our system

Avoid attributing every sleep complaint to depression and distinguish fatigue/sleepiness from reduced sleep need.

## Scope and interpretation

Focused insomnia/OSA/schedule differential. Other sleep disorders are review possibilities rather than fully implemented diagnostic modules.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- Insomnia reference includes difficulty initiating/maintaining sleep or early waking despite adequate opportunity, with burden and alternative explanations reviewed. DSM-5-TR reference frequency is at least three nights weekly for at least three months; shorter-duration problems can still need care.
- An irregular/shift schedule or insufficient opportunity can explain short sleep without establishing insomnia. Clarify when the person sleeps on free days and whether sleep is possible at preferred times.
- OSA clues include snoring, witnessed pauses/choking, unrefreshing sleep and daytime effects. Symptoms prompt appropriate clinical assessment/testing rather than a diagnosis from snoring or a questionnaire.
- The older AASM guideline informs history and investigation principles; its ICSD-era duration is not substituted for the DSM reference. Routine polysomnography is not required for every insomnia complaint, although suspected breathing/other sleep disorders can need testing.

Sources for these distinctions: [DSM_SLEEP; NICE_202; AASM_2008].

## When and how to explore

Explore any reported sleep change, unexplained fatigue/sleepiness, cognitive difficulty or breathing/schedule clue.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Clarify actual schedule, opportunity and complaint.
2. Distinguish sleepiness, fatigue and restedness after short sleep.
3. Ask relevant breathing/other sleep clues and daytime consequences.
4. Review mood, medical/exposure context and professional assessment needs.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

### Sleep opportunity and schedule — `sleep_opportunity_timing`

Distinguish insomnia, restricted opportunity and schedule mismatch using actual sleep/wake patterns.

Sources: [DSM_SLEEP; AASM_2008].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `bed_wake_times` | Usual and variable timings, including days off. | Supported text; preserve timing/units and uncertainty |
| `opportunity` | Time and conditions available for sleep. | Supported text; preserve timing/units and uncertainty |
| `difficulty` | Falling asleep, staying asleep or early waking as reported. | Supported text; preserve timing/units and uncertainty |
| `frequency_duration` | Nights affected and how long the pattern has existed. | Supported text; preserve timing/units and uncertainty |
| `daytime_effect` | Sleepiness, fatigue and functional impact distinguished. | Supported text; preserve timing/units and uncertainty |
| `shift_circadian_context` | Work/schedule mismatch and sleep at preferred times. | Supported text; preserve timing/units and uncertainty |
| `exposures` | Actual caffeine/medicines/substance use and timing. | Supported text; preserve timing/units and uncertainty |

**Example question:** What does a typical night look like, including when you can sleep and when you need to get up?

**Follow-up:** Ask relevant detail; less time in bed is not automatically insomnia.

**Do not infer:** Do not assign a sleep disorder from hours alone, or reduced sleep need when exhausted.

### Sleep-related breathing clues — `sleep_breathing_clues`

Reported snoring, witnessed breathing pauses/choking and daytime effects that may merit sleep assessment.

Sources: [NICE_202].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `snoring` | Reported snoring and source. | Supported text; preserve timing/units and uncertainty |
| `pauses_choking` | Witnessed pauses, gasping/choking or uncertain report. | Supported text; preserve timing/units and uncertainty |
| `refreshment` | Whether sleep is refreshing. | Supported text; preserve timing/units and uncertainty |
| `daytime_effects` | Actual sleepiness, fatigue or cognitive concerns. | Supported text; preserve timing/units and uncertainty |
| `medical_context` | Relevant reported health factors or tests. | Supported text; preserve timing/units and uncertainty |
| `functional_safety` | Reported effects on safety-sensitive activities. | Supported text; preserve timing/units and uncertainty |

**Example question:** Has anyone noticed loud snoring or pauses in your breathing while you sleep?

**Follow-up:** Clarify actual reports and arrange appropriate clinical assessment when indicated.

**Do not infer:** Snoring alone, absent sleepiness or a questionnaire score does not independently confirm or exclude OSA.

### Sleep disturbance — `sleep_disturbance`

Difficulty sleeping or excessive sleep.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve timing/units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve timing/units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve timing/units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve timing/units and uncertainty |
| `pattern` | Reported sleep complaint. | onset_difficulty / maintenance_difficulty / early_waking / excessive_sleep / mixed / unclear |
| `latency` | Time taken to fall asleep. | Supported text; preserve timing/units and uncertainty |
| `awakenings` | Waking during sleep and return-to-sleep account. | Supported text; preserve timing/units and uncertainty |
| `wake_timing` | Actual versus intended/usual waking. | Supported text; preserve timing/units and uncertainty |
| `total_sleep` | Reported sleep hours with period. | Supported text; preserve timing/units and uncertainty |
| `sleep_opportunity` | Opportunity and external interruptions. | Supported text; preserve timing/units and uncertainty |
| `daytime_effect` | Sleepiness, exhaustion or other reported effects. | Supported text; preserve timing/units and uncertainty |

**Example question:** How has your sleep changed from what is usual for you?

**Follow-up:** Identify complaint before asking subtype-specific details.

**Do not infer:** Insomnia while tired is not reduced sleep need; insufficient opportunity is not automatically insomnia.

### Energy and fatigue — `energy_fatigue`

Unusual tiredness or reduced energy.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve timing/units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve timing/units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve timing/units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve timing/units and uncertainty |
| `experience` | Fatigue, low energy or both. | Supported text; preserve timing/units and uncertainty |
| `sleepiness` | Reported sleepiness if distinguished. | Supported text; preserve timing/units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve timing/units and uncertainty |

**Example question:** How has your energy been compared with usual?

**Follow-up:** Examples and timing; separate sleepiness if ambiguous.

**Do not infer:** Do not automatically attribute fatigue to depression or infer it from short sleep.

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

### Medical context — `medical_context`

Relevant reported medical history and symptoms.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `conditions` | Reported conditions; distinguish reported diagnosis from confirmation. | Supported text; preserve timing/units and uncertainty |
| `timeline` | Relationship to symptoms. | Supported text; preserve timing/units and uncertainty |
| `investigations` | Results only if actually supplied. | Supported text; preserve timing/units and uncertainty |
| `clinician_review` | Known professional assessment or unresolved need. | Supported text; preserve timing/units and uncertainty |

**Example question:** Are there health conditions that might be relevant to these changes?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

### Medicines and substances — `exposure_context`

Relevant treatment/substance exposure account.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `name` | Named exposure. | Supported text; preserve timing/units and uncertainty |
| `dose_use` | Reported amount/use; never recommend a dose. | Supported text; preserve timing/units and uncertainty |
| `start_change_stop` | Timing of changes. | Supported text; preserve timing/units and uncertainty |
| `symptom_timing` | Reported temporal relationship. | Supported text; preserve timing/units and uncertainty |
| `source_kind` | Medicine, alcohol, other substance or unclear. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have any medicines or substance-use patterns changed around this time?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

## Interpretation limits

- Hours alone do not prove normal sleep, insomnia or mania.
- No reported daytime sleepiness does not by itself exclude OSA.
- Do not automatically prescribe sleep restriction or sleeping medication during assessment.
- Restless legs, parasomnias or narcolepsy-like experiences can need specialist review; complete criteria/scoring are outside this package.

## Professional review and handoff

Professional sleep/medical assessment follows the actual findings; safety-sensitive daytime impairment deserves specific review without waiting for chronic-duration criteria.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### DSM_SLEEP

[APA DSM-5-TR (2022), Insomnia Disorder](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed p.410 / PDF viewer p.590

**Contribution:** Frequency/duration/opportunity and alternate sleep/exposure explanations

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.

### NICE_202

[NICE NG202, Obstructive sleep apnoea/hypopnoea syndrome](https://www.nice.org.uk/guidance/ng202/chapter/1-obstructive-sleep-apnoeahypopnoea-syndrome)

**Location:** 1.1 initial assessment; symptom features and scales; rationale for initial assessment

**Contribution:** Sleep history, breathing clues, daytime effects and limits of sleepiness scales

**Access:** Official primary guidance/indexed recommendation text inspected

### AASM_2008

[Schutte-Rodin et al. (2008), Clinical guideline for chronic insomnia evaluation in adults](https://pmc.ncbi.nlm.nih.gov/articles/PMC2576317/)

**Location:** J Clin Sleep Med 4(5):487–504; Summary Recommendations: Evaluation

**Contribution:** Sleep/medical/psychiatric/substance history; not routine polysomnography for all insomnia

**Access:** Primary AASM guideline/indexed full text inspected; older ICSD-era diagnostic duration is not substituted for DSM-5-TR thresholds.

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

### DSM_BIPOLAR

[APA DSM-5-TR (2022), Bipolar and Related Disorders](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed pp.140–143,150–154,160 / PDF viewer pp.256–259,268–272,279

**Contribution:** Mania/hypomania, bipolar I/II and adult cyclothymic boundaries

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.
