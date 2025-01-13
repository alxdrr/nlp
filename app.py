from flask import Flask,request ,jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
cors = CORS(app, origins="*")
data = pd.read_csv("tracksdata.csv")
data['artists'] = data['artists'].str.lower()

@app.route("/api/users", methods=["POST"])
def search():
    query = request.json.get('query', '').lower()
    artists_list = set()

    for artists in data['artists']:
        if isinstance(artists, str):  # Pastikan artists adalah string
            for artist in artists.split(';'):  # Pisahkan artis berdasarkan ';'
                artist = artist.strip()  # Hilangkan spasi
                if query in artist:  # Cek apakah query ada dalam nama artis
                    artists_list.add(artist)  # Tambahkan ke set jika cocok

    print(artists_list)
    return jsonify({
        "artists": list(artists_list)  # Mengembalikan daftar artis dalam format JSON
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)