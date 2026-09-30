---
title: Guia Rec'n'Play
emoji: 🤖
colorFrom: blue
colorTo: yellow
sdk: docker
app_port: 8000
pinned: false
---
<!-- O bloco acima é o cabeçalho exigido pelo Hugging Face Spaces (deploy opcional, veja docs/DEPLOY.md). -->

# 🤖 Workshop Prático: Construção de Agentes Autônomos com Gemini API e Function Calling

> **Rec'n'Play 2026 · 13h às 17h** · Oficina para quem está começando — nenhum conhecimento prévio de IA é necessário.
>
> Facilitação: **Petros Barreto** — Organizer do Google Developer Group Recife · Coordenador de Sistemas na Magalu Cloud · Professor Universitário (UNIT & UNIFG) · Mestrando no PPGEC/UPE

Ao final destas 4 horas você terá construído o **Guia Rec'n'Play**: um agente que conversa em português, consulta a programação do evento, busca o clima em tempo real, converte CEP em endereço, salva atividades na sua agenda recusando conflitos de horário, e **não inventa** informação.

E você sai com ele **pronto e seu**: no seu GitHub, com interface web e rodando em Docker.

---

## 📍 Mapa da oficina

| Horário | Módulo | O que você vai fazer | Pasta |
|---|---|---|---|
| 13:00 | Boas-vindas | Editor, terminal, API e chave; criar seu repositório e testar | `00_setup/` |
| 13:25 | Fundamentos | O que é LLM, token, prompt, alucinação e agente | — (slides) |
| 13:40 | 1 · Primeira chamada | Falar com o Gemini, criar memória e ver uma alucinação ao vivo | `01_primeira_chamada/` |
| 14:10 | 2 · Structured outputs | Transformar texto bagunçado em dados confiáveis com Pydantic | `02_structured_outputs/` |
| 14:40 | ☕ Intervalo | 15 minutos | — |
| 14:55 | 3 · Function calling | Os 4 passos: declarar, pedir, executar, devolver | `03_function_calling/` |
| 15:25 | 4 · O agente | Laço autônomo, 5 ferramentas, guardrails anti-alucinação | `04_agente/` |
| 16:05 | 5 · Web, Docker e GitHub | Interface de chat, container e push para o seu GitHub | `05_web/`, `Dockerfile` |
| 16:40 | Desafios | Estenda o agente com uma ferramenta sua | `06_desafios/` |
| 16:50 | Encerramento | Limpar o computador do laboratório e próximos passos | — |

> 💾 **Ao fim de cada módulo:** `git add .` → `git commit -m "módulo X"` → `git push`. Passo a passo em [`docs/GITHUB.md`](docs/GITHUB.md).

---

## 🧰 Antes de começar (10 minutos)

> Nunca programou? Leia primeiro [`docs/PRIMEIROS_PASSOS.md`](docs/PRIMEIROS_PASSOS.md): editor, terminal, API, chave e Python básico.

### No laboratório (git, python e docker já instalados)
1. Em uma **janela anônima**, entre no GitHub, abra `https://github.com/petrosbarreto/oficina-agentes-gemini` e clique em **Use this template › Create a new repository** (nome sugerido: `meu-agente-gemini`).
2. No terminal:
```bash
git clone https://github.com/SEU_USUARIO/meu-agente-gemini.git
cd meu-agente-gemini
git config --local user.name "Seu Nome"
git config --local user.email "SEU_USUARIO@users.noreply.github.com"

python -m venv .venv
#    Windows (PowerShell):   .venv\Scripts\Activate.ps1   (ou no cmd: .venv\Scripts\activate.bat)
#    Linux / macOS:          source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # no Windows: copy .env.example .env
#    abra o .env e cole sua chave em GEMINI_API_KEY

python 00_setup/verificar_ambiente.py
```

### Plano B — Google Colab
Se algo travar, abra `oficina_colab.ipynb` no [Google Colab](https://colab.research.google.com), salve sua chave em **Secrets 🔑** como `GEMINI_API_KEY` e rode as células em ordem.

### 🔑 Como gerar a chave da API (gratuita)
1. Acesse **https://aistudio.google.com/apikey** e entre com sua conta Google.
2. Clique em **Create API key** / **Criar chave de API**.
3. Copie a chave e cole no `.env`. **Nunca** publique essa chave no GitHub (o `.gitignore` já protege o `.env`).

---

## 📚 Os módulos, um a um

### Módulo 1 — Primeira chamada
```bash
python 01_primeira_chamada/ola_gemini.py            # uma pergunta, uma resposta
python 01_primeira_chamada/conversa_com_memoria.py  # chat que lembra do contexto
python 01_primeira_chamada/demo_alucinacao.py       # o modelo inventando coisas 😬
```
**Você aprende:** cliente, modelo, `input`, `output_text`, `steps`, `system_instruction` e `previous_interaction_id`.

### Módulo 2 — Structured outputs
```bash
python 02_structured_outputs/extrair_palestra.py    # post de Instagram → objeto Python
python 02_structured_outputs/triagem_feedback.py    # classificar e automatizar decisões
```
**Você aprende:** schemas com Pydantic, `Literal` para categorias, `response_format`, validação.

### Módulo 3 — Function calling
```bash
python 03_function_calling/clima_passo_a_passo.py   # clima real de Recife e Caruaru
```
**Você aprende:** o modelo não executa nada, ele *pede*. Seu código executa e devolve com `function_result` + `call_id`.

### Módulo 4 — O agente autônomo
```bash
python 04_agente/main.py
```
| Arquivo | Papel |
|---|---|
| `ferramentas.py` | As 5 ferramentas + suas declarações. Cada uma valida entradas e devolve `{"erro": ...}` em vez de quebrar. |
| `agente.py` | O laço do agente, as regras de sistema e a saída estruturada opcional (`/json`). |
| `main.py` | A interface de conversa no terminal. |
| `dados/programacao.json` | Programação **fictícia** de exemplo (troque pela oficial se quiser). |

**Roteiro de teste** (digite no chat, nesta ordem):
1. `Quais oficinas de IA tem na sexta?`
2. `Vai chover em Recife nos próximos dias?`
3. `Me mostra oficinas para iniciantes na quinta e adiciona a de agentes na minha agenda`
4. `Adiciona também a A03` → observe o **conflito de horário** sendo recusado pelo código
5. `Adiciona a Z99` → id inexistente: o agente precisa admitir, não inventar
6. `Monte meu sábado com algo de IA e algo de carreira, sem conflito, e diga se levo guarda-chuva`
7. `/json` → a mesma resposta como dado estruturado

### Módulo 5 — Do terminal para o mundo
```bash
# Interface web no navegador
uvicorn app:app --app-dir 05_web --reload        # abra http://localhost:8000

# O mesmo agente em um container Docker
docker build -t guia-recnplay .
docker run --rm -p 8000:8000 --env-file .env guia-recnplay
#   ou simplesmente:  docker compose up --build

# Seu código no seu GitHub
git add . && git commit -m "meu agente com interface web" && git push
```
**Você aprende:** transformar o agente em serviço (FastAPI), por que a chave fica no servidor, empacotar com Docker e versionar com Git.
Quer um link público? Veja [`docs/DEPLOY.md`](docs/DEPLOY.md) (Hugging Face Spaces, gratuito).

### Testes automáticos (sem chave, sem internet)
```bash
pytest -q
```
Inclui um teste do **laço do agente** e da **interface web** com um modelo de mentira — ótimo para entender o fluxo.

### 🧹 Antes de sair do laboratório
```bash
python 00_setup/limpar_computador.py
```
Confere se tudo foi enviado ao GitHub, apaga seu `.env`, remove o container e desconecta sua conta do GitHub neste computador.

---

## 🛡️ Como este agente evita alucinações

1. **Fontes únicas de verdade:** fatos só vêm das ferramentas (regra 1 do `INSTRUCOES`).
2. **Validação no código:** CEP com 8 dígitos, id que existe, conflito de horário. O modelo não consegue "forçar" uma ação inválida.
3. **Erros viram dados:** a ferramenta devolve `{"erro": "..."}` e o modelo conta a verdade ao usuário.
4. **Limite de passos:** `MAX_PASSOS = 8` impede laços infinitos.
5. **Structured outputs:** a resposta final pode sair em JSON validado, com campo de `confianca`.
6. **Auditoria:** cada passo aparece no terminal (`🔧 passo 1: ...`).

---

## 📂 Estrutura
```
meu-agente-gemini/
├── comum.py                    # cliente, modelo e cores do terminal
├── oficina_colab.ipynb         # a oficina inteira em um notebook (plano B)
├── Dockerfile · docker-compose.yml
├── 00_setup/                   # checar ambiente, checar laboratório, limpar computador
├── 01_primeira_chamada/        # chamadas, memória, alucinação
├── 02_structured_outputs/      # Pydantic + response_format
├── 03_function_calling/        # os 4 passos, sem mágica
├── 04_agente/                  # o agente completo
├── 05_web/                     # FastAPI + interface de chat
├── 06_desafios/                # exercícios para ir além
├── tests/                      # testes automáticos (sem chave, sem internet)
└── docs/                       # GitHub, laboratório, deploy, glossário, problemas comuns, roteiro
```

## 🔗 Para continuar estudando
- Documentação oficial de function calling: https://ai.google.dev/gemini-api/docs/function-calling
- Structured outputs: https://ai.google.dev/gemini-api/docs/structured-output
- Interactions API: https://ai.google.dev/gemini-api/docs/interactions-overview
- Cookbook oficial com notebooks: https://github.com/google-gemini/cookbook
- Comunidade: **GDG Recife** — participe dos próximos encontros e do DevFest!

> Tecnologia usada: SDK `google-genai` (≥ 2.3) com a **Interactions API** e o modelo `gemini-3.8-flash` (configurável no `.env`). APIs públicas sem chave: [Open-Meteo](https://open-meteo.com) e [ViaCEP](https://viacep.com.br).
