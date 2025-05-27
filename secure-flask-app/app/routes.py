from flask import jsonify
from app import app
from flask_cors import CORS

CORS(app)  # Allow external API calls


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Secure Flask App"}), 200
