from flask import Blueprint, jsonify
from reports.r_tage_zunahme_standort import get_zunahme_tage_standort
from backend.utils.auth import token_required

bp = Blueprint("tage_zunahme_standort", __name__, url_prefix="/api")

@bp.route("/tage_zunahme_standort", methods=["GET"])
@token_required
def tage_zunahme_standort():
    return jsonify(get_zunahme_tage_standort())
