"""
MÓDULO 2.2 — Structured Outputs para CLASSIFICAR e AUTOMATIZAR decisões.

Rode com:  python 02_structured_outputs/triagem_feedback.py

Cenário: chegam vários feedbacks sobre o evento. Queremos que o modelo
classifique cada um, e o NOSSO código (não o modelo) decide o que fazer.

Repare no padrão que vai aparecer de novo no agente:
  → o modelo INTERPRETA a linguagem natural
  → o código EXECUTA as regras de negócio, de forma previsível
"""
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import MODELO, criar_cliente, titulo, cor


class Triagem(BaseModel):
    sentimento: Literal["positivo", "neutro", "negativo"]
    categoria: Literal["conteudo", "infraestrutura", "comida", "acessibilidade", "outro"]
    urgente: bool = Field(description="True se exige ação da organização ainda hoje")
    resumo: str = Field(description="Resumo do feedback em até 12 palavras")


FEEDBACKS = [
    "A oficina de agentes foi incrível, saí sabendo fazer function calling!",
    "O wi-fi da sala Frevo caiu de novo e ninguém consegue instalar as bibliotecas.",
    "Não tem rampa de acesso no palco principal, meu amigo cadeirante não conseguiu subir.",
    "O café acabou cedo, mas de resto tudo ok.",
]

ACOES = {  # Regras de negócio: quem decide é o código
    "infraestrutura": "Abrir chamado para a equipe de TI",
    "acessibilidade": "Acionar a coordenação de acessibilidade",
    "comida": "Avisar a equipe de alimentação",
    "conteudo": "Enviar para a curadoria",
    "outro": "Registrar na planilha geral",
}

cliente = criar_cliente()
titulo("Triagem automática de feedbacks")

for texto in FEEDBACKS:
    resposta = cliente.interactions.create(
        model=MODELO,
        input=f"Classifique este feedback de um participante de evento: {texto}",
        response_format={"type": "text", "mime_type": "application/json", "schema": Triagem.model_json_schema()},
    )
    t = Triagem.model_validate_json(resposta.output_text)

    marcador = cor("🔴 URGENTE", "vermelho") if t.urgente else cor("🟢 normal ", "verde")
    print(f"\n{marcador} [{t.sentimento:>8}] {t.resumo}")
    print(cor(f"            → Ação automática: {ACOES[t.categoria]}", "cinza"))
