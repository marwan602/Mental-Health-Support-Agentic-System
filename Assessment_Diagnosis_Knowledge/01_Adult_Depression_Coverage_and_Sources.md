# 01 — Adult depression coverage, age scope and boundaries

Source-linked adult coverage map. Clinical definitions, scope and limitations are distinguished from application implementation.

## Population and classification

Our implementation scope is adults aged **18 and above**, including older adults, with no fixed upper age limit. This is a project decision, not a clinical minimum age for depression. Menstrual, pregnancy/postpartum, cognitive, sensory and medical context need individual assessment. Pediatric/adolescent pathways are outside this implementation phase.

The seven primary reference packages follow the DSM-5-TR depressive-category inventory for this adult scope. Episodes, specifiers, illness courses and life-stage contexts are not additional peer disorders. ICD-11 remains a separate classification/mapping task; no unreviewed DSM–ICD equivalence is implemented. [APA DSM-5-TR](https://doi.org/10.1176/appi.books.9780890425787)

## Primary category coverage

| Category | Adult applicability | Current reference package |
|---|---|---|
| Major depressive disorder | 18+, including older adults | [MDD guide](02_MDD_Assessment_Information_Requirements.md) |
| Persistent depressive disorder | 18+, adult long-term-course requirements | [PDD guide](03_PDD_Assessment_Information_Requirements.md) |
| Premenstrual dysphoric disorder | Adults 18+ with relevant menstrual/ovarian context; no guessed upper-age limit | [PMDD guide](04_PMDD_Assessment_Information_Requirements.md) |
| Substance/medication-induced depressive disorder | 18+ where exposure and possible causal relationship require assessment | [Exposure guide](05_Substance_Medication_Induced_Depression_Assessment.md) |
| Depressive disorder due to another medical condition | 18+ where individual physiological attribution requires review | [Medical guide](06_Depression_Due_To_Medical_Condition_Assessment.md) |
| Other specified depressive disorder | 18+, with presentation-specific requirements and clinical reason | [Other-specified guide](07_Other_Specified_Depressive_Disorder_Assessment.md) |
| Unspecified depressive disorder | 18+, clinical residual formulation; not an automatic incomplete-interview label | [Unspecified guide](08_Unspecified_Depressive_Disorder_Assessment.md) |

Each guide and its `sources.json` identify sources, locations, uses and access limitations. Packages are reference/contract designs requiring clinical review. They are not connected to the agents and are not evidence of clinical efficacy.

## DMDD boundary

DMDD is not implemented as a new adult diagnostic pathway here. APA describes onset before age 10 and no first diagnosis before age 6 or after age 18. Age 18 is a developmental boundary requiring appropriate specialist interpretation. Relevant childhood history may still be collected; childhood irritability is not automatically adult bipolar disorder or depression. [APA DMDD fact sheet](https://www.psychiatry.org/File%20Library/Psychiatrists/Practice/DSM/APA_DSM-5-Disruptive-Mood-Disregulation-Disorder.pdf)

## Features, course and life-stage context

MDD reference cards include anxious distress, mixed/melancholic/atypical features, psychotic experiences, catatonic signs, seasonal pattern and peripartum context, plus severity/course/remission information. Their detailed applicability and source locations are in the MDD guide. They must not all be automatically attached to every depressive disorder.

PDD's symptom-feature branches are anxious distress and atypical features; its onset, course, severity and remission descriptions are separate axes. The formal classification permits severe/persistent major depressive episodes, so simplified mild-only public descriptions do not override it. [APA PDD correction](https://www.psychiatry.org/getmedia/fd3dfaad-d409-4e94-8605-0350adec5b91/APA-DSM5TR-PersistentDepressive.pdf)

Pregnancy/postpartum, perimenopause and older adulthood are assessment contexts rather than an invented list of separate diagnoses. Formal peripartum timing and broader perinatal assessment are distinguished in the relevant guide. Clinical review and further age/life-stage refinements remain pending before implementing detailed rules.

## Alternatives and coexisting conditions

The [focused alternatives guide](09_Alternative_Assessment_Pathways_and_Sources.md) now supplies 11 source-linked pathways: bipolar spectrum; anxiety; trauma/PTSD; adjustment; grief/PGD; psychosis; delirium; cognitive decline; sleep; medical conditions; and substance/medication effects. Each gives its purpose, benefit, concepts, questions, limits and professional-review role.

These are focused depression-assessment branches, not full diagnostic/treatment implementations of every alternative. A condition may explain or coexist with depression. Existing medical/exposure packages are reused. ADHD, personality, OCD-related, eating and other possibilities can need review, but comprehensive modules are not implemented. Missing information does not rule them out.

## Safety, readiness and next work

Suicidal thoughts/behaviour and self-harm are a separate connected assessment/safety area, not depressive subtypes. A JSON flag or source citation does not implement a safety response. Operational review/referral steps must be appropriate to the actual care setting and verified before delivery is claimed.

The exactly-four-day other-specified source discrepancy is explicitly marked for professional review. See the original classification reference and the [current package index](00_Knowledge_Package_Index.md).

The research conversation flow and conditional routing rules are documented. Qualified clinical review, instrument/language decisions, application integration and evaluation remain required. This file records clinical coverage; it does not assert that the complete platform is implemented or clinically validated.
