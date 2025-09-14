from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Produit
from auth_routes import login_required

produits_bp = Blueprint("produits", __name__)

# --------------------------
# Web routes (HTML views)
# --------------------------

@produits_bp.route("/", methods=["GET"])
@login_required
def list_produits():
    """Afficher la liste des produits"""
    produits = Produit.query.all()
    return render_template("produits.html", produits=produits)


@produits_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_produit():
    """Ajouter un produit"""
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        stock = request.form.get("stock")

        if not name or not price:
            flash("Nom et prix sont obligatoires.", "error")
            return redirect(url_for("produits.add_produit"))

        try:
            price = float(price)
            stock = int(stock) if stock else 0
        except ValueError:
            flash("Prix ou stock invalide.", "error")
            return redirect(url_for("produits.add_produit"))

        new_produit = Produit(
            name=name,
            description=description,
            price=price,
            stock=stock
        )

        db.session.add(new_produit)
        db.session.commit()

        flash("Produit ajouté avec succès.", "success")
        return redirect(url_for("produits.list_produits"))

    return render_template("produits.html", add_mode=True)


@produits_bp.route("/edit/<int:produit_id>", methods=["GET", "POST"])
@login_required
def edit_produit(produit_id):
    """Modifier un produit"""
    produit = Produit.query.get_or_404(produit_id)

    if request.method == "POST":
        produit.name = request.form.get("name")
        produit.description = request.form.get("description")
        try:
            produit.price = float(request.form.get("price"))
            produit.stock = int(request.form.get("stock"))
        except ValueError:
            flash("Prix ou stock invalide.", "error")
            return redirect(url_for("produits.edit_produit", produit_id=produit.id))

        db.session.commit()
        flash("Produit modifié avec succès.", "success")
        return redirect(url_for("produits.list_produits"))

    return render_template("produits.html", edit_mode=True, produit=produit)


@produits_bp.route("/delete/<int:produit_id>", methods=["POST"])
@login_required
def delete_produit(produit_id):
    """Supprimer un produit"""
    produit = Produit.query.get_or_404(produit_id)
    db.session.delete(produit)
    db.session.commit()
    flash("Produit supprimé avec succès.", "success")
    return redirect(url_for("produits.list_produits"))


# --------------------------
# API routes (JSON endpoints)
# --------------------------

@produits_bp.route("/api", methods=["GET"])
def api_list_produits():
    """Retourner tous les produits en JSON"""
    produits = Produit.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock": p.stock,
        }
        for p in produits
    ])


@produits_bp.route("/api/<int:produit_id>", methods=["GET"])
def api_get_produit(produit_id):
    """Retourner un produit en JSON"""
    produit = Produit.query.get_or_404(produit_id)
    return jsonify({
        "id": produit.id,
        "name": produit.name,
        "description": produit.description,
        "price": produit.price,
        "stock": produit.stock,
    })


@produits_bp.route("/api", methods=["POST"])
def api_add_produit():
    """Ajouter un produit via API"""
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"message": "Name and price are required"}), 400

    new_produit = Produit(
        name=data["name"],
        description=data.get("description"),
        price=float(data["price"]),
        stock=int(data.get("stock", 0)),
    )

    db.session.add(new_produit)
    db.session.commit()

    return jsonify({"message": "Produit created", "id": new_produit.id}), 201


@produits_bp.route("/api/<int:produit_id>", methods=["PUT"])
def api_update_produit(produit_id):
    """Modifier un produit via API"""
    produit = Produit.query.get_or_404(produit_id)
    data = request.get_json()

    produit.name = data.get("name", produit.name)
    produit.description = data.get("description", produit.description)
    produit.price = float(data.get("price", produit.price))
    produit.stock = int(data.get("stock", produit.stock))
