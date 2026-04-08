from flask import Flask, request, jsonify
import os

# ================== SAFE OPENAI SETUP ==================
try:
    from openai import OpenAI

    API_BASE_URL = os.getenv("API_BASE_URL", "local")
    MODEL_NAME = os.getenv("MODEL_NAME", "startup-simulator")
    HF_TOKEN = os.getenv("HF_TOKEN")

    if HF_TOKEN:
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=HF_TOKEN
        )
    else:
        client = None

except:
    client = None  # Prevent crash if OpenAI fails


app = Flask(__name__)

# ================== ROUTES ==================

@app.route("/")
def home():
    return "AI Startup Simulator Running"

@app.route("/start")
def start():
    print("START: Simulation started")
    return jsonify({"message": "Simulation started"})

@app.route("/on", methods=["POST"])
def on():
    print("START: Environment reset")
    return jsonify({"status": "ok", "message": "Environment reset"})

@app.route("/reset", methods=["POST"])
def reset():
    print("START: Simulation reset")
    return jsonify({"status": "ok", "message": "Reset done"})

@app.route("/action", methods=["POST"])
def action():
    print("STEP: User action received")
    data = request.json or {}
    return jsonify({"result": "Action received", "data": data})

@app.route("/ai")
def ai():
    print("STEP: AI response generated")

    if client:
        response = "AI working"
    else:
        response = "AI not connected but route working"

    return jsonify({"ai": response})

@app.route("/simulate")
def simulate():
    print("END: Simulation finished")
    return jsonify({"status": "Simulation working"})


# ================== OPENENV ENTRY ==================

def main():
    return app


# ================== RUN SERVER (HF ONLY) ==================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    print(f"Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port)
