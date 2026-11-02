"""Mechanical checks for proposed PMDD evidence and DRSP-input contracts."""
import copy,json
from pathlib import Path
from datetime import date,datetime,timezone,timedelta
from jsonschema import Draft202012Validator,ValidationError,FormatChecker
HERE=Path(__file__).resolve().parent
def load(n):return json.loads((HERE/n).read_text(encoding='utf-8-sig'))
K=load('knowledge.json');S=load('sources.json');EX=load('examples.json');DX=load('diary_examples.json')
ES=load('evidence_output.schema.json');DS=load('diary_input.schema.json')
for schema in [ES,DS]:Draft202012Validator.check_schema(schema)
EV=Draft202012Validator(ES,format_checker=FormatChecker())
DV=Draft202012Validator(DS,format_checker=FormatChecker())
def validate_evidence(x,msgs):
 EV.validate(x)
 by_id={m['id']:m for m in msgs};order={m['id']:i for i,m in enumerate(msgs)}
 if len(by_id)!=len(msgs):raise ValueError('Duplicate message ID')
 seen=set()
 for r in x['records']:
  key=(r['concept_id'],r['episode_key'],r['subject'])
  if key in seen:raise ValueError('Duplicate concept/period record')
  seen.add(key);supported=set()
  for e in r['evidence']:
   if e['message_id'] not in by_id:raise ValueError('Unknown source message')
   source=by_id[e['message_id']]
   if source['speaker']!='patient':raise ValueError('Patient evidence required')
   if e['quote'] not in source['text']:raise ValueError('Quote is not exact source text')
   for mid in e['context_message_ids']:
    if mid not in order or order[mid]>=order[e['message_id']]:raise ValueError('Context must precede source answer')
   for a in e['supports']:
    if a!='finding_status' and (a not in r['attributes'] or r['attributes'][a]['status']!='known'):
     raise ValueError('Support points to absent/unknown/inapplicable detail')
    supported.add(a)
  if 'finding_status' not in supported:raise ValueError('Status lacks source linkage')
  for a,d in r['attributes'].items():
   if d['status']=='known' and a not in supported:raise ValueError('Known detail lacks source linkage')
  if r['finding_status']=='conflicting':
   if len({(e['message_id'],e['quote']) for e in r['evidence']})<2:raise ValueError('Conflict needs distinct reports')
   if not r['uncertainty_notes'] or r['semantic_check_status']!='needs_review':raise ValueError('Conflict needs notes/review')
 return True
def validate_diary(x):
 DV.validate(x)
 refs={c['cycle_ref'] for c in x['cycles']}
 if len(refs)!=len(x['cycles']):raise ValueError('Duplicate cycle reference')
 seen=set();limitations=[]
 for r in x['ratings']:
  key=(r['observation_date'],r['item_id'])
  if key in seen:raise ValueError('Duplicate day/item entry needs explicit resolution')
  seen.add(key)
  if r['cycle_ref'] is not None and r['cycle_ref'] not in refs:raise ValueError('Unknown cycle reference')
  if r['recorded_at'] is not None:
   timestamp=datetime.fromisoformat(r['recorded_at'].replace('Z','+00:00'))
   day=date.fromisoformat(r['observation_date'])
   offset=r['observation_utc_offset']
   if offset is None:
    limitations.append('Observation timezone is unverified; date comparison not established.')
   else:
    sign=1 if offset[0]=='+' else -1
    local_zone=timezone(sign*timedelta(hours=int(offset[1:3]),minutes=int(offset[4:6])))
    recorded_day=timestamp.astimezone(local_zone).date()
    if recorded_day<day:raise ValueError('Rating timestamp precedes observation date')
    if recorded_day!=day and r['collection_mode']=='prospective_daily':
     limitations.append('Delayed entry needs provenance review; prospective status is not established by schema.')
  if r['collection_mode']!='prospective_daily':limitations.append('Entry is not verified prospective daily data.')
 if any(r['rating'] is None for r in x['ratings']):limitations.append('Missing ratings retained, not zero-imputed.')
 if not x['cycles']:limitations.append('Cycle coverage not established.')
 if 'unverified' in x['instrument_version'].lower():limitations.append('Instrument version not verified.')
 return {'structurally_valid':True,'limitations':list(dict.fromkeys(limitations)),
  'clinical_confirmation':'NOT_DETERMINED','distinct_observation_days':len({r['observation_date'] for r in x['ratings']})}
def run():
 results=[]
 def check(name,fn):
  try:fn();results.append({'check':name,'passed':True})
  except Exception as e:results.append({'check':name,'passed':False,'error':str(e)})
 def e_mut(fn):
  x=copy.deepcopy(EX['later_snapshot']);fn(x);return x
 def d_mut(fn):
  x=copy.deepcopy(DX['example']);fn(x);return x
 def e_reject(x,msgs=None):
  try:validate_evidence(x,msgs or EX['messages'])
  except (ValueError,ValidationError):return
  raise AssertionError('Invalid evidence fixture accepted')
 def d_reject(x):
  try:validate_diary(x)
  except (ValueError,ValidationError):return
  raise AssertionError('Invalid diary fixture accepted')
 def refs():
  ids=[c['id'] for c in K['concepts']];assert len(ids)==len(set(ids))
  def visit(x):
   if isinstance(x,dict):
    for name,value in x.items():
     if name.endswith('source_ids'):assert value and all(i in S for i in value),(name,value)
     if name=='concept_ids':assert all(i in ids for i in value)
     visit(value)
   elif isinstance(x,list):
    for item in x:visit(item)
  visit(K)
  assert {x['id'] for x in K['criteria_information_map']}==set('ABCDEFG')
 check('source_and_criteria_references_resolve',refs)
 def grouping():
  core=[c for c in K['concepts'] if c['role']=='core_affective']
  additional=[c for c in K['concepts'] if c['role']=='additional_symptom']
  assert len(core)==4 and len(additional)==7
  assert len({c['count_group'] for c in core+additional})==11
  assert next(c for c in additional if c['id']=='physical_symptoms')['count_group']=='physical'
  assert not K['clinical_reference_rules']['requires_both_distress_and_impairment']
  assert not K['clinical_reference_rules']['coexisting_disorder_automatically_excludes_pmdd']
 check('eleven_groups_four_core_and_correct_boundaries',grouping)
 check('first_snapshot_valid',lambda:validate_evidence(EX['first_snapshot'],EX['messages'][:2]))
 check('later_snapshot_valid',lambda:validate_evidence(EX['later_snapshot'],EX['messages']))
 check('reject_wrong_module',lambda:e_reject(e_mut(lambda x:x.update(module_id='adult_pdd'))))
 check('reject_invented_quote',lambda:e_reject(e_mut(lambda x:x['records'][0]['evidence'][0].update(quote='I have confirmed PMDD.'))))
 check('reject_future_context',lambda:e_reject(e_mut(lambda x:x['records'][3]['evidence'][1].update(context_message_ids=['m8']))))
 check('reject_same_message_context',lambda:e_reject(e_mut(lambda x:x['records'][3]['evidence'][1].update(context_message_ids=['m4']))))
 check('reject_wrong_concept_detail',lambda:e_reject(e_mut(lambda x:x['records'][0]['attributes'].update(sleep_hours={'status':'known','value':'eight hours'}))))
 check('reject_unknown_with_value',lambda:e_reject(e_mut(lambda x:x['records'][0]['attributes'].update(intensity_as_reported={'status':'unknown','value':'severe'}))))
 check('reject_known_without_support',lambda:e_reject(e_mut(lambda x:x['records'][0]['attributes'].update(intensity_as_reported={'status':'known','value':'severe'}))))
 check('reject_duplicate_concept_period',lambda:e_reject(e_mut(lambda x:x['records'].append(copy.deepcopy(x['records'][0])))))
 check('reject_confirmed_prospective_state',lambda:e_reject(e_mut(lambda x:x['prospective_review'].update(status='confirmed_pmdd'))))
 check('reject_diagnosis_field',lambda:e_reject(e_mut(lambda x:x.update(diagnosis='PMDD'))))
 check('diary_partial_example_valid',lambda:validate_diary(DX['example']))
 check('reject_drsp_zero',lambda:d_reject(d_mut(lambda x:x['ratings'][0].update(rating=0))))
 check('reject_drsp_seven',lambda:d_reject(d_mut(lambda x:x['ratings'][0].update(rating=7))))
 check('reject_invalid_item_number',lambda:d_reject(d_mut(lambda x:x['ratings'][0].update(item_id=25))))
 check('reject_invalid_calendar_date',lambda:d_reject(d_mut(lambda x:x['ratings'][0].update(observation_date='2026-02-30'))))
 check('reject_missing_without_reason',lambda:d_reject(d_mut(lambda x:x['ratings'][1].update(missing_reason=None))))
 check('reject_prospective_without_timestamp',lambda:d_reject(d_mut(lambda x:x['ratings'][0].update(recorded_at=None))))
 check('reject_timestamp_before_observation',lambda:d_reject(d_mut(lambda x:x['ratings'][0].update(recorded_at='2026-10-28T21:00:00+02:00'))))
 def timezone_boundary():
  x=d_mut(lambda x:x['ratings'][0].update(recorded_at='2026-10-28T23:30:00Z'))
  validate_diary(x)
 check('utc_timestamp_respects_observation_calendar_offset',timezone_boundary)
 check('reject_duplicate_day_item',lambda:d_reject(d_mut(lambda x:x['ratings'].append(copy.deepcopy(x['ratings'][0])))))
 check('reject_unknown_cycle_reference',lambda:d_reject(d_mut(lambda x:x['ratings'][0].update(cycle_ref='missing'))))
 def no_confirmation():
  summary=validate_diary(DX['example'])
  assert summary['distinct_observation_days']==2
  assert summary['clinical_confirmation']=='NOT_DETERMINED'
  assert summary['limitations']
 check('two_partial_days_are_not_two_confirmed_cycles',no_confirmation)
 def fixture():
  mapping={c['id']:c for c in K['concepts']}
  groups={mapping[r['concept_id']]['count_group'] for r in EX['first_snapshot']['records'] if mapping[r['concept_id']]['count_group']}
  assert len(groups)==3
  later={r['concept_id']:r for r in EX['later_snapshot']['records']}
  assert later['prospective_records']['attributes']['availability']['value']=='not_collected'
  assert 'background_symptoms' in later
  assert 'preceding_year_pattern' not in later['cyclical_timeline']['attributes']
  assert 'history_duration' in later['cyclical_timeline']['attributes']
  assert EX['later_snapshot']['safety_handoff']['status']=='not_assessed'
 check('gold_fixture_grouping_background_and_diary_gap',fixture)
 def no_runtime():
  assert not K['diagnostic_automation_enabled']
  assert not K['prospective_measurement']['cpass_implemented']
  assert K['runtime_integration']=='NOT_CONNECTED'
 check('no_automatic_diagnosis_or_unimplemented_scorer_claim',no_runtime)
 report={'checked_at':datetime.now(timezone.utc).isoformat(),'passed':all(r['passed'] for r in results),
  'check_count':len(results),'checks':results,'clinical_validation':False,
  'diary_example_summary':validate_diary(DX['example']),
  'limits':'Mechanical contracts and manually authored fictional fixtures. No semantic/model/clinical accuracy established, no validated prospective administration or C-PASS implementation.'}
 (HERE/'VALIDATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 for r in results:print(('PASS ' if r['passed'] else 'FAIL ')+r['check'])
 print(f"{sum(r['passed'] for r in results)}/{len(results)} checks passed; no clinical/model validation.")
 if not report['passed']:raise SystemExit(1)
if __name__=='__main__':run()
