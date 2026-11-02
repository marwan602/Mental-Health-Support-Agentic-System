"""Mechanical focused-differential contract checks; no clinical classification."""
import copy,json
from pathlib import Path
from jsonschema import Draft202012Validator,ValidationError
HERE=Path(__file__).resolve().parent
def load(n):return json.loads((HERE/n).read_text(encoding='utf-8-sig'))
K=load('knowledge.json');S=load('sources.json');X=load('examples.json');SC=load('evidence_output.schema.json')
Draft202012Validator.check_schema(SC);V=Draft202012Validator(SC)
def validate(x,messages):
 V.validate(x)
 by={m['id']:m for m in messages};order={m['id']:i for i,m in enumerate(messages)}
 if len(by)!=len(messages):raise ValueError('Duplicate message ID')
 seen=set()
 for r in x['records']:
  key=tuple(r[n] for n in ['concept_id','episode_key','subject'])
  if key in seen:raise ValueError('Duplicate concept/period/subject')
  seen.add(key);supported=set()
  for e in r['evidence']:
   m=by.get(e['message_id'])
   if not m or m['speaker']!='patient' or e['quote'] not in m['text']:raise ValueError('Invalid patient quote')
   for mid in e['context_message_ids']:
    if mid not in order or order[mid]>=order[e['message_id']]:raise ValueError('Context must precede answer')
   for a in e['supports']:
    if a!='finding_status' and (a not in r['attributes'] or r['attributes'][a]['status']!='known'):raise ValueError('Invalid support target')
    supported.add(a)
  if 'finding_status' not in supported:raise ValueError('Finding lacks source link')
  for a,d in r['attributes'].items():
   if d['status']=='known' and a not in supported:raise ValueError('Known detail lacks source link')
  if r['finding_status']=='conflicting':
   if len({(e['message_id'],e['quote']) for e in r['evidence']})<2 or not r['uncertainty_notes'] or r['semantic_check_status']!='needs_review':raise ValueError('Conflict requires distinct accounts and review')
 return True
def source_refs(value):
 if isinstance(value,dict):
  for key,entry in value.items():
   if key.endswith('source_ids') and (not isinstance(entry,list) or any(sid not in S for sid in entry)):
    raise ValueError('Unresolved nested source IDs: '+key)
   source_refs(entry)
 elif isinstance(value,list):
  for entry in value:source_refs(entry)

def run():
 results=[]
 def check(name,fn):
  try:fn();results.append(dict(check=name,passed=True))
  except Exception as e:results.append(dict(check=name,passed=False,error=(e.message if isinstance(e,ValidationError) else str(e))[:600]))
 def require(ok):
  if not ok:raise AssertionError('Check failed')
 def fixture(cid):return next(c for c in X['cases'] if c['id']==cid)
 def mutate(fn):
  x=copy.deepcopy(X['history_case']['later_snapshot']);fn(x);return x
 def reject(x,messages=None):
  try:validate(x,messages or X['history_case']['messages'])
  except (ValueError,ValidationError):return
  raise AssertionError('Invalid example accepted')
 def attr(r,n,v):r['attributes'][n]=v
 check('schema valid Draft 2020-12',lambda:Draft202012Validator.check_schema(SC))
 for case in X['cases']:
  check('authored case schema/provenance: '+case['id'],lambda c=case:validate(c['output'],c['messages']))
 for stage in ['first_snapshot','later_snapshot']:
  check('history fixture '+stage,lambda st=stage:validate(X['history_case'][st],X['history_case']['messages']))
 ids={c['id'] for c in K['concepts']}
 check('unique concept IDs and described optional project fields',lambda:require(len(ids)==len(K['concepts']) and all(f.get('meaning') and f.get('origin')=='PROJECT_DESIGN' and not f.get('required_on_every_report') for c in K['concepts'] for f in c['attribute_specs'].values())))
 check('all concept sources resolve',lambda:require(all(s in S for c in K['concepts'] for s in c['clinical_source_ids'])))
 check('eleven agreed focused pathway groups present',lambda:require(len(K['pathways'])==11 and len({p['id'] for p in K['pathways']})==11))
 check('every pathway states purpose benefit scope followups limits and review',lambda:require(all(all(p.get(n) for n in ['purpose','benefit_for_depression_assessment','scope','clinical_reference','when_to_explore','suggested_local_order','interpretation_limits','professional_review']) for p in K['pathways'])))
 check('pathway concept and source references resolve',lambda:require(all(all(c in ids for c in p['concept_ids']) and all(s in S for s in p['clinical_source_ids']) for p in K['pathways'])))
 check('sources have links exact locations contributions access and dates',lambda:require(all(all(s.get(n) for n in ['title','url','locator','used_for','access','checked_at']) for s in S.values())))
 check('each canonical pathway has a readable Markdown projection',lambda:require(all((HERE/(p['id']+'.md')).is_file() and p['label'] in (HERE/(p['id']+'.md')).read_text(encoding='utf-8') for p in K['pathways'])))
 check('existing medical/exposure module links resolve',lambda:require(all((HERE.parent/name/'README.md').is_file() for p in K['pathways'] for name in p['existing_module_links'])))
 check('adult scope and no diagnostic/runtime/clinical validation claims',lambda:require(K['population']['minimum_age']==18 and K['population']['maximum_age'] is None and K['runtime_integration']=='NOT_CONNECTED' and K['clinical_review']=='NOT_PERFORMED' and all(not p['independent_diagnosis_enabled'] for p in K['pathways'])))
 check('coexistence and shared evidence reuse explicit',lambda:require(K['shared_rules']['coexistence_allowed'] and K['shared_rules']['shared_fact_may_inform_multiple_pathways']))
 check('unknown decline error and questionnaire shortcuts disabled',lambda:require(all(K['shared_rules'][n] is False for n in ['unknown_equals_absent','declined_equals_denied','diagnostic_automation_enabled','routine_interview_continues_during_urgent_concern','model_error_or_turn_limit_is_diagnosis','questionnaires_equal_diagnoses'])))
 check('short-sleep/exhaustion fixture does not claim reduced sleep need',lambda:require('reduced_sleep_need' not in {r['concept_id'] for r in fixture('short_sleep_with_exhaustion')['output']['records']}))
 check('panic-fear fixture does not assert suicidal intent',lambda:require('death_suicide' not in {r['concept_id'] for r in fixture('panic_fear_not_suicidal_intent')['output']['records']}))
 check('acute-change fixture records review need without delivered contact',lambda:require(fixture('acute_change_interrupts_routine')['output']['safety_handoff']['status']=='urgent_review_needed' and 'not confirmed' in fixture('acute_change_interrupts_routine')['output']['safety_handoff']['unresolved_questions'][0]))
 check('declined trauma context not converted to PTSD denial',lambda:require(fixture('trauma_declined')['output']['question_tracking'][0]['question_status']=='declined' and not any(r['finding_status']=='reported_absent' for r in fixture('trauma_declined')['output']['records'])))
 check('history update retains earlier and later evidence',lambda:require({e['message_id'] for e in X['history_case']['later_snapshot']['records'][0]['evidence']}=={'m2','m4'}))
 check('contextual yes uses earlier messages',lambda:require('m3' in X['history_case']['later_snapshot']['records'][1]['evidence'][0]['context_message_ids']))
 check('invented quote rejected',lambda:reject(mutate(lambda x:x['records'][0]['evidence'][0].update(quote='invented'))))
 check('assistant text cannot become patient evidence',lambda:reject(mutate(lambda x:x['records'][0]['evidence'][0].update(message_id='m1',quote='What was different during that period?'))))
 check('future context rejected',lambda:reject(mutate(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m4']))))
 check('same-message context rejected',lambda:reject(mutate(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m2']))))
 check('unknown context rejected',lambda:reject(mutate(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['missing']))))
 check('wrong concept-specific field rejected',lambda:reject(mutate(lambda x:attr(x['records'][0],'snoring',dict(status='unknown')))))
 check('unsupported known field rejected',lambda:reject(mutate(lambda x:attr(x['records'][0],'observer',dict(status='known',value='doctor')))))
 check('unknown cannot carry value',lambda:reject(mutate(lambda x:attr(x['records'][0],'observer',dict(status='unknown',value='doctor')))))
 check('not-applicable requires reason',lambda:reject(mutate(lambda x:attr(x['records'][0],'observer',dict(status='not_applicable')))))
 check('unknown optional field accepted without value',lambda:validate(mutate(lambda x:attr(x['records'][0],'observer',dict(status='unknown'))),X['history_case']['messages']))
 check('confirmed alternative diagnosis property rejected',lambda:reject(mutate(lambda x:x.update(diagnosis='bipolar II'))))
 check('forced single-pathway assignment rejected',lambda:reject(mutate(lambda x:x.update(diagnostic_branch='01_bipolar_spectrum'))))
 check('criterion count property rejected',lambda:reject(mutate(lambda x:x['records'][0].update(criteria_met=4))))
 check('invented instrument score property rejected',lambda:reject(mutate(lambda x:x.update(PCL5_score=42))))
 check('duplicate record rejected',lambda:reject(mutate(lambda x:x['records'].append(copy.deepcopy(x['records'][0])))))
 check('separate period can have same concept',lambda:validate(mutate(lambda x:x['records'].append(dict(copy.deepcopy(x['records'][0]),episode_key='another_reported_period'))),X['history_case']['messages']))
 check('unsubstantiated conflict rejected',lambda:reject(mutate(lambda x:x['records'][0].update(finding_status='conflicting'))))
 check('empty evidence rejected',lambda:reject(mutate(lambda x:x['records'][0].update(evidence=[]))))
 check('duplicate message ID rejected',lambda:reject(copy.deepcopy(X['history_case']['later_snapshot']),X['history_case']['messages']+[copy.deepcopy(X['history_case']['messages'][0])]))
 check('invalid clinical-confirmation status rejected',lambda:reject(mutate(lambda x:x['records'][0].update(finding_status='confirmed'))))
 check('reference knowledge cannot be inserted as patient output',lambda:reject(mutate(lambda x:x.update(clinical_reference=K['pathways']))))
 check('all_nested_source_ids_resolve',lambda:source_refs(K))
 report=dict(passed=all(r['passed'] for r in results),checks=len(results),results=results,scope='Mechanical schema/reference/provenance and authored-fixture checks only. No live LLM, clinical validation, diagnostic accuracy, semantic proof or care delivery.')
 (HERE/'VALIDATION_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(run())
