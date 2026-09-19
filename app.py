from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VALID_KEYS = {
    "SP-12345",
    "SP-67890",
    "SP-DEMO-001"
}


@app.get("/")
def home():
    return jsonify({
        "success": True,
        "message": "SP PANEL V2 API is running"
    })


@app.post("/verify")
def verify_key():
    data = request.get_json(silent=True) or {}
    api_key = data.get("key", "").strip()

    if not api_key:
        return jsonify({
            "success": False,
            "message": "API key is required"
        }), 400

    if api_key in VALID_KEYS:
        return jsonify({
            "success": True,
            "message": "API key is valid"
        })

    return jsonify({
        "success": False,
        "message": "Invalid API key"
    }), 401


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
