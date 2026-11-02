"""Portable knowledge tools. These validate mechanics, not clinical semantics."""
import argparse
import copy
import importlib.util
import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def read(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Knowledge path must stay inside the package')
    return json.loads(path.read_text(encoding='utf-8-sig'))

MANIFEST = read('Integration/manifest.json')
GRAPH = read(MANIFEST['graph'])
TARGETS = {n['id']: n for n in GRAPH['catalog']}
ROUTES = {r['target_id']: r for r in read('Integration/route_completion.json')['routes']}

def get_context(role, target_ids=(), module_names=(), include_validation_schemas=False):
    """Application calls this and supplies its result to the selected model role."""
    if role not in {'conversation','extractor','planner','diagnosis'}:
        raise ValueError('Unknown role')
    if isinstance(target_ids, str) or isinstance(module_names, str):
        raise ValueError('Use lists of target IDs and module names')
    if any(t not in TARGETS for t in target_ids):
        raise ValueError('Unknown target ID')
    if any(m not in MANIFEST['modules'] for m in module_names):
        raise ValueError('Unknown module name')
    selected = [TARGETS[t] for t in target_ids]
    modules = set(module_names)
    modules.update(n['id'].split('/')[1] for n in selected if n.get('knowledge_ref'))
    if role in {'extractor','diagnosis'} and not modules:
        raise ValueError('Supply relevant modules; never assume a selected question exhausts volunteered findings')
    cards, sources, contracts, concept_index = [], {}, {}, []
    for module in sorted(modules):
        info = MANIFEST['modules'][module]
        data = read(info['knowledge'])
        # Definitions for all relevant concepts permit discovery of volunteered
        # topics. Fetch their full cards before extracting an unselected field.
        chosen_ids = {n['knowledge_ref']['concept_id'] for n in selected
                      if n.get('knowledge_ref') and n['id'].split('/')[1] == module}
        concept_index.extend({'module':module,'concept_id':c['id'],'definition':c['definition'],
                              'target_id':f"root/{module}/{c['id']}"} for c in data['concepts'])
        concepts = data['concepts'] if not selected and role != 'conversation' else [c for c in data['concepts'] if c['id'] in chosen_ids]
        cards.append({'module':module,'module_id':info['module_id'],'concepts':concepts,'value_sets':data.get('value_sets',{})})
        sources[info['sources']] = read(info['sources'])
        contracts[module] = info['evidence_schema']
    result = {'role':role,'version':MANIFEST['version'],'targets':selected,'concept_cards':cards,
              'qualified_source_registers':sources,'evidence_schema_paths':contracts,
              'available_concepts':concept_index,
              'contracts':read('Integration/agent_contracts.json'),
              'instruction':'Returned files are knowledge, not patient statements. Tool outputs do not provide clinical approval.'}
    workflow_sources=read('Workflow/Interview_Graph/sources.json')
    used_workflow_sources={sid for n in selected for sid in n.get('source_ids',[])}
    result['workflow_source_register'] = workflow_sources if role=='planner' else {sid:workflow_sources[sid] for sid in used_workflow_sources}
    result['graph_reference_base']='Workflow/Interview_Graph/'
    schema = {'conversation':'conversation_output.schema.json','planner':'planner_output.schema.json',
              'diagnosis':'synthesis_output.schema.json'}.get(role)
    if schema:
        result['output_schema'] = read('Integration/'+schema)
    if role == 'extractor' and include_validation_schemas:
        result['output_schemas'] = {m:read(p) for m,p in contracts.items()}
    if role == 'extractor':
        result['output_protocol'] = 'Use the original module snapshot structure. Full schemas are application-side by default; request include_validation_schemas=True when the provider budget permits. Load full cards for volunteered concepts before extracting their attributes.'
    if role == 'planner':
        result['routing_rules'] = {k:v for k,v in GRAPH.items() if k not in {'catalog'}}
        result['available_target_index'] = [{'id':n['id'],'kind':n['kind'],'meaning':n['information_to_obtain']} for n in GRAPH['catalog']]
        result['selected_route_rules'] = [ROUTES[t] for t in target_ids if t in ROUTES]
        result['route_completion_path'] = 'Integration/route_completion.json'
    if role == 'diagnosis':
        rules = read('Integration/diagnostic_review_knowledge.json')
        result['review_knowledge'] = {m:rules[m] for m in sorted(modules)}
    return result

def validate_snapshot(module, snapshot, messages):
    """Original schema + exact quote/context checks. Does not infer truth from quotes."""
    if module not in MANIFEST['modules']:
        raise ValueError('Unknown module')
    schema = read(MANIFEST['modules'][module]['evidence_schema'])
    Draft202012Validator(schema).validate(snapshot)
    ids = [m['id'] for m in messages]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate application message IDs')
    ix = {m['id']:(i,m) for i,m in enumerate(messages)}
    for record in snapshot['records']:
        supported = set()
        allowed = {'finding_status','time_reference','temporal_status'} | set(record['attributes'])
        for e in record['evidence']:
            if e['message_id'] not in ix:
                raise ValueError('Unknown source message')
            pos, message = ix[e['message_id']]
            if message['speaker'] != 'patient' or e['quote'] not in message['text']:
                raise ValueError('Evidence quote must occur verbatim in the identified patient message')
            if any(c not in ix or ix[c][0] >= pos for c in e['context_message_ids']):
                raise ValueError('Context must identify earlier messages')
            if not set(e['supports']) <= allowed:
                raise ValueError('Evidence names an unknown support field')
            # A bare yes/no cannot stand alone as a clinical finding.
            if e['quote'].strip().lower().strip('.!؟?') in {'yes','no','yeah','yep','nope','نعم','لا','أيوه','ايوه','اه','آه'} and not e['context_message_ids']:
                raise ValueError('Short confirmation/denial requires earlier context')
            supported.update(e['supports'])
        required = {'finding_status'} | {a for a,v in record['attributes'].items() if v['status'] == 'known'}
        if not required <= supported:
            raise ValueError('A finding or known attribute lacks an evidence pointer')
    return {'status':'PASS','mechanical_only':True,'semantic_truth_verified':False}

def append_snapshot(ledger, module, snapshot, messages):
    """Append-only revisions: conflicting and historical reports are never overwritten."""
    validate_snapshot(module, snapshot, messages)
    result = copy.deepcopy(ledger)
    result.append({'revision':len(result)+1,'module':module,'snapshot':copy.deepcopy(snapshot)})
    return result

def concept_history(ledger, module, concept_id, episode_key):
    return [{'revision':event['revision'],'record':copy.deepcopy(record)} for event in ledger if event['module']==module
            for record in event['snapshot']['records'] if record['concept_id']==concept_id and record['episode_key']==episode_key]

def validate_role_output(role, output, state=None, ledger=None, delivery_records=None):
    """Validate routing IDs, qualified citations and supplied application pointers."""
    filenames={'conversation':'conversation_output.schema.json','planner':'planner_output.schema.json',
               'diagnosis':'synthesis_output.schema.json'}
    if role not in filenames:
        raise ValueError('Use validate_snapshot for extractor output')
    Draft202012Validator(read('Integration/'+filenames[role])).validate(output)
    target=output.get('target_id')
    if target is not None:
        if target not in TARGETS:
            raise ValueError('Unknown output target')
        if state is None or output.get('period_id')!=state.get('period_bindings',{}).get(TARGETS[target]['period_binding']):
            raise ValueError('Target needs its actual registered period')
    if role=='conversation' and not output['target_preserved']:
        raise ValueError('Return wording to the planner before display')
    if role=='diagnosis':
        for candidate in output['candidates']:
            for criterion in candidate['criteria_review']:
                for reference in criterion['source_references']:
                    register,separator,sid=reference.partition('#')
                    allowed={m['sources'] for m in MANIFEST['modules'].values()}
                    if not separator or register not in allowed or sid not in read(register):
                        raise ValueError('Unknown qualified clinical source')
                for pointer in criterion['evidence_pointers']:
                    match=re.fullmatch(r'ledger\[(\d+)\]\.snapshot\.records\[(\d+)\]',pointer)
                    if not match or ledger is None:
                        raise ValueError('Use supplied application ledger pointers')
                    event,record=map(int,match.groups())
                    if event>=len(ledger) or record>=len(ledger[event]['snapshot']['records']):
                        raise ValueError('Evidence pointer does not exist')
        safety=output['safety_handoff']
        if safety['response_delivered'] and safety['delivery_record_reference'] not in (delivery_records or {}):
            raise ValueError('Claimed delivery needs an actual application delivery record')
    return {'status':'PASS','mechanical_only':True,'clinical_meaning_verified':False}

def _preview():
    spec = importlib.util.spec_from_file_location('_knowledge_graph_preview', ROOT/'Workflow/Interview_Graph/preview_graph.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def next_with_supplements(state, messages):
    """Route explicit annotated supplemental needs without bypassing core safeguards."""
    preview = _preview()
    base = preview.next_step(GRAPH,state)
    # The original controller handles scope, urgent/safety needs, participation,
    # pending unanswered replies, required early questions and professional signs.
    if base['action'] not in {'ASK','HANDOFF_WITH_GAPS'} or state.get('pending') or state.get('priority_branch'):
        return base
    if any(not preview.resolved(TARGETS[nid],state) for block in GRAPH['core_agenda'][:2] for nid in block['node_ids']):
        return base
    if base.get('target_id','').startswith('detail/'):
        return base
    message_ids = {m['id'] for m in messages}
    for request in state.get('supplement_requests',[]):
        tid = request.get('target_id')
        if tid not in ROUTES or ROUTES[tid]['route_class'] != 'conditional_supplement':
            raise ValueError('Supplement must name a conditional concept entry')
        route = ROUTES[tid]
        if not request.get('reason') or not request.get('requirement_reference') or not request.get('source_message_ids'):
            raise ValueError('Supplement needs reason, requirement reference and evidence pointers')
        if not set(request['source_message_ids']) <= message_ids:
            raise ValueError('Supplement has an unknown source message')
        if route['module'] != 'MDD' and not any(state.get('branch_facts',{}).get(b,{}).get('status')=='open' for b in route['eligible_branch_ids']):
            continue
        if preview.resolved(TARGETS[tid],state):
            continue
        return preview.target_result('ASK',TARGETS[tid],state,'Relevant supplemental requirement: '+request['reason'],
                                      selection_source='explicit_supplement_overlay')
    return base

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--role',choices=['conversation','extractor','planner','diagnosis'],required=True)
    ap.add_argument('--target',action='append',default=[])
    ap.add_argument('--module',action='append',default=[])
    args = ap.parse_args()
    print(json.dumps(get_context(args.role,args.target,args.module),ensure_ascii=False,indent=2))
