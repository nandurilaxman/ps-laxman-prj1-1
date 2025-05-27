import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "db.sqlite3")

if os.path.exists(DB_PATH):
    print(f"✅ Database file found at {DB_PATH}")
else:
    print(f"🚨 Database file NOT found at {DB_PATH}")

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"  # ✅ Use absolute path as a formatted string
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-default-key")
