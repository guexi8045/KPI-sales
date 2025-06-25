from flask import Blueprint, jsonify
from reports.r_abschluesse_standort import get_abschluesse_standort
from backend.utils.auth import token_required

bp = Blueprint("abschluesse_standort", __name__, url_prefix="/api")

@bp.route("/abschluesse_standort", methods=["GET"])
@token_required
def abschluesse_standort():
    return jsonify(get_abschluesse_standort())
