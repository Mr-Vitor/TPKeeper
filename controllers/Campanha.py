from flask import Blueprint, render_template, request, redirect, url_for
from models.config import db, Campanha
from flask_login import current_user, login_required

bp = Blueprint(name="Campanha", url_prefix="/Campanha", template_folder="templates", import_name=__name__)

@bp.route('/')
@login_required
def campanha():
    campanhas= db.session.execute(db.select(Campanha).where(Campanha.mestre_id == current_user.id)).scalars()
    return render_template("campanhas.html", campanhas = campanhas)

@bp.route("/<int:id>/excluir",methods=["POST"])
@login_required
def excluir(id):
    campanha = db.session.execute(db.select(Campanha).where(Campanha.id == id)).fetchone()
    db.session.delete(campanha)
    return redirect(url_for("Campanha.campanha"))

@bp.route('/criar', methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                file = None
            else:
                filedata = file.read()
        else:
            file = None
        mestre_id = current_user.id
        nome = request.form["nome"]
        desc = request.form["desc"]
        
        campanha = Campanha(mestre_id= mestre_id, nome=nome, desc=desc, imagem= filedata, imagem_nome = file.filename)
        db.session.add(campanha)
        db.session.commit()
        return redirect(url_for("Campanha.campanha"))

    else:
        return render_template("criar.html")

