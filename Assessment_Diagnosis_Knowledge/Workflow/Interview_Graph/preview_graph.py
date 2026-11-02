"""Offline graph preview for annotated fictional state; not a clinical application."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESOLVED = {"supported", "declined", "deferred", "not_applicable"}


def load_graph():
    return json.loads((HERE / "question_graph.json").read_text(encoding="utf-8"))


def node_index(graph):
    return {x["id"]: x for x in graph["catalog"]}


def period_for(node, state):
    p = state.get("period_bindings", {}).get(node["period_binding"])
    if not isinstance(p, str) or not p.strip():
        raise ValueError("Missing explicit period binding: " + node["period_binding"])
    return p


def coverage_for(node, state):
    c = state.get("coverage", {}).get(node["id"], {})
    return c if c.get("period_id") == period_for(node, state) else {}


def blocked(node, state):
    b=state.get("blocked_targets",{}).get(node["id"],{})
    return b.get("period_id")==period_for(node,state) and bool(b.get("reason"))


def resolved(node, state):
    return blocked(node,state) or coverage_for(node,state).get("status") in RESOLVED


def result(action, why, **kwargs):
    return dict(action=action, why=why, diagnostic_conclusion=None,
                review_delivered_by_preview=False, **kwargs)


def target_result(action, node, state, why, **kwargs):
    k = node.get("knowledge_ref")
    full = None
    if k:
        data = json.loads((HERE / k["knowledge_path"]).resolve().read_text(encoding="utf-8"))
        concept = next(x for x in data["concepts"] if x["id"] == k["concept_id"])
        full = dict(concept_definition=concept["definition"],
                    do_not_infer=concept.get("do_not_infer"),
                    followup_focus=concept.get("followup_focus"))
        if k.get("attribute"):
            full["attribute_definition"] = concept["attribute_specs"][k["attribute"]]
    return result(action, why, target_id=node["id"], period_id=period_for(node, state),
                  information_to_obtain=node["information_to_obtain"],
                  example_question=node.get("example_question"), relevant_knowledge=full,
                  source_ids=node["source_ids"], clinical_source_refs=node.get("clinical_source_refs", []),
                  **kwargs)


def validate_state(graph, state):
    ix = node_index(graph)
    if not isinstance(state, dict):
        raise ValueError("State must be an object")
    for key in ["urgent_review_required", "safety_review_needed", "channel_usable"]:
        if type(state.get(key)) is not bool:
            raise ValueError("Explicit boolean required: " + key)
    if state.get("participation") not in {"not_started", "proceed", "pause", "stop"}:
        raise ValueError("Invalid participation state")
    for nid, c in state.get("coverage", {}).items():
        if nid not in ix or c.get("status") not in graph["coverage_states"]:
            raise ValueError("Unknown target/coverage state: " + nid)
        if not c.get("period_id") or type(c.get("revision")) is not int or c["revision"] < 1:
            raise ValueError("Coverage needs an explicit period and positive revision")
        if c["status"] == "supported" and not c.get("source_message_ids"):
            raise ValueError("Supported coverage needs source message pointers")
        if c["status"] in {"declined", "deferred", "not_applicable"} and not c.get("reason"):
            raise ValueError("Coverage decision needs a reason")
        if c.get('finding_status') is not None and c['finding_status'] not in graph['finding_status_values']:
            raise ValueError('Unknown clinical finding status')
    for nid,b in state.get('blocked_targets',{}).items():
        if nid not in ix or not b.get('period_id') or not b.get('reason'):
            raise ValueError('Invalid scoped target block')
    bids = {b["id"] for b in graph["branches"]}
    for bid, f in state.get("branch_facts", {}).items():
        if bid not in bids or f.get("status") not in graph["branch_fact_states"]:
            raise ValueError("Invalid branch fact: " + bid)
        if f["status"] != "unknown" and not f.get("reason"):
            raise ValueError("Branch decision needs reason")
        if f["status"] in {"open", "not_indicated"} and not f.get("source_message_ids"):
            raise ValueError("Clinical branch decision needs evidence pointers")
    for req in state.get("detail_requests", []):
        if req.get("target_id") not in ix or ix[req["target_id"]]["kind"] != "concept_detail" or not req.get("reason"):
            raise ValueError("Invalid detail request")
    n = state.get("consecutive_detail_questions", 0)
    if type(n) is not int or n < 0:
        raise ValueError("Invalid detail burst count")
    pending = state.get("pending")
    if pending:
        if pending.get("target_id") not in ix:
            raise ValueError("Unknown pending target")
        if pending.get("reply_class") not in {x["id"] for x in graph["reply_classes"]}:
            raise ValueError("Unknown reply class")
        for k in ["clarification_offers", "return_offers", "option_offers"]:
            if type(pending.get(k, 0)) is not int or pending.get(k, 0) < 0:
                raise ValueError("Invalid offer count")


def next_step(graph, state):
    """Return one proposed action; never parse text or mutate the supplied state."""
    validate_state(graph, state)
    ix = node_index(graph)
    if state["urgent_review_required"]:
        return result("URGENT_REVIEW", "Interrupt ordinary assessment; use the reviewed setting-specific response. Respect any stop request and record it.", participation=state["participation"])
    if state["safety_review_needed"]:
        return result("REVIEW_REQUIRED", "Safety review need is unresolved; this preview cannot deliver review or declare clearance.", participation=state["participation"])
    if state["participation"] in {"pause", "stop"}:
        return result(state["participation"].upper(), "Respect participation; retain findings and unresolved review needs.")
    if not state["channel_usable"]:
        return result("PAUSE_CHANNEL", "Resolve communication access; do not infer a clinical answer.")
    age = state.get("age")
    if age is None:
        return result("CHECK_SCOPE", "Establish adult eligibility without guessing age.")
    if type(age) is not int or age < 18:
        return result("OUT_OF_SCOPE", "This research graph is for adults 18+.")
    if state["participation"] == "not_started":
        return target_result("ASK", ix["q.welcome"], state, "Explain participation before assessment.")

    # Safety coverage must not become clearance. A review acknowledgement is
    # tied to the current target, period and revision, not just a timeless flag.
    for nid in ["q.safety.death_wish", "q.safety.suicidal_thoughts", "q.safety.past_behaviour"]:
        c = coverage_for(ix[nid], state)
        if blocked(ix[nid],state) and not state['blocked_targets'][nid].get('review_record'):
            return result('REVIEW_REQUIRED','Declined safety scope needs an appropriate review decision; prior answers are preserved but do not close the current information limit.',target_id=nid)
        missing_safety_finding = c.get('status')=='supported' and c.get('finding_status') is None
        needs_review = missing_safety_finding or c.get("finding_status") in {"reported_present", "unclear", "conflicting"} or c.get("status") in {"declined", "deferred", "needs_clarification"}
        ack = state.get("safety_review_acknowledgements", {}).get(nid, {})
        matches = ack.get("period_id") == c.get("period_id") and ack.get("coverage_revision") == c.get("revision") and bool(ack.get("review_record"))
        if needs_review and not matches:
            return result("REVIEW_REQUIRED", "Positive/unclear or unanswered important safety information needs an appropriate review decision; no forced answer.", target_id=nid)

    p = state.get("pending")
    if p:
        node = ix[p["target_id"]]
        c = coverage_for(node, state)
        kind = p["reply_class"]
        if kind == "communication_failure":
            return result("PAUSE_CHANNEL", "Clarify channel/transcription failure before treating the reply as an answer.")
        if kind == "pause_or_stop":
            return result("PAUSE", "Application must reconcile the participation request before continuing.")
        if kind == "declined":
            scope = p.get("decline_scope", "target")
            if scope == "session":
                return result("STOP", "Session-level decline; keep previous facts and unresolved needs.")
            ids = [node["id"]]
            kr = node.get("knowledge_ref")
            if scope == "concept" and kr:
                ids = [n["id"] for n in graph["catalog"] if n.get("knowledge_ref") and
                       n["knowledge_ref"]["module_id"] == kr["module_id"] and n["knowledge_ref"]["concept_id"] == kr["concept_id"]]
            elif scope == "module":
                mid = p.get("declined_module")
                ids=graph['decline_module_members'].get(mid,[])
                if not ids:
                    branch = next((b for b in graph["branches"] if b["id"] == mid), None)
                    ids = branch["node_ids"] if branch else []
                if not ids:
                    return result("RECONCILE_SCOPE", "Clarify the scope of module decline; do not keep questioning while scope is unresolved.")
            elif scope != "target":
                return result("RECONCILE_SCOPE", "Clarify decline scope before further questions.")
            root_ids=set(ids)
            ids=sorted(set(ids)|{n['id'] for n in graph['catalog'] if n.get('root_id') in root_ids})
            blocks=[dict(target_id=nid,period_id=period_for(ix[nid],state),reason='Person declined this scope for the current assessment.') for nid in ids]
            return result("RECORD_DECLINE", "Record outstanding targets at the stated scope; preserve existing supported facts and do not infer absence. Apply separate target blocks even for concepts with earlier supported facts.", affected_target_ids=ids,
                          blocked_target_specs=blocks,update_only_unresolved=True, coverage_status="declined", requires_review_decision=any(n.startswith('q.safety.') for n in ids))
        if not resolved(node,state):
            if kind in {"unclear", "contradictory", "partial"}:
                if p.get("clarification_offers", 0) < graph["retry_policy"]["max_clarification_offers"]:
                    return target_result("CLARIFY", node, state, "Clarify only the unresolved meaning/part; preserve what is already supported and both reports if conflicting.")
            elif kind in {"relevant_off_topic", "unrelated_off_topic"}:
                if p.get("return_offers", 0) < graph["retry_policy"]["max_return_offers"]:
                    return target_result("RETURN_OFFER", node, state, "First retain relevant volunteered information and check updated priorities; offer a return only if still useful.")
            elif kind in {"does_not_know", "no_answer"}:
                if p.get("option_offers", 0) < 1:
                    return target_result("OFFER_OPTIONS", node, state, "Offer a simpler wording, an optional time anchor, leaving it for now, or a pause. Do not force a choice.")
            elif kind == "answered":
                return result("RECONCILE_EVIDENCE", "An answered reply lacks resolved target coverage; adapter must distinguish supported/unclear/declined before routing.", target_id=node["id"])
            return result("DEFER_TARGET", "Ordinary target remains unresolved after the offered clarification/return; retain a gap and move on after applying this update.", target_id=node["id"],period_id=period_for(node,state),coverage_status="deferred",requires_review_decision=node["id"].startswith("q.safety."))

    # No details may delay the initial account/early safety checkpoints.
    prefix = graph["core_agenda"][:2]
    for block in prefix:
        for nid in block["node_ids"]:
            if not resolved(ix[nid],state):
                return target_result("ASK", ix[nid], state, "Next unanswered initial account or early safety target.")

    # An explicitly justified open branch may move earlier. This is relevance,
    # never a positive diagnostic label; routine branches otherwise follow core.
    priority = state.get("priority_branch")
    if priority:
        branch = next((b for b in graph["branches"] if b["id"] == priority.get("id")), None)
        if not branch or not priority.get("reason") or state.get("branch_facts",{}).get(branch["id"],{}).get("status") != "open":
            raise ValueError("Priority branch must be open and justified")
        if branch.get("requires_professional_review"):
            return result("FEATURE_REVIEW_REQUIRED", "Feature needs professional observation/examination; do not administer a lay diagnostic sign checklist.", branch_id=branch["id"])
        for nid in branch["node_ids"]:
            if not resolved(ix[nid],state):
                return target_result("ASK",ix[nid],state,"Explicitly justified early branch: "+priority["reason"])

    if state.get("consecutive_detail_questions",0) < graph["followup_policy"]["ordinary_detail_burst_limit"]:
        for req in state.get("detail_requests",[]):
            node = ix[req["target_id"]]
            if resolved(node,state):
                continue
            parent = ix[node["root_id"]]
            pc = coverage_for(parent,state)
            if pc.get('status')!='supported' or pc.get("finding_status") != "reported_present" or blocked(parent,state):
                continue
            tag = node.get("required_fact_tag")
            if tag and tag not in state.get("fact_tags",{}).get(node["root_id"],[]):
                continue
            return target_result("ASK",node,state,"Relevant missing detail requested by planner: "+req["reason"])

    for block in graph["core_agenda"][2:]:
        for nid in block["node_ids"]:
            if not resolved(ix[nid],state):
                return target_result("ASK", ix[nid], state, "Next uncovered core target; default module order is project design.")
    for branch in graph["branches"]:
        if state.get("branch_facts",{}).get(branch["id"],{}).get("status") != "open":
            continue
        if branch.get("requires_professional_review"):
            return result("FEATURE_REVIEW_REQUIRED", "Professional observation/examination is needed for this feature; record review rather than self-diagnosis.",branch_id=branch["id"])
        for nid in branch["node_ids"]:
            if not resolved(ix[nid],state):
                return target_result("ASK",ix[nid],state,"Next uncovered target in an explicitly open branch.")
    if state.get("measurement_requested"):
        nid = graph["optional_measurement_node"]
        if not resolved(ix[nid],state):
            return target_result("ASK",ix[nid],state,"Optional measurement offer; actual tools need a separate protocol.")
    nid = graph["summary_node"]
    if not resolved(ix[nid],state):
        return target_result("PREPARE_SUMMARY",ix[nid],state,"Present supported findings and gaps, then invite corrections; do not declare assessment or diagnosis complete.")
    unresolved = [b["id"] for b in graph["branches"] if state.get("branch_facts",{}).get(b["id"],{}).get("status","unknown") in {"unknown","deferred"}]
    unresolved_details=[r['target_id'] for r in state.get('detail_requests',[]) if coverage_for(ix[r['target_id']],state).get('status')!='supported']
    limited=[nid for nid,c in state.get('coverage',{}).items() if c.get('status') in {'declined','deferred','needs_clarification'}]
    return result("HANDOFF_WITH_GAPS", "Prepare source-grounded candidate explanations for qualified review, including unresolved branches; no automatic diagnosis/treatment.",unresolved_branch_ids=unresolved,unresolved_detail_ids=unresolved_details,limited_target_ids=limited,blocked_target_ids=list(state.get('blocked_targets',{})))


def validate_graph(graph):
    ix = node_index(graph)
    assert len(ix) == len(graph["catalog"]), "Duplicate target IDs"
    sources=json.loads((HERE/graph["sources"]).read_text(encoding="utf-8"))
    for n in graph["catalog"]:
        assert n["information_to_obtain"].strip()
        assert all(s in sources for s in n["source_ids"])
        kr=n.get("knowledge_ref")
        if kr:
            k=json.loads((HERE/kr["knowledge_path"]).resolve().read_text(encoding="utf-8"))
            assert k["module_id"] == kr["module_id"]
            c=next(c for c in k["concepts"] if c["id"]==kr["concept_id"])
            if kr.get("attribute"): assert kr["attribute"] in c["attribute_specs"]
        for sr in n.get("clinical_source_refs",[]):
            sd=json.loads((HERE/sr["source_path"]).resolve().read_text(encoding="utf-8"))
            assert sr["source_id"] in sd
        if n["kind"]=="concept_detail":assert n["root_id"] in ix
    scheduled=set()
    for b in graph["core_agenda"]+graph["branches"]:
        for nid in b["node_ids"]:assert nid in ix
        scheduled.update(b["node_ids"])
    assert all(s in sources for b in graph["branches"] for s in b["source_ids"])
    rules={r['id']:r for r in graph['rule_source_map']}
    controls={n['id'] for n in graph['control_graph']['nodes']}
    for e in graph['control_graph']['edges']:
        assert e['source'] in controls and e['target'] in controls
        assert e['rule_id'] in rules and e['condition']
    assert all(s in sources for r in rules.values() for s in r['source_ids'])
    assert not graph["confirmed_diagnosis_enabled"] and not graph["operational_safety_pathway_implemented"]
    assert not graph["licensed_instrument_items_included"]
    return dict(catalog_targets=len(ix), branches=len(graph["branches"]),scheduled_entry_targets=len(scheduled),references="PASS")


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--validate",action="store_true")
    ap.add_argument("--case",default="all")
    ap.add_argument("--state",type=Path)
    ap.add_argument("--target")
    args=ap.parse_args()
    g=load_graph()
    if args.target:
        n=node_index(g).get(args.target)
        if n is None:raise ValueError("Unknown target ID")
        print(json.dumps(n,indent=2,ensure_ascii=True));return
    if args.state:
        print(json.dumps(next_step(g,json.loads(args.state.read_text(encoding="utf-8"))),indent=2,ensure_ascii=True));return
    report=validate_graph(g)
    fixtures=json.loads((HERE/"fictional_cases.json").read_text(encoding="utf-8"))
    outcomes=[]
    for case in fixtures:
        if args.case!="all" and args.case!=case["id"]:continue
        before=json.dumps(case["state"],sort_keys=True)
        try:
            actual=next_step(g,case["state"])
        except ValueError:
            if case.get("expected_error")!="ValueError":raise
            actual={"action":"REJECT_INVALID_STATE"}
        assert json.dumps(case["state"],sort_keys=True)==before,"Router mutated state"
        for key,value in case["expected"].items():assert actual.get(key)==value,(case["id"],key,actual)
        if case['id']=='module_decline_emits_root_and_detail_blocks':
            assert 'detail/MDD/depressed_mood/duration' in actual['affected_target_ids']
            assert actual['update_only_unresolved'] is True
            assert actual['blocked_target_specs']
        outcomes.append(dict(case=case["id"],action=actual["action"],target_id=actual.get("target_id"),status="PASS"))
    if not outcomes:raise ValueError("No matching fictional case")
    print(json.dumps(dict(structure=report,case_count=len(outcomes),cases=outcomes,interpretation="Mechanical routing of annotated fictional state only; not NLP extraction, diagnostic accuracy or clinical safety validation."),indent=2))


if __name__=="__main__":main()
