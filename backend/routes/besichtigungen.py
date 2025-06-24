from flask import Blueprint, jsonify
from reports.r_besichtigungen import get_besichtigungen_pro_monat

bp = Blueprint("besichtigungen", __name__, url_prefix="/api")

@bp.route("/besichtigungen", methods=["GET"])
def besichtigungen():
    return jsonify(get_besichtigungen_pro_monat())
