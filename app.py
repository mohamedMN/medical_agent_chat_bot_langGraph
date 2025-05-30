import streamlit as st
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

# Set page configuration
st.set_page_config(
    page_title="Medical Assistant",
    page_icon="🏥",
    layout="centered"
)

# Initialize session state for storing conversation and medical history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "medical_history" not in st.session_state:
    st.session_state.medical_history = {"allergies": [], "conditions": []}


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


# App title
st.title("Medical Assistant")
st.markdown(
    "*Please note: This is not a substitute for professional medical advice.*")

# Sidebar for medical history input
with st.sidebar:
    st.header("Medical History")

    # Input for allergies
    allergies_input = st.text_input(
        "Allergies (comma-separated)",
        value=", ".join(
            st.session_state.medical_history["allergies"]) if st.session_state.medical_history["allergies"] else ""
    )

    # Input for existing conditions
    conditions_input = st.text_input(
        "Existing Medical Conditions (comma-separated)",
        value=", ".join(st.session_state.medical_history["conditions"]
                        ) if st.session_state.medical_history["conditions"] else ""
    )

    # Update button
    if st.button("Update Medical History"):
        st.session_state.medical_history["allergies"] = [
            item.strip() for item in allergies_input.split(",")] if allergies_input else []
        st.session_state.medical_history["conditions"] = [
            item.strip() for item in conditions_input.split(",")] if conditions_input else []
        st.success("Medical history updated!")

# Display conversation history
st.subheader("Conversation")
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Assistant:** {message['content']}")
        st.write("---")

# User input
user_input = st.text_area(
    "Describe your symptoms or health concern", height=100)

# Submit button
if st.button("Submit"):
    if user_input:
        # Add user message to conversation history
        st.session_state.conversation_history.append(
            {"role": "user", "content": user_input})

        # Get medical assistant response
        response = run_medical_chat(
            user_input, st.session_state.medical_history)

        # Add assistant response to conversation history
        st.session_state.conversation_history.append(
            {"role": "assistant", "content": response})

        # Rerun the app to update the conversation display
        st.rerun()
    else:
        st.warning("Please enter your symptoms or health concern.")

# Clear conversation button
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()
