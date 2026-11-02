"""Mechanical/provenance checks; cannot establish semantic or clinical correctness."""
import copy,json
from pathlib import Path
from jsonschema import Draft202012Validator,ValidationError
HERE=Path(__file__).resolve().parent
def load(n):return json.loads((HERE/n).read_text(encoding='utf-8-sig'))
K=load('knowledge.json');S=load('sources.json');C=load('capability_reference.json');X=load('examples.json');SC=load('evidence_output.schema.json')
Draft202012Validator.check_schema(SC);V=Draft202012Validator(SC)
AGENT_SPECIFIC={'exposure_details','exposure_events','exposure_mood_timing'}
def validate(x,messages):
 V.validate(x)
 by={m['id']:m for m in messages};order={m['id']:i for i,m in enumerate(messages)}
 if len(by)!=len(messages):raise ValueError('Duplicate message ID')
 refs=set()
 for a in x['exposures']:
  if a['exposure_ref'] in refs:raise ValueError('Duplicate exposure reference')
  refs.add(a['exposure_ref'])
  m=by.get(a['source_message_id'])
  if not m or m['speaker']!='patient' or a['quote'] not in m['text']:raise ValueError('Invalid exposure source quote')
  if a['name_as_reported'] not in a['quote']:raise ValueError('Reported name is not linked to registry quote')
 seen=set()
 for r in x['records']:
  key=tuple(r[k] for k in ['concept_id','episode_key','subject','exposure_ref'])
  if key in seen:raise ValueError('Duplicate concept/period/subject/exposure record')
  seen.add(key)
  if r['exposure_ref'] is not None and r['exposure_ref'] not in refs:raise ValueError('Unknown exposure reference')
  if r['concept_id'] in AGENT_SPECIFIC and r['exposure_ref'] is None:raise ValueError('Agent-specific record needs a registry reference, even for an unidentified product')
  supported=set()
  for e in r['evidence']:
   m=by.get(e['message_id'])
   if not m or m['speaker']!='patient' or e['quote'] not in m['text']:raise ValueError('Invalid patient quote')
   for mid in e['context_message_ids']:
    if mid not in order or order[mid]>=order[e['message_id']]:raise ValueError('Context must precede answer')
   for n in e['supports']:
    if n!='finding_status' and (n not in r['attributes'] or r['attributes'][n]['status']!='known'):raise ValueError('Invalid supported field')
    supported.add(n)
  if 'finding_status' not in supported:raise ValueError('Finding status lacks source link')
  for n,a in r['attributes'].items():
   if a['status']=='known' and n not in supported:raise ValueError('Known detail lacks evidence link')
  if r['finding_status']=='conflicting':
   if len({(e['message_id'],e['quote']) for e in r['evidence']})<2 or not r['uncertainty_notes'] or r['semantic_check_status']!='needs_review':raise ValueError('Conflict needs distinct reports, notes and review')
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
  except Exception as e:results.append(dict(check=name,passed=False,error=str(e)))
 def require(ok):
  if not ok:raise AssertionError('Check failed')
 def changed(fn):
  x=copy.deepcopy(X['later_snapshot']);fn(x);return x
 def reject(x,msgs=None):
  try:validate(x,msgs or X['messages'])
  except (ValueError,ValidationError):return
  raise AssertionError('Invalid example accepted')
 def attr(r,n,v):r['attributes'][n]=v
 check('schema is valid Draft 2020-12',lambda:Draft202012Validator.check_schema(SC))
 check('first fictional snapshot accepted',lambda:validate(X['first_snapshot'],X['messages']))
 check('later contextual multi-exposure snapshot accepted',lambda:validate(X['later_snapshot'],X['messages']))
 check('source IDs resolve across cards and criteria map',lambda:require(all(s in S for c in K['concepts']+K['criteria_information_map'] for s in c.get('clinical_source_ids',c.get('source_ids',[])))))
 check('capability reference sources resolve',lambda:require(all(x['source_id'] in S for x in C['classification_reference']+C['medication_examples'])))
 check('all source entries have links locators uses and access notes',lambda:require(all(all(s.get(k) for k in ['title','url','locator','used_for','access','checked_at']) for s in S.values())))
 check('unique concepts and described optional project fields',lambda:require(len({c['id'] for c in K['concepts']})==len(K['concepts']) and all(f.get('meaning') and f.get('origin')=='PROJECT_DESIGN' and not f.get('required_on_every_report') for c in K['concepts'] for f in c['attribute_specs'].values())))
 check('clinical map covers A through E with known concepts',lambda:require([c['id'] for c in K['criteria_information_map']]==list('ABCDE') and all(n in {c['id'] for c in K['concepts']} for c in K['criteria_information_map'] for n in c['concept_ids'])))
 check('MDD count duration and universal wait rules not imported',lambda:require(all(K['clinical_reference_rules'][n] is False for n in ['mdd_five_of_nine_required','universal_fourteen_day_minimum','automatic_one_month_wait','substance_use_disorder_required','timing_alone_proves_causation','tox_screen_proves_causation'])))
 check('adult scope and unconnected unvalidated status explicit',lambda:require(K['population']['minimum_age']==18 and K['population']['maximum_age'] is None and K['runtime_integration']=='NOT_CONNECTED' and K['clinical_review']=='NOT_PERFORMED' and not K['diagnostic_automation_enabled']))
 check('initial mood duration not copied from medication duration',lambda:require('duration' not in X['first_snapshot']['records'][0]['attributes']))
 check('contextual answer carries earlier question reference',lambda:require('m3' in X['later_snapshot']['records'][4]['evidence'][0]['context_message_ids']))
 check('prior independent-period clue preserved separately',lambda:require(X['later_snapshot']['records'][5]['episode_key']=='last_year' and X['later_snapshot']['records'][5]['temporal_status']=='historical'))
 check('two agents retain distinct exposure-event records',lambda:require({r['exposure_ref'] for r in X['later_snapshot']['records'] if r['concept_id']=='exposure_events'}=={'agent_a','agent_b'}))
 check('invented quote rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(quote='invented'))))
 check('assistant text cannot be patient evidence',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(message_id='m1',quote='What has changed recently?'))))
 check('future context reference rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m8']))))
 check('same-message context reference rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m2']))))
 check('unsupported known detail rejected',lambda:reject(changed(lambda x:attr(x['records'][0],'duration',dict(status='known',value='three weeks')))))
 check('wrong concept-specific field rejected',lambda:reject(changed(lambda x:attr(x['records'][0],'route',dict(status='unknown')))))
 check('unknown detail cannot carry a value',lambda:reject(changed(lambda x:attr(x['records'][0],'duration',dict(status='unknown',value='three weeks')))))
 check('not-applicable detail requires reason',lambda:reject(changed(lambda x:attr(x['records'][0],'duration',dict(status='not_applicable')))))
 check('invalid controlled event value rejected',lambda:reject(changed(lambda x:attr(x['records'][1],'event',dict(status='known',value='caused_depression')))))
 check('diagnosis property outside extractor contract rejected',lambda:reject(changed(lambda x:x.update(diagnosis='confirmed induced depression'))))
 check('unknown exposure reference rejected',lambda:reject(changed(lambda x:x['records'][1].update(exposure_ref='missing_agent'))))
 check('agent-specific timing cannot be unassigned',lambda:reject(changed(lambda x:x['records'][4].update(exposure_ref=None))))
 check('duplicate registry reference rejected',lambda:reject(changed(lambda x:x['exposures'].append(copy.deepcopy(x['exposures'][0])))))
 check('invented registry name rejected',lambda:reject(changed(lambda x:x['exposures'][0].update(name_as_reported='invented name'))))
 check('duplicate snapshot key rejected',lambda:reject(changed(lambda x:x['records'].append(copy.deepcopy(x['records'][0])))))
 check('unsubstantiated conflict rejected',lambda:reject(changed(lambda x:x['records'][0].update(finding_status='conflicting'))))
 check('same-concept unknown field accepted without fabricated value',lambda:validate(changed(lambda x:attr(x['records'][0],'duration',dict(status='unknown'))),X['messages']))
 check('empty evidence list rejected',lambda:reject(changed(lambda x:x['records'][0].update(evidence=[]))))
 check('duplicate message ID rejected',lambda:reject(copy.deepcopy(X['later_snapshot']),X['messages']+[copy.deepcopy(X['messages'][0])]))
 check('capability material cannot be inserted as patient output',lambda:reject(changed(lambda x:x.update(capability_reference=C))))
 check('one substance table has no invented cannabis depressive entry',lambda:require(len(C['classification_reference'])==8 and 'cannabis' not in {a['class'] for a in C['classification_reference']}))
 check('all_nested_source_ids_resolve',lambda:source_refs(K))
 report=dict(passed=all(r['passed'] for r in results),checks=len(results),results=results,
  scope='Mechanical schema, provenance and fixture assertions only; no live LLM, diagnostic accuracy or clinical validation performed.')
 (HERE/'VALIDATION_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(run())
