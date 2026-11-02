"""Mechanical evidence-contract checks; not clinical or causal validation."""
import copy,json
from pathlib import Path
from jsonschema import Draft202012Validator,ValidationError
HERE=Path(__file__).resolve().parent
def load(n):return json.loads((HERE/n).read_text(encoding='utf-8-sig'))
K=load('knowledge.json');S=load('sources.json');R=load('medical_condition_reference.json');X=load('examples.json');SC=load('evidence_output.schema.json')
Draft202012Validator.check_schema(SC);V=Draft202012Validator(SC)
CONDITION_SPECIFIC={'condition_identification','medical_condition_course','mood_medical_timing'}
def validate(x,messages):
 V.validate(x)
 by={m['id']:m for m in messages};order={m['id']:i for i,m in enumerate(messages)}
 if len(by)!=len(messages):raise ValueError('Duplicate message ID')
 refs=set()
 for a in x['conditions']:
  if a['condition_ref'] in refs:raise ValueError('Duplicate condition reference')
  refs.add(a['condition_ref'])
  m=by.get(a['source_message_id'])
  if not m or m['speaker']!='patient' or a['quote'] not in m['text']:raise ValueError('Invalid condition source quote')
  if a['name_as_reported'] not in a['quote']:raise ValueError('Reported condition name lacks registry quote support')
 seen=set()
 for r in x['records']:
  key=tuple(r[k] for k in ['concept_id','episode_key','subject','condition_ref'])
  if key in seen:raise ValueError('Duplicate concept/period/subject/condition record')
  seen.add(key)
  if r['condition_ref'] is not None and r['condition_ref'] not in refs:raise ValueError('Unknown condition reference')
  if r['concept_id'] in CONDITION_SPECIFIC and r['condition_ref'] is None:raise ValueError('Condition-specific record needs registry reference')
  supported=set()
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
 def gold(cid):return next(r for r in X['later_snapshot']['records'] if r['concept_id']==cid)
 check('schema valid Draft 2020-12',lambda:Draft202012Validator.check_schema(SC))
 check('first fictional snapshot accepted',lambda:validate(X['first_snapshot'],X['messages']))
 check('later contextual multi-condition snapshot accepted',lambda:validate(X['later_snapshot'],X['messages']))
 check('all card and clinical map sources resolve',lambda:require(all(s in S for c in K['concepts']+K['criteria_information_map']+K['descriptive_specifiers'] for s in c.get('clinical_source_ids',c.get('source_ids',[])))))
 check('medical reference sources resolve',lambda:require(all(s in S for c in R['entries'] for s in c['source_ids'])))
 check('sources have links locations uses access notes and check dates',lambda:require(all(all(s.get(k) for k in ['title','url','locator','used_for','access','checked_at']) for s in S.values())))
 check('unique concepts with described optional project fields',lambda:require(len({c['id'] for c in K['concepts']})==len(K['concepts']) and all(f.get('meaning') and f.get('origin')=='PROJECT_DESIGN' and not f.get('required_on_every_report') for c in K['concepts'] for f in c['attribute_specs'].values())))
 check('A-E information map resolves concept references',lambda:require([c['id'] for c in K['criteria_information_map']]==list('ABCDE') and all(n in {c['id'] for c in K['concepts']} for c in K['criteria_information_map'] for n in c['concept_ids'])))
 check('all three medical-condition specifiers retained separately',lambda:require({s['id'] for s in K['descriptive_specifiers']}=={'with_depressive_features','with_major_depressive_like_episode','with_mixed_features'}))
 check('base category does not universally require a full major episode',lambda:require(K['clinical_reference_rules']['universal_full_major_episode_required'] is False))
 check('major-depressive-like specifier reference keeps five groups and two weeks separate from base category',lambda:require(K['clinical_reference_rules']['major_depressive_like_reference']['minimum_symptom_groups']==5 and K['clinical_reference_rules']['major_depressive_like_reference']['minimum_duration_days']==14 and K['clinical_reference_rules']['major_depressive_like_reference']['automatic_count_from_reported_presence'] is False))
 check('physiological attribution and differential requirements explicit',lambda:require(K['clinical_reference_rules']['direct_pathophysiological_evidence_required'] and K['clinical_reference_rules']['exclusive_delirium_excluded'] and K['clinical_reference_rules']['distress_or_impairment_required']))
 check('unsupported causal shortcuts disabled',lambda:require(all(K['clinical_reference_rules'][n] is False for n in ['physical_diagnosis_alone_sufficient','timing_alone_proves_causation','diagnosis_date_equals_disease_onset','universal_fixed_onset_window','absence_of_family_history_proves_cause'])))
 check('adult scope and unconnected unvalidated status explicit',lambda:require(K['population']['minimum_age']==18 and K['population']['maximum_age'] is None and K['runtime_integration']=='NOT_CONNECTED' and K['clinical_review']=='NOT_PERFORMED' and not K['diagnostic_automation_enabled']))
 check('reference file does not order tests or automate attribution',lambda:require(not R['automated_attribution'] and not R['medical_tests_ordered']))
 check('fictional diagnosis-before-disease-onset ambiguity preserved',lambda:require(gold('mood_medical_timing')['attributes']['relationship']['value']=='mood_before_diagnosis_onset_uncertain'))
 check('contextual yes links to earlier question',lambda:require('m3' in gold('mood_medical_timing')['evidence'][0]['context_message_ids']))
 check('physical activity limitation does not become anhedonia in gold fixture',lambda:require('interest_pleasure' not in {r['concept_id'] for r in X['later_snapshot']['records']} and 'still enjoys' in gold('overlapping_symptoms')['attributes']['contexts']['value']))
 check('treatment alternative preserved without forced condition attribution',lambda:require(gold('treatment_exposure_review')['condition_ref'] is None and gold('treatment_exposure_review')['attributes']['named_exposures']['value']=='prednisone'))
 check('prior mood period separate with unknown medical context retained',lambda:require(gold('prior_depressive_course')['temporal_status']=='historical' and gold('prior_depressive_course')['episode_key']=='five_years_ago' and 'not remembered' in gold('prior_depressive_course')['attributes']['medical_context_then']['value']))
 check('reported clinician uncertainty remains attributed',lambda:require('might' in gold('reported_professional_opinion')['attributes']['opinion']['value']))
 check('same concept can belong to two different conditions',lambda:require(len([r for r in X['later_snapshot']['records'] if r['concept_id']=='condition_identification'])==2))
 check('invented quote rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(quote='invented quotation'))))
 check('assistant cannot be source of patient claim',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(message_id='m1',quote='What changes would you like to discuss?'))))
 check('future context reference rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m10']))))
 check('same-message context rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['m2']))))
 check('unknown context message rejected',lambda:reject(changed(lambda x:x['records'][0]['evidence'][0].update(context_message_ids=['missing']))))
 check('unsupported known detail rejected',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='known',value='daily')))))
 check('wrong concept-specific field rejected',lambda:reject(changed(lambda x:attr(x['records'][0],'diagnosis_basis',dict(status='unknown')))))
 check('unknown detail cannot have value',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='unknown',value='daily')))))
 check('not-applicable detail requires reason',lambda:reject(changed(lambda x:attr(x['records'][0],'frequency',dict(status='not_applicable')))))
 check('invalid diagnostic-basis value rejected',lambda:reject(changed(lambda x:attr(x['records'][1],'diagnosis_basis',dict(status='known',value='confirmed_by_chatbot')))))
 check('patient-reported document cannot be declared verified',lambda:reject(changed(lambda x:x['records'].append(dict(x['records'][1],concept_id='reported_investigation',attributes={'document_status':dict(status='known',value='verified_by_patient_quote')})))))
 check('confirmed diagnosis outside extractor contract rejected',lambda:reject(changed(lambda x:x.update(diagnosis='confirmed physiological depression'))))
 check('causal property outside record contract rejected',lambda:reject(changed(lambda x:x['records'][0].update(caused_by='thyroid'))))
 check('unknown condition reference rejected',lambda:reject(changed(lambda x:x['records'][1].update(condition_ref='missing_condition'))))
 check('condition-specific record cannot be unassigned',lambda:reject(changed(lambda x:x['records'][1].update(condition_ref=None))))
 check('duplicate registry reference rejected',lambda:reject(changed(lambda x:x['conditions'].append(copy.deepcopy(x['conditions'][0])))))
 check('invented registry condition name rejected',lambda:reject(changed(lambda x:x['conditions'][0].update(name_as_reported='invented disease'))))
 check('duplicate snapshot key rejected',lambda:reject(changed(lambda x:x['records'].append(copy.deepcopy(x['records'][0])))))
 check('unsubstantiated conflict rejected',lambda:reject(changed(lambda x:x['records'][0].update(finding_status='conflicting'))))
 check('unknown optional detail accepted without fabricated value',lambda:validate(changed(lambda x:attr(x['records'][0],'frequency',dict(status='unknown'))),X['messages']))
 check('empty evidence rejected',lambda:reject(changed(lambda x:x['records'][0].update(evidence=[]))))
 check('duplicate message ID rejected',lambda:reject(copy.deepcopy(X['later_snapshot']),X['messages']+[copy.deepcopy(X['messages'][0])]))
 check('reference knowledge cannot be inserted as patient output',lambda:reject(changed(lambda x:x.update(medical_condition_reference=R))))
 check('all_nested_source_ids_resolve',lambda:source_refs(K))
 report=dict(passed=all(r['passed'] for r in results),checks=len(results),results=results,
  scope='Mechanical schema, reference, provenance and authored-fixture checks; no live LLM, clinical validation, causal verification or diagnostic accuracy study.')
 (HERE/'VALIDATION_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(run())
