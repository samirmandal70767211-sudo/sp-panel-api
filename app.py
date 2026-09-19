from flask import Flask, request, jsonify
from datetime import date, datetime

app = Flask(__name__)

# =========================================================
# USERS
# username: {
#     "key": API key,
#     "expiry": YYYY-MM-DD,
#     "active": True/False
# }
# =========================================================

USERS = {
    "samir": {
        "key": "SP-AB12-CD34",
        "expiry": "2026-12-31",
        "active": True
    },

    "demo": {
        "key": "SP-DEMO-001",
        "expiry": "2026-10-31",
        "active": True
    }
}


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return jsonify({
        "success": True,
        "message": "SP PANEL V2 API is running"
    })


# =========================================================
# STATUS
# =========================================================

@app.get("/api/status")
def status():
    return jsonify({
        "success": True,
        "status": "online",
        "app": "SP PANEL V2 API"
    })


# =========================================================
# LOGIN
# =========================================================

@app.post("/api/login")
def login():

    data = request.get_json(silent=True) or {}

    username = str(
        data.get("username", "")
    ).strip()

    api_key = str(
        data.get("key", "")
    ).strip()

    if not username or not api_key:
        return jsonify({
            "success": False,
            "message": "Username and API key are required"
        }), 400

    # Check username
    user = USERS.get(username)

    if user is None:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 401

    # Check Active / Inactive
    if not user["active"]:
        return jsonify({
            "success": False,
            "message": "Account is inactive"
        }), 403

    # Check API key
    if api_key != user["key"]:
        return jsonify({
            "success": False,
            "message": "Invalid API key"
        }), 401

    # Check expiry
    try:
        expiry_date = datetime.strptime(
            user["expiry"],
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Invalid expiry date on server"
        }), 500

    today = date.today()

    if today > expiry_date:
        return jsonify({
            "success": False,
            "message": "API key has expired",
            "expiry": user["expiry"]
        }), 403

    # Everything is valid
    return jsonify({
        "success": True,
        "message": "Login successful",
        "username": username,
        "active": True,
        "expiry": user["expiry"]
    }), 200


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    import os

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
