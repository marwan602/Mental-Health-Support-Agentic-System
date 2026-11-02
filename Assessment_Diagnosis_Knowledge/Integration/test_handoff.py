import copy
import json
import unittest
from knowledge_access import (ROOT, GRAPH, ROUTES, MANIFEST, get_context, read,
    validate_snapshot, append_snapshot, concept_history, next_with_supplements, validate_role_output)

class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.example = read('MDD/examples.json')
        self.messages = self.example['messages']
        self.snapshot = copy.deepcopy(self.example['later_snapshot'])
        self.state = copy.deepcopy(read('Workflow/Interview_Graph/fictional_cases.json')[1]['state'])
        for n in ['q.opening','q.safety.death_wish','q.safety.suicidal_thoughts','q.safety.past_behaviour']:
            node = next(x for x in GRAPH['catalog'] if x['id']==n)
            self.state['coverage'][n] = {'status':'supported','finding_status':'reported_absent',
                'period_id':self.state['period_bindings'][node['period_binding']], 'revision':1,'source_message_ids':['m2']}

    def supplement(self):
        self.state['branch_facts']['persistent'] = {'status':'open','reason':'Reported long-term pattern','source_message_ids':['m2']}
        self.state['supplement_requests'] = [{'target_id':'root/PDD/anxious_distress',
            'reason':'Relevant features during long-term low mood need clarification',
            'source_message_ids':['m2'],'requirement_reference':'PDD/knowledge.json#concepts/anxious_distress'}]

    def test_all_219_concepts_and_1428_attributes_have_routes(self):
        self.assertEqual(len(ROUTES),219)
        self.assertEqual(sum(len(r['attributes']) for r in ROUTES.values()),1428)
        self.assertEqual({n['id'] for n in GRAPH['catalog'] if n['kind']=='concept_entry'},set(ROUTES))

    def test_original_schema_and_contextual_yes_pass(self):
        self.assertEqual(validate_snapshot('MDD',self.snapshot,self.messages)['status'],'PASS')

    def test_fabricated_quote_rejected(self):
        self.snapshot['records'][0]['evidence'][0]['quote']='This quote does not exist.'
        with self.assertRaises(ValueError): validate_snapshot('MDD',self.snapshot,self.messages)

    def test_future_context_rejected(self):
        self.snapshot['records'][1]['evidence'][1]['context_message_ids']=['m6']
        with self.assertRaises(ValueError): validate_snapshot('MDD',self.snapshot,self.messages)

    def test_same_message_context_rejected(self):
        self.snapshot['records'][1]['evidence'][1]['context_message_ids']=['m4']
        with self.assertRaises(ValueError): validate_snapshot('MDD',self.snapshot,self.messages)

    def test_bare_yes_without_context_rejected(self):
        self.snapshot['records'][1]['evidence'][1]['context_message_ids']=[]
        with self.assertRaises(ValueError): validate_snapshot('MDD',self.snapshot,self.messages)

    def test_known_attribute_without_pointer_rejected(self):
        self.snapshot['records'][0]['evidence'][0]['supports']=['finding_status']
        with self.assertRaises(ValueError): validate_snapshot('MDD',self.snapshot,self.messages)

    def test_assistant_cannot_be_patient_evidence(self):
        self.snapshot['records'][0]['evidence'][0].update(message_id='m1',quote=self.messages[0]['text'])
        with self.assertRaises(ValueError): validate_snapshot('MDD',self.snapshot,self.messages)

    def test_wrong_module_schema_rejected(self):
        with self.assertRaises(Exception): validate_snapshot('PDD',self.snapshot,self.messages)

    def test_duplicate_message_ids_rejected(self):
        with self.assertRaises(ValueError): validate_snapshot('MDD',self.snapshot,self.messages+[self.messages[0]])

    def test_history_appends_without_overwriting(self):
        first = append_snapshot([],'MDD',self.example['first_snapshot'],self.messages)
        second = append_snapshot(first,'MDD',self.snapshot,self.messages)
        self.assertEqual(len(first),1)
        self.assertEqual(len(second),2)
        h = concept_history(second,'MDD','sleep_disturbance','presenting_period')
        self.assertNotIn('duration',h[0]['record']['attributes'])
        self.assertEqual(h[1]['record']['attributes']['duration']['value'],'two weeks')
        self.assertEqual(concept_history(second,'MDD','sleep_disturbance','different_episode'),[])

    def test_extractor_sees_volunteered_unasked_concepts(self):
        c=get_context('extractor',['root/MDD/depressed_mood'])
        self.assertIn('sleep_disturbance',{x['concept_id'] for x in c['available_concepts']})
        sleep=get_context('extractor',['root/MDD/sleep_disturbance'])
        self.assertIn('sleep_disturbance',{x['id'] for x in sleep['concept_cards'][0]['concepts']})

    def test_conversation_gets_only_selected_concept(self):
        c=get_context('conversation',['detail/MDD/depressed_mood/duration'])
        self.assertEqual([x['id'] for x in c['concept_cards'][0]['concepts']],['depressed_mood'])

    def test_diagnosis_gets_module_specific_rules(self):
        c=get_context('diagnosis',module_names=['PMDD'])
        self.assertEqual(c['review_knowledge']['PMDD']['rules']['clinical_reference_rules']['minimum_symptomatic_cycles_for_prospective_confirmation'],2)

    def test_unknown_target_rejected(self):
        with self.assertRaises(ValueError):get_context('conversation',['made_up'])

    def test_extraction_requires_explicit_module(self):
        with self.assertRaises(ValueError):get_context('extractor')

    def test_supplement_is_reachable_with_justified_open_branch(self):
        self.supplement()
        self.assertEqual(next_with_supplements(self.state,self.messages)['target_id'],'root/PDD/anxious_distress')

    def test_supplement_does_not_open_inactive_module(self):
        self.supplement(); self.state['branch_facts']={}
        self.assertNotEqual(next_with_supplements(self.state,self.messages).get('target_id'),'root/PDD/anxious_distress')

    def test_supplement_cannot_bypass_urgent_review(self):
        self.supplement(); self.state['urgent_review_required']=True
        self.assertEqual(next_with_supplements(self.state,self.messages)['action'],'URGENT_REVIEW')

    def test_supplement_cannot_bypass_stop(self):
        self.supplement(); self.state['participation']='stop'
        self.assertEqual(next_with_supplements(self.state,self.messages)['action'],'STOP')

    def test_supplement_cannot_bypass_early_safety(self):
        self.supplement(); del self.state['coverage']['q.safety.suicidal_thoughts']
        self.assertEqual(next_with_supplements(self.state,self.messages)['target_id'],'q.safety.suicidal_thoughts')

    def test_supplement_respects_scoped_decline(self):
        self.supplement(); self.state['blocked_targets']={'root/PDD/anxious_distress':{'period_id':'longstanding_period','reason':'Declined'}}
        self.assertNotEqual(next_with_supplements(self.state,self.messages).get('target_id'),'root/PDD/anxious_distress')

    def test_supplement_requires_real_message_pointer(self):
        self.supplement(); self.state['supplement_requests'][0]['source_message_ids']=['nonexistent']
        with self.assertRaises(ValueError):next_with_supplements(self.state,self.messages)

    def test_all_modules_have_real_schemas_and_registers(self):
        for info in MANIFEST['modules'].values():
            for key in ['knowledge','sources','evidence_schema','examples']:
                self.assertTrue((ROOT/info[key]).is_file())

    def test_route_sources_resolve_from_package_root(self):
        for route in ROUTES.values():
            for source in route['clinical_source_refs']:
                self.assertIn(source['source_id'],read(source['source_path']))

    def test_all_output_schemas_are_valid(self):
        from jsonschema import Draft202012Validator
        for name in ['conversation_output.schema.json','planner_output.schema.json','synthesis_output.schema.json']:
            Draft202012Validator.check_schema(read('Integration/'+name))

    def test_existing_module_history_examples_use_same_adapter(self):
        for module in MANIFEST['modules']:
            data=read(module+'/examples.json')
            containers=[data] if 'messages' in data else data.get('cases',[])+[data['history_case']]
            for container in containers:
                for value in container.values():
                    if isinstance(value,dict) and 'records' in value:
                        self.assertEqual(validate_snapshot(module,value,container['messages'])['status'],'PASS')

    def test_role_examples_validate_with_supplied_state_and_ledger(self):
        data=read('Integration/example_input_output.json')
        ledger=append_snapshot([],'MDD',data['extraction_output'][0],data['messages'])
        for role,key in [('conversation','conversation_output'),('planner','planner_output'),('diagnosis','synthesis_output')]:
            self.assertEqual(validate_role_output(role,data[key],state=self.state,ledger=ledger)['status'],'PASS')

    def test_output_cannot_invent_question_id(self):
        data=read('Integration/example_input_output.json')['planner_output'];data['target_id']='made_up'
        with self.assertRaises(ValueError):validate_role_output('planner',data,state=self.state)

    def test_output_cannot_mix_periods(self):
        data=read('Integration/example_input_output.json')['planner_output'];data['period_id']='unrelated_historical_episode'
        with self.assertRaises(ValueError):validate_role_output('planner',data,state=self.state)

    def test_unpreserved_wording_is_rejected(self):
        data=read('Integration/example_input_output.json')['conversation_output'];data['target_preserved']=False
        with self.assertRaises(ValueError):validate_role_output('conversation',data,state=self.state)

    def test_synthesis_cannot_invent_source(self):
        data=read('Integration/example_input_output.json')['synthesis_output']
        data['candidates'][0]['criteria_review'][0]['source_references']=['MDD/sources.json#INVENTED']
        with self.assertRaises(ValueError):validate_role_output('diagnosis',data)

    def test_synthesis_cannot_invent_evidence_pointer(self):
        data=read('Integration/example_input_output.json')['synthesis_output']
        data['candidates'][0]['criteria_review'][0]['evidence_pointers']=['ledger[99].snapshot.records[0]']
        with self.assertRaises(ValueError):validate_role_output('diagnosis',data,ledger=[])

    def test_synthesis_cannot_claim_undelivered_review(self):
        data=read('Integration/example_input_output.json')['synthesis_output']
        data['candidates']=[]
        data['safety_handoff'].update(response_delivered=True,delivery_record_reference='unverified_delivery')
        with self.assertRaises(ValueError):validate_role_output('diagnosis',data)

if __name__=='__main__':
    unittest.main()
