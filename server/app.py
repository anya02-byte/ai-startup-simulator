from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Startup Simulator Running"

@app.route('/on', methods=['POST'])
def on():
    return jsonify({"status": "ok", "message": "Environment reset"})

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({"status": "ok", "message": "Reset done"})

@app.route('/action', methods=['POST'])
def action():
    data = request.json or {}
    return jsonify({"status": "ok", "data": data})

@app.route('/ai')
def ai():
    return jsonify({
        "status": "ok",
        "decision": "Build product first"
    })

@app.route('/simulate')
def simulate():
    return jsonify({
        "status": "ok",
        "result": "Simulation complete"
    })

# ✅ IMPORTANT: DO NOT run app here
def main():
    return app
