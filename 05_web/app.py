"""
MÓDULO 5 — Do terminal para a web: o agente com interface de chat.

Rode com:  uvicorn app:app --app-dir 05_web --reload
Depois abra:  http://localhost:8000

Arquitetura:
    Navegador (index.html)  ──POST /api/chat──▶  FastAPI (este arquivo)  ──▶  Agente  ──▶  Gemini
                            ◀── resposta + passos ──

Por que a chave fica AQUI e não no navegador?
  Tudo que vai para o navegador pode ser visto por qualquer pessoa (F12).
  O servidor guarda a chave e só devolve o resultado. Regra de ouro de segurança.
"""
import os
import sys
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "04_agente"))

from comum import MODELO, criar_cliente  # noqa: E402
from agente import Agente  # noqa: E402
from ferramentas import ver_minha_agenda  # noqa: E402

NOME_DO_AGENTE = os.getenv("AGENTE_NOME", "Guia Rec'n'Play")
MAX_MENSAGENS_POR_SESSAO = int(os.getenv("MAX_MENSAGENS_POR_SESSAO", "40"))  # protege sua cota

app = FastAPI(title=NOME_DO_AGENTE)

_cliente = None
_sessoes: dict[str, dict] = {}  # cada aba do navegador tem seu próprio agente (e memória)
_trava = threading.Lock()


def _obter_cliente():
    global _cliente
    if _cliente is None:
        try:
            _cliente = criar_cliente()
        except SystemExit:  # criar_cliente encerra o programa se não houver chave
            raise HTTPException(500, "Chave GEMINI_API_KEY não configurada no servidor (.env ou variável de ambiente).")
    return _cliente


def _obter_sessao(sessao_id: str) -> dict:
    with _trava:
        if sessao_id not in _sessoes:
            _sessoes[sessao_id] = {"agente": Agente(_obter_cliente(), verboso=True), "mensagens": 0}
        return _sessoes[sessao_id]


class Pergunta(BaseModel):
    sessao: str = Field(min_length=8, max_length=64)
    mensagem: str = Field(min_length=1, max_length=2000)


class Sessao(BaseModel):
    sessao: str = Field(min_length=8, max_length=64)


@app.get("/")
def pagina_inicial():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/api/info")
def info():
    return {"nome": NOME_DO_AGENTE, "modelo": MODELO}


@app.get("/saude")
def saude():
    """Rota simples para saber se o servidor está no ar (usada por Docker e deploy)."""
    return {"status": "ok"}


@app.post("/api/chat")
def conversar(p: Pergunta):
    s = _obter_sessao(p.sessao)
    if s["mensagens"] >= MAX_MENSAGENS_POR_SESSAO:
        raise HTTPException(429, "Limite de mensagens desta sessão atingido. Clique em 'Nova conversa'.")
    s["mensagens"] += 1
    try:
        resposta = s["agente"].perguntar(p.mensagem)
    except Exception as e:  # erro de cota, rede, chave...
        raise HTTPException(502, f"Falha ao falar com a Gemini API: {e}")
    return {"resposta": resposta, "passos": s["agente"].passos}


@app.post("/api/json")
def ultima_resposta_em_json(p: Sessao):
    s = _sessoes.get(p.sessao)
    if not s or not s["agente"].id_conversa:
        raise HTTPException(400, "Faça uma pergunta primeiro.")
    return s["agente"].resumir_em_json().model_dump()


@app.post("/api/nova")
def nova_conversa(p: Sessao):
    with _trava:
        _sessoes.pop(p.sessao, None)
    return {"ok": True}


@app.get("/api/agenda")
def agenda():
    return ver_minha_agenda()
