"""
MÓDULO 1.2 — Conversa com memória (multi-turn) e instruções de sistema.

Rode com:  python 01_primeira_chamada/conversa_com_memoria.py

Conceitos:
  • O modelo NÃO lembra de nada sozinho. Cada chamada é independente.
  • previous_interaction_id → diz à API: "continue a partir daquela conversa".
  • system_instruction → regras de comportamento (persona, tom, limites).
    Atenção: system_instruction e tools precisam ser enviados em TODA chamada.

Digite 'sair' para encerrar.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import MODELO, criar_cliente, titulo, cor

INSTRUCOES = (
    "Você é um monitor simpático de uma oficina de IA no Rec'n'Play, em Recife. "
    "Responda em português do Brasil, de forma curta (no máximo 4 frases) "
    "e sempre com um exemplo do dia a dia."
)

cliente = criar_cliente()
titulo("Chat com memória — digite 'sair' para encerrar")

id_anterior = None  # Na primeira mensagem não existe conversa anterior

while True:
    pergunta = input(cor("\nVocê: ", "verde")).strip()
    if pergunta.lower() in {"sair", "exit", "quit"}:
        break
    if not pergunta:
        continue

    parametros = dict(model=MODELO, input=pergunta, system_instruction=INSTRUCOES)
    if id_anterior:  # Da 2ª mensagem em diante, ligamos à conversa anterior
        parametros["previous_interaction_id"] = id_anterior

    interaction = cliente.interactions.create(**parametros)
    print(cor("Gemini: ", "azul") + interaction.output_text)

    id_anterior = interaction.id  # Guardamos para a próxima volta do laço
