from flask import Blueprint

bp = Blueprint(name="Campanha", url_prefix="Campanha", template_folder="templates")

@bp.route('/')
def inicial():
    pass