from flask import Flask, render_template
from models import db

# Flask app
app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "super-secret-key"

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Routes simples
@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/factures")
def factures():
    return render_template("facture.html")

@app.route("/commandes")
def commandes():
    return render_template("commandes.html")
