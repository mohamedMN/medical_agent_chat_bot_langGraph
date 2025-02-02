medical_knowledge = {
    "chest_pain": {
        "related_conditions": ["heart_attack", "angina", "acid_reflux"],
        "urgency": "high",
        "questions": ["duration", "radiation", "intensity"]
    },
    "shortness_of_breath": {
        "related_conditions": ["asthma", "copd", "pulmonary_embolism"],
        "urgency": "high"
    }
}


def query_knowledge_graph(symptoms: list[str]):
    urgency_levels = []
    for symptom in symptoms:
        if symptom in medical_knowledge:
            urgency = medical_knowledge[symptom].get("urgency", "medium")
            urgency_levels.append(urgency)

    if "high" in urgency_levels:
        return "emergency"
    return "non_emergency"
