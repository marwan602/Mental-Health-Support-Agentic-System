"""Mechanical contract checks and fictional fixtures, not clinical validation."""
import copy
import json
from pathlib import Path
from datetime import datetime,timezone
from jsonschema import Draft202012Validator,ValidationError

HERE=Path(__file__).resolve().parent
def load(name):return json.loads((HERE/name).read_text(encoding='utf-8-sig'))
K=load('knowledge.json');S=load('sources.json');E=load('examples.json');SCHEMA=load('evidence_output.schema.json')
Draft202012Validator.check_schema(SCHEMA)
V=Draft202012Validator(SCHEMA)

def validate_snapshot(snapshot,messages):
    V.validate(snapshot)
    by_id={m['id']:m for m in messages};order={m['id']:i for i,m in enumerate(messages)}
    if len(by_id)!=len(messages):raise ValueError('Duplicate message ID')
    seen=set()
    for r in snapshot['records']:
        key=(r['concept_id'],r['episode_key'],r['subject'])
        if key in seen:raise ValueError('Duplicate concept/period/subject record')
        seen.add(key);supported=set()
        for e in r['evidence']:
            if e['message_id'] not in by_id:raise ValueError('Missing source message')
            m=by_id[e['message_id']]
            if m['speaker']!='patient':raise ValueError('Patient source required')
            if e['quote'] not in m['text']:raise ValueError('Quote not an exact source substring')
            for mid in e['context_message_ids']:
                if mid not in order or order[mid]>=order[e['message_id']]:
                    raise ValueError('Context must precede source answer')
            for a in e['supports']:
                if a!='finding_status':
                    if a not in r['attributes']:raise ValueError('Evidence supports missing attribute')
                    if r['attributes'][a]['status']!='known':raise ValueError('Evidence supports unknown/inapplicable value')
                supported.add(a)
        if 'finding_status' not in supported:raise ValueError('Finding status lacks source linkage')
        for n,d in r['attributes'].items():
            if d['status']=='known' and n not in supported:raise ValueError('Known value lacks source linkage')
        if r['finding_status']=='conflicting':
            if len({(e['message_id'],e['quote']) for e in r['evidence']})<2:
                raise ValueError('Conflict needs distinct reports')
            if not r['uncertainty_notes'] or r['semantic_check_status']!='needs_review':
                raise ValueError('Conflict needs notes and review')
    return True

def run():
    results=[]
    def check(name,fn):
        try:fn();results.append({'check':name,'passed':True})
        except Exception as exc:results.append({'check':name,'passed':False,'error':str(exc)})
    def reject(x,msgs=None):
        try:validate_snapshot(x,msgs or E['messages'])
        except (ValueError,ValidationError):return
        raise AssertionError('Invalid fixture accepted')
    def mutation(fn):
        x=copy.deepcopy(E['later_snapshot']);fn(x);return x
    def refs():
        ids=[c['id'] for c in K['concepts']]
        assert len(ids)==len(set(ids))
        def visit(x):
            if isinstance(x,dict):
                for name,value in x.items():
                    if name.endswith('source_ids'):assert value and all(v in S for v in value),(name,value)
                    if name=='concept_ids':assert all(v in ids for v in value)
                    visit(value)
            elif isinstance(x,list):
                for v in x:visit(v)
        visit(K)
        assert all(s['url'].startswith('https://') and s['locator'] for s in S.values())
    check('source_and_concept_references_resolve',refs)
    def clinical_group_structure():
        core=[c for c in K['concepts'] if c['role']=='associated_symptom']
        assert len(core)==6 and len({c['count_group'] for c in core})==6
        assert len([c for c in K['concepts'] if c['role']=='required_mood'])==1
        assert next(c for c in K['concepts'] if c['id']=='death_suicide')['count_group'] is None
        assert K['clinical_reference_rules']['apply_mdd_nearly_daily_rule_to_all_pdd_symptoms'] is False
        assert next(c for c in K['criteria_information_map'] if c['id']=='D')['kind']=='compatibility_note'
    check('pdd_six_groups_and_mde_compatibility_are_distinct',clinical_group_structure)
    check('first_snapshot_valid',lambda:validate_snapshot(E['first_snapshot'],E['messages'][:2]))
    check('later_snapshot_contextual_yes_and_intervals_valid',lambda:validate_snapshot(E['later_snapshot'],E['messages']))
    check('reject_wrong_module',lambda:reject(mutation(lambda x:x.update(module_id='adult_mdd'))))
    check('reject_invented_quote',lambda:reject(mutation(lambda x:x['records'][0]['evidence'][0].update(quote='I have confirmed PDD.'))))
    check('reject_future_context',lambda:reject(mutation(lambda x:x['records'][1]['evidence'][1].update(context_message_ids=['m7']))))
    check('reject_same_message_context',lambda:reject(mutation(lambda x:x['records'][1]['evidence'][1].update(context_message_ids=['m6']))))
    check('reject_unknown_source',lambda:reject(mutation(lambda x:x['records'][0]['evidence'][0].update(message_id='missing'))))
    check('reject_wrong_concept_field',lambda:reject(mutation(lambda x:x['records'][0]['attributes'].update(future_expectations={'status':'known','value':'example'}))))
    check('reject_unknown_with_value',lambda:reject(mutation(lambda x:x['records'][0]['attributes'].update(duration={'status':'unknown','value':'three years'}))))
    check('reject_known_without_source_link',lambda:reject(mutation(lambda x:x['records'][0]['attributes'].update(frequency={'status':'known','value':'every day'}))))
    check('reject_duplicate_concept_period',lambda:reject(mutation(lambda x:x['records'].append(copy.deepcopy(x['records'][0])))))
    check('reject_unjustified_conflict',lambda:reject(mutation(lambda x:x['records'][0].update(finding_status='conflicting'))))
    check('reject_invalid_interval_enum',lambda:reject(mutation(lambda x:x['records'][2]['attributes']['intervals']['value'][0].update(change_kind='confirmed_remission'))))
    check('reject_unstructured_interval_value',lambda:reject(mutation(lambda x:x['records'][2]['attributes']['intervals'].update(value='better for six weeks'))))
    check('reject_claimed_diagnosis_field',lambda:reject(mutation(lambda x:x.update(diagnosis='PDD'))))
    def unknown():
        x=copy.deepcopy(E['later_snapshot']);x['records'][0]['attributes']['frequency']={'status':'unknown'}
        validate_snapshot(x,E['messages'])
    check('unknown_without_invented_value_allowed',unknown)
    def valid_na():
        x=copy.deepcopy(E['later_snapshot']);x['records'][0]['attributes']['baseline_comparison']={'status':'not_applicable','reason':'Illustrative contract state only; real applicability needs review.'}
        validate_snapshot(x,E['messages'])
    check('not_applicable_requires_explanation',lambda:reject(mutation(lambda x:x['records'][0]['attributes'].update(baseline_comparison={'status':'not_applicable'}))))
    def distinct_periods():
        x=copy.deepcopy(E['later_snapshot']);r=copy.deepcopy(x['records'][0]);r['episode_key']='earlier_period';r['temporal_status']='historical';x['records'].append(r)
        validate_snapshot(x,E['messages'])
    check('different_period_keys_supported_structurally',distinct_periods)
    def correct_fixture():
        first={r['concept_id']:r for r in E['first_snapshot']['records']}
        later={r['concept_id']:r for r in E['later_snapshot']['records']}
        assert 'duration' not in first['sleep_disturbance']['attributes']
        assert later['sleep_disturbance']['attributes']['duration']['value']=='about three years'
        assert later['longitudinal_timeline']['attributes']['intervals']['value'][0]['change_kind']=='partial_improvement'
        assert not any(r['concept_id']=='death_suicide' for r in E['later_snapshot']['records'])
        assert E['later_snapshot']['safety_handoff']['status']=='not_assessed'
    check('gold_fixture_preserves_partial_improvement_and_safety_unknown',correct_fixture)
    def no_overclaim():
        assert not K['diagnostic_automation_enabled']
        assert K['runtime_integration']=='NOT_CONNECTED'
        feature_ids={c['id'] for c in K['concepts'] if c['role']=='feature_evidence'}
        assert feature_ids=={'anxious_distress','atypical_features'}
    check('only_applicable_feature_branches_and_no_automation',no_overclaim)
    def assistant_source():
        msgs=copy.deepcopy(E['messages']);msgs[1]['speaker']='assistant';reject(E['later_snapshot'],msgs)
    check('reject_assistant_quote_as_patient_evidence',assistant_source)
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'passed':all(r['passed'] for r in results),
      'check_count':len(results),'checks':results,'clinical_validation':False,
      'limits':'Mechanical contracts and manually authored gold fixtures only. Exact quotations and schema validity do not prove semantic interpretation, clinical criteria, safety or live-model behaviour.'}
    (HERE/'VALIDATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    for r in results:print(('PASS ' if r['passed'] else 'FAIL ')+r['check'])
    print(f"{sum(r['passed'] for r in results)}/{len(results)} checks passed; no clinical/model validation.")
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':run()
