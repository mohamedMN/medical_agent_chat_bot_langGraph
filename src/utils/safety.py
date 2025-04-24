from typing import List, Dict, Optional
import os
from groq import Groq
from dotenv import load_dotenv
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('medical_system.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables with error handling
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logging.error("GROQ_API_KEY not found in environment variables")
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Initialize Groq client
try:
    client = Groq(api_key=api_key)
    logging.info("Groq client initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize Groq client: {str(e)}")
    raise

MODEL = "gemma2-9b-it"

SAFETY_KEYWORDS = [
    "emergency", "urgent", "911", "ER",
    "hospital", "ambulance", "severe",
    "dangerous", "life-threatening"
]


def safety_check(response: str) -> str:
    try:
        logging.debug(
            f"Performing safety check on response: {response[:100]}...")

        has_emergency = any(keyword in response.lower()
                            for keyword in SAFETY_KEYWORDS)

        if has_emergency:
            logging.warning(f"Emergency keywords detected in response")

        disclaimer = (
            "\n\n🚨 SAFETY WARNING: This is not medical advice. Seek immediate professional care!"
            if has_emergency else
            "\n\n🔒 Medical Disclaimer: This is not a substitute for professional medical diagnosis or treatment."
        )
        disclaimer += "\n⚕️ Always consult a qualified healthcare provider."

        return response + disclaimer
    except Exception as e:
        logging.error(
            f"Error in safety_check: {str(e)}\n{traceback.format_exc()}")
        raise


def identify_missing_symptoms(state_symptoms: List[str]) -> Optional[List[str]]:
    try:
        if not isinstance(state_symptoms, list):
            logging.error("state_symptoms must be a list")
            raise TypeError("state_symptoms must be a list")

        logging.info(f"Analyzing symptoms: {state_symptoms}")

        required_details = {
            "chest_pain": ["duration", "radiation", "intensity"],
            "headache": ["onset", "frequency", "associated_nausea"],
            "fever": ["duration", "max_temperature", "response_to_medication"]
        }

        missing = []
        for symptom in state_symptoms:
            if not isinstance(symptom, str):
                logging.warning(f"Non-string symptom found: {symptom}")
                continue

            if symptom in required_details:
                logging.debug(f"Checking details for symptom: {symptom}")
                for detail in required_details[symptom]:
                    if not any(detail in s for s in state_symptoms):
                        missing.append(f"{symptom}_{detail}")
                        logging.debug(
                            f"Missing detail found: {symptom}_{detail}")

        logging.info(
            f"Analysis complete. Missing details: {missing if missing else 'None'}")
        return missing if missing else None

    except Exception as e:
        logging.error(
            f"Error in identify_missing_symptoms: {str(e)}\n{traceback.format_exc()}")
        raise


def generate_recommendations(symptoms: List[str], medical_history: Dict) -> str:
    try:
        if not isinstance(symptoms, list) or not isinstance(medical_history, dict):
            logging.error("Invalid input types")
            raise TypeError(
                "symptoms must be a list and medical_history must be a dict")

        logging.info(f"Generating recommendations for symptoms: {symptoms}")
        logging.debug(f"Medical history: {medical_history}")

        prompt = f"""Given these symptoms: {', '.join(symptoms)} and medical history: {medical_history},
        provide 3-5 general recommendations. Follow these rules:
        1. Never diagnose conditions
        2. Suggest only OTC medications as examples
        3. Always recommend consulting a doctor
        4. Prioritize safety over specificity
        5. Include first aid measures if relevant
        
        Format as markdown bullets with emojis:"""

        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cautious medical assistant. Your responses must include:\n"
                        "- 'Consult a healthcare professional' as first point\n"
                        "- Clear disclaimer that this is not medical advice\n"
                        "- Only WHO/CDC-approved recommendations"
                    },
                    {"role": "user", "content": prompt}
                ],
                model=MODEL,
                temperature=0.3,
                max_tokens=400
            )

            logging.info("Successfully generated recommendations")
            response_text = response.choices[0].message.content
            return f"{response_text}\n\n⚠️ Remember: This is not medical advice. Always consult a doctor for proper evaluation."

        except Exception as e:
            logging.error(f"API call failed: {str(e)}")
            raise

    except Exception as e:
        logging.error(
            f"Error in generate_recommendations: {str(e)}\n{traceback.format_exc()}")
        raise


def extract_symptoms(user_input: str, llm_client) -> List[str]:
    try:
        if not isinstance(user_input, str):
            logging.error("user_input must be a string")
            raise TypeError("user_input must be a string")

        logging.info(f"Extracting symptoms from input: {user_input[:100]}...")

        try:
            response = llm_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Extract medical symptoms and return them as a comma-separated list."
                    },
                    {"role": "user",
                        "content": f"Extract medical symptoms from: {user_input}"}
                ],
                model=MODEL,
                temperature=0.3,
                max_tokens=400
            )

            symptoms_text = response.choices[0].message.content
            symptoms = [s.strip()
                        for s in symptoms_text.split(',') if s.strip()]

            logging.info(f"Successfully extracted symptoms: {symptoms}")
            return symptoms

        except Exception as e:
            logging.error(f"API call failed: {str(e)}")
            return []

    except Exception as e:
        logging.error(
            f"Error in extract_symptoms: {str(e)}\n{traceback.format_exc()}")
        return []

# Add basic test function


def run_tests():
    try:
        print("\n=== Starting Tests ===\n")

        # Test safety_check
        print("1. Testing safety_check:")
        test_response = "Patient reports severe chest pain and difficulty breathing."
        result = safety_check(test_response)
        print(f"Input: {test_response}")
        print(f"Output: {result}\n")

        # Test identify_missing_symptoms
        print("2. Testing identify_missing_symptoms:")
        test_symptoms = ["headache", "fever"]
        missing = identify_missing_symptoms(test_symptoms)
        print(f"Input symptoms: {test_symptoms}")
        print(f"Missing details: {missing}\n")

        # Test generate_recommendations
        print("3. Testing generate_recommendations:")
        test_history = {"allergies": ["penicillin"], "conditions": ["asthma"]}
        print(f"Input symptoms: {test_symptoms}")
        print(f"Medical history: {test_history}")
        recommendations = generate_recommendations(test_symptoms, test_history)
        print(f"Recommendations:\n{recommendations}\n")

        print("=== Tests Completed ===")

    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        raise


if __name__ == "__main__":
    run_tests()
