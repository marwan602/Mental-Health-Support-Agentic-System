# Cognitive decline and possible neurocognitive disorder

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Understand longer-term decline, daily functioning and contributors while separating acute change from chronic symptoms.

## Benefit for our system

Avoid both labelling depressive concentration problems as dementia and dismissing genuine cognitive decline as depression.

## Scope and interpretation

Focused cognitive differential, not full major/mild neurocognitive subtype diagnosis, capacity assessment or cognitive-test service.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- Review actual decline from prior ability, course and real-world function, with authorized informant/records where appropriate. Cognitive and physical reasons for needing help must be distinguished.
- Depression, delirium, sensory impairment and medicines can contribute to cognitive complaints. Coexistence is possible; one explanation need not erase another.
- NICE cautions against ruling out dementia solely because a cognitive instrument score is normal. Specialist assessment and appropriate investigations determine diagnosis; a short chat cannot establish etiology or capacity.

Sources for these distinctions: [NICE_97; NICE_103].

## When and how to explore

Explore when decline in memory, language, reasoning or daily tasks is reported; sudden change instead prioritizes the delirium pathway.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Clarify baseline and concrete examples.
2. Determine onset/progression and cognitive versus physical reasons for difficulty.
3. Review mood, sleep, sensory, medical and medicine factors.
4. Identify professional/informant review needs with distinct source provenance.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

### Longer-term cognitive and functional course — `cognitive_function_course`

Reported decline against prior abilities, daily independence and potentially reversible contributors.

Sources: [NICE_97].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `domains` | Actual memory, language, attention, planning or other cognitive changes. | Supported text; preserve timing/units and uncertainty |
| `onset_progression` | Gradual versus sudden onset and course. | Supported text; preserve timing/units and uncertainty |
| `independence` | Daily tasks and why help is required; cognitive versus physical/contextual limitations. | Supported text; preserve timing/units and uncertainty |
| `mood_relationship` | Cognition relative to mood periods. | Supported text; preserve timing/units and uncertainty |
| `informant_context` | Whether an appropriate informant/record is available, not imported as patient testimony. | Supported text; preserve timing/units and uncertainty |
| `contributors` | Sensory, medical, sleep and medication context. | Supported text; preserve timing/units and uncertainty |
| `tests_as_reported` | Actual reported testing/result without verified interpretation. | Supported text; preserve timing/units and uncertainty |

**Example question:** What changes have you noticed in memory or everyday tasks compared with your usual abilities?

**Follow-up:** Clarify baseline, real examples and contributors; seek appropriate assessment.

**Do not infer:** Do not label dementia or dismiss decline as depression from one chat or one normal screening score.

### Concentration and decisions — `cognition_decisions`

Reported thinking, attention or decision difficulty.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `onset` | When this particular experience began; preserve approximate wording. | Supported text; preserve timing/units and uncertainty |
| `duration` | How long this particular experience has continued, not time needed to perform an activity. | Supported text; preserve timing/units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve timing/units and uncertainty |
| `baseline_comparison` | How this differs from the person's usual state. | Supported text; preserve timing/units and uncertainty |
| `kind` | Reported difficulty. | concentration / thinking / indecision / mixed / unclear |
| `tasks` | Concrete affected tasks. | Supported text; preserve timing/units and uncertainty |
| `impact` | Concrete reported consequences of this experience. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have concentrating or making decisions become harder than usual?

**Follow-up:** Task examples and change from baseline.

**Do not infer:** Do not label dementia, ADHD or depression from this alone.

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

### Assessment participation and limits — `assessment_limits`

Reported inability to recall, decline, uncertainty or communication difficulty; not symptom absence.

Sources: [NICE_222; VA_2022].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `target` | Specific unresolved topic. | Supported text; preserve timing/units and uncertainty |
| `limit` | Reported limitation. | cannot_recall / declined / ambiguous / communication_difficulty / conflicting_reports / other_reported_limit |
| `known_part` | Actual partial information. | Supported text; preserve timing/units and uncertainty |
| `support_requested` | Actual requested accommodation. | Supported text; preserve timing/units and uncertainty |

**Example question:** Would you prefer that I ask this another way or leave it for now?

**Follow-up:** Respect choice and carry the unresolved target into review.

**Do not infer:** A declined question does not establish a negative differential history.

## Interpretation limits

- Do not infer dementia from age, forgetfulness or one score.
- Depression-related cognition is not automatically benign or proven reversible.
- Do not import another person's report as a patient quote or presume impaired decision-making capacity.

## Professional review and handoff

Appropriate medical/cognitive assessment is needed for suspected decline; rapidly progressive or acute changes need a more urgent clinical pathway.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### NICE_97

[NICE NG97, Dementia assessment and management](https://www.nice.org.uk/guidance/ng97/chapter/Recommendations)

**Location:** 1.2.1–1.2.11; delirium/dementia differentiation

**Contribution:** Baseline decline, informant history, reversible contributors and test limitations

**Access:** Official primary guidance/indexed recommendation text inspected

### NICE_103

[NICE CG103, delirium](https://www.nice.org.uk/guidance/cg103/chapter/Recommendations)

**Location:** 1.3.1, 1.5 and 1.6.1–1.6.3; 2023 assessment update: competent practitioner/4AT and final clinical diagnosis

**Contribution:** Acute/fluctuating changes in attention/cognition need assessment; hospital/long-term-care guideline context

**Access:** Public primary-source material; relevant sections inspected

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

### DSM_SLEEP

[APA DSM-5-TR (2022), Insomnia Disorder](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed p.410 / PDF viewer p.590

**Contribution:** Frequency/duration/opportunity and alternate sleep/exposure explanations

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.

### AASM_2008

[Schutte-Rodin et al. (2008), Clinical guideline for chronic insomnia evaluation in adults](https://pmc.ncbi.nlm.nih.gov/articles/PMC2576317/)

**Location:** J Clin Sleep Med 4(5):487–504; Summary Recommendations: Evaluation

**Contribution:** Sleep/medical/psychiatric/substance history; not routine polysomnography for all insomnia

**Access:** Primary AASM guideline/indexed full text inspected; older ICSD-era diagnostic duration is not substituted for DSM-5-TR thresholds.
