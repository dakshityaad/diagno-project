from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()  # this loads variables from .env


# Import your agents
from agents.symptom_agent import SymptomAgent
from agents.report import ReportAgent
from agents.knowledge import KnowledgeAgent
from agents.coordinator import CoordinatorAgent

app = Flask(__name__)

# ===== Initialize Agents =====
symptom_agent = SymptomAgent()
report_agent = ReportAgent()
knowledge_agent = KnowledgeAgent()
coordinator = CoordinatorAgent([symptom_agent, report_agent, knowledge_agent])

# ===== API Key Check =====
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("❌ API Key not found! Set OPENROUTER_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY.")

# ===== Routes =====
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handle text chat requests"""
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "⚠️ Please enter a message."})

        # Pass message to coordinator
        reply = coordinator.handle_message(user_message)

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Internal error: {str(e)}"})


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file uploads (PDFs, reports, etc.)"""
    if "file" not in request.files:
        return jsonify({"reply": "⚠️ No file uploaded."})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"reply": "⚠️ File has no name."})

    # Pass file to coordinator (not directly to report_agent)
    reply = coordinator.handle_report(file)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
