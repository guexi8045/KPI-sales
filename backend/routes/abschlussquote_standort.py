from flask import Blueprint, jsonify
from reports.r_abschlussquote_standort import get_abschlussquote_standort

bp = Blueprint("abschlussquote_standort", __name__, url_prefix="/api")

@bp.route("/abschlussquote/standort", methods=["GET"])
def abschlussquote_standort():
    return jsonify(get_abschlussquote_standort())