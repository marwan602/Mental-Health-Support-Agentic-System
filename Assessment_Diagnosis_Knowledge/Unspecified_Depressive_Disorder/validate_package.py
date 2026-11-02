"""Mechanical evidence/reference checks; no clinical diagnostic decisions."""
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
   if not m or m['speaker']!='patient' or e['quote'] not in m['text']:raise ValueError('Invalid patient quotation')
   for mid in e['context_message_ids']:
    if mid not in order or order[mid]>=order[e['message_id']]:raise ValueError('Context must precede answer')
   for n in e['supports']:
    if n!='finding_status' and (n not in r['attributes'] or r['attributes'][n]['status']!='known'):raise ValueError('Invalid support target')
    supported.add(n)
  if 'finding_status' not in supported:raise ValueError('Finding lacks source link')
  for n,a in r['attributes'].items():
   if a['status']=='known' and n not in supported:raise ValueError('Known detail lacks source link')
  if r['finding_status']=='conflicting':
   if len({(e['message_id'],e['quote']) for e in r['evidence']})<2 or not r['uncertainty_notes'] or r['semantic_check_status']!='needs_review':raise ValueError('Conflict needs distinct accounts, notes and review')
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
 rules=K['clinical_reference_rules']
 check('schema valid Draft 2020-12',lambda:Draft202012Validator.check_schema(SC))
 check('first fictional snapshot accepted',lambda:validate(X['first_snapshot'],X['messages']))
 check('later contextual snapshot accepted',lambda:validate(X['later_snapshot'],X['messages']))
 check('all card and rule sources resolve',lambda:require(all(s in S for c in K['concepts'] for s in c['clinical_source_ids']) and all(s in S for s in rules['source_ids'])))
 check('classification reference sources resolve',lambda:require(all(s in S for s in R['clinical_source_ids'])))
 check('sources have links locations uses access notes and dates',lambda:require(all(all(s.get(n) for n in ['title','url','locator','used_for','access','checked_at']) for s in S.values())))
 check('unique concepts and described optional project fields',lambda:require(len({c['id'] for c in K['concepts']})==len(K['concepts']) and all(f.get('meaning') and f.get('origin')=='PROJECT_DESIGN' and not f.get('required_on_every_report') for c in K['concepts'] for f in c['attribute_specs'].values())))
 check('clinical significance and predominance retained',lambda:require(rules['distress_or_impairment_required'] and rules['predominant_depressive_presentation_required']))
 check('no invented fixed count or minimum duration',lambda:require(R['numeric_thresholds']['category_specific_minimum_symptom_count'] is None and R['numeric_thresholds']['category_specific_minimum_days'] is None and not rules['universal_two_week_minimum'] and not rules['universal_five_symptom_minimum']))
 check('no-threshold is not any sadness and no reason is invented',lambda:require(not rules['no_numeric_minimum_means_any_sadness_qualifies'] and not rules['reason_must_be_invented']))
 check('all automatic diagnosis shortcuts disabled',lambda:require(all(v is False for v in R['automatic_rules'].values()) and not R['automated_classifier_implemented']))
 check('uncertainty not represented as verified negative differential',lambda:require(not rules['missing_data_proves_no_other_disorder'] and not rules['all_alternatives_must_be_verified_absent_before_any_professional_use']))
 check('separate diagnostic and workflow meanings represented',lambda:require({x['term'] for x in R['distinctions']}=={'other_specified_depressive_disorder','unspecified_depressive_disorder','assessment_incomplete','mdd_with_unspecified_severity_or_course','unspecified_mood_disorder','reported_or_provisional_diagnosis'}))
 check('adult scope and review/runtime limitations explicit',lambda:require(K['population']['minimum_age']==18 and K['population']['maximum_age'] is None and K['clinical_review']=='NOT_PERFORMED' and K['runtime_integration']=='NOT_CONNECTED' and not K['diagnostic_automation_enabled']))
 check('initial duration unknown without value',lambda:require(X['first_snapshot']['records'][0]['attributes']['duration']==dict(status='unknown')))
 check('later approximate duration updated with provenance',lambda:require(gold('depressed_mood')['attributes']['duration']['value']=='about six weeks' and {e['message_id'] for e in gold('depressed_mood')['evidence']}=={'m2','m4'}))
 check('contextual answer links to earlier question',lambda:require('m3' in gold('depressed_mood')['evidence'][1]['context_message_ids']))
 check('reported prior formulation remains historical and attributed',lambda:require(gold('reported_clinical_formulation')['episode_key']=='last_year' and gold('reported_clinical_formulation')['temporal_status']=='historical' and gold('reported_clinical_formulation')['attributes']['professional']['value']=='doctor'))
 check('decline does not become absent activation',lambda:require(gold('assessment_limit')['attributes']['reported_limit']['value']=='declines_for_now' and not any(r['concept_id']=='activation_history' and r['finding_status']=='reported_absent' for r in X['later_snapshot']['records'])))
 check('declined target remains in question tracking',lambda:require(X['later_snapshot']['question_tracking'][0]['question_status']=='declined' and bool(X['later_snapshot']['question_tracking'][0]['unanswered_target'])))
 check('safety not falsely marked assessed in fixture',lambda:require(X['later_snapshot']['safety_handoff']['status']=='not_assessed'))
 check('invented quote rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(quote='invented'))))
 check('assistant cannot supply patient evidence',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(message_id='m1',quote='What would you like to discuss today?'))))
 check('future context rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m8']))))
 check('same-message context rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m2']))))
 check('unknown context rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['missing']))))
 check('unsupported known detail rejected',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='known',value='daily')))))
 check('wrong concept-specific field rejected',lambda:reject(changed(lambda x:attr(x['records'][0],'reported_limit',dict(status='unknown')))))
 check('unknown cannot carry value',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='unknown',value='daily')))))
 check('not-applicable requires reason',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='not_applicable')))))
 check('confirmed diagnosis outside contract rejected',lambda:reject(changed(lambda x:x.update(diagnosis='unspecified depressive disorder'))))
 check('billing code outside contract rejected',lambda:reject(changed(lambda x:x.update(billing_code='F32.A'))))
 check('criterion count outside record rejected',lambda:reject(changed(lambda x:x['records'][0].update(criteria_met=3))))
 check('invalid finding status rejected',lambda:reject(changed(lambda x:x['records'][0].update(finding_status='confirmed_diagnosis'))))
 check('invalid decline value rejected',lambda:reject(changed(lambda x:attr(x['records'][-1],'reported_limit',dict(status='known',value='symptom_absent')))))
 check('unknown optional detail accepted without value',lambda:validate(changed(lambda x:attr(x['records'][0],'frequency',dict(status='unknown'))),X['messages']))
 check('different historical period allows a separate record',lambda:validate(changed(lambda x:x['records'].append(dict(copy.deepcopy(x['records'][0]),episode_key='separate_reported_period'))),X['messages']))
 check('duplicate snapshot key rejected',lambda:reject(changed(lambda x:x['records'].append(copy.deepcopy(x['records'][0])))))
 check('unsubstantiated conflict rejected',lambda:reject(changed(lambda x:x['records'][0].update(finding_status='conflicting'))))
 check('empty evidence rejected',lambda:reject(changed(lambda x:x['records'][0].update(evidence=[]))))
 check('duplicate message ID rejected',lambda:reject(copy.deepcopy(X['later_snapshot']),X['messages']+[copy.deepcopy(X['messages'][0])]))
 check('classification knowledge cannot be inserted as patient output',lambda:reject(changed(lambda x:x.update(classification_reference=R))))
 check('all_nested_source_ids_resolve',lambda:source_refs(K))
 report=dict(passed=all(r['passed'] for r in results),checks=len(results),results=results,scope='Mechanical schema/reference/provenance and authored-fixture checks only; no clinical validation, semantic proof, live LLM or diagnostic accuracy study.')
 (HERE/'VALIDATION_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(run())
