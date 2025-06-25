from flask import Blueprint, jsonify
from reports.r_besichtigungen_standort import get_besichtigungen_standort
from backend.utils.auth import token_required

bp = Blueprint("besichtigungen_standort", __name__, url_prefix="/api")

@bp.route("/besichtigungen_standort", methods=["GET"])
@token_required
def besichtigungen_standort():
    return jsonify(get_besichtigungen_standort())
