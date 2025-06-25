from flask import Blueprint, jsonify
from reports.r_besichtigungsquote import get_besichtigungsquote
from backend.utils.auth import token_required

bp = Blueprint("besichtigungsquote", __name__, url_prefix="/api")

@bp.route("/besichtigungsquote", methods=["GET"])
@token_required
def besichtigungsquote():
    return jsonify(get_besichtigungsquote())
