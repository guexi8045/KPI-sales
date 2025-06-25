import jwt
import os
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token fehlt!'}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token abgelaufen!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Ungültiger Token!'}), 401

        return f(*args, **kwargs)
    return decorated
