from flask import Blueprint, jsonify
from reports.r_abschlussquote_standort_rohdaten import get_abschlussquote_standort_rohdaten
from backend.utils.auth import token_required

bp = Blueprint("abschlussquote_bs_roh", __name__, url_prefix="/api")

@bp.route("/abschlussquote_standort_roh", methods=["GET"])
@token_required
def quote_bs_roh():
    return jsonify(get_abschlussquote_standort_rohdaten())
