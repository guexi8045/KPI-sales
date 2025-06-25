from flask import Blueprint, jsonify
from reports.r_anfrage_kanal import get_anfragen_nach_kanal
from backend.utils.auth import token_required

bp = Blueprint("anfrage_kanal", __name__, url_prefix="/api")

@bp.route("/anfrage_kanal", methods=["GET"])
@token_required
def anfrage_kanal():
    return jsonify(get_anfragen_nach_kanal())
