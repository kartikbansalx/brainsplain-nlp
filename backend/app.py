import os
import time
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from nlp_utils import analyze_input, readability

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='', template_folder='templates')
# Allow cross-origin requests
CORS(app)

# Configure Gemini
api_key = os.environ.get("Gemini_API_KEY")

if not api_key:
    # Handle missing API key gracefully
    pass
genai.configure(api_key=api_key)

# Define prompts based on age levels
SYSTEM_PROMPTS = {
    "Age 5": "You are an expert at explaining complex topics simply. When given a topic, explain it as if the user is 5 years old. Use simple words, fun analogies, and at least 2 relevant emojis. Keep it under 200 words. Never use jargon. Start with a one-sentence hook that makes the topic feel exciting.",
    "Age 10": "You are an expert at explaining complex topics simply. Explain the following topic as if the user is 10 years old. Use clear language, relatable analogies, and a few relevant emojis. Avoid overly technical jargon but introduce simple concepts clearly. Keep it under 250 words. Start with a hook.",
    "Teen": "You are an expert at explaining complex topics simply. Explain the following topic for a teenager. The explanation should be accurate, conversational, and completely free of obscure jargon. Use clear analogies to explain mechanisms. Keep it under 300 words. Start with an engaging intro."
}

@app.route('/')
def serve_frontend():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/explain', methods=['POST'])
def explain_topic():
    data = request.json
    topic = data.get('topic')
    level = data.get('level', 'Age 5')

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    if level not in SYSTEM_PROMPTS:
        return jsonify({"error": "Invalid level selected"}), 400

    system_instruction = SYSTEM_PROMPTS[level]

    try:
        # Initialize the model with the system prompt
        model = genai.GenerativeModel(
            model_name='gemini-flash-latest',
            system_instruction=system_instruction
        )
        
        response = model.generate_content(
            f"Please explain this: {topic}"
        )
        explanation = response.text
        return jsonify({
            "explanation": explanation,
            "nlp": {**analyze_input(topic), "readability": readability(explanation, level)}
        })

    except Exception as e:
        error_msg = str(e)
        print(f"Error calling Gemini API: {error_msg}")
        return jsonify({"error": f"API Error: {error_msg}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting ELI5 Backend Server on http://localhost:{port}")
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", host='0.0.0.0', port=port)
