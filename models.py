from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, DateTime, func
from sqlalchemy.orm import relationship

class user(db.Model):
    __tablename__ = "user"
    email = Column(String(50), primary_key=True)
    name = Column(String(50))
    date_of_birth = Column(Date)
    gender = Column(String(20))
    password = Column(String(20))
    profile_image = Column(String(20))
    playlists = relationship("playlist", back_populates="user")

class playlist(Base):
    __tablename__ = "playlist"
    playlist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(50), ForeignKey("user.email"))
    playlist_name = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("user", back_populates="playlists")
    tracks = relationship("playlist_track", back_populates="playlist")

class track(Base):
    __tablename__ = "track"
    track_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    duration = Column(Time)
    artist = Column(String(100))
    album = Column(String(100))
    genre = Column(String(50))

    playlists = relationship("playlist_track", back_populates="track")

class playlist_track(Base):
    __tablename__ = "playlist_track"
    playlist_id = Column(Integer, ForeignKey("playlist.playlist_id"), primary_key=True)
    track_id = Column(Integer, ForeignKey("track.track_id"), primary_key=True)

    playlist = relationship("playlist", back_populates="tracks")
    track = relationship("track", back_populates="playlists")
