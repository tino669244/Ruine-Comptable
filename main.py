from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
import os

# Import routes
from auth_routes import auth_bp
from clients_routes import clients_bp
from produits_routes import produits_bp
from stocks_routes import stocks_bp
from reservations_routes import reservations_bp
from ventes_routes import ventes_bp
from livraisons_routes import livraisons_bp
from dashboard_routes import dashboard_bp
from exports_routes import exports_bp

def create_app():
    app = Flask(__name__)

    # ------------------------
    # Configuration
    # ------------------------
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "supersecretkey")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "DATABASE_URL",
        "sqlite:///database.sqlite3"  # Default SQLite (local)
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT Config
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")

    # ------------------------
    # Init Extensions
    # ------------------------
    db.init_app(app)
    jwt = JWTManager(app)

    # ------------------------
    # Register Blueprints
    # ------------------------
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(produits_bp, url_prefix="/produits")
    app.register_blueprint(stocks_bp, url_prefix="/stocks")
    app.register_blueprint(reservations_bp, url_prefix="/reservations")
    app.register_blueprint(ventes_bp, url_prefix="/ventes")
    app.register_blueprint(livraisons_bp, url_prefix="/livraisons")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(exports_bp, url_prefix="/exports")

    # ------------------------
    # Create database tables
    # ------------------------
    with app.app_context():
        db.create_all()

    return app


# ------------------------
# Entry point (for Vercel/Gunicorn)
# ------------------------
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
