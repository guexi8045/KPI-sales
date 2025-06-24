from flask import Blueprint, jsonify
from reports.r_tage_pro_standort_final import get_tage_gesamt_pro_standort

bp = Blueprint("tage_pro_standort_final", __name__, url_prefix="/api")

@bp.route("/tage_pro_standort_final", methods=["GET"])
def tage_pro_standort_final():
    return jsonify(get_tage_gesamt_pro_standort())
