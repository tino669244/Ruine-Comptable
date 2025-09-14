from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -------------------
# Client
# -------------------
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    telephone = db.Column(db.String(20))
    commandes = db.relationship('Commande', backref='client', lazy=True)

# -------------------
# Produit
# -------------------
class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

# -------------------
# Commande
# -------------------
class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(20), default="En attente")
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    lignes = db.relationship('CommandeLigne', backref='commande', lazy=True)

class CommandeLigne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'))
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'))
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)
    produit = db.relationship('Produit')

# -------------------
# Facture
# -------------------
class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'))
    total_ht = db.Column(db.Float, nullable=False)
    tva = db.Column(db.Float, default=0.2)
    total_ttc = db.Column(db.Float, nullable=False)
    commande = db.relationship('Commande')
