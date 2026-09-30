"""
ferramentas.py — as "mãos" do agente.

Cada ferramenta tem DUAS partes:
  1. A função Python que faz o trabalho de verdade
  2. A DECLARAÇÃO (dicionário) que explica ao modelo o que ela faz

Regras de ouro que seguimos aqui (e que evitam alucinação):
  • Nunca deixar uma exceção "explodir": devolvemos {"erro": "..."} para o modelo
    entender o que deu errado e contar a verdade ao usuário.
  • Validar TUDO que o modelo manda (um CEP com 8 dígitos, um id que existe...).
  • Devolver dados objetivos e pequenos. O modelo escreve o texto bonito depois.
"""
import json
import re
from pathlib import Path

import requests

PASTA_DADOS = Path(__file__).resolve().parent / "dados"
ARQUIVO_PROGRAMACAO = PASTA_DADOS / "programacao.json"
ARQUIVO_AGENDA = PASTA_DADOS / "minha_agenda.json"
TIMEOUT = 10  # segundos. Nunca chame uma API externa sem timeout!


# ════════════════════════════════════════════════════════════════
# Funções auxiliares (não são ferramentas, o modelo não as vê)
# ════════════════════════════════════════════════════════════════
def _carregar_atividades() -> list[dict]:
    return json.loads(ARQUIVO_PROGRAMACAO.read_text(encoding="utf-8"))["atividades"]


def _normalizar(texto: str) -> str:
    """Deixa em minúsculas e sem acentos, para buscas mais tolerantes."""
    trocas = str.maketrans("áàâãéêíóôõúüç", "aaaaeeiooouuc")
    return (texto or "").lower().translate(trocas).strip()


def _ler_agenda() -> list[str]:
    if not ARQUIVO_AGENDA.exists():
        return []
    return json.loads(ARQUIVO_AGENDA.read_text(encoding="utf-8"))


def _salvar_agenda(ids: list[str]):
    ARQUIVO_AGENDA.write_text(json.dumps(ids, ensure_ascii=False, indent=2), encoding="utf-8")


def _conflita(a: dict, b: dict) -> bool:
    """Duas atividades no mesmo dia se sobrepõem no horário?"""
    return a["dia"] == b["dia"] and a["inicio"] < b["fim"] and b["inicio"] < a["fim"]


# ════════════════════════════════════════════════════════════════
# FERRAMENTA 1 — Consultar a programação (dados locais)
# ════════════════════════════════════════════════════════════════
def consultar_programacao(termo: str = "", dia: str = "", trilha: str = "", a_partir_das: str = "") -> dict:
    atividades = _carregar_atividades()
    encontradas = []
    for a in atividades:
        if termo and _normalizar(termo) not in _normalizar(a["titulo"] + " " + a["trilha"]):
            continue
        if dia and _normalizar(dia) not in _normalizar(a["dia"]):
            continue
        if trilha and _normalizar(trilha) not in _normalizar(a["trilha"]):
            continue
        if a_partir_das and a["inicio"] < a_partir_das:
            continue
        encontradas.append(a)
    return {"total": len(encontradas), "atividades": encontradas}


DECL_CONSULTAR_PROGRAMACAO = {
    "type": "function",
    "name": "consultar_programacao",
    "description": (
        "Busca atividades na programação oficial do evento. É a ÚNICA fonte confiável sobre "
        "palestras, oficinas, horários e salas. Todos os filtros são opcionais e podem ser combinados. "
        "Sem filtros, retorna a programação completa."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "termo": {"type": "string", "description": "Palavra-chave no título ou trilha, ex.: 'python', 'IA', 'agentes'"},
            "dia": {"type": "string", "enum": ["quinta", "sexta", "sábado"], "description": "Dia do evento"},
            "trilha": {"type": "string", "description": "Trilha temática, ex.: 'Inteligência Artificial', 'Cloud', 'Carreira'"},
            "a_partir_das": {"type": "string", "description": "Horário mínimo de início no formato HH:MM"},
        },
    },
}


# ════════════════════════════════════════════════════════════════
# FERRAMENTA 2 — Clima (API externa: Open-Meteo, sem chave)
# ════════════════════════════════════════════════════════════════
def previsao_do_tempo(cidade: str) -> dict:
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": cidade, "count": 1, "language": "pt", "countryCode": "BR"},
            timeout=TIMEOUT,
        ).json()
        if not geo.get("results"):
            return {"erro": f"Cidade '{cidade}' não encontrada no Brasil."}
        lugar = geo["results"][0]

        dados = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lugar["latitude"],
                "longitude": lugar["longitude"],
                "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                "forecast_days": 3,
                "timezone": "America/Recife",
            },
            timeout=TIMEOUT,
        ).json()
    except requests.RequestException as e:
        return {"erro": f"Serviço de clima indisponível no momento: {e.__class__.__name__}"}

    atual, dias = dados["current"], dados["daily"]
    return {
        "cidade": f"{lugar['name']} - {lugar.get('admin1', '')}",
        "agora": {
            "temperatura_c": atual["temperature_2m"],
            "umidade_pct": atual["relative_humidity_2m"],
            "chuva_mm": atual["precipitation"],
            "vento_kmh": atual["wind_speed_10m"],
            "medido_em": atual["time"],
        },
        "proximos_dias": [
            {"data": d, "max_c": mx, "min_c": mn, "chance_chuva_pct": pc}
            for d, mx, mn, pc in zip(dias["time"], dias["temperature_2m_max"],
                                     dias["temperature_2m_min"], dias["precipitation_probability_max"])
        ],
        "fonte": "open-meteo.com",
    }


DECL_PREVISAO_DO_TEMPO = {
    "type": "function",
    "name": "previsao_do_tempo",
    "description": "Clima atual e previsão para os próximos 3 dias de uma cidade brasileira (temperatura e chance de chuva).",
    "parameters": {
        "type": "object",
        "properties": {"cidade": {"type": "string", "description": "Nome da cidade, ex.: Recife"}},
        "required": ["cidade"],
    },
}


# ════════════════════════════════════════════════════════════════
# FERRAMENTA 3 — Endereço por CEP (API externa: ViaCEP, sem chave)
# ════════════════════════════════════════════════════════════════
def buscar_endereco_por_cep(cep: str) -> dict:
    somente_digitos = re.sub(r"\D", "", cep or "")
    if len(somente_digitos) != 8:  # validação ANTES de chamar a API
        return {"erro": "CEP inválido. Um CEP tem exatamente 8 dígitos, ex.: 50030-230."}
    try:
        dados = requests.get(f"https://viacep.com.br/ws/{somente_digitos}/json/", timeout=TIMEOUT).json()
    except requests.RequestException as e:
        return {"erro": f"Serviço de CEP indisponível: {e.__class__.__name__}"}
    if dados.get("erro"):
        return {"erro": f"CEP {somente_digitos} não existe na base dos Correios."}
    return {k: dados.get(k) for k in ("cep", "logradouro", "bairro", "localidade", "uf")}


DECL_BUSCAR_ENDERECO_POR_CEP = {
    "type": "function",
    "name": "buscar_endereco_por_cep",
    "description": "Converte um CEP brasileiro em endereço (rua, bairro, cidade e UF).",
    "parameters": {
        "type": "object",
        "properties": {"cep": {"type": "string", "description": "CEP com ou sem hífen, ex.: 50030-230"}},
        "required": ["cep"],
    },
}


# ════════════════════════════════════════════════════════════════
# FERRAMENTA 4 — Adicionar à minha agenda (uma AÇÃO que muda o mundo)
# ════════════════════════════════════════════════════════════════
def adicionar_na_minha_agenda(id_atividade: str) -> dict:
    atividades = {a["id"]: a for a in _carregar_atividades()}
    id_atividade = (id_atividade or "").strip().upper()

    # Guardrail anti-alucinação: só aceitamos ids que EXISTEM
    if id_atividade not in atividades:
        return {"erro": f"Não existe atividade com id '{id_atividade}'. Consulte a programação primeiro."}

    agenda = _ler_agenda()
    if id_atividade in agenda:
        return {"ok": False, "mensagem": "Essa atividade já está na sua agenda."}

    nova = atividades[id_atividade]
    conflitos = [atividades[i] for i in agenda if i in atividades and _conflita(nova, atividades[i])]
    if conflitos:  # Regra de negócio: não deixamos marcar duas coisas no mesmo horário
        return {
            "ok": False,
            "mensagem": "Conflito de horário. Nada foi adicionado.",
            "conflita_com": [{"id": c["id"], "titulo": c["titulo"], "inicio": c["inicio"], "fim": c["fim"]} for c in conflitos],
        }

    agenda.append(id_atividade)
    _salvar_agenda(agenda)
    return {"ok": True, "adicionada": nova, "total_na_agenda": len(agenda)}


DECL_ADICIONAR_NA_MINHA_AGENDA = {
    "type": "function",
    "name": "adicionar_na_minha_agenda",
    "description": (
        "Salva uma atividade na agenda pessoal do usuário. Só use quando o usuário pedir claramente "
        "para adicionar/salvar/marcar. Exige o id exato (ex.: 'A04') obtido em consultar_programacao. "
        "Recusa automaticamente se houver conflito de horário."
    ),
    "parameters": {
        "type": "object",
        "properties": {"id_atividade": {"type": "string", "description": "Id da atividade, ex.: A04"}},
        "required": ["id_atividade"],
    },
}


# ════════════════════════════════════════════════════════════════
# FERRAMENTA 5 — Ver minha agenda
# ════════════════════════════════════════════════════════════════
def ver_minha_agenda() -> dict:
    atividades = {a["id"]: a for a in _carregar_atividades()}
    itens = [atividades[i] for i in _ler_agenda() if i in atividades]
    ordem_dias = {"quinta": 0, "sexta": 1, "sábado": 2}
    itens.sort(key=lambda a: (ordem_dias.get(a["dia"], 9), a["inicio"]))
    return {"total": len(itens), "atividades": itens}


DECL_VER_MINHA_AGENDA = {
    "type": "function",
    "name": "ver_minha_agenda",
    "description": "Lista as atividades que o usuário já salvou na agenda pessoal, em ordem cronológica.",
    "parameters": {"type": "object", "properties": {}},
}


# ════════════════════════════════════════════════════════════════
# Registro: juntamos tudo num lugar só
# ════════════════════════════════════════════════════════════════
DECLARACOES = [
    DECL_CONSULTAR_PROGRAMACAO,
    DECL_PREVISAO_DO_TEMPO,
    DECL_BUSCAR_ENDERECO_POR_CEP,
    DECL_ADICIONAR_NA_MINHA_AGENDA,
    DECL_VER_MINHA_AGENDA,
]

FUNCOES = {
    "consultar_programacao": consultar_programacao,
    "previsao_do_tempo": previsao_do_tempo,
    "buscar_endereco_por_cep": buscar_endereco_por_cep,
    "adicionar_na_minha_agenda": adicionar_na_minha_agenda,
    "ver_minha_agenda": ver_minha_agenda,
}


def executar_ferramenta(nome: str, argumentos: dict) -> dict:
    """Executa a ferramenta pedida pelo modelo, sem nunca quebrar o agente."""
    funcao = FUNCOES.get(nome)
    if funcao is None:
        return {"erro": f"Ferramenta '{nome}' não existe."}
    try:
        return funcao(**(argumentos or {}))
    except TypeError as e:  # o modelo mandou um argumento com nome errado
        return {"erro": f"Argumentos inválidos para {nome}: {e}"}
    except Exception as e:  # qualquer outra falha vira informação, não crash
        return {"erro": f"Falha inesperada em {nome}: {e}"}
