from sqlalchemy.orm import sessionmaker
from app.modelos import db


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()
