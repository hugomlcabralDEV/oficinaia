# 🎤 Roteiro do instrutor — minuto a minuto

**Oficina:** Workshop Prático: Construção de Agentes Autônomos com Gemini API e Function Calling
**Evento:** Rec'n'Play 2026 · **Local:** laboratório de informática (git, python, docker instalados)
**Duração:** 13:00–17:00 · **Público:** iniciantes · **Facilitador:** Petros Barreto

> Regra de ouro para turma iniciante: **explique → mostre rodando → deixe rodar → pergunte**. Rode os scripts prontos e comente linha a linha. E a cada módulo: **commit e push**.

---

## ✅ Checklist da semana anterior
- [ ] Publicar o template no GitHub e marcar *Template repository* (`docs/PUBLICAR_REPOSITORIO.md`)
- [ ] Enviar `docs/LABORATORIO.md` à equipe técnica e pedir `python 00_setup/checar_laboratorio.py` em todas as máquinas
- [ ] Confirmar: VS Code instalado, Docker Desktop rodando para o usuário do aluno, `python:3.12-slim` pré-baixado
- [ ] Perguntar à equipe se as máquinas são restauradas ao reiniciar (Deep Freeze)
- [ ] Enviar `docs/PRE_OFICINA.md` aos inscritos (conta GitHub + chave da API)
- [x] Link do template e QR Code nos slides 9 e 51

## ✅ Checklist do dia (chegar 30 min antes)
- [ ] Rodar `verificar_ambiente.py` e `docker compose up --build` em uma máquina do laboratório
- [ ] Ter **2 chaves de API reserva** para quem travar no cadastro
- [ ] Fonte do terminal em 20pt+ na máquina do projetor
- [ ] Apagar `04_agente/dados/minha_agenda.json` antes da demo
- [ ] Monitores briefados: cada um cuida de 1 fileira; sinal de ajuda = tampa do monitor/post-it
- [ ] Plano B de cota: `GEMINI_MODEL=gemini-3.5-flash-lite` no `.env`

---

## 13:00 · Boas-vindas, primeiros conceitos e setup (25 min) — slides 1 a 9
- Apresentação (slide 2). Quebra-gelo: "quem já usou um chatbot? E quem já **programou** um?"
- Mostre o resultado final primeiro (slide 4): abra a interface web (`uvicorn app:app --app-dir 05_web`) e faça a pergunta do sábado.
- **Base para quem nunca programou (slides 5 a 8, ~10 min):**
  - Slide 5: editor, terminal e resultado. Mostre o VS Code ao vivo: abrir pasta, abrir arquivo, abrir terminal.
  - Slide 6: API = garçom; chave = comanda.
  - Slide 7: gerar a chave no AI Studio, **todos juntos**, na tela do projetor.
  - Slide 8: guardar a chave no `.env`. Erros comuns: espaço, aspas, não salvar o arquivo.
- Setup (slide 9): template → clone → `git config --local` → venv → `pip install` → `.env` → `verificar_ambiente.py`.
- **Checkpoint:** 80% com "🎉 Tudo pronto!". Quem travar no GitHub segue e o monitor resolve em paralelo; quem travar no Python vai para o Colab.

## 13:25 · Fundamentos (15 min) — slides 10 a 15
- LLM = autocompletar gigante. Token, prompt, modelo.
- **Alucinação:** sempre responde algo plausível, mesmo sem saber.
- Agente = LLM + ferramentas + laço + objetivo (analogia do estagiário com telefone).

## 13:40 · Módulo 1 (30 min) — slides 16 a 23
1. Python em 2 minutos (slide 17): comentário, texto, variável, função, import, ponto.
2. `ola_gemini.py` (slides 18 a 20, 10 min): visão geral → linha por linha → rodar e ler o resultado. **Mão na massa:** cada um troca o `input` por uma pergunta sua.
3. `interaction` (slide 21): `steps` e `id`.
4. `conversa_com_memoria.py` (slide 22, 7 min): "meu nome é Ana" → "qual meu nome?"; depois sem `previous_interaction_id`.
5. `demo_alucinacao.py` (slide 23, 5 min): "como você saberia qual está certa?".
6. 💾 `git commit -m "módulo 1"` + `git push` — **o primeiro push abre o login do GitHub: faça junto com a turma**.

## 14:10 · Módulo 2 (30 min) — slides 24 a 28
1. Texto informal → quais campos um app precisa?
2. `extrair_palestra.py`: `Field(description=...)` e `Literal`.
3. **Mão na massa (10 min):** campo `precisa_notebook: bool`.
4. `triagem_feedback.py`: "o modelo interpreta, o código decide".
5. 💾 commit + push.

## 14:40 · Intervalo (15 min) — slide 29
- Monitores ajudam quem ficou para trás, principalmente no `git push`.

## 14:55 · Módulo 3 (30 min) — slides 30 a 34
- Desenhe os **4 passos** (slide 31) no quadro antes do código.
- `clima_passo_a_passo.py`: pare em cada `PASSO`; chamadas paralelas (Recife e Caruaru); `call_id`; `tools` em toda chamada.
- 💾 commit + push.

## 15:25 · Módulo 4 (40 min) — slides 35 a 41
1. `ferramentas.py` (8 min): validação, `{"erro": ...}`, conflito de horário.
2. `agente.py` (8 min): o laço e a condição de parada.
3. `main.py` com as 7 perguntas do slide 40 (15 min). Leia o log `🔧 passo`.
4. `pytest -q` (4 min).
5. **Personalização (5 min):** cada um muda a persona em `INSTRUCOES` e o `AGENTE_NOME` no `.env`. Agora o agente é **deles**.
6. 💾 `git commit -m "módulo 4: meu agente"` + push.

## 16:05 · Módulo 5 (35 min) — slides 42 a 47
1. Arquitetura web e a regra da chave no servidor (slides 43–44, 5 min).
2. Todos rodam `uvicorn app:app --app-dir 05_web --reload` e usam a interface (10 min).
3. Docker (slide 45, 10 min): `docker build` e `docker run --env-file .env`. **Se o Docker de alguma máquina falhar, siga sem ele** — o uvicorn já basta.
4. GitHub (slide 46, 5 min): commit + push; cada um abre o repositório no celular.
5. Deploy (slide 47, 5 min): só mostrar; fica como tarefa de casa (`docs/DEPLOY.md`).

## 16:40 · Desafios (10 min) — slide 48
- Nível 1 de `06_desafios/DESAFIOS.md`. Quem terminar faz commit + push. 2 voluntários mostram.

## 16:50 · Encerramento (10 min) — slides 49 a 51
- Slide 49: **"o modelo decide, o código executa, os dados provam"**.
- Slide 50: **limpeza guiada**, item por item. Monitores só liberam quem mostrar o repositório no celular.
- Slide 51: feedback, GDG Recife, DevFest, foto da turma.

---

## 🆘 Problemas frequentes na sala
| Sintoma | Ação rápida |
|---|---|
| `429` / quota | Trocar `GEMINI_MODEL` no `.env` ou usar chave reserva |
| `403` / chave inválida | Chave copiada com espaço? Gerar outra no AI Studio |
| `ModuleNotFoundError` | venv não ativado → ativar e `pip install -r requirements.txt` |
| PowerShell bloqueia `Activate.ps1` | Use o cmd com `.venv\Scripts\activate.bat`, ou `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `git push` pede senha e recusa | Senha do GitHub não funciona no terminal: usar o login do navegador ou um token (`docs/GITHUB.md`) |
| `git push` rejeitado (repo de outra pessoa) | Clonou o template em vez do próprio repo → `git remote set-url origin https://github.com/SEU_USUARIO/meu-agente-gemini.git` |
| `docker: permission denied` / daemon não roda | Seguir sem Docker (uvicorn local) e avisar a equipe técnica |
| `localhost:8000` não abre | Porta ocupada: `--port 8001`; ou firewall local |
| Rede bloqueia tudo | Colab com `oficina_colab.ipynb` |
