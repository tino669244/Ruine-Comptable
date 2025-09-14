from flask import Blueprint, jsonify, request, send_file
from models import db, Client, Produit, Stock, Vente, Reservation, Livraison
import csv
import io
from datetime import datetime

exports_bp = Blueprint("exports", __name__)

@exports_bp.route("/csv/<string:table_name>", methods=["GET"])
def export_csv(table_name):
    """Exporter les données en CSV (Clients, Produits, Stocks, Ventes, Réservations, Livraisons)"""
    si = io.StringIO()
    cw = csv.writer(si)

    if table_name == "clients":
        data = Client.query.all()
        cw.writerow(["id", "name", "email", "phone"])
        for c in data:
            cw.writerow([c.id, c.name, c.email, c.phone])

    elif table_name == "produits":
        data = Produit.query.all()
        cw.writerow(["id", "name", "price"])
        for p in data:
            cw.writerow([p.id, p.name, p.price])

    elif table_name == "stocks":
        data = Stock.query.all()
        cw.writerow(["id", "produit_id", "quantity"])
        for s in data:
            cw.writerow([s.id, s.produit_id, s.quantity])

    elif table_name == "ventes":
        data = Vente.query.all()
        cw.writerow(["id", "client_id", "produit_id", "quantity", "total_price"])
        for v in data:
            cw.writerow([v.id, v.client_id, v.produit_id, v.quantity, v.total_price])

    elif table_name == "reservations":
        data = Reservation.query.all()
        cw.writerow(["id", "client_id", "produit_id", "quantity", "date"])
        for r in data:
            cw.writerow([r.id, r.client_id, r.produit_id, r.quantity, r.date])

    elif table_name == "livraisons":
        data = Livraison.query.all()
        cw.writerow(["id", "vente_id", "date_livraison", "statut"])
        for l in data:
            cw.writerow([l.id, l.vente_id, l.date_livraison, l.statut])

    else:
        return jsonify({"error": "Table inconnue"}), 400

    output = io.BytesIO()
    output.write(si.getvalue().encode("utf-8"))
    output.seek(0)

    filename = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )
