from flask import Blueprint, request, jsonify
from models.playlist import Playlist
from models.user import User
from models import db

# Inisialisasi Blueprint dengan URL prefix
playlist_bp = Blueprint("playlist", __name__, url_prefix="/api/playlist")

@playlist_bp.route("/create", methods=["POST"])
def create_playlist():
    """Endpoint untuk membuat playlist baru bagi user yang sedang login."""
    # Ambil email pengguna dari session
    data = request.json
    user_email = data.get("user")

    if not user_email:
        return jsonify({"error": "User not logged in"}), 401

    playlist_name = data.get("playlist_name")

    if not playlist_name:
        return jsonify({"error": "Playlist name is required"}), 400

    try:
        # Pastikan user valid
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Buat playlist baru
        new_playlist = Playlist(user_email=user_email, playlist_name=playlist_name)
        db.session.add(new_playlist)
        db.session.commit()

        return jsonify({"message": "Playlist created successfully!", "name": playlist_name}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@playlist_bp.route("/get", methods=["POST"])
def get_user_playlists():
    """Endpoint untuk mendapatkan semua playlist milik user yang sedang login."""
    # Ambil email pengguna dari session
    data = request.json
    user_email = data.get("user")
    print("nih :", user_email)
    if not user_email:
        return jsonify({"error": "User not logged in"}), 401

    try:
        # Ambil playlist berdasarkan email pengguna
        playlists = Playlist.query.filter_by(user_email=user_email).all()

        # Konversi ke format JSON
        playlist_data = [
            {
                "playlist_id": p.playlist_id,
                "playlist_name": p.playlist_name,
                "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": p.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for p in playlists
        ]

        return jsonify({"playlists": playlist_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@playlist_bp.route("/<int:playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):

    """Endpoint untuk mendapatkan playlist berdasarkan ID."""
    try:
        # Mencari playlist berdasarkan ID
        playlist = Playlist.query.get_or_404(playlist_id)

        # Mengonversi data playlist ke format JSON
        playlist_data = {
            "playlist_id": playlist.playlist_id,
            "playlist_name": playlist.playlist_name,
            "created_at": playlist.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": playlist.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        return jsonify(playlist_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@playlist_bp.route("/delete/<int:playlist_id>", methods=["DELETE"])
def delete_playlist(playlist_id):
    """Endpoint untuk menghapus playlist berdasarkan ID."""
    try:
        # Mencari playlist berdasarkan ID
        playlist = Playlist.query.get_or_404(playlist_id)
        db.session.delete(playlist)
        db.session.commit()

        return jsonify({"message": "Playlist deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500