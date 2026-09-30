# 🧯 Problemas comuns e soluções

**`✖ Chave da API não encontrada!`**
Você não criou o `.env` ou não colou a chave. Rode `cp .env.example .env` (Windows: `copy .env.example .env`) e edite o arquivo. A linha deve ficar `GEMINI_API_KEY=AIza...` sem aspas e sem espaços.

**`ModuleNotFoundError: No module named 'google'`**
O ambiente virtual não está ativado ou as bibliotecas não foram instaladas. Ative (`source .venv/bin/activate` ou `.venv\Scripts\Activate.ps1`) e rode `pip install -r requirements.txt`.

**`AttributeError: 'Client' object has no attribute 'interactions'`**
Sua versão do `google-genai` é antiga. Rode `pip install -U "google-genai>=2.3.0"`.

**Erro `429` / `RESOURCE_EXHAUSTED`**
Limite de uso do plano gratuito. Espere um minuto, ou troque o modelo no `.env` (ex.: `GEMINI_MODEL=gemini-3.5-flash-lite`).

**Erro `400` / `INVALID_ARGUMENT` citando o modelo**
O nome do modelo mudou ou não está disponível para sua conta. Veja a lista atual em https://ai.google.dev/gemini-api/docs/models e ajuste `GEMINI_MODEL`.

**Erro `403` / `PERMISSION_DENIED`**
Chave inválida ou de outro projeto. Gere uma nova em https://aistudio.google.com/apikey.

**Windows: "a execução de scripts foi desabilitada neste sistema"**
No PowerShell: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e confirme com `S`.

**`python` não é reconhecido (Windows)**
Reinstale o Python marcando *Add Python to PATH*, ou use `py` no lugar de `python`.

**A ferramenta de clima/CEP devolve `erro`**
A rede pode estar bloqueando `open-meteo.com` ou `viacep.com.br`. O agente vai admitir a falha (é o comportamento correto!). Teste a programação local, que não depende de internet.

**O agente respondeu sem usar ferramentas**
Melhore a `description` da ferramenta e seja explícito na pergunta. Descrições vagas geram decisões vagas.

## Git e Docker (laboratório)

**`git push` pede usuário e senha e recusa a senha**
O GitHub não aceita a senha da conta no terminal. Use o login pelo navegador (Git Credential Manager) ou crie um token em https://github.com/settings/tokens e cole no lugar da senha. Veja `docs/GITHUB.md`.

**`remote: Permission denied` ao dar push**
Você clonou o template em vez do seu repositório. Corrija com:
`git remote set-url origin https://github.com/SEU_USUARIO/meu-agente-gemini.git`

**`Cannot connect to the Docker daemon` / `permission denied`**
O Docker Desktop não está aberto ou seu usuário não tem permissão. Abra o Docker Desktop e espere ficar verde. Se não resolver, siga sem Docker: `uvicorn app:app --app-dir 05_web` faz o mesmo.

**`localhost:8000` não abre**
Outra coisa está usando a porta. Rode com `--port 8001` (uvicorn) ou `-p 8001:8000` (docker) e abra `localhost:8001`.
