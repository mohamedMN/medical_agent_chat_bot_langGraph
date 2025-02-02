# main.py
from typing import Dict, Any
from src.utils.safety import (
    extract_symptoms,
    identify_missing_symptoms,
    generate_recommendations,
    client,
    safety_check
)
from src.core.workflow import create_medical_workflow
import logging


def collect_medical_history() -> dict:
    """Collect basic medical history from the user"""
    print("\n=== Medical History Setup ===")
    return {
        "allergies": input("Enter any allergies (comma-separated): ").strip().split(', '),
        "conditions": input("Enter existing medical conditions (comma-separated): ").strip().split(', ')
    }


def run_medical_chat(user_input: str, medical_history: dict) -> str:
    """Execute the medical workflow for a given user input"""
    try:
        workflow = create_medical_workflow(
            extract_fn=extract_symptoms,
            recommend_fn=generate_recommendations,
            missing_symptoms_fn=identify_missing_symptoms,
            llm_client=client
        )

        initial_state = {
            "user_input": user_input,
            "symptoms": [],
            "medical_history": medical_history,
            "current_step": "",
            "triage_level": None,
            "language": "en",
            "emergency_detected": False,
            "response": None,
            "needs_clarification": False,
            "missing_symptoms": None
        }

        final_state = workflow.invoke(initial_state)

        if final_state.get("response"):
            return safety_check(final_state["response"])

        return "No response generated. Please try again."

    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    # Collect medical history once
    medical_history = collect_medical_history()

    print("\n=== Medical Chat ===")
    print("Type your symptoms or health concern (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye! Remember to consult a real doctor for medical concerns.")
            break

        if not user_input:
            print("Please describe your symptoms")
            continue

        response = run_medical_chat(user_input, medical_history)
        print("\nAssistant:", response)
        print("\n" + "-"*50 + "\n")
