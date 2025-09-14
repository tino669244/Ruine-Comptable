import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Init DB
db = SQLAlchemy()

# Import routes
from routes.auth_routes import auth_bp
from routes.clients_routes import clients_bp
from routes.produits_routes import produits_bp
from routes.stocks_routes import stocks_bp
from routes.reservations_routes import reservations_bp
from routes.ventes_routes import ventes_bp
from routes.livraisons_routes import livraisons_bp
from routes.dashboard_routes import dashboard_bp
from routes.export_routes import export_bp
from routes.factures_routes import factures_bp
from routes.commandes_routes import commandes_bp  # raha efa nataonao

def create_app():
    # Mampiasa /tmp satria read-only ny FS an’i Vercel
    app = Flask(__name__, instance_path="/tmp")

    # Config DB
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join("/tmp", "app.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.getenv("SECRET_KEY", "mysecret")

    # Init DB
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(produits_bp, url_prefix="/produits")
    app.register_blueprint(stocks_bp, url_prefix="/stocks")
    app.register_blueprint(reservations_bp, url_prefix="/reservations")
    app.register_blueprint(ventes_bp, url_prefix="/ventes")
    app.register_blueprint(livraisons_bp, url_prefix="/livraisons")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(export_bp, url_prefix="/exports")
    app.register_blueprint(factures_bp, url_prefix="/factures")
    app.register_blueprint(commandes_bp, url_prefix="/commandes")

    # Root route
    @app.route("/")
    def home():
        return "✅ Flask Gestion Commerciale sur Vercel fonctionne bien !"

    return app

# Vercel mitady app
app = create_app()
