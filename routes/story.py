from flask import Blueprint, request, jsonify
import openai
from config import Config

story_bp = Blueprint("story", __name__)

@story_bp.route('/get-song-story', methods=['POST'])
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
