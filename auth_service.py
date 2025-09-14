from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

class AuthService:
    @staticmethod
    def create_user(username, password):
        """Create new user with hashed password"""
        try:
            # Check if username already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return False
            
            # Hash password
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, password=hashed_pw)
            
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception as e:
            print(f"[AuthService] Error creating user: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def authenticate_user(username, password):
        """Verify user credentials"""
        try:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                return user
            return None
        except Exception as e:
            print(f"[AuthService] Error authenticating user: {e}")
            return None
