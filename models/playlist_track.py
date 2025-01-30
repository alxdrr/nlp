from sqlalchemy.orm import relationship
from . import db  # Pastikan impor ke database yang benar

class PlaylistTrack(db.Model):
    __tablename__ = "playlist_track"
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.playlist_id"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("track.track_id"), primary_key=True)

    # Relasi balik ke Playlist dan Track, gunakan string agar bisa dihubungkan setelah kedua model dibuat
    playlist = relationship("Playlist", back_populates="tracks")
    track = relationship("Track", back_populates="playlists")
