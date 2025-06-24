from flask import Blueprint, jsonify
from reports.r_tage_entwicklung import get_tage_entwicklung

bp = Blueprint("tage_entwicklung", __name__, url_prefix="/api")

@bp.route("/tage-entwicklung", methods=["GET"])
def tage_entwicklung():
    return jsonify(get_tage_entwicklung())
