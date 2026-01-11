import os
import requests
import json
from flask import Blueprint, render_template, request, jsonify
from dotenv import load_dotenv
from flask_login import login_required

chatbot_bp = Blueprint("chatbot", __name__)

SYSTEM_PROMPT = """
You are AgriBot, a specialized AI assistant for livestock farming. Your purpose is to provide accurate, practical, and easy-to-understand advice on raising healthy and productive livestock, including cattle, goats, and poultry (broilers).

Your responses should be:
- Focused on farming topics.
- Clear, concise, and actionable.
- Empathetic to the challenges farmers face.
- If a question is outside your scope of farming, politely state that you are specialized in agriculture and cannot answer.
- You must not engage in casual conversation.
"""

@chatbot_bp.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html")

@chatbot_bp.route("/ask", methods=["POST"])
@login_required
def get_chatbot_response(user_message):
    """
    Determines whether to use the OpenRouter API or a fallback and returns a response.
    """
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

    if openrouter_api_key:
        try:
            payload = {
                "model": "meta-llama/llama-3.1-8b-instruct",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            }
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": request.host_url,
                    "X-Title": "Farmer Pocket"
                },
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"]["content"]
            else:
                return "Error: Invalid response from API."
        except requests.exceptions.RequestException as e:
            return f"Error connecting to the chatbot service: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    else:
        return "Chatbot is not configured. Missing OPENROUTER_API_KEY."

@chatbot_bp.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return jsonify({"error": "OpenRouter API key not configured."}), 503

    try:
        payload = {
            "model": "meta-llama/llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ Meta Llama error: {e}")
        return jsonify({"error": "Failed to get a response from Meta Llama."}), 500