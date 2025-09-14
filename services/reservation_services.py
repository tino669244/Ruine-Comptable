from models import db, Reservation

class ReservationService:
    @staticmethod
    def create_reservation(client_id, produit_id, quantity, date):
        reservation = Reservation(
            client_id=client_id,
            produit_id=produit_id,
            quantity=quantity,
            date=date
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation

    @staticmethod
    def get_all():
        return Reservation.query.all()

    @staticmethod
    def get_by_id(reservation_id):
        return Reservation.query.get(reservation_id)

    @staticmethod
    def update_reservation(reservation_id, **kwargs):
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return None
        for key, value in kwargs.items():
            setattr(reservation, key, value)
        db.session.commit()
        return reservation

    @staticmethod
    def delete_reservation(reservation_id):
        reservation = Reservation.query.get(reservation_id)
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
            return True
        return False
