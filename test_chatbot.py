import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# System prompt for AgriBot
SYSTEM_PROMPT = "You are AgriBot, a knowledgeable and friendly assistant for farmers. You provide concise, accurate, and practical advice on agriculture, covering topics like crop management, pest control, soil health, and livestock care. You can also provide information on market trends and government schemes related to farming. Your goal is to help farmers make informed decisions and improve their farming practices."

def get_chatbot_response(messages):
    """Sends a request to the OpenRouter API and gets a response."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in .env file.")
        return None

    try:
        payload = {
            "model": "meta-llama/llama-3.1-8b-instruct",
            "messages": messages
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",  # Example Referer
            "X-Title": "Farmer Pocket"  # Example Title
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )

        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        reply = response.json()["choices"][0]["message"]["content"]
        return reply

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    print("🤖 AgriBot is ready. Type 'quit' to exit.")
    # Initialize conversation history with the system prompt
    conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("👨‍🌾 You: ")
        if user_input.lower() == 'quit':
            print("🤖 Goodbye!")
            break

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})

        # Get chatbot response
        assistant_response = get_chatbot_response(conversation_history)

        if assistant_response:
            print(f"🤖 AgriBot: {assistant_response}")
            # Add assistant response to history
            conversation_history.append({"role": "assistant", "content": assistant_response})
        else:
            # If the API call fails, remove the last user message to allow a retry
            conversation_history.pop()