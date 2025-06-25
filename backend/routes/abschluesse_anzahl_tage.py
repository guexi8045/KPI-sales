from flask import Blueprint, jsonify
from reports.r_abschluesse_anzahl_tage import get_abschluesse_anzahl_tage
from backend.utils.auth import token_required

bp = Blueprint("abschluesse_anzahl_tage", __name__, url_prefix="/api")

@bp.route("/abschluesse_anzahl_tage", methods=["GET"])
@token_required
def abschluesse_anzahl_tage():
    return jsonify(get_abschluesse_anzahl_tage())
