from flask import Blueprint, jsonify
from reports.r_kuendigungsgruende import get_kuendigungen_nach_grund
from backend.utils.auth import token_required


bp = Blueprint("kuendigungsgruende", __name__, url_prefix="/api")

@bp.route("/kuendigungsgruende", methods=["GET"])
@token_required
def kuendigungsgruende():
    return jsonify(get_kuendigungen_nach_grund())