"""Arithmetic/provenance checks; not clinical or language validation."""
import unittest
from score_answers import score_record,fictional_record,item9_review

class MeasurementChecks(unittest.TestCase):
    def test_phq9_complete_example(self):
        r=score_record(fictional_record(values=[2,2,2,1,1,1,1,0,0]))
        self.assertEqual((r['total'],r['symptom_band']),(10,'moderate'))
        self.assertIsNone(r['diagnosis'])
        self.assertFalse(r['item9_review']['safety_clearance'])
    def test_phq9_band_boundaries(self):
        for total,band in [(0,'none_minimal'),(4,'none_minimal'),(5,'mild'),(9,'mild'),(10,'moderate'),(14,'moderate'),(15,'moderately_severe'),(19,'moderately_severe'),(20,'severe'),(27,'severe')]:
            values=[];left=total
            for _ in range(9):v=min(3,left);values.append(v);left-=v
            self.assertEqual(score_record(fictional_record(values=values))['symptom_band'],band)
    def test_missing_is_not_zero(self):
        r=score_record(fictional_record(values=[0,0,0,None,0,0,0,0,0]))
        self.assertEqual(r['status'],'incomplete');self.assertIsNone(r['total'])
    def test_item9_endorsement_with_incomplete_total(self):
        r=score_record(fictional_record(values=[None,0,0,0,0,0,0,0,1]))
        self.assertIsNone(r['total']);self.assertTrue(r['item9_review']['followup_needed'])
    def test_missing_item9_is_information_limit(self):
        r=score_record(fictional_record(values=[0]*8+[None]))
        self.assertTrue(r['item9_review']['followup_needed']);self.assertFalse(r['item9_review']['safety_clearance'])
    def test_low_total_does_not_suppress_item9(self):
        r=score_record(fictional_record(values=[0]*8+[1]))
        self.assertEqual(r['total'],1);self.assertTrue(r['item9_review']['followup_needed'])
    def test_negative_item9_not_clearance(self):
        r=item9_review(fictional_record())
        self.assertFalse(r['followup_needed']);self.assertFalse(r['safety_clearance'])
    def test_other_invalid_item_keeps_item9_review(self):
        r=score_record(fictional_record(values=[99]+[0]*7+[1]))
        self.assertEqual(r['status'],'invalid');self.assertTrue(r['item9_review']['followup_needed'])
    def test_phq2_boundary(self):
        self.assertFalse(score_record(fictional_record('PHQ2',[1,1]))['screening_threshold_met'])
        self.assertTrue(score_record(fictional_record('PHQ2',[1,2]))['screening_threshold_met'])
    def test_who5_direction_and_conversion(self):
        a=score_record(fictional_record('WHO5',[5]*5));b=score_record(fictional_record('WHO5',[0]*5))
        self.assertEqual(a['wellbeing_percent'],100);self.assertEqual(b['wellbeing_percent'],0)
        self.assertEqual(a['score_direction'],'better_reported_wellbeing')
    def test_who5_cutpoint(self):
        self.assertTrue(score_record(fictional_record('WHO5',[3,3,2,2,2]))['poor_wellbeing_further_assessment_suggested'])
        self.assertFalse(score_record(fictional_record('WHO5',[3,3,3,2,2]))['poor_wellbeing_further_assessment_suggested'])
    def test_unstructured_chat_blocked(self):
        x=fictional_record();x['administration_mode']='unstructured_chat_estimate'
        self.assertEqual(score_record(x)['status'],'not_scored')
    def test_llm_inference_origin_blocked(self):
        x=fictional_record();x['responses'][0]['response_origin']='LLM_guess'
        self.assertEqual(score_record(x)['status'],'not_scored')
    def test_bool_is_not_numeric_category(self):
        x=fictional_record();x['responses'][0]['category_code']=True
        self.assertEqual(score_record(x)['status'],'invalid')
    def test_extra_function_item_not_added(self):
        x=fictional_record();x['responses'].append(dict(x['responses'][0],item_id='PHQ9_10'))
        self.assertEqual(score_record(x)['status'],'invalid')
        x=fictional_record();x['functioning_response']='very difficult'
        self.assertEqual(score_record(x)['total'],0)
    def test_duplicate_item_blocked(self):
        x=fictional_record();x['responses'].append(x['responses'][0])
        self.assertEqual(score_record(x)['status'],'invalid')
    def test_wrong_recall_blocked(self):
        x=fictional_record();x['recall_days']=42
        self.assertEqual(score_record(x)['status'],'not_scored')
    def test_missing_source_blocked(self):
        x=fictional_record();x['responses'][0]['source_message_id']=''
        self.assertEqual(score_record(x)['status'],'invalid')
    def test_no_consent_no_score(self):
        x=fictional_record();x['consent_to_measurement']=False
        self.assertEqual(score_record(x)['status'],'not_scored')
    def test_candidate_tool_has_no_scorer(self):
        for tool in ['EPDS','GDS15','MADRS','DRSP','ASQ']:
            self.assertEqual(score_record({'instrument_id':tool})['status'],'not_implemented')
    def test_language_review_declaration_required(self):
        x=fictional_record();x['protocol_language_reviewed']=False
        self.assertEqual(score_record(x)['status'],'not_scored')
    def test_version_mismatch_blocked(self):
        x=fictional_record();x['profile_version']='unknown_version'
        self.assertEqual(score_record(x)['status'],'not_scored')
    def test_unknown_tool_not_scored(self):
        self.assertEqual(score_record({'instrument_id':'made_up'})['status'],'invalid')
    def test_valid_zero_distinct_from_missing(self):
        self.assertEqual(score_record(fictional_record())['total'],0)
        self.assertIsNone(score_record(fictional_record(values=[None]*9))['total'])

if __name__=='__main__':unittest.main(verbosity=2)
