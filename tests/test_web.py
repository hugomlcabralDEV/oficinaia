"""Testes da interface web (módulo 5) com um agente de mentira: sem chave, sem internet."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "05_web"))

from fastapi.testclient import TestClient  # noqa: E402

import app as web  # noqa: E402


class AgenteFalso:
    def __init__(self, *a, **k):
        self.id_conversa = None
        self.passos = []

    def perguntar(self, texto):
        self.id_conversa = "int_1"
        self.passos = [{"passo": 1, "ferramenta": "ver_minha_agenda", "argumentos": {}, "resultado": {"total": 0}}]
        return f"Eco: {texto}"


def test_chat_devolve_resposta_e_passos(monkeypatch):
    monkeypatch.setattr(web, "Agente", AgenteFalso)
    monkeypatch.setattr(web, "_obter_cliente", lambda: None)
    cliente = TestClient(web.app)

    r = cliente.post("/api/chat", json={"sessao": "sessao-teste-1", "mensagem": "oi"})
    assert r.status_code == 200
    assert r.json()["resposta"] == "Eco: oi"
    assert r.json()["passos"][0]["ferramenta"] == "ver_minha_agenda"


def test_pagina_e_saude():
    cliente = TestClient(web.app)
    assert cliente.get("/saude").json() == {"status": "ok"}
    assert "Guia" in cliente.get("/").text


def test_mensagem_vazia_e_recusada():
    cliente = TestClient(web.app)
    assert cliente.post("/api/chat", json={"sessao": "sessao-teste-2", "mensagem": ""}).status_code == 422
