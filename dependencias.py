from sqlalchemy.orm import sessionmaker
from modelos import db

def pegar_sessao():
    try:
        #cria uma sessao do banco de dados
        Session = sessionmaker(bind=db)
        session = Session()
        #em vez de usar return Session que poderia nao ser fechada depois
        #usa-se o yield que mantem uma geração da sessão enquanto ela for usada    
        yield session
    finally:
        session.close()