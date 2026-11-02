"""Offline arithmetic reference for explicit instrument responses, not chat scoring."""
import argparse
from datetime import date
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ORIGINS={'direct_selection','confirmed_instrument_response'}
STATES={'answered','declined','does_not_know','unclear','not_asked'}
MODES={'standardized_self_report','standardized_interviewer_readout'}

def profiles():
    return {p['id']:p for p in json.loads((HERE/'instrument_profiles.json').read_text(encoding='utf-8'))}

def item9_review(record):
    """Independent of total completeness. This is a review need, not acuity."""
    out={'safety_clearance':False,'actual_review_delivered':False}
    if not isinstance(record,dict) or record.get('instrument_id')!='PHQ9':
        return dict(out,status='not_assessed_by_this_instrument',followup_needed=None)
    responses=record.get('responses',[])
    if not isinstance(responses,list):responses=[]
    rows=[r for r in responses if isinstance(r,dict) and r.get('item_id')=='PHQ9_9']
    if len(rows)!=1:
        return dict(out,status='unanswered_or_duplicate_requires_review_decision',followup_needed=True)
    r=rows[0];value=r.get('category_code')
    if r.get('status')!='answered' or type(value) is not int or value not in range(4) or r.get('response_origin') not in ORIGINS:
        return dict(out,status='unresolved_requires_review_decision',followup_needed=True)
    if value>0:return dict(out,status='endorsed_requires_followup',followup_needed=True)
    return dict(out,status='not_endorsed_in_this_item',followup_needed=False)

def score_record(record):
    """Check declared protocol and compute only complete supported instruments.

    Declarations do not authenticate administration or clinical approval. The
    application must check source evidence and safety independently of scoring.
    """
    review=item9_review(record)
    out=dict(arithmetic_reference_only=True,administration_verification='application_declaration_not_independently_verified',
             total=None,symptom_band=None,diagnosis=None,treatment_recommendation=None,item9_review=review)
    def fail(status,reason):return dict(out,status=status,reason=reason)
    if not isinstance(record,dict):return fail('invalid','record_must_be_object')
    p=profiles().get(record.get('instrument_id'))
    if not p:return fail('invalid','unknown_instrument')
    out.update(instrument_id=p['id'],profile_version=p['profile_version'],score_direction=p.get('higher_means'))
    if not p['scoring_reference_enabled']:return fail('not_implemented','candidate_protocol_only')
    if type(record.get('age')) is not int or record['age']<18:return fail('not_scored','adult_scope_not_established')
    if record.get('consent_to_measurement') is not True:return fail('not_scored','measurement_not_agreed')
    if record.get('administration_mode') not in MODES:return fail('not_scored','not_standardized_item_administration')
    if record.get('profile_version')!=p['profile_version']:return fail('not_scored','profile_version_mismatch')
    if not isinstance(record.get('language'),str) or not record['language'].strip():return fail('invalid','missing_form_language')
    if not isinstance(record.get('form_reference'),str) or not record['form_reference'].strip():return fail('invalid','missing_exact_form_reference')
    for flag in ['standardized_items_presented','standardized_timeframe_presented','protocol_language_reviewed']:
        if record.get(flag) is not True:return fail('not_scored',flag+'_not_declared')
    if type(record.get('recall_days')) is not int or record['recall_days']!=p['recall_days']:
        return fail('not_scored','wrong_or_undefined_recall_window')
    try:date.fromisoformat(record['reference_date'])
    except (ValueError,TypeError,KeyError):return fail('invalid','reference_date_required_as_ISO_date')
    out.update(reference_date=record['reference_date'],recall_days=p['recall_days'],language=record['language'],form_reference=record['form_reference'],administration_mode=record['administration_mode'])
    rows=record.get('responses')
    if not isinstance(rows,list):return fail('invalid','responses_must_be_list')
    expected=[f"{p['id']}_{i}" for i in range(1,p['items']+1)]
    keyed={}
    for r in rows:
        if not isinstance(r,dict):return fail('invalid','item_response_must_be_object')
        iid=r.get('item_id')
        if iid not in expected or iid in keyed:return fail('invalid','unexpected_or_duplicate_item')
        if r.get('status') not in STATES:return fail('invalid','unknown_item_status')
        value=r.get('category_code')
        if r['status']=='answered':
            if type(value) is not int or not p['code_min']<=value<=p['code_max']:return fail('invalid','item_code_out_of_range_or_wrong_type')
            if r.get('response_origin') not in ORIGINS:return fail('not_scored','unvalidated_estimated_response_origin')
            if not isinstance(r.get('source_message_id'),str) or not r['source_message_id'].strip():return fail('invalid','answered_item_needs_source_pointer')
        elif value is not None:return fail('invalid','unanswered_item_cannot_have_numeric_score')
        keyed[iid]=r
    missing=[iid for iid in expected if iid not in keyed or keyed[iid]['status']!='answered']
    out.update(answered_items=p['items']-len(missing),expected_items=p['items'],missing_or_unanswered_items=missing)
    if missing:return fail('incomplete','no_total_without_complete_items_in_this_reference')
    total=sum(keyed[iid]['category_code'] for iid in expected)
    out.update(status='complete',total=total,reason='complete_declared_standardized_item_responses')
    if p['id']=='PHQ9':
        out['symptom_band']=next(name for lo,hi,name in [(0,4,'none_minimal'),(5,9,'mild'),(10,14,'moderate'),(15,19,'moderately_severe'),(20,27,'severe')] if lo<=total<=hi)
        out['screening_threshold_met']=total>=10
        out['threshold_meaning']='Common PHQ-9 screening threshold; not a confirmed diagnosis, safety clearance or automatic treatment decision.'
    elif p['id']=='PHQ2':
        out['screening_threshold_met']=total>=3
        out['threshold_meaning']='Original-study case-finding threshold; positive supports fuller assessment, negative does not close clinical concerns.'
    elif p['id']=='WHO5':
        out['wellbeing_percent']=4*total
        out['poor_wellbeing_further_assessment_suggested']=total<13
        out['threshold_meaning']='WHO suggested poor-wellbeing/further-assessment threshold, not a depressive-disorder diagnosis.'
    return out

def fictional_record(instrument_id='PHQ9',values=None):
    p=profiles()[instrument_id]
    if values is None:values=[0]*p['items']
    return dict(instrument_id=instrument_id,profile_version=p['profile_version'],age=24,
                consent_to_measurement=True,administration_mode='standardized_self_report',
                form_reference='fictional_fixture_of_source_linked_form',language='en',
                protocol_language_reviewed=True,standardized_items_presented=True,standardized_timeframe_presented=True,
                reference_date='2026-11-02',recall_days=p['recall_days'],
                responses=[dict(item_id=f'{instrument_id}_{i+1}',status='answered' if v is not None else 'declined',category_code=v,
                                source_message_id=f'fictional_m{i+1}',response_origin='direct_selection') for i,v in enumerate(values)])

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--record',type=Path)
    args=ap.parse_args()
    if args.record:
        print(json.dumps(score_record(json.loads(args.record.read_text(encoding='utf-8'))),indent=2))
    else:
        print(json.dumps({'fictional_demo_only':True,'result':score_record(fictional_record(values=[2,2,2,1,1,1,1,0,0]))},indent=2))
