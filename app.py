from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from rapidfuzz import process, fuzz
import openai

app = Flask(__name__)
cors = CORS(app, origins="*")

# Konfigurasi OpenAI API Key
openai.api_key = "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"

# Membaca data dari CSV
data = pd.read_csv("tracksdata.csv")
data['track_name'] = data['track_name']

# Fungsi normalisasi teks
def normalize_text(text):
    return text.strip().lower()

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
    app.run(debug=True, port=8000)
