"""
MÓDULO 1.1 — Sua primeira chamada à Gemini API.

Rode com:  python 01_primeira_chamada/ola_gemini.py

Conceitos:
  • cliente     → objeto que sabe falar com a API (usa sua chave)
  • model       → qual "cérebro" vamos usar (ex.: gemini-3.8-flash)
  • input       → o que você está pedindo (o "prompt")
  • interaction → a resposta completa: tem um id, os "steps" (passos) e o texto final
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import MODELO, criar_cliente, titulo, cor

cliente = criar_cliente()

titulo("Primeira chamada ao Gemini")

interaction = cliente.interactions.create(
    model=MODELO,
    input="Explique em 3 frases, para quem nunca programou, o que é uma API.",
)

# output_text junta todo o texto final que o modelo escreveu
print(interaction.output_text)

# Curiosidade: a resposta é organizada em "passos" (steps). Vamos listar quais vieram.
print(cor("\nPassos devolvidos pela API:", "cinza"))
for passo in interaction.steps:
    print(cor(f"  • {passo.type}", "cinza"))
print(cor(f"\nID desta interação: {interaction.id}", "cinza"))
