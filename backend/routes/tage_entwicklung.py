from flask import Blueprint, jsonify
from reports.r_tage_entwicklung import get_tage_total
from backend.utils.auth import token_required


bp = Blueprint("tage_entwicklung", __name__, url_prefix="/api")

@bp.route("/tage_entwicklung", methods=["GET"])
@token_required
def tage_entwicklung():
    return jsonify(get_tage_total())
