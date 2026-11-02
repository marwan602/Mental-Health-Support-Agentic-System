# Medical conditions and depressive symptoms

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Identify reported illness, relevant investigations and physiological-cause versus comorbidity/stress/treatment possibilities.

## Benefit for our system

Avoid a premature unipolar explanation and provide a traceable medical-review handoff without diagnosing physical illness from chat.

## Scope and interpretation

Reuse the detailed existing medical-condition depression package; focused clues, not a complete internal-medicine diagnostic service.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- Physical illness and depression may coexist without a direct physiological causal disorder. Illness effects, distress, treatment effects and independent depression must be kept separate.
- Keep physical-symptom onset, diagnosis, treatment changes and mood chronology distinct. Diagnosis date is not necessarily disease onset.
- Examples already reviewed include thyroid/endocrine, neurological and B12-related contexts; source evidence varies. NICE advises clinician consideration of thyroid tests with depression and context-based B12 assessment, not an AI blanket laboratory panel.
- Record actual reported findings and attributed professional interpretation. An abnormal result or temporal association does not independently establish the mood cause.

Sources for these distinctions: [DSM_MEDICAL; NICE_145; NICE_239; VA_2022].

## When and how to explore

Take relevant medical history in depression assessment and explore targeted findings or atypical/acute changes when reported.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Identify actual reported conditions and diagnostic basis.
2. Compare medical/mood/treatment timelines.
3. Record actual tests and their source.
4. Use the existing detailed module for targeted follow-ups and causal-review needs.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

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

### Previous care — `treatment_history`

Prior mental-health assessment and care.

Sources: [VA_2022; NICE_222].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `reported_diagnosis` | Person-reported professional diagnosis. | Supported text; preserve timing/units and uncertainty |
| `treatment` | Therapy/medicines/admissions as reported. | Supported text; preserve timing/units and uncertainty |
| `period` | When and for which symptoms. | Supported text; preserve timing/units and uncertainty |
| `response` | Reported benefits, persistence or unwanted effects. | Supported text; preserve timing/units and uncertainty |
| `use` | Actual use and barriers as reported. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have you received help for something similar before?

**Follow-up:** Ask only relevant unanswered context; do not conduct every alternative interview.

**Do not infer:** A contextual association is not a confirmed causal explanation.

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

### Acute/fluctuating cognitive change — `acute_attention_change`

New change over hours/days in attention, awareness or thinking, possibly hypoactive rather than agitated.

Sources: [NICE_103].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `baseline` | Usual cognition/behaviour. | Supported text; preserve timing/units and uncertainty |
| `onset` | Reported start and speed of change. | Supported text; preserve timing/units and uncertainty |
| `fluctuation` | Changes across the day. | Supported text; preserve timing/units and uncertainty |
| `attention_awareness` | Actual difficulty attending or altered awareness. | Supported text; preserve timing/units and uncertainty |
| `other_changes` | Reported lethargy/agitation, perception or sleep-wake changes. | Supported text; preserve timing/units and uncertainty |
| `medical_exposures` | Recent illness, treatment or withdrawal context. | Supported text; preserve timing/units and uncertainty |
| `source` | Who noticed, as reported. | Supported text; preserve timing/units and uncertainty |

**Example question:** Has there been a sudden change in confusion or ability to pay attention compared with usual?

**Follow-up:** Current acute change takes priority over the routine depression interview and needs medical assessment.

**Do not infer:** Do not rule out delirium because the person is quiet or has known dementia; chat is not a 4AT assessment.

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

- Do not infer an illness from nonspecific fatigue or order universal scans/cancer testing.
- Medical comorbidity does not exclude independent depression.
- Do not convert a patient report into verified laboratory data.

## Professional review and handoff

The responsible clinician determines investigations, cause and appropriate urgency; current acute physical/cognitive concerns interrupt routine assessment.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Existing detailed knowledge to reuse

- [Depression_Due_To_Medical_Condition README](../Depression_Due_To_Medical_Condition/README.md)

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### DSM_MEDICAL

[APA DSM-5-TR (2022), Depressive Disorder Due to Another Medical Condition](https://doi.org/10.1176/appi.books.9780890425787.x04_Depressive_Disorders)

**Location:** Printed pp.206–209; inspected PDF viewer pp.336–340. Major depressive episode reference: MDD criteria in same chapter.

**Contribution:** Criteria A–E, three descriptive specifiers, attribution, medical examples, course and differential

**Access:** Original APA text inspected locally through previously obtained public psychiatry.ru mirror. Publisher full text blocked; licensing/redistribution rights not inferred. No manual bundled.

### NICE_145

[NICE NG145, Thyroid disease: assessment and management](https://www.nice.org.uk/guidance/ng145/chapter/Recommendations)

**Location:** 1.2.1–1.2.6; particularly 1.2.3 and 1.2.6

**Contribution:** Clinician consideration of thyroid tests with depression and caution about acute illness affecting results

**Access:** Public primary-source recommendations/indexed extracts inspected

### NICE_239

[NICE NG239, Vitamin B12 deficiency in over 16s (2024)](https://www.nice.org.uk/guidance/ng239/chapter/recommendations)

**Location:** 1.2.1–1.2.6; symptom/risk-factor boxes

**Contribution:** Possible mental-health associations, nonspecific symptoms and context-based testing

**Access:** Public primary-source recommendations/indexed extracts inspected

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

### NICE_103

[NICE CG103, delirium](https://www.nice.org.uk/guidance/cg103/chapter/Recommendations)

**Location:** 1.3.1, 1.5 and 1.6.1–1.6.3; 2023 assessment update: competent practitioner/4AT and final clinical diagnosis

**Contribution:** Acute/fluctuating changes in attention/cognition need assessment; hospital/long-term-care guideline context

**Access:** Public primary-source material; relevant sections inspected
