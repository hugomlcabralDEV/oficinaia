"""
MÓDULO 0 — Verificar se o ambiente está pronto.

Rode com:  python 00_setup/verificar_ambiente.py

Este script checa, na ordem:
  1. Versão do Python (precisa ser 3.10 ou maior)
  2. Se as bibliotecas foram instaladas
  3. Se a chave da API está no .env
  4. Se conseguimos fazer UMA chamada de verdade ao Gemini
"""
import sys
from pathlib import Path

# Esta linha deixa o Python encontrar o arquivo comum.py que está na pasta raiz
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

print("\n🔎 Verificando seu ambiente para a oficina...\n")

# 1) Python
if sys.version_info < (3, 10):
    print(f"✖ Python {sys.version.split()[0]} é antigo. Instale o 3.10 ou mais novo.")
    sys.exit(1)
print(f"✔ Python {sys.version.split()[0]}")

# 2) Bibliotecas
faltando = []
for pacote in ["google.genai", "pydantic", "dotenv", "requests"]:
    try:
        __import__(pacote)
    except ImportError:
        faltando.append(pacote)
if faltando:
    print(f"✖ Faltam bibliotecas: {faltando}")
    print("   Rode:  pip install -r requirements.txt")
    sys.exit(1)

import google.genai

print(f"✔ Bibliotecas instaladas (google-genai {google.genai.__version__})")

# 3) Chave + 4) Chamada real
from comum import MODELO, criar_cliente, ok, erro

cliente = criar_cliente()
ok("Chave da API encontrada no .env")

try:
    resposta = cliente.interactions.create(
        model=MODELO,
        input="Responda apenas com a palavra: FUNCIONOU",
    )
    ok(f"Chamada ao modelo {MODELO} respondeu: {resposta.output_text.strip()}")
    print("\n🎉 Tudo pronto! Você já pode seguir para o módulo 01.\n")
except Exception as e:
    erro(f"A chamada falhou: {e}")
    print("   Veja docs/TROUBLESHOOTING.md para as soluções mais comuns.")
    sys.exit(1)
