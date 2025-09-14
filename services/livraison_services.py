from models import db, Livraison

class LivraisonService:
    @staticmethod
    def create_livraison(vente_id, date_livraison, statut="En attente"):
        livraison = Livraison(
            vente_id=vente_id,
            date_livraison=date_livraison,
            statut=statut
        )
        db.session.add(livraison)
        db.session.commit()
        return livraison

    @staticmethod
    def get_all():
        return Livraison.query.all()

    @staticmethod
    def update_statut(livraison_id, statut):
        livraison = Livraison.query.get(livraison_id)
        if not livraison:
            return None
        livraison.statut = statut
        db.session.commit()
        return livraison

    @staticmethod
    def delete(livraison_id):
        livraison = Livraison.query.get(livraison_id)
        if livraison:
            db.session.delete(livraison)
            db.session.commit()
            return True
        return False
