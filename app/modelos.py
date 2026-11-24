#parte do instalavel#
import os
import sys

from sqlalchemy import create_engine, Column, ForeignKey, String, Integer
from sqlalchemy.orm import declarative_base

#parte do instalavel#
if getattr(sys, 'frozen', False):
    pasta_app = os.path.dirname(sys.executable)
else:
    pasta_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
caminho_banco = os.path.join(pasta_app, 'banco.db')

db = create_engine(f'sqlite:///{caminho_banco}')
Base = declarative_base()


class Rede(Base):
    __tablename__ = 'redes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)


class No(Base):
    __tablename__ = 'nos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    rede_id = Column(Integer, ForeignKey('redes.id'))
    camada = Column(String)
    descricao = Column(String, default="")
    status = Column(String, default="")
    metrica = Column(String, default="")
    dono = Column(String, default="")
    prazo = Column(String, default="")


class Ligacao(Base):
    __tablename__ = 'ligacoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    no_origem_id = Column(Integer, ForeignKey('nos.id'))
    no_destino_id = Column(Integer, ForeignKey('nos.id'))


Base.metadata.create_all(db)
