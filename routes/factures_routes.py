from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Client, Commande, Facture
from datetime import datetime

facture_bp = Blueprint("facture", __name__, url_prefix="/factures")

# -------------------------
# Liste des factures
# -------------------------
@facture_bp.route("/")
def liste_factures():
    factures = Facture.query.all()
    return render_template("factures.html", factures=factures)


# -------------------------
# Générer une facture depuis une commande
# -------------------------
@facture_bp.route("/generer/<int:commande_id>", methods=["GET", "POST"])
def generer_facture(commande_id):
    commande = Commande.query.get_or_404(commande_id)

    if request.method == "POST":
        # Générer numéro unique
        numero = f"FAC-{datetime.now().year}-{commande.id:04d}"
        montant_total = commande.montant_total()
        mode_paiement = request.form.get("mode_paiement")
        etat_paiement = request.form.get("etat_paiement", "Non Payée")

        # Créer facture
        facture = Facture(
            numero=numero,
            client_id=commande.client_id,
            commande_id=commande.id,
            montant_total=montant_total,
            mode_paiement=mode_paiement,
            etat_paiement=etat_paiement,
        )

        db.session.add(facture)
        db.session.commit()

        flash("Facture générée avec succès ✅", "success")
        return redirect(url_for("facture.detail_facture", facture_id=facture.id))

    return render_template("generer_facture.html", commande=commande)


# -------------------------
# Détail facture
# -------------------------
@facture_bp.route("/<int:facture_id>")
def detail_facture(facture_id):
    facture = Facture.query.get_or_404(facture_id)
    return render_template("facture.html", facture=facture)


# -------------------------
# Marquer comme payée
# -------------------------
@facture_bp.route("/payer/<int:facture_id>")
def payer_facture(facture_id):
    facture = Facture.query.get_or_404(facture_id)
    facture.etat_paiement = "Payée"
    db.session.commit()

    flash("Facture marquée comme payée 💰", "success")
    return redirect(url_for("facture.detail_facture", facture_id=facture.id))


# -------------------------
# Supprimer facture
# -------------------------
@facture_bp.route("/supprimer/<int:facture_id>")
def supprimer_facture(facture_id):
    facture = Facture.query.get_or_404(facture_id)
    db.session.delete(facture)
    db.session.commit()

    flash("Facture supprimée 🗑️", "info")
    return redirect(url_for("facture.liste_factures"))
