from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Livraison
from auth_routes import login_required

livraisons_bp = Blueprint("livraisons", __name__)

# --------------------------
# Web routes (HTML views)
# --------------------------

@livraisons_bp.route("/", methods=["GET"])
@login_required
def list_livraisons():
    """Afficher la liste des livraisons"""
    livraisons = Livraison.query.all()
    return render_template("livraisons.html", livraisons=livraisons)


@livraisons_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_livraison():
    """Ajouter une livraison"""
    if request.method == "POST":
        vente_id = request.form.get("vente_id")
        date_livraison = request.form.get("date_livraison")
        statut = request.form.get("statut")

        new_livraison = Livraison(
            vente_id=vente_id,
            date_livraison=date_livraison,
            statut=statut
        )
        db.session.add(new_livraison)
        db.session.commit()

        flash("Livraison ajoutée avec succès.", "success")
        return redirect(url_for("livraisons.list_livraisons"))

    return render_template("livraisons.html", add_mode=True)


@livraisons_bp.route("/edit/<int:livraison_id>", methods=["GET", "POST"])
@login_required
def edit_livraison(livraison_id):
    """Modifier une livraison"""
    livraison = Livraison.query.get_or_404(livraison_id)

    if request.method == "POST":
        livraison.vente_id = request.form.get("vente_id")
        livraison.date_livraison = request.form.get("date_livraison")
        livraison.statut = request.form.get("statut")

        db.session.commit()
        flash("Livraison modifiée avec succès.", "success")
        return redirect(url_for("livraisons.list_livraisons"))

    return render_template("livraisons.html", edit_mode=True, livraison=livraison)


@livraisons_bp.route("/delete/<int:livraison_id>", methods=["POST"])
@login_required
def delete_livraison(livraison_id):
    """Supprimer une livraison"""
    livraison = Livraison.query.get_or_404(livraison_id)
    db.session.delete(livraison)
    db.session.commit()
    flash("Livraison supprimée avec succès.", "success")
    return redirect(url_for("livraisons.list_livraisons"))


# --------------------------
# API routes (JSON endpoints)
# --------------------------

@livraisons_bp.route("/api", methods=["GET"])
def api_list_livraisons():
    """Retourner toutes les livraisons en JSON"""
    livraisons = Livraison.query.all()
    return jsonify([
        {
            "id": l.id,
            "vente_id": l.vente_id,
            "date_livraison": l.date_livraison.isoformat() if l.date_livraison else None,
            "statut": l.statut,
        }
        for l in livraisons
    ])


@livraisons_bp.route("/api/<int:livraison_id>", methods=["GET"])
def api_get_livraison(livraison_id):
    """Retourner une livraison en JSON"""
    livraison = Livraison.query.get_or_404(livraison_id)
    return jsonify({
        "id": livraison.id,
        "vente_id": livraison.vente_id,
        "date_livraison": livraison.date_livraison.isoformat() if livraison.date_livraison else None,
        "statut": livraison.statut,
    })


@livraisons_bp.route("/api", methods=["POST"])
def api_add_livraison():
    """Ajouter une livraison via API"""
    data = request.get_json()
    if not data or "vente_id" not in data:
        return jsonify({"message": "vente_id is required"}), 400

    new_livraison = Livraison(
        vente_id=data["vente_id"],
        date_livraison=data.get("date_livraison"),
        statut=data.get("statut", "En attente"),
    )

    db.session.add(new_livraison)
    db.session.commit()

    return jsonify({"message": "Livraison created", "id": new_livraison.id}), 201


@livraisons_bp.route("/api/<int:livraison_id>", methods=["PUT"])
def api_update_livraison(livraison_id):
    """Modifier une livraison via API"""
    livraison = Livraison.query.get_or_404(livraison_id)
    data = request.get_json()

    livraison.vente_id = data.get("vente_id", livraison.vente_id)
    livraison.date_livraison = data.get("date_livraison", livraison.date_livraison)
    livraison.statut = data.get("statut", livraison.statut)

    db.session.commit()
    return jsonify({"message": "Livraison updated"})


@livraisons_bp.route("/api/<int:livraison_id>", methods=["DELETE"])
def api_delete_livraison(livraison_id):
    """Supprimer une livraison via API"""
    livraison = Livraison.query.get_or_404(livraison_id)
    db.session.delete(livraison)
    db.session.commit()
    return jsonify({"message": "Livraison deleted"})
