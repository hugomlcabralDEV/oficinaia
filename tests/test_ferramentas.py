"""
Testes automáticos das ferramentas e do laço do agente — rodam SEM chave e SEM internet.

Rode com:  pytest -q

Por que testar? Porque o modelo é imprevisível, mas as ferramentas NÃO podem ser.
Se a ferramenta está certa e bem testada, o agente fica muito mais confiável.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "04_agente"))

import ferramentas  # noqa: E402
from agente import Agente  # noqa: E402


def _agenda_temporaria(tmp_path, monkeypatch):
    monkeypatch.setattr(ferramentas, "ARQUIVO_AGENDA", tmp_path / "agenda.json")


def test_busca_sem_acento_e_por_dia():
    r = ferramentas.consultar_programacao(termo="inteligencia artificial", dia="sexta")
    assert r["total"] == 2
    assert {a["id"] for a in r["atividades"]} == {"A07", "A10"}


def test_busca_sem_filtros_retorna_tudo():
    assert ferramentas.consultar_programacao()["total"] == 14


def test_id_inexistente_e_recusado(tmp_path, monkeypatch):
    _agenda_temporaria(tmp_path, monkeypatch)
    assert "erro" in ferramentas.adicionar_na_minha_agenda("Z99")


def test_conflito_de_horario(tmp_path, monkeypatch):
    _agenda_temporaria(tmp_path, monkeypatch)
    assert ferramentas.adicionar_na_minha_agenda("a04")["ok"] is True  # minúsculo também vale
    r = ferramentas.adicionar_na_minha_agenda("A03")  # 14h, dentro da oficina 13h-17h
    assert r["ok"] is False and r["conflita_com"][0]["id"] == "A04"
    assert ferramentas.ver_minha_agenda()["total"] == 1


def test_cep_invalido_nem_chama_a_api():
    assert "erro" in ferramentas.buscar_endereco_por_cep("123")


def test_ferramenta_desconhecida_nao_quebra():
    assert "erro" in ferramentas.executar_ferramenta("hackear_nasa", {})
    assert "erro" in ferramentas.executar_ferramenta("ver_minha_agenda", {"parametro_errado": 1})


# ─── Teste do LAÇO do agente com um "modelo de mentira" (mock) ───
class ClienteFalso:
    """Simula a API: 1ª chamada pede uma ferramenta, 2ª chamada responde texto."""

    def __init__(self):
        self.chamadas = []
        self.interactions = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.chamadas.append(kwargs)
        if len(self.chamadas) == 1:
            pedido = SimpleNamespace(type="function_call", name="consultar_programacao",
                                     arguments={"dia": "sábado"}, id="call_1")
            return SimpleNamespace(id="int_1", steps=[pedido], output_text="")
        texto = SimpleNamespace(type="model_output")
        return SimpleNamespace(id="int_2", steps=[texto], output_text="No sábado tem A11, A12, A13 e A14.")


def test_laco_do_agente_executa_ferramenta_e_devolve_resultado():
    cliente = ClienteFalso()
    agente = Agente(cliente, verboso=False)
    resposta = agente.perguntar("O que tem no sábado?")

    assert "A13" in resposta
    assert agente.ferramentas_usadas == ["consultar_programacao"]
    segunda = cliente.chamadas[1]
    assert segunda["previous_interaction_id"] == "int_1"          # manteve a conversa
    assert segunda["input"][0]["type"] == "function_result"        # devolveu o resultado
    assert segunda["input"][0]["call_id"] == "call_1"              # para o pedido certo
    assert "tools" in segunda and "system_instruction" in segunda  # reenviou as regras
