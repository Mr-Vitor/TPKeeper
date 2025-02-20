from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Mestre(db.Model, UserMixin):
    __tablename__ = 'mestres'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(db.String(200), nullable=False)
    
    campanhas: Mapped[list["Campanha"]] = relationship("Campanha", back_populates="mestre", cascade="all, delete")

class Campanha(db.Model):
    __tablename__ = 'campanhas'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    mestre_id: Mapped[int] = mapped_column(db.Integer, ForeignKey('mestres.id'), nullable=False)
    nome: Mapped[str] = mapped_column(db.String(150), nullable=False)
    desc: Mapped[str] = mapped_column(db.String(1000), nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    
    mestre: Mapped["Mestre"] = relationship("Mestre", back_populates="campanhas")
    anotacoes: Mapped[list["Anotacao"]] = relationship("Anotacao", back_populates="campanha", cascade="all, delete")
    dados: Mapped[list["Dado"]] = relationship("Dado", back_populates="campanha", cascade="all, delete")

class Anotacao(db.Model):
    __tablename__ = 'anotacoes'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    campanha_id: Mapped[int] = mapped_column(db.Integer, ForeignKey('campanhas.id'), nullable=False)
    nome: Mapped[str] = mapped_column(db.String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(db.Text, nullable=False)
    data_criacao: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    
    campanha: Mapped["Campanha"] = relationship("Campanha", back_populates="anotacoes")

class Dado(db.Model):
    __tablename__ = 'dados'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    campanha_id: Mapped[int] = mapped_column(db.Integer, ForeignKey('campanhas.id'), nullable=False)
    nome: Mapped[str] = mapped_column(db.String(50), nullable=False)
    quantidade_faces: Mapped[int] = mapped_column(db.Integer, nullable=False)
    modificador: Mapped[int] = mapped_column(db.Integer, default=0)
    
    campanha: Mapped["Campanha"] = relationship("Campanha", back_populates="dados")

def init_db(app):
    app.config['SECRET_KEY'] = "superdificil2"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()



