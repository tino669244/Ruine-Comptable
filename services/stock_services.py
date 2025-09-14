from models import db, Stock, Produit

class StockService:
    @staticmethod
    def add_stock(produit_id, quantity):
        produit = Produit.query.get(produit_id)
        if not produit:
            return None
        stock = Stock(produit_id=produit_id, quantity=quantity)
        db.session.add(stock)
        db.session.commit()
        return stock

    @staticmethod
    def update_stock(stock_id, quantity):
        stock = Stock.query.get(stock_id)
        if not stock:
            return None
        stock.quantity = quantity
        db.session.commit()
        return stock

    @staticmethod
    def get_all():
        return Stock.query.all()

    @staticmethod
    def delete_stock(stock_id):
        stock = Stock.query.get(stock_id)
        if stock:
            db.session.delete(stock)
            db.session.commit()
            return True
        return False
