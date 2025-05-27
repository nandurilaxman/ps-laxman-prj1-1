from sqlalchemy import inspect
from datetime import datetime
from app import db, app


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("tasks", lazy=True))


with app.app_context():
    inspector = inspect(db.engine)
    print("Existing tables before creation:", inspector.get_table_names())
    print("Creating tables manually...")
    db.metadata.tables["user"].extend_existing = True
    db.create_all()
    print("Existing tables after creation:", inspector.get_table_names())
