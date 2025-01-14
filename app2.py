from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
cors = CORS(app, origins="*")
openai.api_key = "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"

@app.route('/get-song-story', methods=['POST'])
def get_song_story():
    data = request.json
    title = data.get('title')
    artist = data.get('artist')

    # Prompt untuk OpenAI
    prompt = f"Dalam bahasa inggris, buatkan kisah (jika ada, masukkan latar belakang penulisan lagu, inspirasi, dan makna emosionalnya) dari lagu : {title} - {artist}. Buatkan langsung, 1 paragraf dengan maximal 100 kata atau 600 huruf."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5",  # Atau gunakan gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        story = response['choices'][0]['message']['content']
        return jsonify({'story': story})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)