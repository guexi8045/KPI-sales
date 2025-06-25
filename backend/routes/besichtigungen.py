from flask import Blueprint, jsonify
from reports.r_besichtigungen import get_besichtigungen_pro_monat
from backend.utils.auth import token_required

bp = Blueprint("besichtigungen", __name__, url_prefix="/api")

@bp.route("/besichtigungen", methods=["GET"])
@token_required
def besichtigungen():
    return jsonify(get_besichtigungen_pro_monat())
