# 11 - Main adult depression assessment route

Version 0.1.0-design | 2 November 2026 | Adults 18+, including older adults

This expands stage 3 of [the overall session map](10_Overall_Session_Map.md). It is an assessment-support design for fictional testing and later professional review. It is not a validated diagnostic interview, a treatment protocol or an implemented emergency service. Existing agents are unchanged.

## Our choice: a semi-structured modular interview

We will define the information to cover and the conditions for follow-up. The wording and route can adapt to the person's account. A module is a related group of information needs, not a compulsory page of identical questions. Several modules can be partly answered by one reply.

Start with the person's concern, narrow to relevant questions, and summarize for correction. Clinical Methods chapter 3 supports an open-to-focused interviewing approach; its 1990 publication is used for communication technique, not current diagnostic criteria. [INTERVIEW_BOOK]

WHO's training example links symptom/function assessment to alternative explanations, safety and further modules. We use its modular reasoning and concrete-language approach. We do **not** import its simplified depression decision thresholds or treatment slides as current DSM-5-TR rules. The WHO training publication is marked for field testing. [WHO_TRAIN_DEP; WHO_IG2]

The VA/DoD chart separates work-up, acute safety and diagnostic review. It is an MDD clinical algorithm, not a complete interview for all our categories. [VA_POCKET_2022]

**The ten modules, their exact order, example wording, coverage states and agent rules below are our project design. No cited source validates this exact AI workflow.**

## Starting the conversation

Application setup establishes adult scope and usable text/voice/video access. Explain AI involvement and use of conversation content accurately; do not promise confidentiality or emergency capabilities the application does not provide. Permissions for recording/transcription are separate from agreeing to talk.

An example opening, delivered in short turns:

> I'm an AI assessment assistant. I can help organize what you tell me for professional review. You can skip questions, pause or stop. Would you like to begin?

After the person agrees:

> What has been troubling you, and what would you like help with?

These are project-authored examples, not MINI/SCID/PHQ questions. Explain an actual session time limit if one exists. An agreed agenda and participation choices are supported by NICE shared decision-making guidance. [NICE_197]

## Default route and transition rules

The route is a starting order. A concern can change it, volunteered information can satisfy later targets, and important unanswered targets can remain explicitly unresolved. Moving to another module never means a disorder has been ruled out.

| Module | What we do | When we move on |
|---|---|---|
| M0 Welcome | Explain purpose, scope, participation and channel. | Person chooses to proceed, or we address access/scope needs. |
| M1 Person's story | Invite their account; identify the concern and an initial timeline/impact. | We understand enough to choose a focused question. |
| M2 Early safety enquiry | Ask directly about suicide-related concerns; clarify relevant death wishes/self-harm separately. | Review needs are addressed through the appropriate pathway, or documented as unresolved; no automatic clearance. |
| M3 Recent symptoms and functioning | Explore relevant depressive symptoms, timing, baseline change and daily impact. | We have useful breadth and key details, or explicit gaps. |
| M4 Important alternatives | Review activation history, health, medicines/supplements and substance exposure. | Relevant findings and further assessment needs are recorded. |
| M5 Course and previous care | Understand earlier periods, persistent background, recovery and previous care. | We can organize a provisional timeline, preserving uncertainty. |
| M6 Pattern/feature branches | Explore applicable menstrual, seasonal, perinatal and other feature/course questions. | Relevant branches are covered or deferred for records/review. |
| M7 Context and coexisting concerns | Clarify relevant stressors, supports, other concerns and care priorities. | Important context is represented without demanding unnecessary detail. |
| M8 Optional measurement | Offer an appropriate standardized measure under a separate protocol. | Record valid results, incompleteness or why it was not administered. |
| M9 Summary and handoff | Check understanding and prepare evidence, gaps and candidate explanations for review. | Useful summary is ready, or assessment pauses with unresolved needs. |

Safety enquiry is supported by NICE NG222 1.2.8-1.2.9. Our decision to place a checkpoint soon after the opening is a project safety-design choice, not a source-mandated third step. Do not wait for M2 if a concern appears earlier; revisit after relevant change. [NICE_222]

Thoughts of death, self-harm, suicidal thinking, current intent and past acts should not collapse into one label. NIMH's adult BSSA identifies assessment domains but is a clinician guide after a positive ASQ screen; we are not silently adopting its protocol for every chat. Current concerns require a reviewed, setting-specific response. [NIMH_BSSA]

Acute confusion, possible mania, psychosis, catatonic signs or urgent physical problems can also change priority. A possible feature does not always imply the same urgency; actual presentation and professional review matter. The focused packages define relevant domains. A no-answer or declined safety question is not a negative finding. Do not generate predictive low/medium/high suicide labels or discharge decisions from a score. [NICE_185; NICE_225; existing Alternatives/MDD packages]

## How the main clinical modules work

### M3: recent symptoms without tunnel vision

Use the person's description, then ask focused questions. Review mood, interest/pleasure, sleep, appetite/weight, energy, concentration/decisions, self-worth/guilt, movement changes and death/suicide concerns, where not already covered. Ask about distress and functioning alongside symptoms. [WHO_TRAIN_DEP; existing MDD package]

The recent two-week window helps episode assessment, but the timeline must also retain earlier onset, longstanding symptoms and recovery intervals. Do not force every experience into the last two weeks. A negative brief current screen does not close historical, persistent, cyclic or brief-presentation pathways.

NICE requires more than a symptom count, including illness course and functional impact. Its broader assessment also considers health, treatment, relationships, strengths, stressors and substance use. [NICE_222]

The exact symptom order is flexible. Our default is to start with the presenting symptom and mood/interest anchors, collect useful breadth, then revisit consequential gaps. If sleep is the main concern, start there and connect to the broader assessment. Do not finish ten sleep details before checking other important domains.

### M4-M5: avoid premature unipolar-depression conclusions

Ask about distinct past activation/overactivity as well as current low mood. If relevant, clarify associated changes and consequences using the bipolar pathway; a questionnaire or a four-day referral rule does not establish bipolar disorder. [NICE_185]

Record relevant medical/neurological history, prescribed/nonprescribed medicines and supplements, substance use, previous psychiatric treatment/response, reproductive context and family history. These are assessment domains identified by APA's adult-evaluation guideline. Their exact order is ours. [APA_EVALUATION]

Use a short overview first, then expand relevant findings. Record exposure changes and symptom timing without asserting causation. Clinical examination, investigations or collateral information may be needed; the agents cannot invent their results. The earlier symptom episode and longstanding background must remain distinguishable. [existing medical, exposure and PDD packages]

### M6: cover all seven adult categories through relevant branches

We do not conduct seven complete interviews in sequence.

| Existing category/package | How the shared route reaches it |
|---|---|
| [MDD](MDD/knowledge.json) | Recent symptom assessment, impairment, course and alternative review. An episode alone does not confirm MDD. |
| [PDD](PDD/knowledge.json) | Longstanding symptoms or incomplete recovery trigger detailed adult course review. |
| [PMDD](PMDD/knowledge.json) | With relevant menstrual/ovarian context and consent, establish timing across the cycle and consider prospective records. |
| [Substance/medication-induced](Substance_Medication_Induced_Depression/knowledge.json) | Relevant exposure/change and symptom relationship trigger the attribution pathway. |
| [Due to another medical condition](Depression_Due_To_Medical_Condition/knowledge.json) | Relevant illness or unexplained presentation triggers medical evidence/work-up review. |
| [Other specified](Other_Specified_Depressive_Disorder/knowledge.json) | Professional review of significant presentations that do not fit a named category, with the specific reason documented. |
| [Unspecified](Unspecified_Depressive_Disorder/knowledge.json) | Professional residual-category review where appropriate; an unfinished conversation alone is not this diagnosis. |

Symptom features and life-stage contexts are additional axes, not more peer disorders. Apply them only where the relevant package allows. Menstrual applicability is not guessed from name, gender presentation or age alone. Prospective daily records are central to reliable cycle-pattern assessment; one chat cannot supply them. [ISPMD_2011]

Pregnancy/postpartum opens a relevant context branch, including review of bipolar/psychotic concerns. Broader perinatal service scope and a formal onset specifier are different concepts. [ACOG_4] Seasonal questions require a longitudinal pattern, not merely symptoms occurring in winter. [NIMH_SEASONAL]

Older adults use the same adult route with appropriate communication, medical and cognitive context; age does not itself explain symptoms. New cognitive concerns can open the focused cognitive/delirium pathway. [NIMH_DEP; existing Alternatives package]

The focused alternatives can coexist with depression. They identify what needs clarification/review; they do not automatically diagnose every alternative or demand that one explanation exclude all others.

## The rule after every patient reply

This is our proposed orchestration policy:

1. Keep the reply and its speaker/source context. Clarify uncertain transcription rather than treating it as reliable evidence.
2. Extract **all clinically relevant information volunteered**, including answers to later topics. Keep care goals/preferences separately; do not discard them.
3. Update findings by concept, subject and relevant period. Preserve corrections and provenance rather than overwriting current/historical differences.
4. Check safety, acute concerns and pause/skip/stop requests before ordinary progression.
5. Check whether the selected target and other targets were already answered.
6. Choose one useful missing target, or summarize/pause with gaps. Ask naturally, then repeat the loop.

The extractor receives history and relevant concept definitions/attributes. The planner receives updated evidence, coverage, applicable branch rules and unresolved needs. The conversational agent receives the selected target, its meaning, relevant context and participation boundaries. These are planned role contracts, not existing integration changes.

### When to follow up

Ask if a detail is applicable, still unknown/ambiguous, and useful for interpreting the finding or deciding the next step. Examples include clarifying which period a report concerns, what an ambiguous answer means, or an important concept-specific detail. Do not require every optional attribute for every finding.

Example: "For six weeks, almost every day, most of the day" already answers duration, frequency and daily extent **for the symptom it clearly describes**. Do not ask them again. It does not automatically describe every other symptom.

Example: after "Have you had trouble falling asleep?", a clear "Yes" can be interpreted using that question. After "Is your sleep longer or shorter?", "Yes" does not establish a direction; clarify. Context links are allowed, but quotations and uncertainty must remain traceable.

### When the reply changes topic

If it adds relevant information, save it and update priorities before returning. For an unrelated topic, briefly acknowledge it and offer a bridge. Example:

> We can come back to that. Would you be comfortable returning to how your sleep has changed?

If they decline, mark the target declined/deferred and explain its relevance briefly when helpful. Do not repeat the same question until they comply. If a current safety concern is present, follow the reviewed safety pathway rather than ordinary topic-return logic.

## Measurement is a separate procedure

The original PHQ-9 study evaluated a symptom measure against an independent professional interview; it does not validate diagnosing every depressive category from a score. The PHQ-2 study evaluated a shorter screen. [PHQ9_2001; PHQ2_2003]

Our proposed default is to offer PHQ-9 as an optional baseline after the initial account/safety review, when useful and acceptable; M8 is the checkpoint to decide whether measurement is needed or already done. PHQ-2 can serve a brief case-finding route where appropriate, but does not need to precede every assessment. Exact placement is project design and can be evaluated.

Use an approved instrument/language protocol with its specified wording, timeframe, response options and scoring. Do not turn paraphrased conversational answers into a purported completed PHQ. Keep missing answers visible. Tool-specific routing, translations and any prospective PMDD instrument are a separate next design step. No measure should gate access to safety support or appropriate review.

## Coverage and finishing

Proposed software states: `supported`, `needs_clarification`, `not_asked`, `declined`, `deferred`, `not_applicable`. Definitions are in [the route JSON](Workflow/main_assessment_route.json). They are our tracking labels, **not clinical rating-scale values**. Keep question coverage separate from whether a symptom is present, denied or uncertain. Do not silently replace existing module enums.

Summarize when there is a useful reviewable picture, the person wants to stop, burden makes deferral appropriate, or another pathway takes priority. Identify missing information rather than claiming completion. Invite corrections. Any candidate diagnosis remains provisional until qualified review; unavailable review does not equal approval.

Therapy-specific beliefs, homework and activity scores stay separate from diagnostic criteria. Raw clinical/safety statements arising in therapy can still update assessment. This route ends in a handoff, not automatic treatment activation.

## Sources, exact contributions and access

The source register below distinguishes books, guidelines, original validation papers and consensus. There is no universal book chapter that supplies a proven exact question sequence for all seven adult categories. Full source locations, contributions and access limitations are in [the source register](Workflow/main_assessment_route_sources.json).

| Source | Exact contribution and locator |
|---|---|
| [INTERVIEW_BOOK: Lichstein, The Medical Interview, Clinical Methods, 3rd ed. (1990), chapter 3](https://www.ncbi.nlm.nih.gov/books/NBK349/) | The History of Present Illness; open-to-focused questioning; metadata PMID 21250190. General interviewing technique only; not current depressive diagnostic criteria or proof of our sequence. |
| [APA_EVALUATION: APA Practice Guidelines for the Psychiatric Evaluation of Adults, executive summary (2015)](https://psychiatryonline.org/doi/pdf/10.1176/appi.ajp.2015.1720501) | Table 1, printed p.800: evaluation domains; official APA guideline landing page. Psychiatric, treatment, medical, reproductive, medication and substance-use background domains. |
| [WHO_TRAIN_DEP: WHO mhGAP training manual for mhGAP-IG version 2.0 (for field testing), Depression module (2017)](https://cdn.who.int/media/docs/default-source/brain-health/mhgap-training-manuals/dep_module.pdf) | Session 2, printed pp.150-156 / PDF pp.8-14; especially pp.151,153,156. Worked assessment example: patient's language, symptom/function assessment, other explanations, safety and appropriate modules. |
| [WHO_IG2: WHO mhGAP Intervention Guide version 2.0 (2016)](https://www.who.int/publications/i/item/9789241549790) | Essential Care and Practice; DEP 1 assessment, printed pp.21-25. Modular decision-chart architecture for non-specialist clinical services; illustrative framework only. |
| [NICE_222: NICE NG222, Depression in adults: treatment and management](https://www.nice.org.uk/guidance/ng222/chapter/Recommendations) | 1.2.1-1.2.9: recognition, comprehensive assessment, relevant history and direct suicide enquiry. Broad assessment requirements; does not prescribe our numbered route. |
| [VA_POCKET_2022: VA/DoD MDD Clinical Practice Guideline pocket card (February 2022)](https://www.healthquality.va.gov/guidelines/MH/mdd/VADoDMDDCPG_PocketCard_Final_508_updated.pdf) | PDF p.1: Module A boxes 1-8 and Sidebar 1. Suspected depression -> work-up/safety -> diagnostic review; history/function and optional PHQ-9. |
| [NICE_185: NICE CG185, Bipolar disorder: assessment and management](https://www.nice.org.uk/guidance/cg185/chapter/recommendations) | 1.2.1-1.2.3; 1.3.2. Explore previous activation in people presenting with depression; specialist assessment rather than questionnaire diagnosis. |
| [NIMH_BSSA: NIMH Adult Outpatient Brief Suicide Safety Assessment Guide](https://www.nimh.nih.gov/research/research-conducted-at-nimh/asq-toolkit-materials/adult-outpatient/adult-outpatient-brief-suicide-safety-assessment-guide) | Intended users; current thoughts, plan, past behaviour, supports and disposition. Safety enquiry domains and need for qualified review; used after a positive ASQ in its original protocol. |
| [NICE_225: NICE NG225, Self-harm](https://www.nice.org.uk/guidance/ng225/chapter/recommendations) | 1.6.1-1.6.6. Needs-focused safety assessment; no predictive low/medium/high labels or score-only discharge. |
| [NICE_197: NICE NG197, Shared decision making](https://www.nice.org.uk/guidance/ng197/chapter/recommendations) | 1.2.7-1.2.11. Shared agenda, participation, preferences and manageable information. |
| [PHQ9_2001: Kroenke, Spitzer & Williams (2001), The PHQ-9: Validity of a Brief Depression Severity Measure](https://pmc.ncbi.nlm.nih.gov/articles/PMC1495268/) | Methods: Mental Health Professional Validation Interviews; PMID 11556941. Original primary validation: questionnaire compared with independent interview; no proof of all-type diagnosis or our ordering. |
| [PHQ2_2003: Kroenke, Spitzer & Williams (2003), The Patient Health Questionnaire-2: validity of a two-item depression screener](https://pubmed.ncbi.nlm.nih.gov/14583691/) | Abstract, purpose and methods. Brief two-item screening purpose; not a universal entry/exit gate for all depressive presentations. |
| [ISPMD_2011: O'Brien et al. (2011), ISPMD Montreal consensus](https://pmc.ncbi.nlm.nih.gov/articles/PMC4134928/) | Methods of measurement; prospective daily symptom ratings. Cycle-wide prospective tracking instead of confirming a menstrual pattern from a single conversation. |
| [ACOG_4: ACOG Clinical Practice Guideline No.4 (2023), Screening and Diagnosis of Mental Health Conditions During Pregnancy and Postpartum](https://www.acog.org/clinical/clinical-guidance/clinical-practice-guideline/articles/2023/06/screening-and-diagnosis-of-mental-health-conditions-during-pregnancy-and-postpartum) | Purpose and target population; linked module has detailed source locations. Perinatal context includes broader assessment than a formal onset specifier; includes bipolar and postpartum psychosis concerns. |
| [NIMH_DEP: NIMH, Depression](https://www.nimh.nih.gov/health/publications/depression) | Symptoms; diagnosis; older-adult presentation. Medical/contextual review and age-sensitive assessment; no exclusion of depression based on age. |
| [NIMH_SEASONAL: NIMH, Seasonal Affective Disorder](https://www.nimh.nih.gov/health/publications/seasonal-affective-disorder) | Diagnosis section. Repeated seasonal course requires longitudinal history, not one winter episode. |

No licensed MINI/SCID item set or DSM manual text is reproduced here. Existing disorder packages retain their own classification sources, detailed concept attributes, source limitations and review gates. This route does not replace those packages or flatten their concepts.

## Files and what remains

- This Markdown file: readable route, reasoning, examples and boundaries for the team.
- [Route JSON](Workflow/main_assessment_route.json): proposed modules, branch references, selection rules and tracking-state meanings.
- [Source register](Workflow/main_assessment_route_sources.json): evidence provenance for this route.

These are design artifacts and are not wired into the running agents. Structural checks verify file references and design consistency, not clinical safety, diagnostic accuracy or benefit.

Next: review this route together, then build the detailed target/follow-up catalogue for M3 using each concept's own information requirements. Operational safety/referral workflow, clinical review, shared concept mapping, standardized-tool/language protocols and fictional-case evaluation remain required before execution claims.

<!-- detailed-interview-graph-design -->

A first detailed graph draft is now available: [interview graph and rules](12_Adult_Depression_Interview_Graph_and_Rules.md). It includes catalog references, reply/branch policies and an offline annotated-state preview. The runtime and clinical review status above remain unchanged.
