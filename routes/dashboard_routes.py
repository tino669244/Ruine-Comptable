from flask import Blueprint, render_template
from models import db, Client, Produit, Stock, Vente, Reservation, Livraison
from auth_routes import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def dashboard():
    """Page principale du dashboard avec quelques stats"""
    nb_clients = Client.query.count()
    nb_produits = Produit.query.count()
    nb_stocks = Stock.query.count()
    nb_ventes = Vente.query.count()
    nb_reservations = Reservation.query.count()
    nb_livraisons = Livraison.query.count()

    stats = {
        "clients": nb_clients,
        "produits": nb_produits,
        "stocks": nb_stocks,
        "ventes": nb_ventes,
        "reservations": nb_reservations,
        "livraisons": nb_livraisons,
    }

    return render_template("dashboard.html", stats=stats)
