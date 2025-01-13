from flask import Flask,request ,jsonify
from flask_cors import CORS
import pandas as pd
from rapidfuzz import process, fuzz

app = Flask(__name__)
cors = CORS(app, origins="*")
data = pd.read_csv("tracksdata.csv")
data['track_name'] = data['track_name']

@app.route("/api/users", methods=["POST"])
def search():
    query = request.json.get('query', '')
    track_list = set()

    all_tracks = []
    for tracks in data['track_name']:
        if isinstance(tracks, str):  # Pastikan tracks adalah string
            all_tracks.extend(track.strip() for track in tracks.split(';'))

    # Menggunakan RapidFuzz untuk melakukan fuzzy matching
    matches = process.extract(query, all_tracks, limit=10, scorer=fuzz.partial_token_sort_ratio)  # Mencari hingga 10 hasil teratas

    for match in matches:
        track_name, score, _ = match
        if score >= 50:  # Ambil hasil dengan skor di atas threshold (misalnya 70)
            track_list.add(track_name)

    print(track_list)
    return jsonify({
        "tracks": list(track_list)  # Mengembalikan daftar artis dalam format JSON
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)