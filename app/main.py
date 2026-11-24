#parte do instalavel#
import os
import sys

from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.dependencias import pegar_sessao
from app.modelos import Rede, No, Ligacao
from app.rotas import rotas

app = FastAPI()
app.include_router(rotas)

#parte do instalavel#
if hasattr(sys, '_MEIPASS'):
    pasta_templates = os.path.join(sys._MEIPASS, "app", "templates")
else:
    pasta_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=pasta_templates)


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

    ids_nos = [no.id for no in nos]
    ligacoes = [
        lig for lig in session.query(Ligacao).all()
        if lig.no_origem_id in ids_nos and lig.no_destino_id in ids_nos
    ]

    return templates.TemplateResponse(
        request=request,
        name="cri_rede.html",
        context={"rede": rede, "nos": nos, "ligacoes": ligacoes}
    )
