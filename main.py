from flask import Flask, render_template
from models import db

app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "super-secret-key"

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/facture")
def facture():
    return render_template("facture.html")

@app.route("/bon-commande")
def bon_commande():
    return render_template("bon_commande.html")
