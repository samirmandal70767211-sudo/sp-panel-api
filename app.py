from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Demo credentials
API_USERNAME = os.getenv("API_USERNAME", "12345")
API_PASSWORD = os.getenv("API_PASSWORD", "1234")


@app.get("/")
def home():
    return jsonify({
        "success": True,
        "message": "SP PANEL V2 API is running"
    })


@app.get("/api/status")
def status():
    return jsonify({
        "success": True,
        "status": "online",
        "app": "SP PANEL V2 API"
    })


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}

    username = str(data.get("username", ""))
    password = str(data.get("password", ""))

    if username == API_USERNAME and password == API_PASSWORD:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "username": username
        }), 200

    return jsonify({
        "success": False,
        "message": "Invalid username or password"
    }), 401


@app.get("/api/hello")
def hello():
    return jsonify({
        "success": True,
        "message": "Hello from SP PANEL V2 API"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
