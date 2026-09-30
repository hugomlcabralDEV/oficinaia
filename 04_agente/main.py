"""
MÓDULO 4 — O agente completo: Guia Rec'n'Play 🤖

Rode com:  python 04_agente/main.py

Comandos especiais durante a conversa:
  /json    → mostra a última resposta em formato estruturado (structured output)
  /silencio → liga/desliga o log dos passos do agente
  /nova    → começa uma conversa nova (esquece o contexto)
  /sair    → encerra

Perguntas para testar (da mais simples à mais complexa):
  1. Quais oficinas de IA tem na sexta?
  2. Vai chover em Recife nos próximos dias?
  3. Qual o endereço do CEP 50030-230?
  4. Me mostra oficinas para iniciantes na quinta e adiciona a de agentes na minha agenda
  5. Adiciona também a A03 (→ repare no conflito de horário!)
  6. Adiciona a atividade Z99 (→ id que não existe: ele NÃO pode inventar)
  7. Monte meu sábado: quero algo de IA e algo de carreira, sem conflito,
     e me diga se preciso levar guarda-chuva
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import criar_cliente, titulo, cor, erro  # noqa: E402
from agente import Agente  # noqa: E402


def main():
    agente = Agente(criar_cliente())
    titulo("Guia Rec'n'Play 🤖  —  /json  /silencio  /nova  /sair")

    while True:
        try:
            texto = input(cor("\nVocê: ", "verde")).strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not texto:
            continue
        if texto == "/sair":
            break
        if texto == "/nova":
            agente.id_conversa = None
            print(cor("Conversa reiniciada.", "amarelo"))
            continue
        if texto == "/silencio":
            agente.verboso = not agente.verboso
            print(cor(f"Log dos passos {'ligado' if agente.verboso else 'desligado'}.", "amarelo"))
            continue
        if texto == "/json":
            if not agente.id_conversa:
                print(cor("Faça uma pergunta primeiro.", "amarelo"))
                continue
            print(agente.resumir_em_json().model_dump_json(indent=2))
            continue

        try:
            resposta = agente.perguntar(texto)
            print(cor("\nGuia: ", "azul") + resposta)
        except Exception as e:  # erro de rede, cota, chave inválida...
            erro(f"Algo deu errado ao falar com a API: {e}")
            print("   Dica: veja docs/TROUBLESHOOTING.md")

    print("\nAté mais! 👋")


if __name__ == "__main__":
    main()
