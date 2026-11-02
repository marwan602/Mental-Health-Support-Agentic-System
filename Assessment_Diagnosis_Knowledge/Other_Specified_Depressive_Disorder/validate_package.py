"""Mechanical reference/provenance checks, not a diagnostic implementation."""
import copy,json
from pathlib import Path
from jsonschema import Draft202012Validator,ValidationError
HERE=Path(__file__).resolve().parent
def load(n):return json.loads((HERE/n).read_text(encoding='utf-8-sig'))
K=load('knowledge.json');S=load('sources.json');R=load('classification_reference.json');X=load('examples.json');SC=load('evidence_output.schema.json')
Draft202012Validator.check_schema(SC);V=Draft202012Validator(SC)
def validate(x,messages):
 V.validate(x)
 by={m['id']:m for m in messages};order={m['id']:i for i,m in enumerate(messages)}
 if len(by)!=len(messages):raise ValueError('Duplicate message ID')
 seen=set()
 for r in x['records']:
  key=tuple(r[k] for k in ['concept_id','episode_key','subject'])
  if key in seen:raise ValueError('Duplicate concept/period/subject record')
  seen.add(key);supported=set()
  for e in r['evidence']:
   m=by.get(e['message_id'])
   if not m or m['speaker']!='patient' or e['quote'] not in m['text']:raise ValueError('Invalid patient quote')
   for mid in e['context_message_ids']:
    if mid not in order or order[mid]>=order[e['message_id']]:raise ValueError('Context must precede answer')
   for n in e['supports']:
    if n!='finding_status' and (n not in r['attributes'] or r['attributes'][n]['status']!='known'):raise ValueError('Invalid support target')
    supported.add(n)
  if 'finding_status' not in supported:raise ValueError('Finding lacks source link')
  for n,a in r['attributes'].items():
   if a['status']=='known' and n not in supported:raise ValueError('Known detail lacks source link')
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
  except Exception as e:results.append(dict(check=name,passed=False,error=(e.message if isinstance(e,ValidationError) else str(e))[:600]))
 def require(ok):
  if not ok:raise AssertionError('Check failed')
 def changed(fn):
  x=copy.deepcopy(X['later_snapshot']);fn(x);return x
 def reject(x,msgs=None):
  try:validate(x,msgs or X['messages'])
  except (ValueError,ValidationError):return
  raise AssertionError('Invalid example accepted')
 def attr(r,n,v):r['attributes'][n]=v
 def gold(cid):return next(r for r in X['later_snapshot']['records'] if r['concept_id']==cid)
 p=R['named_examples'];rules=K['clinical_reference_rules']
 check('schema valid Draft 2020-12',lambda:Draft202012Validator.check_schema(SC))
 check('first authored snapshot valid',lambda:validate(X['first_snapshot'],X['messages']))
 check('later context and correction snapshot valid',lambda:validate(X['later_snapshot'],X['messages']))
 check('all concept source IDs resolve',lambda:require(all(s in S for c in K['concepts'] for s in c['clinical_source_ids'])))
 check('all classification/example/source-issue references resolve',lambda:require(all(s in S for c in p+R['source_issues'] for s in c['source_ids']) and all(s in S for s in R['clinical_source_ids'])))
 check('source records include links locations uses access and dates',lambda:require(all(all(s.get(k) for k in ['title','url','locator','used_for','access','checked_at']) for s in S.values())))
 check('unique concepts and described optional fields',lambda:require(len({c['id'] for c in K['concepts']})==len(K['concepts']) and all(f.get('meaning') and f.get('origin')=='PROJECT_DESIGN' and not f.get('required_on_every_report') for c in K['concepts'] for f in c['attribute_specs'].values())))
 check('all four named examples included and linked',lambda:require(len(p)==4 and {q['id'] for q in p}==set(K['named_example_ids'])))
 check('examples not represented as exhaustive peer disorders',lambda:require(not R['examples_are_exhaustive'] and not R['examples_are_separate_peer_disorders']))
 check('2025 depressive-like example names used',lambda:require('depressive-like' in p[1]['label'] and 'Depressive-like' in p[2]['label']))
 check('RBD duration recurrence menstrual and symptom requirements present',lambda:require(p[0]['requirements']['duration_days_inclusive']==[2,13] and p[0]['requirements']['minimum_other_symptoms']==4 and '12 consecutive' in p[0]['requirements']['recurrence'] and not p[0]['requirements']['menstrual_association_allowed']))
 check('exact-four-day source issue not silently classified',lambda:require(p[1]['requirements']['exact_four_day_boundary']=='REQUIRES_CLINICAL_SOURCE_CLARIFICATION_NO_AUTOMATIC_RULE' and not R['automated_classifier_implemented']))
 check('2025 deleted recurrent-brief exclusion not applied to short-duration example',lambda:require('Recurrent brief depression' not in p[1]['exclusions'] and R['revision_application']['deleted_exclusions_applied']))
 check('2025 deleted mixed-anxiety exclusion not applied to insufficient-symptom example',lambda:require(not any('mixed anxiety' in e.lower() for e in p[2]['exclusions']) and {x['id'] for x in R['source_issues']}=={'four_day_boundary'}))
 check('insufficient symptoms minimum not a fixed total',lambda:require(p[2]['requirements']['minimum_other_symptoms']==1 and p[2]['requirements']['minimum_duration_days']==14 and p[2]['requirements']['full_other_disorder_not_met_required']))
 check('psychosis branch and schizoaffective boundary retained',lambda:require(p[3]['requirements']['full_major_depressive_episode_required'] and 'schizoaffective' in p[3]['exclusions'][0]))
 check('psychosis exclusion not generalized to every example',lambda:require(rules['psychotic_exclusion_applies_to_all_examples'] is False))
 check('unknown incomplete or mildness shortcuts disabled',lambda:require(all(rules[n] is False for n in ['unknown_equals_absent','incomplete_interview_proves_subthreshold','all_other_specified_presentations_are_mild'])))
 check('adult scope and pending clinical/runtime status explicit',lambda:require(K['population']['minimum_age']==18 and K['population']['maximum_age'] is None and K['clinical_review']=='NOT_PERFORMED' and K['runtime_integration']=='NOT_CONNECTED' and not K['diagnostic_automation_enabled']))
 check('gold recurrence leaves consecutive months unresolved',lambda:require('consecutive_months' not in gold('recurrence_pattern')['attributes'] and 'cannot remember' in gold('recurrence_pattern')['attributes']['exceptions']['value']))
 check('prior longer period kept historical and separate',lambda:require(gold('lifetime_threshold_history')['episode_key']=='age_22' and gold('lifetime_threshold_history')['temporal_status']=='historical'))
 check('contextual yes references preceding question',lambda:require('m5' in gold('between_period_course')['evidence'][0]['context_message_ids']))
 check('latest correction keeps both source reports',lambda:require(gold('brief_period_details')['attributes']['duration']['value']=='exactly four days, corrected by patient' and {e['message_id'] for e in gold('brief_period_details')['evidence']}=={'m2','m10'}))
 check('unknown unreported symptoms not fabricated absent in fixture',lambda:require(not any(r['finding_status']=='reported_absent' for r in X['later_snapshot']['records'])))
 check('invented quote rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(quote='invented'))))
 check('assistant cannot source patient evidence',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(message_id='m1',quote='What has been happening?'))))
 check('future context rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m10']))))
 check('same-message context rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m2']))))
 check('unknown context message rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['missing']))))
 check('unsupported known detail rejected',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='known',value='every day')))))
 check('wrong concept-specific detail rejected',lambda:reject(changed(lambda x:attr(x['records'][0],'episodes_per_month',dict(status='unknown')))))
 check('unknown detail cannot carry value',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='unknown',value='daily')))))
 check('not-applicable needs reason',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='not_applicable')))))
 check('confirmed diagnosis property rejected',lambda:reject(changed(lambda x:x.update(diagnosis='other specified depression'))))
 check('automated presentation label property rejected',lambda:reject(changed(lambda x:x.update(assigned_presentation='recurrent_brief_depression'))))
 check('criterion count outside patient record rejected',lambda:reject(changed(lambda x:x['records'][0].update(criteria_met=3))))
 check('invalid finding status rejected',lambda:reject(changed(lambda x:x['records'][0].update(finding_status='clinically_confirmed'))))
 check('unknown optional detail accepted without value',lambda:validate(changed(lambda x:attr(x['records'][0],'frequency',dict(status='unknown'))),X['messages']))
 check('same concept under a different period permitted',lambda:validate(changed(lambda x:x['records'].append(dict(copy.deepcopy(x['records'][0]),episode_key='distinct_reported_period'))),X['messages']))
 check('duplicate snapshot key rejected',lambda:reject(changed(lambda x:x['records'].append(copy.deepcopy(x['records'][0])))))
 check('unsubstantiated conflict rejected',lambda:reject(changed(lambda x:x['records'][0].update(finding_status='conflicting'))))
 check('empty evidence rejected',lambda:reject(changed(lambda x:x['records'][0].update(evidence=[]))))
 check('duplicate message ID rejected',lambda:reject(copy.deepcopy(X['later_snapshot']),X['messages']+[copy.deepcopy(X['messages'][0])]))
 check('reference knowledge cannot be inserted into patient output',lambda:reject(changed(lambda x:x.update(classification_reference=R))))
 check('all_nested_source_ids_resolve',lambda:source_refs(K))
 report=dict(passed=all(r['passed'] for r in results),checks=len(results),results=results,
  scope='Mechanical schema/reference/provenance and authored-fixture checks; no clinical validation, semantic proof, live LLM or diagnostic accuracy evaluation.')
 (HERE/'VALIDATION_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(run())
