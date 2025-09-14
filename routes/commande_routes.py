from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Commande, CommandeLigne, Produit, Client
from datetime import datetime

commandes_bp = Blueprint('commandes', __name__)

@commandes_bp.route("/commandes")
def list_commandes():
    commandes = Commande.query.all()
    return render_template("commandes.html", commandes=commandes)

@commandes_bp.route("/commandes/add", methods=["GET", "POST"])
def add_commande():
    clients = Client.query.all()
    produits = Produit.query.all()
    if request.method == "POST":
        client_id = request.form["client_id"]
        ref = f"CMD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        commande = Commande(ref=ref, client_id=client_id, statut="En attente")
        db.session.add(commande)
        db.session.commit()

        for produit in produits:
            qty = int(request.form.get(f"quantite_{produit.id}", 0))
            if qty > 0:
                ligne = CommandeLigne(
                    commande_id=commande.id,
                    produit_id=produit.id,
                    quantite=qty,
                    prix_unitaire=produit.prix
                )
                db.session.add(ligne)
        db.session.commit()
        flash("Commande créée avec succès", "success")
        return redirect(url_for("commandes.list_commandes"))

    return render_template("commande_form.html", clients=clients, produits=produits)

@commandes_bp.route("/commandes/<int:id>")
def detail_commande(id):
    commande = Commande.query.get_or_404(id)
    return render_template("commande_detail.html", commande=commande)
