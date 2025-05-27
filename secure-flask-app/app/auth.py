import logging
from flask import request, jsonify
from flask_jwt_extended import create_access_token # pyright: ignore[reportMissingImports]
import bcrypt # pyright: ignore[reportMissingImports]
import re
from app import app, db
from app.models import User

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # ✅ Validate required fields
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Username, email, and password are required!"}), 400

    # ✅ Validate email format
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, data["email"]):
        return jsonify({"error": "Invalid email format!"}), 400

    # ✅ Check if user already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "Email already registered!"}), 409

    # ✅ Hash password securely
    hashed_password = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    # ✅ Store user in database
    new_user = User(
        username=data["username"],
        email=data["email"],
        password_hash=hashed_password,
    )  
    db.session.add(new_user)
    db.session.commit()

    # ✅ Generate JWT token for immediate authentication
    access_token = create_access_token(identity=new_user.id)

    return jsonify({"message": "User created successfully!", "access_token": access_token}), 201

# ✅ Ensure logs write to `security.log`
log_filename = "logs/security.log"

# ✅ Initialize logger
security_logger = logging.getLogger("security_logger")
security_logger.setLevel(logging.INFO)

# ✅ Create file handler explicitly
file_handler = logging.FileHandler(log_filename, mode="a")  # ✅ Use append mode
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# ✅ Attach handler only if it hasn’t been added already
if not security_logger.hasHandlers():
    security_logger.addHandler(file_handler)

# ✅ Prevent Flask’s default logger from interfering
security_logger.propagate = False

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        security_logger.warning("❌ Login attempt failed: Missing email or password")
        file_handler.flush()  # ✅ Force log to be written immediately
        return jsonify({"error": "Email and password are required!"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not bcrypt.checkpw(data["password"].encode("utf-8"), user.password_hash.encode("utf-8")):
        security_logger.warning(f"❌ Failed login attempt: {data['email']}")
        file_handler.flush()  # ✅ Force log to be written immediately
        return jsonify({"error": "Invalid email or password!"}), 401

    access_token = create_access_token(identity=user.id)
    security_logger.info(f"✅ Successful login: {data['email']}")
    file_handler.flush()  # ✅ Force log to be written immediately

    return jsonify({"message": "Login successful!", "access_token": access_token}), 200