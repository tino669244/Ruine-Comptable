from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    @staticmethod
    def create_user(username, password):
        if User.query.filter_by(username=username).first():
            return False
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return True

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return user
        return None
