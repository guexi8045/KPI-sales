from flask import Blueprint, jsonify
from reports.r_abschluesse_herkunft import get_abschluesse_herkunft
from backend.utils.auth import token_required

bp = Blueprint("abschluesse_herkunft", __name__, url_prefix="/api")

@bp.route("/abschluesse_herkunft", methods=["GET"])
@token_required
def abschluesse_herkunft():
    return jsonify(get_abschluesse_herkunft())
