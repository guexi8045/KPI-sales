from flask import Blueprint, jsonify
from reports.r_besichtigung_abschlussquote import get_besichtigungs_abschlussquote

bp = Blueprint("besichtigung_abschlussquote", __name__, url_prefix="/api")

@bp.route("/besichtigung_abschlussquote", methods=["GET"])
def besichtigung_abschlussquote():
    return jsonify(get_besichtigungs_abschlussquote())
