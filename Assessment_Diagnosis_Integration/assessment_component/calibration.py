"""A fixed non-benchmark fixture for the blinded interview judge."""
from uuid import uuid4
from .harness.providers import LLMCaller, ResponseCache
from .harness.runlog import EventLog
from .harness.util import dump_json

def challenge():
    utterances=[
        ("interviewer","How have you been feeling lately?","opening"),
        ("patient","I felt low on six days last week.","answer"),
        ("interviewer","How many days last week did you feel low?","follow_up"),
        ("patient","Six days.","answer"),
        ("interviewer","How has that affected work?","follow_up"),
        ("patient","I missed one shift.","answer")]
    turns=[{"message_id":f"m{n:04}","speaker":s,"text":t,"kind":k} for n,(s,t,k) in enumerate(utterances,1)]
    findings=[
        {"finding_id":"f0001","topic":"low mood","attributes":{"days_in_previous_week":7},"quote":turns[1]["text"],"message_id":"m0002"},
        {"finding_id":"f0002","topic":"work impact","attributes":{"missed_shifts":1},"quote":turns[-1]["text"],"message_id":"m0006"}]
    return {"transcript":turns,"findings":findings,"plans":[],"end_reason":"question_budget"}

def checks(obj):
    findings={f["id"]:f for f in obj["findings"]}
    questions={q["turn"]:q for q in obj["questions"]}
    return {"flags_wrong_frequency":findings["f0001"]["supported"] is False,
            "accepts_supported_work_fact":findings["f0002"]["supported"] is True,
            "detects_repeat_with_earlier_answer":questions["m0003"]["repeated"] is True and questions["m0003"]["earlier_turn"]=="m0002",
            "allows_new_question":questions["m0005"]["repeated"] is False}

def calibrate(out,client,spec,prompt,mock):
    folder=out/"judge_check";folder.mkdir(exist_ok=True)
    log=EventLog(folder/f"events_{uuid4().hex[:8]}.jsonl");cache=ResponseCache(folder/"responses.jsonl")
    def validate(obj):
        checks(obj)
        return []
    try:
        caller=LLMCaller(client,spec,log,cache,{"temperature":0,"max_tokens":spec["max_tokens"]})
        data=challenge()
        obj,meta=caller.call_json("judge_interview",prompt,data,validate,context=data)
        if obj is None: raise ValueError(f"Judge check: {meta['errors']}")
        ratings=checks(obj)
        dump_json(folder/"report.json",{"mock":mock,"fixture":data,"review":obj,"checks":ratings,"passed":all(ratings.values()),
                  "model_returned":sorted(caller.models_returned)})
        return all(ratings.values())
    finally:
        log.close();cache.close()
