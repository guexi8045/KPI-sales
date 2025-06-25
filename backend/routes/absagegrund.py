from flask import Blueprint, jsonify
from reports.r_absagegrund import get_absagegruende
from backend.utils.auth import token_required


bp = Blueprint("absagegruende", __name__, url_prefix="/api")

@bp.route("/absagegruende", methods=["GET"])
@token_required
def absagegruende():
    return jsonify(get_absagegruende())
