from flask import Blueprint, request, jsonify
from models.playlist import Playlist
from models.user import User
from models import db

playlist_bp = Blueprint("playlist", __name__)

@playlist_bp.route("/create", methods=["POST"])
def create_playlist():
    data = request.json
    user = User.query.filter_by(email=data["user_email"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_playlist = Playlist(user_email=data["user_email"], playlist_name=data["playlist_name"])
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify({"message": "Playlist created successfully!"}), 201
