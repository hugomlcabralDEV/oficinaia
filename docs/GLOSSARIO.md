# 📖 Glossário para iniciantes

| Termo | Em uma frase | Exemplo |
|---|---|---|
| **IA generativa** | IA que cria conteúdo novo (texto, imagem, código). | Pedir um resumo de um artigo. |
| **LLM** | *Large Language Model*: modelo treinado em muito texto que prevê a próxima palavra. | O Gemini. |
| **Token** | Pedaço de texto que o modelo processa (≈ ¾ de palavra). A cobrança e os limites são em tokens. | "Recife" pode ser 1 ou 2 tokens. |
| **Prompt** | A instrução/pergunta que você envia. | "Explique API em 3 frases." |
| **System instruction** | Regras permanentes de comportamento enviadas junto do prompt. | "Responda sempre em português." |
| **API** | Um "balcão de atendimento" entre programas: você pede de um jeito combinado e recebe uma resposta. | ViaCEP devolve o endereço de um CEP. |
| **Chave de API** | Senha que identifica você na API. Nunca publique. | `GEMINI_API_KEY` no `.env`. |
| **SDK** | Biblioteca que facilita usar uma API numa linguagem. | `google-genai` para Python. |
| **Interaction** | Um turno completo com o Gemini: tem `id`, `steps` e `output_text`. | `cliente.interactions.create(...)` |
| **Step (passo)** | Cada etapa dentro de uma interaction: pensamento, pedido de função, texto final. | `function_call`, `model_output` |
| **Alucinação** | Resposta confiante e errada, inventada pelo modelo. | Inventar o horário de uma palestra. |
| **Structured output** | Forçar a resposta a seguir um formato JSON definido por você. | Schema Pydantic `Palestra`. |
| **JSON** | Formato de texto para dados: chaves e valores. | `{"cidade": "Recife"}` |
| **Schema** | A "forma" que os dados devem ter: campos e tipos. | `titulo: str`, `duracao: int` |
| **Pydantic** | Biblioteca Python para declarar e validar schemas como classes. | `class Palestra(BaseModel)` |
| **Function calling** | O modelo pede para uma função sua ser executada, com argumentos estruturados. | `previsao_do_tempo(cidade="Recife")` |
| **Declaração de função** | O "cardápio" da ferramenta: nome, descrição e parâmetros. | `DECL_PREVISAO_DO_TEMPO` |
| **call_id** | Identificador que liga o resultado ao pedido de função correto. | `"call_id": pedido.id` |
| **Agente** | LLM + ferramentas + laço + objetivo: decide sozinho os próximos passos. | O Guia Rec'n'Play. |
| **Laço do agente** | Repetir "modelo pede → código executa → modelo decide" até terminar. | `for passo in range(MAX_PASSOS)` |
| **Guardrail** | Proteção que limita o que o agente pode fazer ou afirmar. | Recusar id inexistente. |
| **Grounding** | Ancorar a resposta em dados reais de uma fonte. | Clima vindo da Open-Meteo. |
| **Ambiente virtual (venv)** | Pasta isolada com as bibliotecas de um projeto. | `.venv/` |
| **Mock** | Uma imitação usada em testes no lugar do serviço real. | `ClienteFalso` em `tests/`. |
