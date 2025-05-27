from sqlalchemy import inspect  # ✅ Ensure 'inspect' is imported
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db, app  # ✅ Ensure 'app' and 'db' are correctly imported

class User(db.Model):
    __tablename__ = "user"  # ✅ Explicitly define table name to prevent conflicts
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Task(db.Model):
    __tablename__ = "task"  # ✅ Explicitly define table name to prevent conflicts
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("tasks", lazy=True))

# ✅ Fix: Use 'extend_existing=True' to prevent duplicate errors
with app.app_context():
    inspector = inspect(db.engine)
    print("Existing tables before creation:", inspector.get_table_names())

    print("Creating tables manually...")
    db.metadata.tables["user"].extend_existing = True
    db.create_all()

    print("Existing tables after creation:", inspector.get_table_names())
