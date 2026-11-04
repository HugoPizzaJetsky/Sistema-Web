from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dependencias import pegar_sessao
from modelos import Rede, No, Ligacao
from rotas import rotas

app = FastAPI()
app.include_router(rotas)

templates = Jinja2Templates(directory="templates")

@app.get("/app")
def listar_redes_pagina(request: Request, session: Session = Depends(pegar_sessao)):
    redes_salvas = session.query(Rede).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"redes": redes_salvas}
    )

@app.get("/editor/{rede_id}")
def abrir_editor(request: Request, rede_id: int, session: Session = Depends(pegar_sessao)):
    rede = session.query(Rede).filter(Rede.id == rede_id).first()
    nos = session.query(No).filter(No.rede_id == rede_id).all()

    ids_nos = []
    for no in nos:
        ids_nos.append(no.id)

    ligacoes = []
    for lig in session.query(Ligacao).all():
        if lig.no_origem_id in ids_nos and lig.no_destino_id in ids_nos:
            ligacoes.append(lig)

    return templates.TemplateResponse(
        request=request,
        name="cri_rede.html",
        context={"rede": rede, "nos": nos, "ligacoes": ligacoes}
    )