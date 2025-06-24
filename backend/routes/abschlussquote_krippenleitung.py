from flask import Blueprint, jsonify
from reports.r_abschlussquote_krippenleitung import get_abschlussquote_krippenleitung

bp = Blueprint("abschlussquote_krippenleitung", __name__, url_prefix="/api")

@bp.route("/abschlussquote/krippenleitung", methods=["GET"])
def abschlussquote_krippenleitung():
    return jsonify(get_abschlussquote_krippenleitung())