from flask import Blueprint, jsonify
from reports.r_kuendigungsgruende import get_kuendigungen_nach_grund

bp = Blueprint("kuendigungsgruende", __name__, url_prefix="/api")

@bp.route("/kuendigungsgruende", methods=["GET"])
def kuendigungsgruende():
    return jsonify(get_kuendigungen_nach_grund())