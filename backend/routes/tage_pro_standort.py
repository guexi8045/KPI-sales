from flask import Blueprint, jsonify
from reports.r_tage_pro_standort import get_tage_pro_standort

bp = Blueprint("tage_pro_standort", __name__, url_prefix="/api")

@bp.route("/tage-pro-standort", methods=["GET"])
def tage_pro_standort():
    return jsonify(get_tage_pro_standort())
