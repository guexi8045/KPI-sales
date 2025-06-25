from flask import Blueprint, request, jsonify
import jwt
import datetime
import os
from backend.utils.auth import SECRET_KEY

bp = Blueprint("login", __name__, url_prefix="/api")

USERNAME = os.getenv("LOGIN_USER")
PASSWORD = os.getenv("LOGIN_PASS")

@bp.route("/login", methods=["POST"])
def login():
    auth = request.get_json()
    username = auth.get("username")
    password = auth.get("password")

    if username != USERNAME or password != PASSWORD:
        return jsonify({"message": "Ungültige Anmeldedaten!"}), 401

    token = jwt.encode({
        "user": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})
