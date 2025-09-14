from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Vente
from auth_routes import login_required

ventes_bp = Blueprint("ventes", __name__)

# --------------------------
# Web routes (HTML views)
# --------------------------

@ventes_bp.route("/", methods=["GET"])
@login_required
def list_ventes():
    """Afficher la liste des ventes"""
    ventes = Vente.query.all()
    return render_template("ventes.html", ventes=ventes)


@ventes_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_vente():
    """Ajouter une vente"""
    if request.method == "POST":
        client_id = request.form.get("client_id")
        produit_id = request.form.get("produit_id")
        quantity = request.form.get("quantity")
        total_price = request.form.get("total_price")

        try:
            quantity = int(quantity)
            total_price = float(total_price)
        except (TypeError, ValueError):
            flash("Quantité ou prix invalide.", "error")
            return redirect(url_for("ventes.add_vente"))

        new_vente = Vente(
            client_id=client_id,
            produit_id=produit_id,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(new_vente)
        db.session.commit()

        flash("Vente ajoutée avec succès.", "success")
        return redirect(url_for("ventes.list_ventes"))

    return render_template("ventes.html", add_mode=True)


@ventes_bp.route("/edit/<int:vente_id>", methods=["GET", "POST"])
@login_required
def edit_vente(vente_id):
    """Modifier une vente"""
    vente = Vente.query.get_or_404(vente_id)

    if request.method == "POST":
        try:
            vente.quantity = int(request.form.get("quantity"))
            vente.total_price = float(request.form.get("total_price"))
        except (TypeError, ValueError):
            flash("Quantité ou prix invalide.", "error")
            return redirect(url_for("ventes.edit_vente", vente_id=vente.id))

        vente.client_id = request.form.get("client_id")
        vente.produit_id = request.form.get("produit_id")

        db.session.commit()
        flash("Vente modifiée avec succès.", "success")
        return redirect(url_for("ventes.list_ventes"))

    return render_template("ventes.html", edit_mode=True, vente=vente)


@ventes_bp.route("/delete/<int:vente_id>", methods=["POST"])
@login_required
def delete_vente(vente_id):
    """Supprimer une vente"""
    vente = Vente.query.get_or_404(vente_id)
    db.session.delete(vente)
    db.session.commit()
    flash("Vente supprimée avec succès.", "success")
    return redirect(url_for("ventes.list_ventes"))


# --------------------------
# API routes (JSON endpoints)
# --------------------------

@ventes_bp.route("/api", methods=["GET"])
def api_list_ventes():
    """Retourner toutes les ventes en JSON"""
    ventes = Vente.query.all()
    return jsonify([
        {
            "id": v.id,
            "client_id": v.client_id,
            "produit_id": v.produit_id,
            "quantity": v.quantity,
            "total_price": v.total_price,
        }
        for v in ventes
    ])


@ventes_bp.route("/api/<int:vente_id>", methods=["GET"])
def api_get_vente(vente_id):
    """Retourner une vente en JSON"""
    vente = Vente.query.get_or_404(vente_id)
    return jsonify({
        "id": vente.id,
        "client_id": vente.client_id,
        "produit_id": vente.produit_id,
        "quantity": vente.quantity,
        "total_price": vente.total_price,
    })


@ventes_bp.route("/api", methods=["POST"])
def api_add_vente():
    """Ajouter une vente via API"""
    data = request.get_json()
    if not data or "client_id" not in data or "produit_id" not in data or "quantity" not in data or "total_price" not in data:
        return jsonify({"message": "client_id, produit_id, quantity et total_price sont requis"}), 400

    new_vente = Vente(
        client_id=data["client_id"],
        produit_id=data["produit_id"],
        quantity=int(data["quantity"]),
        total_price=float(data["total_price"]),
    )

    db.session.add(new_vente)
    db.session.commit()

    return jsonify({"message": "Vente created", "id": new_vente.id}), 201


@ventes_bp.route("/api/<int:vente_id>", methods=["PUT"])
def api_update_vente(vente_id):
    """Modifier une vente via API"""
    vente = Vente.query.get_or_404(vente_id)
    data = request.get_json()

    vente.client_id = data.get("client_id", vente.client_id)
    vente.produit_id = data.get("produit_id", vente.produit_id)
    vente.quantity = int(data.get("quantity", vente.quantity))
    vente.total_price = float(data.get("total_price", vente.total_price))

    db.session.commit()
    return jsonify({"message": "Vente updated"})


@ventes_bp.route("/api/<int:vente_id>", methods=["DELETE"])
def api_delete_vente(vente_id):
    """Supprimer une vente via API"""
    vente = Vente.query.get_or_404(vente_id)
    db.session.delete(vente)
    db.session.commit()
    return jsonify({"message": "Vente deleted"})
