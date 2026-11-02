# PTSD and other trauma-related presentations

Version: 1.0.0-source-reviewed. Date: 2 November 2026. Adults 18+, including older adults.

## Purpose

Check whether trauma-linked symptoms contribute to low mood, withdrawal, guilt, numbing or sleep difficulties.

## Benefit for our system

Preserve the event relationship and avoid either missing trauma effects or assuming every stressful event causes PTSD.

## Scope and interpretation

Focused adult PTSD/trauma differential. Acute stress and complex presentations require their own professional formulation; no separate automated acute/complex PTSD diagnosis is implemented.

This is focused differential/coexisting-condition assessment, not an independent diagnostic or treatment service. Sources supply clinical domains; JSON fields, conversational wording and local order are project design. Clinical validation and agent integration remain pending.

## Clinical reference and distinctions

- PTSD requires an appropriate exposure and a pattern of intrusion, avoidance, negative mood/thought and arousal changes with duration and impairment requirements. A distressing event label by itself does not establish the exposure criterion.
- NIMH describes a duration longer than one month for the PTSD syndrome. Earlier distress can still need support and assessment; it is not automatically PTSD or acute stress disorder.
- Dissociation, shame, relationship difficulties and trauma-related negative beliefs can be relevant. Do not silently equate ICD-11 complex PTSD with a DSM-5-TR subtype.
- Depression and PTSD can coexist; determine what is event-linked and what is broader rather than forcing one explanation.

Sources for these distinctions: [NICE_116; NIMH_PTSD; VA_PCL5].

## When and how to explore

Explore when the person reports a potentially relevant event or trauma-linked effects. Ask permission and use broad context before symptom follow-ups.

The following local sequence is a semi-structured project policy, not a validated interview order. Use the whole conversation and skip answered targets.

1. Check willingness to discuss broad context and current safety.
2. Explore actual effects without requiring graphic detail.
3. Clarify endorsed symptom domains, timing and functioning.
4. Preserve uncertainty about exposure/diagnostic requirements and seek appropriate review.

## Information and concept-specific evidence to collect

A shared fact can inform several pathways. Store it once per concept/period with provenance rather than asking it again for each branch. Every detail below is optional in an individual report, and an unmentioned/declined item is not absent.

### Trauma context and assessment permission — `trauma_context`

Reported potentially traumatic exposure and current needs without eliciting unnecessary detailed recounting.

Sources: [NICE_116; NIMH_PTSD].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `broad_event` | Broad type/context only as volunteered or agreed; unnecessary graphic detail is not needed. | Supported text; preserve timing/units and uncertainty |
| `time` | When it happened and whether danger is ongoing. | Supported text; preserve timing/units and uncertainty |
| `exposure_kind` | Reported experience/witnessing/learning/occupational context, without certifying criteria. | Supported text; preserve timing/units and uncertainty |
| `participation` | What the person is comfortable discussing. | Supported text; preserve timing/units and uncertainty |
| `current_needs` | Immediate safety/support or assessment-access needs. | Supported text; preserve timing/units and uncertainty |

**Example question:** Has anything frightening or traumatic happened that you feel may be connected, without going into details you do not want to share?

**Follow-up:** Ask permission and follow the person's pace; focus on effects and current safety.

**Do not infer:** Not every stressful event meets PTSD exposure requirements; do not infer trauma from symptoms or require a detailed retelling.

### Trauma-linked symptom pattern — `trauma_linked_symptoms`

Intrusion, avoidance, negative thoughts/mood, arousal and dissociation in relation to an event.

Sources: [NICE_116; NIMH_PTSD].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `intrusions` | Unwanted event-related memories, nightmares or reliving as reported. | Supported text; preserve timing/units and uncertainty |
| `avoidance` | Avoidance of reminders/thoughts, without forcing disclosure. | Supported text; preserve timing/units and uncertainty |
| `negative_mood_thoughts` | Reported beliefs, blame, numbing or detachment and event relationship. | Supported text; preserve timing/units and uncertainty |
| `arousal` | Hypervigilance, startle, irritability or sleep changes as reported. | Supported text; preserve timing/units and uncertainty |
| `dissociation` | Detachment/unreality experiences as described. | Supported text; preserve timing/units and uncertainty |
| `onset_duration` | Timing, persistence and fluctuation. | Supported text; preserve timing/units and uncertainty |
| `burden` | Reported effects on functioning and distress. | Supported text; preserve timing/units and uncertainty |

**Example question:** How has it affected you—for example, in unwanted memories, feeling on guard or avoiding reminders?

**Follow-up:** Clarify only endorsed domains; PTSD and depression may both need assessment.

**Do not infer:** Do not equate all low mood after stress with PTSD or all intrusive memories with psychosis.

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

### Death/suicide-related reports — `death_suicide`

Death-related thoughts, suicidal thoughts, plans or attempts.

Sources: [ASQ_BSSA; NICE_225].

| Optional output detail | Meaning | Form/values |
|---|---|---|
| `experience` | Preserve distinctions. | death_thoughts / wish_not_alive / suicidal_thoughts / suicide_plan / suicide_attempt / unclear |
| `recency` | When last/current; do not infer resolution. | Supported text; preserve timing/units and uncertainty |
| `frequency` | Reported recurrence within an explicit reference period; no invented numeric conversion. | Supported text; preserve timing/units and uncertainty |
| `intent` | Intent as reported. | Supported text; preserve timing/units and uncertainty |
| `plan_present` | Whether a plan was explicitly reported or denied. | reported / denied / unclear |
| `access` | Access to means as reported, without generating procedural details. | Supported text; preserve timing/units and uncertainty |
| `past_behaviour` | Historical self-injury/attempt account, intent and timing. | Supported text; preserve timing/units and uncertainty |
| `support` | Available support as reported. | Supported text; preserve timing/units and uncertainty |

**Example question:** Have you had thoughts about ending your life?

**Follow-up:** Use dedicated safety pathway; preserve current versus historical information.

**Do not infer:** Fear of death is not automatically recurrent thoughts of death; self-harm and suicidal intent must be distinguished.

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

- Assessment is not trauma processing or exposure therapy.
- Do not ask for detailed recounting to fill a form or assume silence means no trauma.
- Reliving/dissociation and psychosis require contextual differentiation.
- PCL-5 can support screening/monitoring and provisional assessment; clinician interview remains important. No scale or cutoff is implemented or inferred from chat.

## Professional review and handoff

Current danger, severe dissociation or safety concerns require the appropriate immediate review pathway. Trauma-informed professional assessment should respect participation and communication needs.

Include supported findings, relevant period, uncertainties, alternatives, burden, declined/unanswered targets and actual contact/review status. A workflow flag is not proof that a person received care. Safety assessment applies across all pathways rather than being explained away by a diagnosis.

## Output contract

Use the shared [evidence schema](evidence_output.schema.json) and [contract explanation](OUTPUT_CONTRACT.md). The extractor does not output a confirmed alternative diagnosis. Clinical reference thresholds are not a diagnostic scorer. Full source/field definitions are in [knowledge.json](knowledge.json).

## Sources and exact contribution

### NICE_116

[NICE NG116, PTSD](https://www.nice.org.uk/guidance/ng116/chapter/recommendations)

**Location:** 1.1 recognition, symptom domains; 1.2 assessment/coordination

**Contribution:** Trauma-associated symptoms, impairment and appropriate assessment

**Access:** Official primary guidance/indexed recommendation text inspected

### NIMH_PTSD

[NIMH, Post-Traumatic Stress Disorder](https://www.nimh.nih.gov/health/publications/post-traumatic-stress-disorder-ptsd)

**Location:** What is PTSD?; Signs and symptoms

**Contribution:** Exposure/cluster/duration context and coexistence with depression

**Access:** Official primary guidance/indexed recommendation text inspected

### VA_PCL5

[US VA National Center for PTSD, PTSD Checklist for DSM-5](https://www.ptsd.va.gov/professional/assessment/adult-sr/ptsd-checklist.asp)

**Location:** Description; Administration and Scoring; availability

**Contribution:** Self-report screening/monitoring/provisional role versus clinician interview; no instrument implemented

**Access:** Official primary guidance/indexed recommendation text inspected

### ASQ_BSSA

[NIMH Adult Outpatient Brief Suicide Safety Assessment Guide](https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials/adult-outpatient/adult-outpatient-brief-suicide-safety-assessment-guide)

**Location:** Intended users; thoughts, plan, past behaviour, supports and disposition sections

**Contribution:** Safety information domains; clinician guide following positive ASQ, not autonomous LLM validation

**Access:** Public primary-source material inspected

### NICE_225

[NICE NG225, Self-harm](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)

**Location:** 1.6.1–1.6.6

**Contribution:** No predictive low/medium/high stratification; needs-focused assessment

**Access:** Public primary-source material inspected

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
