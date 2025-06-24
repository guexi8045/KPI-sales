from flask import Blueprint, jsonify
from reports.r_absagegrund import get_absagegruende

bp = Blueprint("absagegruende", __name__, url_prefix="/api")

@bp.route("/absagegruende", methods=["GET"])
def absagegruende():
    return jsonify(get_absagegruende())
