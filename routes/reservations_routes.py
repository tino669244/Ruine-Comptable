from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Reservation
from auth_routes import login_required

reservations_bp = Blueprint("reservations", __name__)

# --------------------------
# Web routes (HTML views)
# --------------------------

@reservations_bp.route("/", methods=["GET"])
@login_required
def list_reservations():
    """Afficher la liste des réservations"""
    reservations = Reservation.query.all()
    return render_template("reservations.html", reservations=reservations)


@reservations_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_reservation():
    """Ajouter une réservation"""
    if request.method == "POST":
        client_id = request.form.get("client_id")
        produit_id = request.form.get("produit_id")
        quantity = request.form.get("quantity")

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            flash("Quantité invalide.", "error")
            return redirect(url_for("reservations.add_reservation"))

        new_reservation = Reservation(
            client_id=client_id,
            produit_id=produit_id,
            quantity=quantity
        )
        db.session.add(new_reservation)
        db.session.commit()

        flash("Réservation ajoutée avec succès.", "success")
        return redirect(url_for("reservations.list_reservations"))

    return render_template("reservations.html", add_mode=True)


@reservations_bp.route("/edit/<int:reservation_id>", methods=["GET", "POST"])
@login_required
def edit_reservation(reservation_id):
    """Modifier une réservation"""
    reservation = Reservation.query.get_or_404(reservation_id)

    if request.method == "POST":
        try:
            reservation.quantity = int(request.form.get("quantity"))
        except (TypeError, ValueError):
            flash("Quantité invalide.", "error")
            return redirect(url_for("reservations.edit_reservation", reservation_id=reservation.id))

        reservation.client_id = request.form.get("client_id")
        reservation.produit_id = request.form.get("produit_id")

        db.session.commit()
        flash("Réservation modifiée avec succès.", "success")
        return redirect(url_for("reservations.list_reservations"))

    return render_template("reservations.html", edit_mode=True, reservation=reservation)


@reservations_bp.route("/delete/<int:reservation_id>", methods=["POST"])
@login_required
def delete_reservation(reservation_id):
    """Supprimer une réservation"""
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash("Réservation supprimée avec succès.", "success")
    return redirect(url_for("reservations.list_reservations"))


# --------------------------
# API routes (JSON endpoints)
# --------------------------

@reservations_bp.route("/api", methods=["GET"])
def api_list_reservations():
    """Retourner toutes les réservations en JSON"""
    reservations = Reservation.query.all()
    return jsonify([
        {
            "id": r.id,
            "client_id": r.client_id,
            "produit_id": r.produit_id,
            "quantity": r.quantity,
        }
        for r in reservations
    ])


@reservations_bp.route("/api/<int:reservation_id>", methods=["GET"])
def api_get_reservation(reservation_id):
    """Retourner une réservation en JSON"""
    reservation = Reservation.query.get_or_404(reservation_id)
    return jsonify({
        "id": reservation.id,
        "client_id": reservation.client_id,
        "produit_id": reservation.produit_id,
        "quantity": reservation.quantity,
    })


@reservations_bp.route("/api", methods=["POST"])
def api_add_reservation():
    """Ajouter une réservation via API"""
    data = request.get_json()
    if not data or "client_id" not in data or "produit_id" not in data or "quantity" not in data:
        return jsonify({"message": "client_id, produit_id, and quantity are required"}), 400

    new_reservation = Reservation(
        client_id=data["client_id"],
        produit_id=data["produit_id"],
        quantity=int(data["quantity"])
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({"message": "Reservation created", "id": new_reservation.id}), 201


@reservations_bp.route("/api/<int:reservation_id>", methods=["PUT"])
def api_update_reservation(reservation_id):
    """Modifier une réservation via API"""
    reservation = Reservation.query.get_or_404(reservation_id)
    data = request.get_json()

    reservation.client_id = data.get("client_id", reservation.client_id)
    reservation.produit_id = data.get("produit_id", reservation.produit_id)
    reservation.quantity = int(data.get("quantity", reservation.quantity))

    db.session.commit()
    return jsonify({"message": "Reservation updated"})


@reservations_bp.route("/api/<int:reservation_id>", methods=["DELETE"])
def api_delete_reservation(reservation_id):
    """Supprimer une réservation via API"""
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation deleted"})
