from flask import Blueprint, jsonify
from reports.r_tage_abnahme import get_abnahme_tage
from backend.utils.auth import token_required


bp = Blueprint("tage_abnahme", __name__, url_prefix="/api")

@bp.route("/tage_abnahme", methods=["GET"])
@token_required
def tage_abnahme():
    return jsonify(get_abnahme_tage())
