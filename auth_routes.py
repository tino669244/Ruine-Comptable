from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

# --------------------------
# Middleware login_required
# --------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vous devez être connecté pour accéder à cette page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# --------------------------
# Web routes
# --------------------------
@auth_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = AuthService.authenticate_user(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            access_token = create_access_token(identity=user.id)
            session['access_token'] = access_token
            flash('Connexion réussie', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if AuthService.create_user(username, password):
            flash('Utilisateur créé avec succès', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Erreur lors de la création de l\'utilisateur', 'error')
    
    return render_template('login.html', register_mode=True)


# --------------------------
# API routes (JWT-based)
# --------------------------
@auth_bp.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON payload'}), 400

    username = data.get('username')
    password = data.get('password')
    
    user = AuthService.authenticate_user(username, password)
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token, 'user_id': user.id}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401


@auth_bp.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON payload'}), 400

    username = data.get('username')
    password = data.get('password')
    
    if AuthService.create_user(username, password):
        return jsonify({'message': 'User created successfully'}), 201
    
    return jsonify({'message': 'User creation failed'}), 400
