from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Stock
from auth_routes import login_required

stocks_bp = Blueprint("stocks", __name__)

# --------------------------
# Web routes (HTML views)
# --------------------------

@stocks_bp.route("/", methods=["GET"])
@login_required
def list_stocks():
    """Afficher la liste des stocks"""
    stocks = Stock.query.all()
    return render_template("stocks.html", stocks=stocks)


@stocks_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_stock():
    """Ajouter un stock"""
    if request.method == "POST":
        produit_id = request.form.get("produit_id")
        quantity = request.form.get("quantity")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            flash("Quantité invalide.", "error")
            return redirect(url_for("stocks.add_stock"))

        new_stock = Stock(produit_id=produit_id, quantity=quantity)
        db.session.add(new_stock)
        db.session.commit()

        flash("Stock ajouté avec succès.", "success")
        return redirect(url_for("stocks.list_stocks"))

    return render_template("stocks.html", add_mode=True)


@stocks_bp.route("/edit/<int:stock_id>", methods=["GET", "POST"])
@login_required
def edit_stock(stock_id):
    """Modifier un stock"""
    stock = Stock.query.get_or_404(stock_id)

    if request.method == "POST":
        try:
            stock.quantity = int(request.form.get("quantity"))
        except (TypeError, ValueError):
            flash("Quantité invalide.", "error")
            return redirect(url_for("stocks.edit_stock", stock_id=stock.id))

        db.session.commit()
        flash("Stock modifié avec succès.", "success")
        return redirect(url_for("stocks.list_stocks"))

    return render_template("stocks.html", edit_mode=True, stock=stock)


@stocks_bp.route("/delete/<int:stock_id>", methods=["POST"])
@login_required
def delete_stock(stock_id):
    """Supprimer un stock"""
    stock = Stock.query.get_or_404(stock_id)
    db.session.delete(stock)
    db.session.commit()
    flash("Stock supprimé avec succès.", "success")
    return redirect(url_for("stocks.list_stocks"))


# --------------------------
# API routes (JSON endpoints)
# --------------------------

@stocks_bp.route("/api", methods=["GET"])
def api_list_stocks():
    """Retourner tous les stocks en JSON"""
    stocks = Stock.query.all()
    return jsonify([
        {
            "id": s.id,
            "produit_id": s.produit_id,
            "quantity": s.quantity,
        }
        for s in stocks
    ])


@stocks_bp.route("/api/<int:stock_id>", methods=["GET"])
def api_get_stock(stock_id):
    """Retourner un stock en JSON"""
    stock = Stock.query.get_or_404(stock_id)
    return jsonify({
        "id": stock.id,
        "produit_id": stock.produit_id,
        "quantity": stock.quantity,
    })


@stocks_bp.route("/api", methods=["POST"])
def api_add_stock():
    """Ajouter un stock via API"""
    data = request.get_json()
    if not data or "produit_id" not in data or "quantity" not in data:
        return jsonify({"message": "produit_id and quantity are required"}), 400

    new_stock = Stock(
        produit_id=data["produit_id"],
        quantity=int(data["quantity"])
    )

    db.session.add(new_stock)
    db.session.commit()

    return jsonify({"message": "Stock created", "id": new_stock.id}), 201


@stocks_bp.route("/api/<int:stock_id>", methods=["PUT"])
def api_update_stock(stock_id):
    """Modifier un stock via API"""
    stock = Stock.query.get_or_404(stock_id)
    data = request.get_json()

    stock.produit_id = data.get("produit_id", stock.produit_id)
    stock
