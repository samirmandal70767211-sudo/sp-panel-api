from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Login credentials are read from Render Environment Variables.
# If they are not set, these demo values are used.
API_USERNAME = os.environ.get("API_USERNAME", "12345")
API_PASSWORD = os.environ.get("API_PASSWORD", "1234")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "SP PANEL V2 API is running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "online"
    })


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = str(data.get("username", ""))
    password = str(data.get("password", ""))

    if username == API_USERNAME and password == API_PASSWORD:
        return jsonify({
            "success": True,
            "message": "Login successful"
        }), 200

    return jsonify({
        "success": False,
        "message": "Invalid username or password"
    }), 401


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
