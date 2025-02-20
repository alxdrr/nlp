from flask import Blueprint, request, jsonify
import openai
from config import Config

artist_bp = Blueprint("artist", __name__)

@artist_bp.route('/get-about-artist', methods=['POST'])
def get_song_story():
    data = request.json
    artist = data.get('artist')

    # Prompt untuk OpenAI
    prompt = f"In English, create a story about artist named {artist}. Provide it in several sentences with a maximum of 25 words or 125 characters."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        artist = response['choices'][0]['message']['content']
        return jsonify({'artist': artist})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500