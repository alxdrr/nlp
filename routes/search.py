from flask import Blueprint, request, jsonify
from utils.fuzzy_match import fuzzy_search

search_bp = Blueprint("search", __name__)

@search_bp.route("", methods=["POST"])
def search():
    query = request.json.get('query', '').strip().lower()
    return jsonify({"tracks": fuzzy_search(query)})

