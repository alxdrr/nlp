from flask import Flask, session
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import db
from config import Config
from routes import register_routes
from datetime import timedelta


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
db.init_app(app)
# Konfigurasi Redis untuk session
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_USE_SIGNER"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=5)
app.config["SESSION_SQLALCHEMY"] = db
app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions" 
app.config['SESSION_COOKIE_SECURE'] = False
# Konfigurasi CORS
Session(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

# Inisialisasi database dan session




# Registrasi semua blueprint
register_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
