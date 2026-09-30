"""
comum.py — utilidades compartilhadas por todos os exercícios.

Aqui ficam três coisas que todo script precisa:
  1. Carregar a chave da API do arquivo .env
  2. Criar o "cliente" (o objeto que conversa com a Gemini API)
  3. Funções para imprimir mensagens coloridas no terminal
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent
load_dotenv(RAIZ / ".env")

# Modelo padrão da oficina (pode ser trocado no .env)
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def criar_cliente():
    """Cria o cliente da Gemini API usando a chave do .env."""
    from google import genai

    chave = os.getenv("GEMINI_API_KEY", "")
    if not chave:  # No Google Colab, a chave fica em "Secrets" (ícone de chave 🔑)
        try:
            from google.colab import userdata  # type: ignore

            chave = userdata.get("GEMINI_API_KEY")
        except Exception:
            pass
    if not chave or chave == "cole_sua_chave_aqui":
        erro(
            "Chave da API não encontrada!\n"
            "   1. Gere uma chave em https://aistudio.google.com/apikey\n"
            "   2. Copie .env.example para .env e cole a chave lá"
        )
        sys.exit(1)
    return genai.Client(api_key=chave)


# ---------- Cores no terminal (códigos ANSI, sem bibliotecas extras) ----------
_CORES = {"azul": "34", "verde": "32", "amarelo": "33", "vermelho": "31", "cinza": "90", "magenta": "35"}


def cor(texto: str, nome: str) -> str:
    return f"\033[{_CORES[nome]}m{texto}\033[0m"


def titulo(texto: str):
    print("\n" + cor("━" * 60, "azul"))
    print(cor(f"  {texto}", "azul"))
    print(cor("━" * 60, "azul"))


def info(texto: str):
    print(cor("ℹ ", "azul") + texto)


def ok(texto: str):
    print(cor("✔ ", "verde") + texto)


def aviso(texto: str):
    print(cor("⚠ ", "amarelo") + texto)


def erro(texto: str):
    print(cor("✖ ", "vermelho") + texto)
