from . import db

class User(db.Model):
    __tablename__ = "user"
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(100), nullable=False)
    playlists = db.relationship("Playlist", back_populates="user")
