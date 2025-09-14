from models import db, Vente, Produit

class VenteService:
    @staticmethod
    def create_vente(client_id, produit_id, quantity):
        produit = Produit.query.get(produit_id)
        if not produit or produit.stock < quantity:
            return None

        total_price = produit.price * quantity
        vente = Vente(
            client_id=client_id,
            produit_id=produit_id,
            quantity=quantity,
            total_price=total_price
        )

        produit.stock -= quantity
        db.session.add(vente)
        db.session.commit()
        return vente

    @staticmethod
    def get_all():
        return Vente.query.all()

    @staticmethod
    def delete_vente(vente_id):
        vente = Vente.query.get(vente_id)
        if vente:
            db.session.delete(vente)
            db.session.commit()
            return True
        return False
