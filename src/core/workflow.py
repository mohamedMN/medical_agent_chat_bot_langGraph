from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Optional, Callable, Any


class MedicalState(TypedDict):
    user_input: str
    symptoms: List[str]
    medical_history: Dict
    current_step: str
    triage_level: Optional[str]
    language: str
    emergency_detected: bool
    response: Optional[str]
    needs_clarification: bool
    missing_symptoms: Optional[List[str]]


def create_medical_workflow(
    extract_fn: Callable[[str, Any], List[str]],  # Updated signature
    recommend_fn: Callable[[List[str], Dict], str],
    missing_symptoms_fn: Callable[[List[str]], Optional[List[str]]],
    llm_client: Any  # Add LLM client parameter
):
    """Updated factory function with proper parameter handling"""

    workflow = StateGraph(MedicalState)

    # Node 1: Process Input (updated)
    # Update all nodes to maintain state continuity


    def process_input(state: MedicalState):
        return {
            **state,
            "symptoms": extract_fn(state["user_input"], llm_client),
            "current_step": "processed_input"
        }


    def assess_triage(state: MedicalState):
        missing = missing_symptoms_fn(state["symptoms"])
        if missing:
            return {**state,
                    "needs_clarification": True,
                    "missing_symptoms": missing,
                    "current_step": "needs_clarification"}
        return {**state,
                "emergency_detected": False,
                "current_step": "triage_assessed"}

    def provide_recommendations(state: MedicalState):
        return {
            **state,
            "response": recommend_fn(state["symptoms"], state["medical_history"])
        }

    # Add nodes to workflow
    workflow.add_node("process_input", process_input)
    workflow.add_node("assess_triage", assess_triage)
    workflow.add_node("handle_emergency", lambda state: {
                      "response": "Emergency!"})
    workflow.add_node("clarify_symptoms", lambda state: {
                      "response": "Please clarify"})
    workflow.add_node("provide_recommendations", provide_recommendations)

    # Define workflow transitions (keep existing edge logic)
    workflow.set_entry_point("process_input")
    workflow.add_edge("process_input", "assess_triage")
    workflow.add_conditional_edges(
        "assess_triage",
        lambda state: (
            "emergency" if state["emergency_detected"]
            else "clarify" if state.get("needs_clarification")
            else "recommend"
        ),
        {
            "emergency": "handle_emergency",
            "clarify": "clarify_symptoms",
            "recommend": "provide_recommendations"
        }
    )
    workflow.add_edge("handle_emergency", END)
    workflow.add_edge("clarify_symptoms", END)
    workflow.add_edge("provide_recommendations", END)

    return workflow.compile()
