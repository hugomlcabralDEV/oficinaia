"""
MÓDULO 2.1 — Structured Outputs: do texto bagunçado para dados organizados.

Rode com:  python 02_structured_outputs/extrair_palestra.py

Problema: texto livre é ótimo para humanos e péssimo para programas.
Se pedimos "me dê em JSON", o modelo PODE obedecer... ou mandar um JSON quebrado.

Solução: descrever o formato com Pydantic e passar como response_format.
A API então é OBRIGADA a devolver um JSON que segue esse schema.

Conceitos:
  • schema      → a "forma" que os dados precisam ter (campos + tipos)
  • Pydantic    → biblioteca Python para   declarar schemas como classes
  • Field(description=...) → explica cada campo para o modelo (ajuda muito!)
  • model_validate_json → converte o texto JSON em um objeto Python validado

"""
import sys
from pathlib import Path
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from comum import MODELO, criar_cliente, titulo, ok, cor


# 1) Descrevemos o FORMATO que queremos receber
class Palestrante(BaseModel):
    nome: str = Field(description="Nome completo da pessoa palestrante")
    cargo: Optional[str] = Field(default=None, description="Cargo ou empresa, se mencionado")


class Palestra(BaseModel):
    titulo: str = Field(description="Título da atividade")
    tipo: Literal["palestra", "oficina", "painel", "outro"] = Field(description="Formato da atividade")
    horario_inicio: str = Field(description="Horário de início no formato HH:MM (24h)")
    duracao_minutos: int = Field(description="Duração total em minutos")
    local: str = Field(description="Sala ou espaço onde acontece")
    palestrantes: List[Palestrante]
    publico_iniciante: bool = Field(description="True se o texto indica que iniciantes são bem-vindos")
    temas: List[str] = Field(description="De 2 a 5 palavras-chave sobre o conteúdo")


# 2) Um texto "do mundo real", escrito do jeito que as pessoas escrevem
TEXTO = """
Galeraaa!! 🚀 Amanhã tem oficina massa no Rec'n'Play: "Construindo agentes com Gemini"
com a Ana Beatriz (dev na Acme Tech) e o Carlos Lima. Começa 1 da tarde e vai até
às 5, lá na sala Frevo, 2º andar. Não precisa saber IA não, é pra quem tá começando!
Vai rolar function calling, APIs e structured outputs. Leva o notebook 💻
"""

cliente = criar_cliente()
titulo("Extraindo dados estruturados de um post informal")

# 3) Pedimos a extração passando o schema em response_format
interaction = cliente.interactions.create(
    model=MODELO,
    input=f"Extraia as informações da atividade descrita neste texto:\n{TEXTO}",
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Palestra.model_json_schema(),
    },
)

print(cor("JSON bruto devolvido pela API:", "cinza"))
print(interaction.output_text)

# 4) Validamos: se algo estiver fora do schema, o Pydantic acusa o erro aqui
palestra = Palestra.model_validate_json(interaction.output_text)

print()
ok("Agora é um objeto Python de verdade. Veja como é fácil usar:")
print(f"   Título:     {palestra.titulo}")
print(f"   Início:     {palestra.horario_inicio}  ({palestra.duracao_minutos} min)")
print(f"   Local:      {palestra.local}")
print(f"   Quem:       {', '.join(p.nome for p in palestra.palestrantes)}")
print(f"   Iniciante?  {'Sim' if palestra.publico_iniciante else 'Não'}")
print(f"   Temas:      {palestra.temas}")
