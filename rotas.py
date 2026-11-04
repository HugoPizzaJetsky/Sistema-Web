from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dependencias import pegar_sessao
from modelos import Rede, No, Ligacao
from schemas import RedeSchema, NoSchema, DetalhesNoSchema, LigacaoSchema, ImportarRedeSchema

rotas = APIRouter(prefix='/redes', tags=['rede'])

LIGACOES_PERMITIDAS = {
    "ti": ["ti", "mudanca", "organizacional"],
    "mudanca": ["mudanca", "organizacional"],
    "organizacional": ["organizacional", "beneficio"],
    "beneficio": ["beneficio", "objetivo"],
    "objetivo": ["objetivo"]
}

@rotas.post('/Criar_e_abrir')
def criar_e_abrir(nome: str = Form(...), session: Session = Depends(pegar_sessao)):
    nova_rede = Rede(nome=nome)
    session.add(nova_rede)
    session.commit()
    return RedirectResponse(url=f"/editor/{nova_rede.id}", status_code=303)

@rotas.put('/atualizar/{rede_id}')
def atualizar_rede(rede_id: int, dados: RedeSchema, session: Session = Depends(pegar_sessao)):
    rede = session.query(Rede).filter(Rede.id == rede_id).first()
    if rede:
        rede.nome = dados.nome
        session.commit()
    return {"mensagem": "Nome atualizado"}

@rotas.post('/duplicar/{rede_id}')
def duplicar_rede(rede_id: int, session: Session = Depends(pegar_sessao)):
    rede_original = session.query(Rede).filter(Rede.id == rede_id).first()
    if not rede_original:
        raise HTTPException(status_code=404, detail="Rede não encontrada")

    nova_rede = Rede(nome=f"{rede_original.nome} (Cópia)")
    session.add(nova_rede)
    session.commit()

    nos_originais = session.query(No).filter(No.rede_id == rede_id).all()
    mapa_nos = {}

    for no in nos_originais:
        novo_no = No(
            nome=no.nome,
            rede_id=nova_rede.id,
            camada=no.camada,
            descricao=no.descricao,
            status=no.status,
            anotacoes=no.anotacoes,
            especificidades_camada=no.especificidades_camada
        )
        session.add(novo_no)
        session.commit()
        mapa_nos[no.id] = novo_no.id

    todas_ligacoes = session.query(Ligacao).all()
    for lig in todas_ligacoes:
        if lig.no_origem_id in mapa_nos and lig.no_destino_id in mapa_nos:
            nova_ligacao = Ligacao(
                no_origem_id=mapa_nos[lig.no_origem_id],
                no_destino_id=mapa_nos[lig.no_destino_id]
            )
            session.add(nova_ligacao)

    session.commit()
    return {"mensagem": "Rede duplicada com sucesso", "id": nova_rede.id}

@rotas.get('/exportar/{rede_id}')
def exportar_rede(rede_id: int, session: Session = Depends(pegar_sessao)):
    rede = session.query(Rede).filter(Rede.id == rede_id).first()
    if not rede:
        raise HTTPException(status_code=404, detail="Rede não encontrada")

    nos = session.query(No).filter(No.rede_id == rede_id).all()
    ids_nos = []
    lista_nos = []

    for no in nos:
        ids_nos.append(no.id)
        lista_nos.append({
            "id": no.id,
            "nome": no.nome,
            "camada": no.camada,
            "descricao": no.descricao or "",
            "status": no.status or "",
            "anotacoes": no.anotacoes or "",
            "especificidades_camada": no.especificidades_camada or ""
        })

    lista_ligacoes = []
    for lig in session.query(Ligacao).all():
        if lig.no_origem_id in ids_nos and lig.no_destino_id in ids_nos:
            lista_ligacoes.append({
                "no_origem_id": lig.no_origem_id,
                "no_destino_id": lig.no_destino_id
            })

    return {
        "nome": rede.nome,
        "nos": lista_nos,
        "ligacoes": lista_ligacoes
    }

@rotas.post('/importar')
def importar_rede(dados: ImportarRedeSchema, session: Session = Depends(pegar_sessao)):
    nova_rede = Rede(nome=dados.nome)
    session.add(nova_rede)
    session.commit()

    mapa_nos = {}
    for item_no in dados.nos:
        novo_no = No(
            nome=item_no.get("nome", "Nó"),
            rede_id=nova_rede.id,
            camada=item_no.get("camada", "ti"),
            descricao=item_no.get("descricao", ""),
            status=item_no.get("status", ""),
            anotacoes=item_no.get("anotacoes", ""),
            especificidades_camada=item_no.get("especificidades_camada", "")
        )
        session.add(novo_no)
        session.commit()
        mapa_nos[item_no["id"]] = novo_no.id

    for item_lig in dados.ligacoes:
        origem = item_lig.get("no_origem_id")
        destino = item_lig.get("no_destino_id")
        if origem in mapa_nos and destino in mapa_nos:
            nova_ligacao = Ligacao(
                no_origem_id=mapa_nos[origem],
                no_destino_id=mapa_nos[destino]
            )
            session.add(nova_ligacao)

    session.commit()
    return {"mensagem": "Rede importada com sucesso", "id": nova_rede.id}

@rotas.delete('/excluir/{rede_id}')
def excluir_rede(rede_id: int, session: Session = Depends(pegar_sessao)):
    rede = session.query(Rede).filter(Rede.id == rede_id).first()
    if not rede:
        raise HTTPException(status_code=404, detail="Rede não encontrada")

    nos = session.query(No).filter(No.rede_id == rede_id).all()
    ids_nos = []
    for no in nos:
        ids_nos.append(no.id)

    for lig in session.query(Ligacao).all():
        if lig.no_origem_id in ids_nos or lig.no_destino_id in ids_nos:
            session.delete(lig)

    for no in nos:
        session.delete(no)

    session.delete(rede)
    session.commit()
    return {"mensagem": "Rede excluída com sucesso"}

@rotas.post('/Criar_no')
def criar_no(dados: NoSchema, session: Session = Depends(pegar_sessao)):
    novo_no = No(
        nome=dados.nome,
        rede_id=dados.rede_id,
        camada=dados.camada,
        descricao=dados.descricao or "",
        status=dados.status or "",
        anotacoes=dados.anotacoes or "",
        especificidades_camada=dados.especificidades_camada or ""
    )
    session.add(novo_no)
    session.commit()
    return {"mensagem": "Nó criado", "id": novo_no.id}

@rotas.put('/atualizar_no/{no_id}')
def atualizar_no(no_id: int, dados: DetalhesNoSchema, session: Session = Depends(pegar_sessao)):
    no = session.query(No).filter(No.id == no_id).first()
    if not no:
        raise HTTPException(status_code=404, detail="Nó não encontrado")

    if dados.nome:
        no.nome = dados.nome
    no.descricao = dados.descricao
    no.status = dados.status
    no.anotacoes = dados.anotacoes
    no.especificidades_camada = dados.especificidades_camada
    session.commit()
    return {"mensagem": "Detalhes atualizados"}

@rotas.post('/Criar_ligacao')
def criar_ligacao(dados: LigacaoSchema, session: Session = Depends(pegar_sessao)):
    if dados.no_origem_id == dados.no_destino_id:
        raise HTTPException(status_code=400, detail="Um nó não pode ser conectado a ele mesmo.")

    no_origem = session.query(No).filter(No.id == dados.no_origem_id).first()
    no_destino = session.query(No).filter(No.id == dados.no_destino_id).first()

    camadas_aceitas = LIGACOES_PERMITIDAS.get(no_origem.camada, [])
    if no_destino.camada not in camadas_aceitas:
        raise HTTPException(status_code=400, detail="Ligação não permitida entre essas camadas.")

    existente = session.query(Ligacao).filter(
        Ligacao.no_origem_id == dados.no_origem_id,
        Ligacao.no_destino_id == dados.no_destino_id
    ).first()

    if not existente:
        nova_ligacao = Ligacao(
            no_origem_id=dados.no_origem_id,
            no_destino_id=dados.no_destino_id
        )
        session.add(nova_ligacao)
        session.commit()

    return {"mensagem": "Ligação criada"}

@rotas.delete('/excluir_no/{no_id}')
def excluir_no(no_id: int, session: Session = Depends(pegar_sessao)):
    no = session.query(No).filter(No.id == no_id).first()
    if not no:
        raise HTTPException(status_code=404, detail="Nó não encontrado")

    for lig in session.query(Ligacao).all():
        if lig.no_origem_id == no_id or lig.no_destino_id == no_id:
            session.delete(lig)

    session.delete(no)
    session.commit()
    return {"mensagem": "Nó excluído"}

@rotas.delete('/excluir_ligacao/{ligacao_id}')
def excluir_ligacao(ligacao_id: int, session: Session = Depends(pegar_sessao)):
    ligacao = session.query(Ligacao).filter(Ligacao.id == ligacao_id).first()
    if ligacao:
        session.delete(ligacao)
        session.commit()
    return {"mensagem": "Ligação excluída"}
