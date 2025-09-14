import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Apetrao instance_path amin'ny /tmp
    app = Flask(__name__, instance_path="/tmp")

    # Config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join("/tmp", "app.db"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.route("/")
    def home():
        return "Hello from Flask with SQLAlchemy on Vercel!"

    return app

# Vercel mitady an'io
app = create_app()
