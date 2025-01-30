from sqlalchemy.orm import relationship
from . import db

class Track(db.Model):
    __tablename__ = "track"
    track_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    playlists = relationship("PlaylistTrack", back_populates="track")