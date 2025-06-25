from flask import Blueprint, jsonify
from reports.r_abschlussquote_krippenleitung_rohdaten import get_abschlussquote_krippenleitung_rohdaten
from backend.utils.auth import token_required

bp = Blueprint("abschlussquote_kl_roh", __name__, url_prefix="/api")

@bp.route("/abschlussquote_krippenleitung_roh", methods=["GET"])
@token_required
def quote_kl_roh():
    return jsonify(get_abschlussquote_krippenleitung_rohdaten())
