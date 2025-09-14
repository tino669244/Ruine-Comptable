from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ===========================
# User model (for auth)
# ===========================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"


# ===========================
# Client model
# ===========================
class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reservations = db.relationship("Reservation", backref="client", lazy=True)
    ventes = db.relationship("Vente", backref="client", lazy=True)

    def __repr__(self):
        return f"<Client {self.name}>"


# ===========================
# Produit model
# ===========================
class Produit(db.Model):
    __tablename__ = "produits"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    stock = db.relationship("Stock", backref="produit", uselist=False)
    ventes = db.relationship("Vente", backref="produit", lazy=True)
    reservations = db.relationship("Reservation", backref="produit", lazy=True)

    def __repr__(self):
        return f"<Produit {self.name}>"


# ===========================
# Stock model
# ===========================
class Stock(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey("produits.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Stock produit_id={self.produit_id} qty={self.quantity}>"


# ===========================
# Reservation model
# ===========================
class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey("produits.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    reserved_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="en_attente")  # ex: en_attente, confirme, annule

    def __repr__(self):
        return f"<Reservation client={self.client_id} produit={self.produit_id}>"


# ===========================
# Vente model
# ===========================
class Vente(db.Model):
    __tablename__ = "ventes"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey("produits.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    date_vente = db.Column(db.DateTime, default=datetime.utcnow)

    livraison = db.relationship("Livraison", backref="vente", uselist=False)

    def __repr__(self):
        return f"<Vente client={self.client_id} produit={self.produit_id}>"


# ===========================
# Livraison model
# ===========================
class Livraison(db.Model):
    __tablename__ = "livraisons"

    id = db.Column(db.Integer, primary_key=True)
    vente_id = db.Column(db.Integer, db.ForeignKey("ventes.id"), nullable=False)
    status = db.Column(db.String(50), default="en_preparation")  # ex: en_preparation, expedie, livre
    date_livraison = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Livraison vente_id={self.vente_id} status={self.status}>"
