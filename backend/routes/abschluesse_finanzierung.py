from flask import Blueprint, jsonify
from reports.r_abschluesse_finanzierung import get_abschluesse_nach_finanzierung
from backend.utils.auth import token_required

bp = Blueprint("abschluesse_finanzierung", __name__, url_prefix="/api")

@bp.route("/abschluesse_finanzierung", methods=["GET"])
@token_required
def abschluesse_finanzierung():
    return jsonify(get_abschluesse_nach_finanzierung())
