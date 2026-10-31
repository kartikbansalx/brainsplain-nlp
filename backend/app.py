import os
import time

import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables before importing modules that read RAG settings.
load_dotenv()

from nlp_utils import analyze_input, readability
from rag import retrieve, build_prompt

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="",
    template_folder="templates",
)
CORS(app)

# Configure Gemini. The API key is read from the deployment environment.
api_key = os.environ.get("Gemini_API_KEY")
if api_key:
    genai.configure(api_key=api_key)


SYSTEM_PROMPTS = {
    "Age 5": (
        "You are an expert at explaining complex topics simply. When given a "
        "topic, explain it as if the user is 5 years old. Use simple words, "
        "fun analogies, and at least 2 relevant emojis. Keep it under 200 "
        "words. Never use jargon. Start with a one-sentence hook that makes "
        "the topic feel exciting."
    ),
    "Age 10": (
        "You are an expert at explaining complex topics simply. Explain the "
        "following topic as if the user is 10 years old. Use clear language, "
        "relatable analogies, and a few relevant emojis. Avoid overly "
        "technical jargon but introduce simple concepts clearly. Keep it "
        "under 250 words. Start with a hook."
    ),
    "Teen": (
        "You are an expert at explaining complex topics simply. Explain the "
        "following topic for a teenager. The explanation should be accurate, "
        "conversational, and completely free of obscure jargon. Use clear "
        "analogies to explain mechanisms. Keep it under 300 words. Start "
        "with an engaging intro."
    ),
}


@app.route("/")
def serve_frontend():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    # Deliberately does not load spaCy, Sentence Transformers, or ChromaDB.
    return jsonify({"status": "healthy"}), 200


@app.route("/api/explain", methods=["POST"])
def explain_topic():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic")
    level = data.get("level", "Age 5")

    if not isinstance(topic, str) or not topic.strip():
        return jsonify({"error": "Topic is required"}), 400
    topic = topic.strip()

    if level not in SYSTEM_PROMPTS:
        return jsonify({"error": "Invalid level selected"}), 400

    if not api_key:
        return jsonify({"error": "Gemini_API_KEY is not configured"}), 500

    started = time.perf_counter()

    try:
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=SYSTEM_PROMPTS[level],
        )

        stage_started = time.perf_counter()
        context = retrieve(topic)
        print(
            f"[TIMING] RAG retrieval: "
            f"{time.perf_counter() - stage_started:.2f}s"
        )

        stage_started = time.perf_counter()
        response = model.generate_content(build_prompt(topic, context))
        explanation = response.text
        print(
            f"[TIMING] Gemini generation: "
            f"{time.perf_counter() - stage_started:.2f}s"
        )

        stage_started = time.perf_counter()
        nlp_result = {
            **analyze_input(topic),
            "readability": readability(explanation, level),
        }
        print(
            f"[TIMING] NLP analysis: "
            f"{time.perf_counter() - stage_started:.2f}s"
        )

        result = {
            "explanation": explanation,
            "nlp": nlp_result,
            "rag": (
                {
                    "used": True,
                    "title": context["title"],
                    "url": context["url"],
                }
                if context
                else {"used": False}
            ),
        }

        print(
            f"[TIMING] Total /api/explain: "
            f"{time.perf_counter() - started:.2f}s"
        )
        return jsonify(result)

    except Exception as exc:
        print(
            f"Error in /api/explain after "
            f"{time.perf_counter() - started:.2f}s: "
            f"{type(exc).__name__}: {exc}"
        )
        return jsonify({"error": f"API Error: {str(exc)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Brainsplain backend on port {port}")
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host="0.0.0.0",
        port=port,
    )
