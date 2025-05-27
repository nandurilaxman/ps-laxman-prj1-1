import os
import logging
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from app import app, db
from sqlalchemy import inspect # pyright: ignore[reportMissingImports]

host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
port = int(os.getenv("FLASK_RUN_PORT", "5000"))
debug_mode = os.getenv("FLASK_DEBUG") == "True"

if __name__ == "__main__":
    with app.app_context():
        print(f"Database URI from Flask config: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # ✅ Explicitly tell Flask where to look
        database_path = os.path.join(app.instance_path, "db.sqlite3")
        print(f"Database location (instance path): {database_path}")

        # ✅ Ensure tables exist before running the server
        inspector = inspect(db.engine)
        if not inspector.get_table_names():
            print("No tables detected, running migrations...")
            db.create_all()

        logging.info("Starting Flask app...")

    # ✅ Ensure `host` and `port` are available at runtime
    app.run(host=host, port=port, debug=debug_mode)