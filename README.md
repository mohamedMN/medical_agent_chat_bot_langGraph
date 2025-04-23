=== Medical History Setup ===

Exemples:

Enter any allergies (comma-separated): penicillin, aspirin
Enter existing medical conditions (comma-separated): hypertension
You: I've had chest pain that radiates to my left arm for the last hour

=== Medical Chat ===

Enter any allergies (comma-separated): penicillin, codeine
Enter existing medical conditions (comma-separated):  diabetes
I've had a sore throat and mild fever for two days, and my blood sugar has been higher than usual

---------------------------------------------------------------------------------------------------------

Architecture :
📁 src/
├── core/
│   ├── conversation.py          # Manages conversation state and flow. It might handle how user input is received, processed, and routed to different components (like LangGraph nodes).
│   ├── workflow.py              # Defines your LangGraph graph. Here you likely describe the various states (nodes) in your chatbot and how transitions between them occur (edges).
│   └── __init__.py              # Initializes core package
│
├── integrations/ # This is where your chatbot connects to external APIs.
│   ├── emergency_services.py    # A module to handle logic for reaching out to emergency APIs (e.g., finding the nearest hospital, calling for help, etc.). It could be using the requests library for these API calls.
│   └── __init__.py              # Integration-level initialization
│
├── knowledge_graph/
│   ├── medical_knowledge.py     # Contains symptom-condition mappings, diagnosis trees, or lookup tables for medical advice. Can be queried from conversation.py as part of the decision process.
│   └── __init__.py
│
├── utils/
│   ├── safety.py                # Ensures all user inputs and bot responses are safe and non-harmful. Could use OpenAI’s moderation endpoint or custom rules.
│   └── __init__.py
│
├── tests/                       # Unit or integration test files (currently empty)

main.py:

The main entry point. Likely responsible for:
        - Loading environment variables with python-dotenv
        - Initializing LangGraph
        - Running the chatbot loop (CLI or web)

.env:
    Stores your secrets like:
        - GROQ_API_KEY=your_groq_key
        - OPENAI_API_KEY=your_openai_key
        

requirements.txt:
        - Lists your dependencies 

medical_system.log:
        - a runtime log storing system messages, errors, or chat history for debugging or analysis.

.gitignore:
        - Ignores files/folders like __pycache__/, .env, and venv/.


------------------------------------------------------------------------------------------------------------------------
![alt text](img/image.png)