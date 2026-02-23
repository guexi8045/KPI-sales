from flask import Blueprint, jsonify, request
from reports.r_zeitbiseintritt import get_zeitbiseintritt
from backend.utils.auth import token_required

bp = Blueprint("zeitbiseintritt", __name__, url_prefix="/api")

@bp.route("/zeitbiseintritt", methods=["GET"])
@token_required
def zeitbiseintritt():
    month = request.args.get("month")
    if not month:
        return jsonify({"error": "month parameter required, e.g. 2025-12"}), 400

    return jsonify(get_zeitbiseintritt(month))
