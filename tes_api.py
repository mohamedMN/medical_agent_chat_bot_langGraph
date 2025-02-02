from anthropic import Anthropic
from dotenv import load_dotenv
import os
import sys


def load_api_key() -> str:
    """
    Load the Anthropic API key from the .env file.
    
    Returns:
        str: The API key if found, empty string otherwise.
        
    This function handles the environment variable loading process
    and provides informative feedback if the key isn't found.
    """
    # Load the environment variables from .env file
    load_dotenv()

    # Try to get the API key from environment variables
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        print("\n❌ Environment Setup Error:")
        print("---------------------------")
        print("API key not found in .env file.")
        print("\nPlease ensure:")
        print("1. You have created a .env file in the project directory")
        print("2. The file contains: ANTHROPIC_API_KEY=your-api-key-here")
        print("3. You've replaced 'your-api-key-here' with your actual API key")
        return ""

    return api_key


def test_api_key(api_key: str) -> bool:
    """
    Test if an Anthropic API key is valid and active.
    
    Args:
        api_key: The API key to test
        
    Returns:
        bool: True if the key is valid and active, False otherwise
        
    This function attempts to make a minimal API call to verify
    the key's functionality and provides detailed status information.
    """
    try:
        # Initialize the client with the provided key
        client = Anthropic(api_key=api_key)

        # Attempt a minimal API call
        print("Testing API key...")
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": "Respond with 'active' if you can read this."
            }]
        )

        # Check if we got a valid response
        if response.content:
            print("\n✅ API Key Status:")
            print("------------------")
            print("Status: Active")
            print("Access: Confirmed")
            print("API Response: Successful")
            print("\nYour API key is valid and working correctly!")
            return True

    except Exception as e:
        print("\n❌ API Key Status:")
        print("------------------")
        print(f"Status: Invalid or Inactive")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        print("\nPossible issues:")
        print("1. Key might be expired")
        print("2. Key might be incorrectly copied")
        print("3. Account might have billing or quota issues")
        print("4. Network connectivity problems")
        return False


def main():
    """
    Main function that orchestrates the API key testing process.
    
    This function handles the overall flow of loading and testing
    the API key while providing clear feedback at each step.
    """
    # Load the API key from .env
    api_key = load_api_key()

    if not api_key:
        return

    # Test the loaded key
    test_api_key(api_key)


if __name__ == "__main__":
    main()
