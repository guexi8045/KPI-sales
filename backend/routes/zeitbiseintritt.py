from flask import Blueprint, jsonify
from reports.r_zeitbiseintritt import get_zeitbiseintritt
from backend.utils.auth import token_required


bp = Blueprint("zeitbiseintritt", __name__, url_prefix="/api")

@bp.route("/zeitbiseintritt", methods=["GET"])
@token_required
def zeitbiseintritt():
    return jsonify(get_zeitbiseintritt())
