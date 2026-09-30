"""
MÓDULO 3 — Function Calling, passo a passo e sem mágica.

Rode com:  python 03_function_calling/clima_passo_a_passo.py

A ideia central (decore isto!):
  O MODELO NÃO EXECUTA NADA. Ele só PEDE para uma função ser executada.
  Quem executa é o SEU código. Depois você devolve o resultado para ele.

Os 4 passos do function calling:
  PASSO 1 → Declarar a ferramenta (nome, descrição, parâmetros)
  PASSO 2 → Enviar a pergunta + a lista de ferramentas ao modelo
  PASSO 3 → Se o modelo pedir (function_call), NÓS executamos a função
  PASSO 4 → Devolver o resultado (function_result) para ele escrever a resposta final

API externa usada: Open-Meteo (https://open-meteo.com) — gratuita e sem chave.
"""
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import MODELO, criar_cliente, titulo, cor, info, ok


# ─────────────────────────────────────────────────────────────
# A função Python "de verdade". Ela não tem nada de IA.
# ─────────────────────────────────────────────────────────────
def previsao_do_tempo(cidade: str) -> dict:
    """Consulta o clima atual de uma cidade na API Open-Meteo."""
    # 1ª chamada: descobrir latitude/longitude da cidade
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": cidade, "count": 1, "language": "pt", "countryCode": "BR"},
        timeout=10,
    ).json()
    if not geo.get("results"):
        return {"erro": f"Cidade '{cidade}' não encontrada."}
    lugar = geo["results"][0]

    # 2ª chamada: clima atual naquela coordenada
    clima = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lugar["latitude"],
            "longitude": lugar["longitude"],
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "timezone": "America/Recife",
        },
        timeout=10,
    ).json()["current"]

    return {
        "cidade": lugar["name"],
        "estado": lugar.get("admin1"),
        "temperatura_c": clima["temperature_2m"],
        "umidade_pct": clima["relative_humidity_2m"],
        "chuva_mm": clima["precipitation"],
        "vento_kmh": clima["wind_speed_10m"],
        "horario_medicao": clima["time"],
    }


# ─────────────────────────────────────────────────────────────
# PASSO 1 — Declarar a ferramenta para o modelo.
# É como um "cardápio": o modelo lê a descrição para decidir quando usar.
# Descrições boas = decisões boas. Escreva como se fosse para um colega.
# ─────────────────────────────────────────────────────────────
DECLARACAO_CLIMA = {
    "type": "function",
    "name": "previsao_do_tempo",
    "description": (
        "Retorna o clima ATUAL (temperatura, umidade, chuva e vento) de uma cidade brasileira. "
        "Use sempre que o usuário perguntar sobre tempo, calor, chuva ou o que vestir."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "cidade": {"type": "string", "description": "Nome da cidade, ex.: Recife, Olinda, Caruaru"}
        },
        "required": ["cidade"],
    },
}

# Tabela que liga o NOME que o modelo pede à FUNÇÃO Python que executamos
FUNCOES_DISPONIVEIS = {"previsao_do_tempo": previsao_do_tempo}


def main():
    cliente = criar_cliente()
    pergunta = "Tá mais quente em Recife ou em Caruaru agora? Preciso levar guarda-chuva?"
    titulo(pergunta)

    # PASSO 2 — Pergunta + ferramentas
    info("PASSO 2: enviando pergunta e a lista de ferramentas...")
    interaction = cliente.interactions.create(
        model=MODELO,
        input=pergunta,
        tools=[DECLARACAO_CLIMA],
    )

    # O modelo respondeu com pedidos de função? (pode pedir mais de um de uma vez!)
    pedidos = [p for p in interaction.steps if p.type == "function_call"]
    if not pedidos:
        print("O modelo respondeu direto, sem usar ferramentas:\n", interaction.output_text)
        return

    # PASSO 3 — Executar cada pedido (quem executa somos NÓS)
    resultados = []
    for pedido in pedidos:
        info(f"PASSO 3: o modelo pediu {cor(pedido.name, 'magenta')}({pedido.arguments})")
        funcao = FUNCOES_DISPONIVEIS[pedido.name]
        resultado = funcao(**pedido.arguments)
        ok(f"Resultado real da API: {resultado}")

        resultados.append({
            "type": "function_result",
            "name": pedido.name,
            "call_id": pedido.id,  # liga este resultado ao pedido certo
            "result": [{"type": "text", "text": json.dumps(resultado, ensure_ascii=False)}],
        })

    # PASSO 4 — Devolver os resultados e receber a resposta final
    info("PASSO 4: devolvendo os resultados para o modelo...")
    final = cliente.interactions.create(
        model=MODELO,
        input=resultados,
        tools=[DECLARACAO_CLIMA],             # ferramentas vão em TODA chamada
        previous_interaction_id=interaction.id,  # continua a mesma conversa
    )
    print("\n" + cor("Resposta final:", "verde"))
    print(final.output_text)


if __name__ == "__main__":
    main()
