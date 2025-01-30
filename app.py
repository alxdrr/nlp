from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})

# Registrasi semua blueprint
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
