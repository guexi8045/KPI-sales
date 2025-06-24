from flask import Blueprint, jsonify
from reports.r_besichtigungen_standort import get_besichtigungen_standort

bp = Blueprint("besichtigungen_standort", __name__, url_prefix="/api")

@bp.route("/besichtigungen_standort", methods=["GET"])
def besichtigungen_standort():
    return jsonify(get_besichtigungen_standort())
