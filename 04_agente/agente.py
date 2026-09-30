"""
agente.py — o "cérebro + laço" do agente autônomo.

O que torna isto um AGENTE (e não só um chatbot)?
  1. Ele tem um OBJETIVO (a pergunta do usuário)
  2. Ele tem FERRAMENTAS (ferramentas.py)
  3. Ele roda em LAÇO: pensa → pede ferramenta → recebe resultado → pensa de novo...
     até decidir que já tem o suficiente para responder.

      ┌─────────────┐   function_call   ┌──────────────┐
      │   Gemini    │ ────────────────▶ │  Nosso código │
      │  (decide)   │ ◀──────────────── │  (executa)    │
      └─────────────┘  function_result  └──────────────┘
             │  sem mais pedidos?
             ▼
      resposta final ao usuário

Proteções contra "agente descontrolado" e alucinação:
  • MAX_PASSOS: limite de voltas no laço (evita loops infinitos e contas altas)
  • INSTRUCOES: regras claras de só afirmar o que veio das ferramentas
  • Erros das ferramentas voltam como dados, para o modelo admitir a falha
  • Registro (log) de cada passo, para você auditar o que aconteceu
"""
import json
import sys
from pathlib import Path
from typing import List, Literal

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import MODELO, cor  # noqa: E402
from ferramentas import DECLARACOES, executar_ferramenta  # noqa: E402

MAX_PASSOS = 8

INSTRUCOES = """
Você é o Guia Rec'n'Play, um assistente que ajuda participantes do evento em Recife.

REGRAS OBRIGATÓRIAS:
1. Informações sobre programação, horários, salas, clima e endereços SÓ podem vir das ferramentas.
   Nunca invente atividades, horários, ids, temperaturas ou endereços.
2. Se uma ferramenta devolver "erro" ou nenhum resultado, diga isso com honestidade
   e sugira o que o usuário pode fazer.
3. Se faltar informação para agir (ex.: qual atividade adicionar), PERGUNTE antes de agir.
4. Só use adicionar_na_minha_agenda quando o usuário pedir claramente.
5. Você pode encadear várias ferramentas para resolver uma tarefa complexa.
6. Responda em português do Brasil, de forma curta e organizada. Cite ids das atividades (ex.: A04).
"""


class RespostaEstruturada(BaseModel):
    """Formato final opcional, útil para exibir em um app ou salvar em banco."""
    resposta: str = Field(description="Resposta final para o usuário, em português")
    ferramentas_usadas: List[str] = Field(description="Nomes das ferramentas usadas para chegar na resposta")
    ids_atividades_citadas: List[str] = Field(description="Ids de atividades mencionadas, ex.: ['A04']")
    confianca: Literal["alta", "media", "baixa"] = Field(
        description="alta se tudo veio das ferramentas; baixa se faltou dado ou houve erro"
    )
    proxima_acao_sugerida: str = Field(description="Uma sugestão curta do que o usuário pode fazer em seguida")


class Agente:
    def __init__(self, cliente, verboso: bool = True):
        self.cliente = cliente
        self.verboso = verboso
        self.id_conversa = None  # guarda o id da última interação (memória da conversa)
        self.ferramentas_usadas: list[str] = []
        self.passos: list[dict] = []  # registro do último turno (usado pela interface web)

    # ───────────────────────── utilitário de log ─────────────────────────
    def _log(self, texto: str):
        if self.verboso:
            print(cor(f"   {texto}", "cinza"))

    # ───────────────────────── chamada ao modelo ─────────────────────────
    def _chamar_modelo(self, entrada):
        parametros = dict(
            model=MODELO,
            input=entrada,
            tools=DECLARACOES,            # interaction-scoped: vai em TODA chamada
            system_instruction=INSTRUCOES,  # idem
        )
        if self.id_conversa:
            parametros["previous_interaction_id"] = self.id_conversa
        interaction = self.cliente.interactions.create(**parametros)
        self.id_conversa = interaction.id
        return interaction

    # ───────────────────────── O LAÇO DO AGENTE ─────────────────────────
    def perguntar(self, pergunta: str) -> str:
        self.ferramentas_usadas = []
        self.passos = []
        interaction = self._chamar_modelo(pergunta)

        for passo in range(1, MAX_PASSOS + 1):
            pedidos = [s for s in interaction.steps if s.type == "function_call"]

            # Condição de parada: o modelo não pediu mais nada → terminou
            if not pedidos:
                return interaction.output_text

            # Executa TODOS os pedidos deste passo (podem vir vários em paralelo)
            resultados = []
            for pedido in pedidos:
                self._log(f"🔧 passo {passo}: {pedido.name}({json.dumps(pedido.arguments, ensure_ascii=False)})")
                resultado = executar_ferramenta(pedido.name, pedido.arguments)
                self.ferramentas_usadas.append(pedido.name)
                self.passos.append({"passo": passo, "ferramenta": pedido.name,
                                    "argumentos": pedido.arguments, "resultado": resultado})
                resumo = json.dumps(resultado, ensure_ascii=False)
                self._log(f"   ↳ {resumo[:160]}{'…' if len(resumo) > 160 else ''}")
                resultados.append({
                    "type": "function_result",
                    "name": pedido.name,
                    "call_id": pedido.id,
                    "result": [{"type": "text", "text": json.dumps(resultado, ensure_ascii=False)}],
                })

            # Devolve os resultados e deixa o modelo decidir o próximo passo
            interaction = self._chamar_modelo(resultados)

        # Se chegou aqui, estourou o limite de passos
        return ("Desculpe, não consegui concluir essa tarefa dentro do limite de "
                f"{MAX_PASSOS} passos. Tente dividir o pedido em partes menores.")

    # ───────────── Saída estruturada da última resposta (bônus) ─────────────
    def resumir_em_json(self) -> RespostaEstruturada:
        """Pede ao modelo para reescrever a ÚLTIMA resposta no formato RespostaEstruturada.

        Usamos previous_interaction_id para ele enxergar tudo o que aconteceu
        (inclusive os resultados das ferramentas), e response_format para
        garantir um JSON válido.
        """
        interaction = self.cliente.interactions.create(
            model=MODELO,
            previous_interaction_id=self.id_conversa,
            input=(
                "Reescreva sua última resposta no formato JSON pedido. "
                f"Ferramentas usadas neste turno: {sorted(set(self.ferramentas_usadas))}."
            ),
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": RespostaEstruturada.model_json_schema(),
            },
        )
        return RespostaEstruturada.model_validate_json(interaction.output_text)
