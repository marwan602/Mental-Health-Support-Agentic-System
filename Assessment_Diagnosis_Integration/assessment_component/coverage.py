"""Shared interview topics and deterministic follow-up rules."""

TOPICS = {
    "main_concern": "What brought the person to the conversation",
    "presenting_pattern": "What happens during the specific difficulty the person describes, including what happens immediately before or after it if that distinction matters",
    "mood": "What their mood has been like",
    "interest": "Changes in interest or enjoyment",
    "timing": "When the current changes began and how often they happen",
    "daily_impact": "Concrete effect on daily life",
    "sleep": "Changes in sleep",
    "energy": "Changes in energy",
    "appetite": "Changes in appetite or weight",
    "concentration": "Changes in concentration or decision-making",
    "self_view": "Changes in how they feel about themselves",
    "movement": "Noticeable slowing or restlessness compared with usual",
    "prior_periods": "Earlier similar periods and how they ended",
    "activation_history": "Past periods of unusually elevated mood or energy",
    "health_conditions": "Health conditions, physical changes or evaluations relevant to this presentation",
    "medication_changes": "Medicines or changes in medicines relevant to this presentation",
    "substances": "Relevant alcohol or other substance use and its timing",
    "life_context": "Recent events, stressors or changes in circumstances",
    "cycle_pattern": "Relationship to the menstrual cycle and any daily records, when a cyclical pattern is reported",
}

TERMINAL = {"answered", "unknown", "declined"}
REPORTED = TERMINAL | {"partial"}


def eligible_topics(coverage, asked, answer_count):
    """Permit one retry after at least one intervening patient answer."""
    eligible = []
    for topic in TOPICS:
        if topic in ("cycle_pattern", "presenting_pattern") and topic not in coverage:
            continue
        if coverage.get(topic, {}).get("status") in TERMINAL:
            continue
        attempts = [a for a in asked if a["topic"] == topic]
        if len(attempts) >= 2:
            continue
        if attempts and answer_count <= attempts[-1]["answer_count"] + 1:
            continue
        eligible.append(topic)
    return eligible
