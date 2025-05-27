from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # pyright: ignore[reportMissingImports]
from flask_jwt_extended import JWTManager  # pyright: ignore[reportMissingImports]
from flask_migrate import Migrate  # pyright: ignore[reportMissingImports]
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

from app import routes, auth  # Register blueprints after initialization
app.register_blueprint(routes.main)
app.register_blueprint(auth.auth)
