from flask import Blueprint, jsonify
from reports.r_tage_zunahme import get_zunahme_tage
from backend.utils.auth import token_required

bp = Blueprint("tage_zunahme", __name__, url_prefix="/api")

@bp.route("/tage_zunahme", methods=["GET"])
@token_required
def tage_zunahme():
    return jsonify(get_zunahme_tage())
