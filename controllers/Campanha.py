from flask import Blueprint, render_template, request, redirect, url_for, send_file
from models.config import db, Campanha, Anotacao, Dado
from flask_login import current_user, login_required
import io

bp = Blueprint(name="Campanha", url_prefix="/Campanha", template_folder="templates", import_name=__name__)

@bp.route('/')
@login_required
def campanha():
    campanhas= db.session.execute(db.select(Campanha).where(Campanha.mestre_id == current_user.id)).scalars()

    return render_template("campanhas.html", campanhas = campanhas)

@bp.route('/campanha/imagem/<int:id>')
@login_required
def get_campanha_imagem(id):
    campanha = db.session.get(Campanha, id)  # Obtém a campanha pelo ID
    if not campanha or not campanha.imagem:
        return "Imagem não encontrada", 404
    
    return send_file(
        io.BytesIO(campanha.imagem),  # Converte bytes em arquivo para enviar
        mimetype="image/png",  # Ajuste conforme o tipo real da imagem
    )

@bp.route("/<int:id>/excluir",methods=["GET"])
@login_required
def excluir(id):
    db.session.query(Campanha).filter(Campanha.id == id).delete()
    db.session.commit()    
    return redirect(url_for("Campanha.campanha"))

@bp.route('/criar', methods=["GET", "POST"])
@login_required
def criar():
    if request.method == "POST":
        
        mestre_id = current_user.id
        nome = request.form["nome"]
        desc = request.form["desc"]
        
        campanha = Campanha(mestre_id= mestre_id, nome=nome, desc=desc)


        file = request.files['imagem']
        if file.filename == '':
            file = None
        else:
            filedata = file.read()
            campanha.imagem= filedata
            campanha.imagem_nome = file.filename

        
        
        db.session.add(campanha)
        db.session.commit()
        return redirect(url_for("Campanha.campanha"))

    else:
        return render_template("criar-campanha.html")
    
@bp.route('/dashboard/<int:campanha_id>/edit', methods=["POST", "GET"])
@login_required
def edit_camp(campanha_id):
    if request.method == "POST":

        campanha = db.session.query(Campanha).filter(Campanha.id == campanha_id).one()

        if "imagem" in request.files:
            if request.files["imagem"] != None:
                file = request.files['imagem']
                if file.filename == '':
                    file = None
                else:
                    filedata = file.read()
                    campanha.imagem = filedata
                    campanha.imagem_nome = file.filename
                

        
        nome = request.form["nome"]
        desc = request.form["desc"]


        

        campanha.nome = nome
        campanha.desc = desc
        
        db.session.commit()
        return redirect(url_for("Campanha.acesso", campanha_id = campanha_id))
    else:
        campanha = db.session.query(Campanha).filter(Campanha.id == campanha_id).one()
        return render_template("editar-campanha.html", campanha_id = campanha_id, campanha = campanha)








@bp.route('/dashboard/<int:campanha_id>', methods=["GET", "POST"])
@login_required
def acesso(campanha_id):
    anotacoes = db.session.query(Anotacao).filter(Anotacao.campanha_id == campanha_id)
    return render_template("lista-notas.html", anotacoes = anotacoes, campanha_id= campanha_id)

@bp.route('/dashboard/<int:campanha_id>/add-note', methods=["POST", "GET"])
@login_required
def add_note(campanha_id):
    if request.method == "GET":
        return render_template("criar-notas.html", campanha_id = campanha_id)
    
    else:
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        nota = Anotacao(campanha_id = campanha_id, nome = nome, descricao = descricao)
        db.session.add(nota)
        db.session.commit()
        return redirect(url_for("Campanha.acesso", campanha_id = campanha_id))


@bp.route('/dashboard/Campanha <int:campanha_id>/view/Nota <int:anotacao_id>')
@login_required
def view(campanha_id, anotacao_id):
    nota = db.session.query(Anotacao).filter(Anotacao.id == anotacao_id).one()
    return render_template("ler-notas.html", nota = nota, campanha_id=campanha_id)



@bp.route('/dashboard/<int:campanha_id>/edit-nota/Nota <int:anotacao_id>', methods=["POST", "GET"])
@login_required
def edit(campanha_id, anotacao_id):
    if request.method == "GET":
        nota = db.session.query(Anotacao).filter(Anotacao.id == anotacao_id).one()
        return render_template("editar-notas.html", nota = nota, campanha_id=campanha_id)
    
    else:
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        nota = db.session.query(Anotacao).filter(Anotacao.id == anotacao_id).one()
        nota.nome = nome
        nota.descricao = descricao
        db.session.commit()
        return redirect(url_for("Campanha.acesso", campanha_id = campanha_id))
    

@bp.route("/dashboard/<int:campanha_id>/delete-note/<int:anotacao_id>",methods=["GET"])
@login_required
def delete_note(anotacao_id, campanha_id):
    db.session.query(Anotacao).filter(Anotacao.id == anotacao_id).delete()
    db.session.commit()    
    return redirect(url_for("Campanha.acesso", campanha_id = campanha_id))


@bp.route('/dashboard/<int:campanha_id>/dados')
def dados(campanha_id):
    dados = db.session.query(Dado).filter(Dado.campanha_id==campanha_id)
    return render_template("rolar-dados.html", campanha_id=campanha_id, dados = dados)


@bp.route('/dashboard/<int:campanha_id>/create-dados', methods=["POST", "GET"])
def criar_dados(campanha_id):
    if request.method == "POST":
        nome = request.form["nome"]
        faces = request.form["faces"]
        dado = Dado(nome=nome, campanha_id=campanha_id, quantidade_faces = faces)
        db.session.add(dado)
        db.session.commit()
        return redirect(url_for("Campanha.dados", campanha_id=campanha_id))
    


    return render_template("criar-dados.html", campanha_id=campanha_id)


@bp.route("/dashboard/<int:campanha_id>/delete-dado/<int:dado_id>",methods=["GET"])
@login_required
def delete_dado(dado_id, campanha_id):
    db.session.query(Dado).filter(Dado.id == dado_id).delete()
    db.session.commit()    
    return redirect(url_for("Campanha.dados", campanha_id = campanha_id))


