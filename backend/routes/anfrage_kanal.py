from flask import Blueprint, jsonify
from reports.r_anfrage_kanal import get_anfragen_nach_kanal

bp = Blueprint("anfrage_kanal", __name__, url_prefix="/api")

@bp.route("/anfrage_kanal", methods=["GET"])
def anfrage_kanal():
    return jsonify(get_anfragen_nach_kanal())
