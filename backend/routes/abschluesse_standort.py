from flask import Blueprint, jsonify
from reports.r_abschluesse_standort import get_abschluesse_standort

bp = Blueprint("abschluesse_standort", __name__, url_prefix="/api")

@bp.route("/abschluesse_standort", methods=["GET"])
def abschluesse_standort():
    return jsonify(get_abschluesse_standort())
