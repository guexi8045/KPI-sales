from flask import Blueprint, jsonify
from reports.r_kuendigungen_standort import get_kuendigungen_nach_standort
from backend.utils.auth import token_required


bp = Blueprint("kuendigungen_standort", __name__, url_prefix="/api")

@bp.route("/kuendigungen_standort", methods=["GET"])
@token_required
def kuendigungen_standort():
    return jsonify(get_kuendigungen_nach_standort())