from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .user import User
from .playlist import Playlist
from .playlist_track import PlaylistTrack
from .track import Track