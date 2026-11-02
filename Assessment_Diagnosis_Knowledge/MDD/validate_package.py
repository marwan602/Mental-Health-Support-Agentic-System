"""Mechanical checks only: no clinical/model validation and no API calls."""
import copy
import json
from pathlib import Path
from datetime import datetime, timezone
from jsonschema import Draft202012Validator, ValidationError

HERE=Path(__file__).resolve().parent
def load(name):return json.loads((HERE/name).read_text(encoding='utf-8-sig'))
K=load('knowledge.json'); S=load('sources.json'); EX=load('examples.json')
SCHEMA=load('evidence_output.schema.json')
Draft202012Validator.check_schema(SCHEMA)
V=Draft202012Validator(SCHEMA)

def validate_snapshot(snapshot,messages):
    V.validate(snapshot)
    by_id={m['id']:m for m in messages}
    if len(by_id)!=len(messages): raise ValueError('Duplicate message ID')
    order={m['id']:i for i,m in enumerate(messages)}
    seen=set()
    for r in snapshot['records']:
        key=(r['concept_id'],r['episode_key'],r['subject'])
        if key in seen:raise ValueError('Duplicate concept/episode/subject snapshot record')
        seen.add(key)
        supported=set()
        for e in r['evidence']:
            if e['message_id'] not in by_id:raise ValueError('Unknown source message')
            source=by_id[e['message_id']]
            if source['speaker']!='patient':raise ValueError('Evidence quote must be from patient in this contract')
            if e['quote'] not in source['text']:raise ValueError('Quote is not an exact source substring')
            for mid in e['context_message_ids']:
                if mid not in order or order[mid]>=order[e['message_id']]:
                    raise ValueError('Context must be an earlier message')
            for item in e['supports']:
                if item!='finding_status' and item not in r['attributes']:
                    raise ValueError('Support points to an absent attribute')
                if item!='finding_status' and r['attributes'][item]['status']!='known':
                    raise ValueError('Support cannot claim an unknown/inapplicable value')
                supported.add(item)
        if 'finding_status' not in supported:raise ValueError('Finding status needs evidence support')
        for name,d in r['attributes'].items():
            if d['status']=='known' and name not in supported:raise ValueError('Known detail lacks linked evidence')
        if r['finding_status']=='conflicting':
            if len({(e['message_id'],e['quote']) for e in r['evidence']})<2:
                raise ValueError('Conflicting record needs distinct reports')
            if not r['uncertainty_notes'] or r['semantic_check_status']!='needs_review':
                raise ValueError('Conflicting record needs notes and review')
    return True

def run():
    results=[]
    def check(name,fn):
        try:fn();results.append({'check':name,'passed':True})
        except Exception as e:results.append({'check':name,'passed':False,'error':str(e)})
    def reject(snapshot,messages=EX['messages']):
        try:validate_snapshot(snapshot,messages)
        except (ValueError,ValidationError):return
        raise AssertionError('Invalid fixture was accepted')
    def mutated(fn):
        x=copy.deepcopy(EX['later_snapshot']);fn(x);return x
    def references():
        ids=[c['id'] for c in K['concepts']]
        assert len(ids)==len(set(ids))
        assert len({c['count_group'] for c in K['concepts'] if c['count_group']})==9
        def visit(x):
            if isinstance(x,dict):
                for key,value in x.items():
                    if key.endswith('source_ids'):
                        assert value and all(i in S for i in value),(key,value)
                    visit(value)
            elif isinstance(x,list):
                for item in x:visit(item)
        visit(K)
        assert all(s['url'].startswith('https://') and s['locator'] for s in S.values())
    check('source_links_unique_concepts_and_nine_groups',references)
    check('first_snapshot_valid',lambda:validate_snapshot(EX['first_snapshot'],EX['messages'][:2]))
    check('later_snapshot_contextual_yes_valid',lambda:validate_snapshot(EX['later_snapshot'],EX['messages']))
    check('reject_missing_module_id',lambda:reject(mutated(lambda x:x.pop('module_id'))))
    check('reject_wrong_module_id',lambda:reject(mutated(lambda x:x.update(module_id='adult_pdd'))))
    check('reject_invented_quote',lambda:reject(mutated(lambda x:x['records'][0]['evidence'][0].update(quote='I have severe MDD.'))))
    check('reject_future_context',lambda:reject(mutated(lambda x:x['records'][1]['evidence'][1].update(context_message_ids=['m6']))))
    check('reject_same_message_context',lambda:reject(mutated(lambda x:x['records'][1]['evidence'][1].update(context_message_ids=['m4']))))
    check('reject_attribute_from_wrong_concept',lambda:reject(mutated(lambda x:x['records'][0]['attributes'].update(latency={'status':'known','value':'one hour'}))))
    check('reject_unknown_with_invented_value',lambda:reject(mutated(lambda x:x['records'][0]['attributes'].update(duration={'status':'unknown','value':'six weeks'}))))
    check('reject_unsupported_known_detail',lambda:reject(mutated(lambda x:x['records'][0]['attributes'].update(frequency={'status':'known','value':'every day'}))))
    check('reject_unknown_message',lambda:reject(mutated(lambda x:x['records'][0]['evidence'][0].update(message_id='missing'))))
    check('reject_duplicate_period_record',lambda:reject(mutated(lambda x:x['records'].append(copy.deepcopy(x['records'][0])))))
    def different_period():
        x=copy.deepcopy(EX['later_snapshot']);r=copy.deepcopy(x['records'][0]);r['episode_key']='past_period';r['temporal_status']='historical';x['records'].append(r)
        # Contract accepts distinct periods; semantic period attribution still requires review.
        validate_snapshot(x,EX['messages'])
    check('same_concept_distinct_period_keys_allowed',different_period)
    def wrong_speaker():
        msgs=copy.deepcopy(EX['messages']);msgs[1]['speaker']='assistant';reject(EX['later_snapshot'],msgs)
    check('reject_assistant_quote_as_patient_evidence',wrong_speaker)
    check('reject_unjustified_conflict',lambda:reject(mutated(lambda x:x['records'][0].update(finding_status='conflicting'))))
    def periods_not_inherited():
        first={r['concept_id']:r for r in EX['first_snapshot']['records']}
        later={r['concept_id']:r for r in EX['later_snapshot']['records']}
        assert 'duration' not in first['sleep_disturbance']['attributes']
        assert later['depressed_mood']['attributes']['duration']['value']=='six weeks'
        assert later['sleep_disturbance']['attributes']['duration']['value']=='two weeks'
    check('fictional_example_separates_mood_and_sleep_duration',periods_not_inherited)
    def no_diag():
        assert K['clinical_review']['diagnostic_automation_enabled'] is False
        assert 'diagnosis' not in SCHEMA['properties']
    check('no_confirmed_diagnosis_field_or_automation',no_diag)
    def unknown_allowed():
        x=copy.deepcopy(EX['later_snapshot']);x['records'][0]['attributes']['frequency']={'status':'unknown'}
        validate_snapshot(x,EX['messages'])
    check('explicit_unknown_detail_allowed',unknown_allowed)
    report={'checked_at':datetime.now(timezone.utc).isoformat(),
      'passed':all(r['passed'] for r in results),'checks':results,
      'check_count':len(results),'clinical_validation':False,
      'limits':'Mechanical contract/fixture checks only. Exact quotations do not prove semantic attribution, clinical criteria, safety or live agent performance.'}
    (HERE/'VALIDATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    for r in results:print(('PASS ' if r['passed'] else 'FAIL ')+r['check'])
    print(f"{sum(r['passed'] for r in results)}/{len(results)} checks passed; no clinical/model validation performed.")
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':run()
