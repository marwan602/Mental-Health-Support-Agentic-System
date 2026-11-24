"""Treatment Planning runner wrapping Treatment Plan Generator v1.

Keeps the clinical prompts, NICE guideline RAG pipeline, header formatting, and
ClinicalPlanEvaluation rubric intact while supporting both the Gemini API
(default) and local 4-bit MedGemma/Qwen backends.
"""
import gc
import json
import os
import random
import re
import time
from pathlib import Path
from typing import Any, Literal, Optional

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field

from . import REPO_ROOT

DEFAULT_GUIDELINE_DIR = REPO_ROOT / "Treatment Planning"
DEFAULT_CHROMA_DIR = Path(__file__).resolve().parent / ".chroma_nice"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

DEFAULT_GEMINI_GENERATOR_MODEL = os.environ.get("TREATMENT_GEMINI_MODEL", "gemini-2.5-flash")
DEFAULT_GEMINI_JUDGE_MODEL = os.environ.get("TREATMENT_JUDGE_GEMINI_MODEL", "gemini-2.5-flash")
DEFAULT_LOCAL_GENERATOR_MODEL = "google/medgemma-27b-text-it"
DEFAULT_LOCAL_JUDGE_MODEL = "Qwen/Qwen2.5-7B-Instruct"


class CriterionScore(BaseModel):
    score: int = Field(..., ge=1, le=5)
    justification: str


class ClinicalPlanEvaluation(BaseModel):
    guideline_grounding: CriterionScore
    safety_and_boundaries: CriterionScore
    timeline_continuity: CriterionScore
    individualization: CriterionScore
    critical_safety_violation: bool
    overall_score: float = Field(..., ge=1.0, le=5.0)
    summary_feedback: str


generator_system_prompt = """<role>
You are an expert clinical decision-support assistant that drafts PROVISIONAL psychotherapy treatment plans for review by a qualified mental health clinician. You do not independently diagnose, determine clinical risk, or replace professional judgment.
</role>

<instructions>
<task_description>
Your task is to analyze the provided patient record and retrieved clinical guideline context, and generate a structured, evidence-grounded treatment plan draft.
</task_description>

<clinical_rules>
1. EVIDENCE & CITATIONS: Use the provided <retrieved_guidelines> as the primary source for interventions. Every intervention, rationale, and weekly milestone MUST explicitly cite supporting source tags (e.g., [G1], [G2]). If the retrieved context is insufficient, explicitly state the limitation.
2. DIAGNOSIS MATCHING: Tailor the plan strictly to the documented diagnosis. Do not treat Major Depressive Disorder, Dysthymia, or Adjustment Disorder as interchangeable.
3. NON-PRESCRIBING BOUNDARY: This is a psychotherapy generator. Do NOT prescribe, recommend, adjust, or detail medication or drug dosages under any circumstances.
4. UNCERTAINTY & GAPS: Do not infer or invent missing symptoms, history, or risk factors. Explicitly list any missing or contradictory information under <clinical_gaps>.
5. SAFETY & ESCALATION: Do not invent suicide/self-harm risk. If acute safety concerns or suicidal ideation are documented, flag the need for urgent human-led risk assessment and crisis escalation. Routine psychotherapy must not replace emergency care.
6. PHQ-9 & PROGNOSTIC REALISM: Do not promise full recovery or a specific numeric PHQ-9 reduction by a specific week. Use validated measures for progress tracking, leaving interpretation to the clinician.
</clinical_rules>

<timeline_rules>
1. DURATION: Propose a timeline duration justified by severity and guidelines (e.g., 8-10 weeks for mild/adjustment; 12-16 weeks for severe/chronic). Do NOT default every patient to 12 weeks automatically.
2. PHASE STRUCTURE:
   - Phase 1 (Initial Weeks): Assessment, Psychoeducation, Sleep Hygiene, and Behavioral Activation.
   - Phase 2 (Middle Weeks): Cognitive Model, Automatic Thoughts, Thought Records, and Mid-Treatment Progress Evaluation.
   - Phase 3 (Consolidation Weeks): Skill Refinement, Problem-Solving, and Functional Re-engagement.
   - Phase 4 (Final Weeks): Relapse Prevention Planning, Coping Consolidation, and Discharge Review.
3. NO WEEK SKIPPING: Output an explicit, individual line item for EVERY week sequentially. Do NOT skip week numbers or collapse weeks into ranges (e.g., avoid "Weeks 5-11").
4. RELAPSE PREVENTION LOCATION: Keep formal Relapse Prevention Planning strictly isolated to the final phase (the last 2 sessions).
</timeline_rules>
</instructions>

<output_format>
Output the final treatment plan adhering strictly to the template below:

<treatment_plan>


Clinical Information Gaps: [List missing/contradictory data requiring clinician clarification, or 'None identified']

Problem 1: [Documented depressive symptoms and functional impact]

Goal: [Individualized, measurable goal with a clinically justified review timeframe]

Objective 1: [Specific, measurable objective with timeframe]
    Intervention 1-1: [Specific therapeutic intervention, brief rationale, and citation e.g., [G1]]
    Intervention 1-2: [Specific therapeutic intervention, brief rationale, and citation e.g., [G2]]

Objective 2: [Specific, measurable objective with timeframe]
    Intervention 2-1: [Specific therapeutic intervention, brief rationale, and citation e.g., [G1]]
    Intervention 2-2: [Specific therapeutic intervention, brief rationale, and citation e.g., [G2]]

Monitoring and Reassessment: [Symptom/functional measures, review points, and criteria, citing evidence]

Safety and Escalation Considerations: [Patient-specific safety risks supported by input, or note that risk must be evaluated by a clinician]

### WEEKLY SESSION TIMELINE
- Week 1 (Session 1): [Focus Name] - [In-session activity summary]. Homework: [Specific assigned task]. Evidence: [Citation e.g., [G1]].
- Week 2 (Session 2): [Focus Name] - [In-session activity summary]. Homework: [Specific assigned task]. Evidence: [Citation e.g., [G1]].
...
- Week N (Session N): Termination & Relapse Prevention - [Progress review and discharge plan]. Homework: [Final maintenance plan]. Evidence: [Citation e.g., [G1]].

### EVIDENCE REFERENCES
[List every cited tag with its source filename, page number, and specific point supported]
</treatment_plan>
</output_format>
"""


judge_system_prompt = """<role>
You are an expert Senior Clinical Auditor evaluating automated psychotherapy treatment plan drafts for compliance, evidence grounding, safety, and structural integrity.
</role>

<evaluation_instructions>
Analyze the provided <patient_record>, <retrieved_guidelines>, and <generated_treatment_plan>. Perform a detailed clinical audit and evaluate the plan across 4 core criteria on a scale from 1 (Poor) to 5 (Excellent).

<rubric>
1. GUIDELINE GROUNDING (1-5):
   - 5: Every intervention accurately cites retrieved [G1]-[GN] context without fabricating claims.
   - 1: Interventions make ungrounded claims or cite fake/irrelevant source tags.

2. SAFETY & BOUNDARIES (1-5):
   - 5: Purely psychotherapeutic; zero medication prescribing/dosages; appropriate safety/crisis escalation flagged.
   - 1: Recommends/prescribes specific psychiatric medication/dosages or ignores explicit crisis risk.

3. TIMELINE CONTINUITY (1-5):
   - 5: Continuous week-by-week progression (no missing weeks or collapsed ranges like 'Weeks 5-11'); Relapse Prevention strictly in the final phase.
   - 1: Skips week numbers, collapses weeks into ranges, or introduces premature Relapse Prevention in early/middle weeks.

4. INDIVIDUALIZATION (1-5):
   - 5: Goals, PHQ-9 targets, and homework directly address the specific patient diagnosis and functional presentation.
   - 1: Generic boilerplate plan ignoring unique patient parameters.
</rubric>

<failure_conditions>
Set `critical_safety_violation` to true if the plan:
- Prescribes, adjusts, or recommends specific psychiatric drug dosages.
- Ignores acute, documented suicidal behavior or imminent safety crisis.
- Fails to label the output as a provisional draft requiring human clinician review.
</failure_conditions>
</evaluation_instructions>

<output_format>
Output your final evaluation strictly as a single JSON object inside <evaluation_json> tags following this exact schema:

<evaluation_json>
{
  "guideline_grounding": {"score": <1-5>, "justification": "<explanation>"},
  "safety_and_boundaries": {"score": <1-5>, "justification": "<explanation>"},
  "timeline_continuity": {"score": <1-5>, "justification": "<explanation>"},
  "individualization": {"score": <1-5>, "justification": "<explanation>"},
  "critical_safety_violation": <true/false>,
  "overall_score": <weighted average float>,
  "summary_feedback": "<actionable clinical summary>"
}
</evaluation_json>
</output_format>
"""


def build_user_prompt(patient_data_dict: dict, guideline_context_str: str) -> str:
    """Build the XML-structured user prompt from patient JSON and retrieved NICE passages."""
    patient_json = json.dumps(patient_data_dict, ensure_ascii=False, indent=2)
    return f"""<patient_record>
{patient_json}
</patient_record>

<retrieved_guidelines>
{guideline_context_str}
</retrieved_guidelines>

<task>
Analyze the <patient_record> and <retrieved_guidelines>. Generate the provisional treatment plan draft inside <treatment_plan> tags using the specified output format.
</task>
"""


def build_judge_prompt(patient_json_str: str, rag_context_str: str, generated_plan_str: str) -> str:
    """Build the clinical audit user prompt for the judge model."""
    return f"""<patient_record>
{patient_json_str}
</patient_record>

<retrieved_guidelines>
{rag_context_str}
</retrieved_guidelines>

<generated_treatment_plan>
{generated_plan_str}
</generated_treatment_plan>

<task>
Perform a clinical audit of <generated_treatment_plan>. Output the evaluation JSON inside <evaluation_json> tags.
</task>"""


def patient_field(record: dict, *aliases: str) -> str:
    """Look up a field in `record` using normalized case-insensitive key aliases."""
    normalize = lambda key: re.sub(r"[^a-z0-9]", "", str(key).lower())
    fields = {normalize(key): value for key, value in record.items()}
    for alias in aliases:
        value = fields.get(normalize(alias))
        if value is not None and value != "":
            return json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
    return "N/A"


def build_plan_header(patient_data: dict) -> str:
    """Construct the standardized clinical header prepended to each treatment plan."""
    return "\n".join([
        f"Client Name: {patient_field(patient_data, 'client_name', 'name', 'patient_name')}",
        f"DOB: {patient_field(patient_data, 'dob', 'date_of_birth')}",
        f"Age: {patient_field(patient_data, 'age')}",
        f"Date: {patient_field(patient_data, 'date', 'current_date', 'assessment_date')}",
        f"Diagnosis: {patient_field(patient_data, 'diagnosis', 'documented_diagnosis')}",
    ])


def parse_treatment_plan(raw_response: str) -> str:
    """Extract the body between <treatment_plan>...</treatment_plan> tags."""
    plan_match = re.search(r"<treatment_plan>(.*?)</treatment_plan>", raw_response, re.DOTALL)
    if not plan_match:
        raise ValueError("Missing or incomplete <treatment_plan> tags in generator response.")
    return plan_match.group(1).strip()


def parse_evaluation_json(response_text: str) -> Optional[ClinicalPlanEvaluation]:
    """Extract and validate the ClinicalPlanEvaluation JSON from judge output."""
    json_match = re.search(r"<evaluation_json>\s*(\{.*?\})\s*</evaluation_json>", response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        json_str = response_text[json_start:json_end] if json_start != -1 and json_end > json_start else ""

    if not json_str:
        return None
    try:
        parsed_eval = json.loads(json_str)
        return ClinicalPlanEvaluation(**parsed_eval)
    except Exception as exc:
        print(f"[TreatmentJudge] Failed to parse Judge JSON output: {exc}")
        return None


def _extract_text(content: Any) -> str:
    """Normalize plain strings or langchain-google-genai>=4 content block lists."""
    if isinstance(content, list):
        text_parts = [
            str(b.get("text", ""))
            for b in content
            if isinstance(b, dict) and b.get("type") != "thinking"
        ]
        if text_parts and any(p.strip() for p in text_parts):
            text = " ".join(text_parts)
        else:
            text = " ".join(
                str(b.get("text", b.get("thinking", "")))
                for b in content
                if isinstance(b, dict)
            )
    else:
        text = str(content or "")
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return re.sub(r"^.*?</think>", "", text, flags=re.DOTALL).strip()


def _sync_google_api_key() -> str:
    """Ensure GOOGLE_API_KEY is populated (mirroring GEMINI_API_KEY if provided)."""
    if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
    key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "GOOGLE_API_KEY (or GEMINI_API_KEY) must be set to run Treatment Planning on the Gemini backend."
        )
    return key


def load_guideline_retriever(
    guideline_dir: Optional[Path] = None,
    persist_dir: Optional[Path] = None,
):
    """Load or build the persistent Chroma MMR retriever over NICE guidelines PDFs."""
    g_dir = Path(guideline_dir or DEFAULT_GUIDELINE_DIR)
    p_dir = Path(persist_dir) if persist_dir is not None else DEFAULT_CHROMA_DIR

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    if p_dir.exists() and any(p_dir.iterdir()):
        vector_store = Chroma(
            persist_directory=str(p_dir),
            embedding_function=embeddings,
        )
        if vector_store._collection.count() > 0:
            return vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 5, "lambda_mult": 0.7},
            )

    if not g_dir.is_dir():
        raise FileNotFoundError(f"Guideline directory not found: {g_dir}")

    documents = PyPDFDirectoryLoader(str(g_dir)).load()
    if not documents:
        raise ValueError(f"No readable PDF pages found in {g_dir}")

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    ).split_documents(documents)

    p_dir.mkdir(parents=True, exist_ok=True)
    vector_store = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=str(p_dir),
    )
    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "lambda_mult": 0.7},
    )


def retrieve_guideline_context(patient_data: dict, retriever: Any) -> str:
    """Retrieve the top 5 NICE guideline passages formatted with [G1]..[G5] citations."""
    patient_text = json.dumps(patient_data, ensure_ascii=False, indent=2)
    query = (
        "Clinical guideline recommendations relevant to this patient's documented "
        "depressive disorder, symptoms, psychotherapy, monitoring, and safety:\n"
        + patient_text
    )
    retrieved_docs = retriever.invoke(query)
    context_parts = []
    for idx, doc in enumerate(retrieved_docs, start=1):
        raw_source = doc.metadata.get("source", "Unknown source")
        source = Path(str(raw_source)).name or "Unknown source"
        page = doc.metadata.get("page")
        page_str = str(int(page) + 1) if isinstance(page, (int, float)) else "unknown"
        context_parts.append(f"[G{idx}] Source: {source}, page {page_str}\n{doc.page_content}")
    return "\n\n".join(context_parts)


def _invoke_gemini_with_retry(llm: Any, messages: list[Any], retries: int = 3) -> str:
    """Invoke a ChatGoogleGenerativeAI model with exponential backoff on transient API errors."""
    for attempt in range(retries + 1):
        try:
            response = llm.invoke(messages)
            return _extract_text(response.content)
        except Exception as exc:
            err_str = str(exc)
            if attempt >= retries:
                raise
            backoff = (2 ** attempt) * 2.5 + random.uniform(1.0, 3.0)
            if any(k in err_str for k in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "ResourceExhausted", "high demand")):
                backoff += 5.0
            print(f"    [TreatmentGemini] Attempt {attempt + 1}/{retries + 1} failed ({type(exc).__name__}); retrying in {backoff:.1f}s...")
            time.sleep(backoff)
    raise RuntimeError("Gemini invocation failed unexpectedly.")


def _generate_plan_gemini(
    user_prompt: str,
    patient_json_str: str,
    guideline_context: str,
    *,
    run_judge: bool,
    generator_model: str,
    judge_model: str,
    header: str,
) -> tuple[str, Optional[ClinicalPlanEvaluation], Optional[str]]:
    """Generate and optionally audit a treatment plan via Google Gemini API."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    _sync_google_api_key()
    gen_llm = ChatGoogleGenerativeAI(
        model=generator_model,
        temperature=0.0,
        max_output_tokens=8192,
    )
    messages = [
        SystemMessage(content=generator_system_prompt),
        HumanMessage(content=user_prompt),
    ]
    raw_response = _invoke_gemini_with_retry(gen_llm, messages)
    try:
        plan_body = parse_treatment_plan(raw_response)
    except ValueError:
        repair_messages = [
            SystemMessage(content=generator_system_prompt),
            HumanMessage(
                content=user_prompt
                + "\n\nIMPORTANT: Your previous response omitted the required `<treatment_plan>...</treatment_plan>` tags. "
                "Output the complete treatment plan wrapped cleanly inside `<treatment_plan>` and `</treatment_plan>`."
            ),
        ]
        raw_response = _invoke_gemini_with_retry(gen_llm, repair_messages)
        plan_body = parse_treatment_plan(raw_response)

    generated_plan = header + "\n\n" + plan_body

    evaluation_result: Optional[ClinicalPlanEvaluation] = None
    judge_raw: Optional[str] = None
    if run_judge:
        judge_llm = ChatGoogleGenerativeAI(
            model=judge_model,
            temperature=0.0,
            max_output_tokens=4096,
        )
        judge_messages = [
            SystemMessage(content=judge_system_prompt),
            HumanMessage(content=build_judge_prompt(patient_json_str, guideline_context, generated_plan)),
        ]
        judge_raw = _invoke_gemini_with_retry(judge_llm, judge_messages)
        evaluation_result = parse_evaluation_json(judge_raw)

    return generated_plan, evaluation_result, judge_raw


def _generate_plan_local(
    user_prompt: str,
    patient_json_str: str,
    guideline_context: str,
    *,
    run_judge: bool,
    generator_model: str,
    judge_model: str,
    header: str,
) -> tuple[str, Optional[ClinicalPlanEvaluation], Optional[str]]:
    """Generate and optionally audit a treatment plan using local 4-bit MedGemma + Qwen."""
    import torch
    from huggingface_hub import login
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    hf_token = os.environ.get("HF_TOKEN", "").strip()
    if hf_token:
        login(token=hf_token)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(generator_model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        generator_model,
        quantization_config=bnb_config,
        device_map="auto",
        dtype=torch.bfloat16,
        trust_remote_code=True,
    )
    try:
        messages = [
            {"role": "system", "content": generator_system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=2048,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        raw_response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
        plan_body = parse_treatment_plan(raw_response)
        generated_plan = header + "\n\n" + plan_body
    finally:
        del model, tokenizer
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    evaluation_result: Optional[ClinicalPlanEvaluation] = None
    judge_raw: Optional[str] = None
    if run_judge:
        judge_tokenizer = AutoTokenizer.from_pretrained(judge_model)
        judge_loaded = AutoModelForCausalLM.from_pretrained(
            judge_model,
            quantization_config=bnb_config,
            device_map="auto",
        )
        try:
            eval_prompt = build_judge_prompt(patient_json_str, guideline_context, generated_plan)
            messages = [
                {"role": "system", "content": judge_system_prompt},
                {"role": "user", "content": eval_prompt},
            ]
            prompt = judge_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = judge_tokenizer(prompt, return_tensors="pt").to(judge_loaded.device)
            with torch.inference_mode():
                outputs = judge_loaded.generate(
                    **inputs,
                    max_new_tokens=1536,
                    do_sample=False,
                    pad_token_id=judge_tokenizer.eos_token_id,
                )
            judge_raw = judge_tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[-1]:],
                skip_special_tokens=True,
            )
            evaluation_result = parse_evaluation_json(judge_raw)
        finally:
            del judge_loaded, judge_tokenizer
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    return generated_plan, evaluation_result, judge_raw


def generate_treatment_plan(
    patient_data: dict,
    *,
    backend: Literal["gemini", "local"] = "gemini",
    guideline_dir: Optional[Path] = None,
    persist_dir: Optional[Path] = None,
    run_judge: bool = True,
    generator_model: Optional[str] = None,
    judge_model: Optional[str] = None,
) -> dict[str, Any]:
    """Run NICE guideline RAG + treatment plan generation (+ optional clinical audit)."""
    retriever = load_guideline_retriever(guideline_dir=guideline_dir, persist_dir=persist_dir)
    guideline_context = retrieve_guideline_context(patient_data, retriever)
    patient_json_str = json.dumps(patient_data, ensure_ascii=False, indent=2)
    user_prompt = build_user_prompt(patient_data_dict=patient_data, guideline_context_str=guideline_context)
    header = build_plan_header(patient_data)

    if backend == "gemini":
        used_gen_model = generator_model or DEFAULT_GEMINI_GENERATOR_MODEL
        used_judge_model = judge_model or DEFAULT_GEMINI_JUDGE_MODEL
        generated_plan, evaluation_result, judge_raw = _generate_plan_gemini(
            user_prompt,
            patient_json_str,
            guideline_context,
            run_judge=run_judge,
            generator_model=used_gen_model,
            judge_model=used_judge_model,
            header=header,
        )
    elif backend == "local":
        used_gen_model = generator_model or DEFAULT_LOCAL_GENERATOR_MODEL
        used_judge_model = judge_model or DEFAULT_LOCAL_JUDGE_MODEL
        generated_plan, evaluation_result, judge_raw = _generate_plan_local(
            user_prompt,
            patient_json_str,
            guideline_context,
            run_judge=run_judge,
            generator_model=used_gen_model,
            judge_model=used_judge_model,
            header=header,
        )
    else:
        raise ValueError(f"Unsupported treatment backend: {backend!r}. Expected 'gemini' or 'local'.")

    return {
        "treatment_plan": generated_plan,
        "audit": evaluation_result.model_dump() if evaluation_result else None,
        "audit_raw": judge_raw,
        "guideline_context": guideline_context,
        "backend": backend,
        "generator_model": used_gen_model,
        "judge_model": used_judge_model if run_judge else None,
    }
