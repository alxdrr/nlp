from models import db

def init_db(app):
    """Inisialisasi database dengan aplikasi Flask."""
    with app.app_context():
        db.create_all()