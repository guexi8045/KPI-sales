from flask import Blueprint, jsonify
from reports.r_datenbereinigung_p1mutationen import get_datenbereinigung_mutationen_ids
from backend.utils.auth import token_required

bp = Blueprint("datenbereinigung_p1mutationen", __name__, url_prefix="/api")

@bp.route("/datenbereinigung_p1mutationen", methods=["GET"])
@token_required
def datenbereinigung_mutationen():
    return jsonify(get_datenbereinigung_mutationen_ids())
