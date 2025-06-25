from flask import Blueprint, jsonify
from reports.r_tage_abnahme_standort import get_abnahme_tage_standort
from backend.utils.auth import token_required


bp = Blueprint("tage_abnahme_standort", __name__, url_prefix="/api")

@bp.route("/tage_abnahme_standort", methods=["GET"])
@token_required
def tage_abnahme_standort():
    return jsonify(get_abnahme_tage_standort())
