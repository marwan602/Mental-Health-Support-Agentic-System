# Anxiety presentations: generalized worry, panic and social anxiety

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Determine whether worry, fear, panic or avoidance explains part of the presentation or coexists with depression.

## Benefit for our system

Distinguish overlapping sleep/fatigue/concentration complaints and reasons for withdrawal; avoid treating every worry or panic attack as a depressive symptom.

## Scope and interpretation

Focused GAD, panic and social-anxiety assessment; not an exhaustive implementation of all anxiety diagnoses. Other anxiety/OCD-related possibilities can be noted for professional review.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- GAD reference: excessive, difficult-to-control worry about multiple domains on more days than not for at least six months, with associated symptoms, burden and alternative-explanation review. Adult associated symptoms include restlessness, fatigue, concentration problems, irritability, tension and sleep disturbance; three are required for the formal syndrome.
- Panic attacks are abrupt surges that peak within minutes with bodily/cognitive symptoms. The formal attack definition includes at least four symptoms from thirteen domains; capture actual sensations rather than making a yes-count from a vague account.
- Panic symptom reference domains: racing/pounding heart, sweating, trembling, breathlessness, choking sensation, chest discomfort, nausea/abdominal distress, dizziness/faintness, chills/heat, numbness/tingling, unreality/detachment, fear of losing control and fear of dying. These describe experiences requiring context, not an instruction to dismiss physical symptoms as psychological.
- Panic disorder additionally requires recurrent unexpected attacks and at least a month of concern or maladaptive behavioural change after an attack, plus medical/exposure and other mental-disorder review. An attack can occur in several disorders.
- Social anxiety concerns fear of scrutiny/negative evaluation, avoidance or distressed endurance, persistence and burden. Clarify whether it existed before/outside depression; reduced social activity alone does not establish it.

Sources for these distinctions: [DSM_ANXIETY; NICE_113; NICE_159].

## When and how to explore

Explore if worry/fear, sudden episodes or avoidance are reported, or when overlapping symptoms remain unexplained.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Ask what makes the situation difficult.
2. Clarify worries, panic episodes or feared evaluation in the person's own words.
3. Check timing, context, persistence and burden.
4. Compare with depressive periods and medical/exposure factors.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

### Generalized worry pattern — `worry_pattern`

Excessive or difficult-to-control worry across domains, rather than assuming all concentration/sleep problems come from depression.

Sources: [DSM_ANXIETY].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `topics` | Actual worries across domains. | Supported text; preserve timing/units and uncertainty |
| `control` | Difficulty controlling worry in the person's account. | Supported text; preserve timing/units and uncertainty |
| `frequency_duration` | How often and for how long. | Supported text; preserve timing/units and uncertainty |
| `associated_changes` | Restlessness, fatigue, irritability, tension, sleep or concentration as reported. | Supported text; preserve timing/units and uncertainty |
| `mood_relationship` | Worry before/during/outside depressive periods. | Supported text; preserve timing/units and uncertainty |
| `burden` | Concrete distress/interference. | Supported text; preserve timing/units and uncertainty |

**Example question:** What worries have been taking up your mind, and how hard are they to set aside?

**Follow-up:** Clarify course and actual somatic/cognitive effects without equating ordinary worry with GAD.

**Do not infer:** Worry-related concentration difficulty is not automatically a separate depressive criterion.

### Panic-like episode — `panic_experience`

Abrupt intense fear/discomfort with rapid peak, actual sensations and context; medical symptoms need appropriate assessment.

Sources: [DSM_ANXIETY].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `onset_peak` | How abruptly it began and time to peak. | Supported text; preserve timing/units and uncertainty |
| `sensations` | Actual bodily/perceptual symptoms and fears. | Supported text; preserve timing/units and uncertainty |
| `unexpectedness` | Unexpected versus linked to a specific situation/reminder. | Supported text; preserve timing/units and uncertainty |
| `recurrence` | Number/pattern of attacks. | Supported text; preserve timing/units and uncertainty |
| `after_effects` | Persistent concern or avoidance/behaviour change and duration. | Supported text; preserve timing/units and uncertainty |
| `medical_exposure_context` | Relevant illness, substances or treatment; no assumed anxiety cause. | Supported text; preserve timing/units and uncertainty |

**Example question:** Could you describe what happens during one of those sudden episodes?

**Follow-up:** Clarify immediate medical concerns before interpreting symptoms as panic.

**Do not infer:** One panic attack is not panic disorder, and fear of dying during an attack is not automatically suicidal intent.

### Social fear and avoidance — `social_fear_avoidance`

Fear of scrutiny/negative evaluation and avoidance, contrasted with low motivation, reduced pleasure or physical inability.

Sources: [NICE_159].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `situations` | Actual feared/avoided social or performance situations. | Supported text; preserve timing/units and uncertainty |
| `feared_outcome` | What the person expects others may think/do. | Supported text; preserve timing/units and uncertainty |
| `avoidance` | Avoided situations or endurance with fear. | Supported text; preserve timing/units and uncertainty |
| `course` | Timing and persistence relative to low mood. | Supported text; preserve timing/units and uncertainty |
| `burden` | Impact on relationships, education or work. | Supported text; preserve timing/units and uncertainty |
| `other_reasons` | Practical, physical or contextual reasons for reduced social activity. | Supported text; preserve timing/units and uncertainty |

**Example question:** What makes seeing people difficult: worry about what might happen, low interest, or something else?

**Follow-up:** Clarify the person's own explanation; do not force the offered possibilities.

**Do not infer:** Not seeing friends does not by itself establish either social anxiety or anhedonia.

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

### Functioning and distress — `functioning_distress`

Reported burden in important life areas.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `domain` | Affected area such as work, relationships or self-care. | Supported text; preserve timing/units and uncertainty |
| `examples` | Concrete difficulty or distress. | Supported text; preserve timing/units and uncertainty |
| `baseline` | Usual functioning. | Supported text; preserve timing/units and uncertainty |
| `supports` | Assistance helping preserve functioning. | Supported text; preserve timing/units and uncertainty |

**Example question:** How have these changes affected your daily life?

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

- New concerning chest/breathing/fainting symptoms must not automatically be called panic.
- Fear of death during panic is not equivalent to suicidal intent.
- Do not infer social fear from physical inability or low opportunity to meet others.
- GAD-2/7 or other scales, if later adopted, need verified versions and scoring; no diagnoses or scores are invented here.

## Professional review and handoff

Arrange appropriate professional assessment for possible anxiety disorders and competing medical causes; urgency follows current medical/safety concerns, not the word anxiety.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### DSM_ANXIETY

[APA DSM-5-TR (2022), Anxiety Disorders](https://doi.org/10.1176/appi.books.9780890425787)

**Location:** Printed pp.235–236 and 250–251 / PDF viewer pp.374–375 and 393

**Contribution:** Panic attack versus panic disorder; generalized worry criteria context

**Access:** Original APA text inspected locally through previously obtained psychiatry.ru mirror; no permission to redistribute inferred; manual not bundled.

### NICE_113

[NICE CG113, Generalised anxiety disorder and panic disorder in adults](https://www.nice.org.uk/guidance/cg113/chapter/Recommendations)

**Location:** 1.2.6–1.2.8; 1.3.1–1.3.3

**Contribution:** Distress/function, comorbidity and assessment of panic presentations

**Access:** Official primary guidance/indexed recommendation text inspected

### NICE_159

[NICE CG159, Social anxiety disorder](https://www.nice.org.uk/guidance/cg159/chapter/recommendations)

**Location:** Adult identification/assessment section 1.2, especially fear/avoidance and depression relationship

**Contribution:** Distinguish social withdrawal related to negative evaluation from depressive withdrawal

**Access:** Official primary guidance/indexed recommendation text inspected

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
