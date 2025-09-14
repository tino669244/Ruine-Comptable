from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Client
from auth_routes import login_required

clients_bp = Blueprint("clients", __name__)

# --------------------------
# Web routes (HTML views)
# --------------------------

@clients_bp.route("/", methods=["GET"])
@login_required
def list_clients():
    """Afficher la liste des clients"""
    clients = Client.query.all()
    return render_template("clients.html", clients=clients)


@clients_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_client():
    """Ajouter un client"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        if not name:
            flash("Le nom est obligatoire.", "error")
            return redirect(url_for("clients.add_client"))

        new_client = Client(name=name, email=email, phone=phone, address=address)
        db.session.add(new_client)
        db.session.commit()

        flash("Client ajouté avec succès.", "success")
        return redirect(url_for("clients.list_clients"))

    return render_template("clients.html", add_mode=True)


@clients_bp.route("/edit/<int:client_id>", methods=["GET", "POST"])
@login_required
def edit_client(client_id):
    """Modifier un client"""
    client = Client.query.get_or_404(client_id)

    if request.method == "POST":
        client.name = request.form.get("name")
        client.email = request.form.get("email")
        client.phone = request.form.get("phone")
        client.address = request.form.get("address")

        db.session.commit()
        flash("Client modifié avec succès.", "success")
        return redirect(url_for("clients.list_clients"))

    return render_template("clients.html", edit_mode=True, client=client)


@clients_bp.route("/delete/<int:client_id>", methods=["POST"])
@login_required
def delete_client(client_id):
    """Supprimer un client"""
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash("Client supprimé avec succès.", "success")
    return redirect(url_for("clients.list_clients"))


# --------------------------
# API routes (JSON endpoints)
# --------------------------

@clients_bp.route("/api", methods=["GET"])
def api_list_clients():
    """Retourner tous les clients en JSON"""
    clients = Client.query.all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "address": c.address,
        }
        for c in clients
    ])


@clients_bp.route("/api/<int:client_id>", methods=["GET"])
def api_get_client(client_id):
    """Retourner un client en JSON"""
    client = Client.query.get_or_404(client_id)
    return jsonify({
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "phone": client.phone,
        "address": client.address,
    })


@clients_bp.route("/api", methods=["POST"])
def api_add_client():
    """Ajouter un client via API"""
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"message": "Name is required"}), 400

    new_client = Client(
        name=data["name"],
        email=data.get("email"),
        phone=data.get("phone"),
        address=data.get("address"),
    )

    db.session.add(new_client)
    db.session.commit()

    return jsonify({"message": "Client created", "id": new_client.id}), 201


@clients_bp.route("/api/<int:client_id>", methods=["PUT"])
def api_update_client(client_id):
    """Modifier un client via API"""
    client = Client.query.get_or_404(client_id)
    data = request.get_json()

    client.name = data.get("name", client.name)
    client.email = data.get("email", client.email)
    client.phone = data.get("phone", client.phone)
    client.address = data.get("address", client.address)

    db.session.commit()
    return jsonify({"message": "Client updated"})


@clients_bp.route("/api/<int:client_id>", methods=["DELETE"])
def api_delete_client(client_id):
    """Supprimer un client via API"""
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted"})
