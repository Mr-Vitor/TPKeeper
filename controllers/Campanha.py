from flask import Blueprint, render_template
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

@bp.route('/criar')
@login_required
def criar():
    pass


