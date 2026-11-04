from sqlalchemy import create_engine, Column, ForeignKey, String, Integer
from sqlalchemy.orm import declarative_base

db = create_engine('sqlite:///banco.db')
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
    anotacoes = Column(String, default="")
    especificidades_camada = Column(String, default="")

class Ligacao(Base):
    __tablename__ = 'ligacoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    no_origem_id = Column(Integer, ForeignKey('nos.id'))
    no_destino_id = Column(Integer, ForeignKey('nos.id'))

Base.metadata.create_all(db)