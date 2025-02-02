# conversation.py
from typing import Dict, Any
from src.utils.safety import (
    extract_symptoms,
    identify_missing_symptoms,
    generate_recommendations
)


def process_input(state: Dict[str, Any]) -> Dict[str, Any]:
    """Process user input and extract symptoms"""
    try:
        symptoms = extract_symptoms(state["user_input"])
        return {
            "symptoms": symptoms,
            "current_step": "triage_assessment"
        }
    except Exception as e:
        return {"response": f"Input error: {str(e)}"}


def assess_triage(state: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate symptom urgency and completeness"""
    try:
        missing = identify_missing_symptoms(state["symptoms"])
        if missing:
            return {
                "needs_clarification": True,
                "missing_symptoms": missing
            }

        # Implement your triage logic here
        is_emergency = check_emergency_conditions(state["symptoms"])
        return {"emergency_detected": is_emergency}

    except Exception as e:
        return {"response": f"Triage error: {str(e)}"}


def handle_emergency(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate emergency response"""
    return {
        "response": "🚨 Please seek immediate medical attention!",
        "current_step": "end"
    }


def clarify_symptoms(state: Dict[str, Any]) -> Dict[str, Any]:
    """Request additional symptom details"""
    missing = state.get("missing_symptoms", [])
    return {
        "response": f"Please clarify: {', '.join(missing)}?",
        "current_step": "awaiting_clarification"
    }


def provide_recommendations(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate safe recommendations"""
    try:
        recs = generate_recommendations(
            state["symptoms"],
            state["medical_history"]
        )
        return {
            "response": recs,
            "current_step": "end"
        }
    except Exception as e:
        return {"response": f"Recommendation error: {str(e)}"}
