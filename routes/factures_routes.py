from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, Facture, Commande
from datetime import datetime

factures_bp = Blueprint('factures', __name__)

@factures_bp.route("/factures")
def list_factures():
    factures = Facture.query.all()
    return render_template("factures.html", factures=factures)

@factures_bp.route("/factures/<int:id>")
def detail_facture(id):
    facture = Facture.query.get_or_404(id)
    return render_template("facture_detail.html", facture=facture)

@factures_bp.route("/factures/generer/<int:commande_id>")
def generer_facture(commande_id):
    commande = Commande.query.get_or_404(commande_id)
    total_ht = sum(l.quantite * l.prix_unitaire for l in commande.lignes)
    total_ttc = total_ht * 1.2

    facture = Facture(
        ref=f"FAC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        commande_id=commande.id,
        total_ht=total_ht,
        total_ttc=total_ttc
    )
    db.session.add(facture)
    db.session.commit()
    flash("Facture générée avec succès", "success")
    return redirect(url_for("factures.list_factures"))
