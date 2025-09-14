from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -------------------------
# Client
# -------------------------
class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telephone = db.Column(db.String(50), nullable=True)

    commandes = db.relationship("Commande", backref="client", lazy=True)
    factures = db.relationship("Facture", backref="client", lazy=True)

    def __repr__(self):
        return f"<Client {self.nom}>"


# -------------------------
# Produit
# -------------------------
class Produit(db.Model):
    __tablename__ = "produits"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    lignes = db.relationship("CommandeLigne", backref="produit", lazy=True)

    def __repr__(self):
        return f"<Produit {self.nom} - Stock: {self.stock}>"


# -------------------------
# Commande
# -------------------------
class Commande(db.Model):
    __tablename__ = "commandes"

    id = db.Column(db.Integer, primary_key=True)
    date_commande = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(50), default="En attente")  # En attente / Validée / Annulée

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)

    lignes = db.relationship("CommandeLigne", backref="commande", lazy=True, cascade="all, delete-orphan")
    facture = db.relationship("Facture", backref="commande", uselist=False)

    def montant_total(self):
        return sum(ligne.quantite * ligne.produit.prix for ligne in self.lignes)

    def __repr__(self):
        return f"<Commande {self.id} - Client {self.client_id}>"


# -------------------------
# Commande Ligne
# -------------------------
class CommandeLigne(db.Model):
    __tablename__ = "commande_lignes"

    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey("commandes.id"), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey("produits.id"), nullable=False)

    quantite = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<CommandeLigne {self.id} - Qte {self.quantite}>"


# -------------------------
# Facture
# -------------------------
class Facture(db.Model):
    __tablename__ = "factures"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(100), unique=True, nullable=False)  # ex: FAC-2025-001
    date_facture = db.Column(db.DateTime, default=datetime.utcnow)

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    commande_id = db.Column(db.Integer, db.ForeignKey("commandes.id"), nullable=False)

    montant_total = db.Column(db.Float, nullable=False)

    # Paiement
    etat_paiement = db.Column(db.String(50), default="Non Payée")  # Non Payée / Payée / Partielle
    mode_paiement = db.Column(db.String(50), nullable=True)  # Espèces, Virement, Mobile Money

    def __repr__(self):
        return f"<Facture {self.numero} - {self.etat_paiement}>"
