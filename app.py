from flask import Flask, redirect, url_for, render_template
from models.config import init_db, Mestre
from flask_login import LoginManager
from controllers.Campanha import bp as Campanha_bp
from controllers.Mestre import bp as Mestre_bp
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
init_db(app)

app.register_blueprint(Mestre_bp)
app.register_blueprint(Campanha_bp)

login_manager.login_view = "Mestre.login"
login_manager.login_message = "Você precisa fazer login para acessar esta página."
login_manager.login_message_category = "warning" 
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return Mestre.get(user_id)

@app.route('/')
def index():
    return render_template("index.html")
