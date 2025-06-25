from flask import Blueprint, jsonify
from reports.r_datenbereinigung_p1deals import get_datenbereinigung_ids
from backend.utils.auth import token_required

bp = Blueprint("datenbereinigung_p1deals", __name__, url_prefix="/api")

@bp.route("/datenbereinigung_p1deals", methods=["GET"])
@token_required
def datenbereinigung():
    return jsonify(get_datenbereinigung_ids())
