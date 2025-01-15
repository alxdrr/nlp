from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
from rapidfuzz import process, fuzz
import openai
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
cors = CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:5173", "supports_credentials": True}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/sonata'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Konfigurasi OpenAI API Key
openai.api_key = "k-proj-r4AqCySYyfqbIjonEJplZPAoKHy4Mx7On2noG0V8LLNrCQpwzJChI0KYE1720dwySrRFd4_JODT3BlbkFJwmautHTXSy8o7fg7l7kw8VaUdojQmqEsUYJ8OPEg7Qhsa0dAekpILMwBavHrAQkVUqaJhvlDYA"

# Membaca data dari CSV
data = pd.read_csv("tracksdata.csv")
data['track_name'] = data['track_name']

# Fungsi normalisasi teks
def normalize_text(text):
    return text.strip().lower()

# Database model
class User(db.Model):
    __tablename__ = "user"
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(100), nullable=False)
    playlists = db.relationship("Playlist", back_populates="user")

class Playlist(db.Model):
    __tablename__ = "playlist"
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(50), db.ForeignKey("user.email"), nullable=False)
    playlist_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relasi balik ke User dan PlaylistTrack
    user = db.relationship("User", back_populates="playlists")
    tracks = db.relationship("PlaylistTrack", back_populates="playlist")

class Track(db.Model):
    __tablename__ = "track"
    track_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    playlists = db.relationship("PlaylistTrack", back_populates="track")

class PlaylistTrack(db.Model):
    __tablename__ = "playlist_track"
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.playlist_id"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("track.track_id"), primary_key=True)
    
    # Relasi balik ke Playlist dan Track
    playlist = db.relationship("Playlist", back_populates="tracks")
    track = db.relationship("Track", back_populates="playlists")

@app.route("/api/users/create", methods=["POST"])
def create_user():
    data = request.json
    print("Data diterima:", data) 
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    try:
        new_user = User(
            email=data["email"],
            name=data["name"],
            date_of_birth=data["dob"],
            gender=data["gender"],
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/users/login", methods=["POST"])
def login_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Validasi input
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        # Cari user berdasarkan email
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):  # Verifikasi password
            # Anda bisa menggunakan session atau token untuk autentikasi
            session["user_id"] = user.email  # Contoh menggunakan session
            return jsonify({"message": "Login successful!", "user": {
                "email": user.email,
                "name": user.name,
                "profile_image": user.profile_image
            }}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/playlists/create", methods=["POST"])
def create_playlist():
    data = request.json
    try:
        # Ambil email pengguna dari data yang dikirimkan
        user_email = data["user_email"]
        playlist_name = data["playlist_name"]

        # Validasi jika email pengguna ada di database
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Buat objek Playlist
        new_playlist = Playlist(
            user_email=user_email,
            playlist_name=playlist_name
        )

        # Tambahkan playlist ke database
        db.session.add(new_playlist)
        db.session.commit()

        return jsonify({"message": "Playlist created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/users", methods=["POST"])
def search():
    query = request.json.get('query', '').strip().lower()  # Normalisasi query
    track_list = set()

    # Normalisasi nama-nama track
    all_tracks = []
    for tracks in data['track_name']:
        if isinstance(tracks, str):  # Pastikan tracks adalah string
            all_tracks.extend(normalize_text(track) for track in tracks.split(';'))

    # Menggunakan RapidFuzz untuk fuzzy matching
    matches = process.extract(query, all_tracks, limit=10, scorer=fuzz.partial_token_sort_ratio)

    for match in matches:
        track_name, score, _ = match
        if score >= 80:  # Ambil hasil dengan skor di atas threshold
            track_list.add(track_name)
    print(list(track_list))
    return jsonify({
        "tracks": list(track_list)  # Mengembalikan daftar track dalam format JSON
    })

@app.route('/get-song-story', methods=['POST'])
def get_song_story():
    data = request.json
    title = data.get('title')
    artist = data.get('artist')

    # Prompt untuk OpenAI
    prompt = f"In English, create a story (if available, include the background of the song's creation, its inspiration, and emotional meaning) for the song: {title} - {artist}. Provide it in one paragraph with a maximum of 100 words or 600 characters."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        story = response['choices'][0]['message']['content']
        return jsonify({'story': story})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Membuat tabel berdasarkan model
    app.run(debug=True, port=8000)
