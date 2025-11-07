import os
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
import google.generativeai as genai

chatbot_bp = Blueprint("chatbot", __name__)

# Configure Gemini once at the top
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the model globally (for efficiency)
model = genai.GenerativeModel("gemini-2.0-flash")

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
def ask():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAgriBot:"

        response = model.generate_content(full_prompt)

        reply = response.text.strip() if response.text else "Sorry, I couldn't generate a response."

        return jsonify({"reply": reply})
    except Exception as e:
        print(f"❌ Error generating response from Gemini: {e}")
        return jsonify({"error": "Failed to get a response from the chatbot. Please try again later."}), 500
