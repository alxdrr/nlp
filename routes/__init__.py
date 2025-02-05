from flask import Blueprint
from .auth import auth_bp
from .playlist import playlist_bp
from .search import search_bp
from .story import story_bp
from .artist import artist_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/users")
    app.register_blueprint(playlist_bp, url_prefix="/api/playlist")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(story_bp, url_prefix="/api")
    app.register_blueprint(artist_bp, url_prefix="/api/artist")