from pydantic import BaseModel
from typing import Optional, List

class RedeSchema(BaseModel):
    nome: str

class NoSchema(BaseModel):
    nome: str
    rede_id: int
    camada: str
    descricao: Optional[str] = ""
    status: Optional[str] = ""
    anotacoes: Optional[str] = ""
    especificidades_camada: Optional[str] = ""

class DetalhesNoSchema(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = ""
    status: Optional[str] = ""
    anotacoes: Optional[str] = ""
    especificidades_camada: Optional[str] = ""

class LigacaoSchema(BaseModel):
    no_origem_id: int
    no_destino_id: int

class ImportarRedeSchema(BaseModel):
    nome: str
    nos: List[dict]
    ligacoes: List[dict] = []
