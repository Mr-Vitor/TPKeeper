from flask import Blueprint, redirect, request, render_template, url_for
from models.config import db, Mestre
from flask_login import login_user, login_required, logout_user

bp = Blueprint(url_prefix="/Mestre", template_folder="templates", name="Mestre", import_name=__name__)



@bp.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        
        mestres = db.session.execute(db.select(Mestre)).scalars()
        if email not in mestres.email:
            mestre = db.session.execute(db.select(Mestre).where(Mestre.email == email)).fetchone()
            if mestre.senha == senha:
                login_user(mestre)
        return redirect(url_for("Campanha.campanha"))
    else:
        return render_template("login.html")
    

@bp.route('/cadastrar', methods = ["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        mestre = Mestre(nome = nome, email = email, senha = senha)
        mestres = db.session.execute(db.select(Mestre)).scalars()
        if mestre.email not in mestres.email:
            db.session.add(mestre)
            db.session.commit()
            return redirect(url_for("Campanha.campanhas"))
        else:
            return redirect(url_for("Mestre.login"))
    else:
        return render_template("cadastrar.html")
    

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))