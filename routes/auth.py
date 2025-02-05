from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import db

auth_bp = Blueprint("auth", __name__)
email = None
@auth_bp.route("/create", methods=["POST"])
def create_user():
    data = request.json
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(email=data["email"], name=data["name"], date_of_birth=data["dob"], gender=data["gender"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

@auth_bp.route("/login", methods=["POST"])
@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Login successful!", "user": {"email": user.email, "name": user.name, "profile_image": user.profile_image}}), 200
    return jsonify({"error": "Invalid email or password"}), 401

@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    print("Session saat ini:", dict(session))  # Log seluruh session
    if email:
        return jsonify({"logged_in": True, "user_email": email}), 200
    return jsonify({"logged_in": False}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_email", None)  # Hapus session user_id
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route("/debug_session", methods=["GET"])
def debug_session():
    return jsonify(dict(session))
