from flask import Blueprint, jsonify
from reports.r_tage_entwicklung_standort import get_tage_entwicklung_standort
from backend.utils.auth import token_required


bp = Blueprint("tage_entwicklung_standort", __name__, url_prefix="/api")

@bp.route("/tage_entwicklung_standort", methods=["GET"])
@token_required
def tage_entwicklung_standort():
    return jsonify(get_tage_entwicklung_standort())
