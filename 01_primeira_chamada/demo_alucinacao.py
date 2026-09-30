"""
MÓDULO 1.3 — Por que precisamos de ferramentas? Uma demonstração de alucinação.

Rode com:  python 01_primeira_chamada/demo_alucinacao.py

Fazemos perguntas que o modelo NÃO tem como saber (dados privados ou de agora).
Observe: às vezes ele inventa uma resposta convincente. Isso é "alucinação".

Depois repetimos com uma instrução de sistema que o autoriza a dizer "não sei".
Isso ajuda, mas não resolve: ele continua sem os dados. A solução de verdade
é dar FERRAMENTAS ao modelo (módulo 03).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import MODELO, criar_cliente, titulo, cor

PERGUNTAS = [
    "Qual oficina acontece às 14h na sala Maracatu do Rec'n'Play 2026?",
    "Quantos graus está fazendo AGORA no Marco Zero, em Recife?",
]

HONESTO = (
    "Se você não tiver certeza absoluta ou não tiver acesso ao dado em tempo real, "
    "diga claramente 'Não tenho essa informação' e explique o que seria necessário para descobrir."
)

cliente = criar_cliente()

for pergunta in PERGUNTAS:
    titulo(pergunta)

    sem_regra = cliente.interactions.create(model=MODELO, input=pergunta)
    print(cor("SEM instrução de honestidade:", "amarelo"))
    print(sem_regra.output_text, "\n")

    com_regra = cliente.interactions.create(model=MODELO, input=pergunta, system_instruction=HONESTO)
    print(cor("COM instrução de honestidade:", "verde"))
    print(com_regra.output_text)
