from flask import Blueprint, jsonify
from reports.r_abschluesse_alter import get_abschluesse_nach_alter
from backend.utils.auth import token_required

bp = Blueprint("abschluesse_alter", __name__, url_prefix="/api")

@bp.route("/abschluesse_alter", methods=["GET"])
@token_required
def abschluesse_alter():
    return jsonify(get_abschluesse_nach_alter())
