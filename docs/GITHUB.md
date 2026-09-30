# 🐙 Seu código no seu GitHub — guia para participantes

A ideia é simples: **você trabalha no SEU repositório desde o primeiro minuto**. Assim, quando sair do laboratório, está tudo na sua conta.

## 1. Criar seu repositório a partir do template (navegador)
1. Abra uma **janela anônima** (o computador é compartilhado) e entre no https://github.com.
2. Acesse o template da oficina: `https://github.com/petrosbarreto/oficina-agentes-gemini`
3. Clique em **Use this template › Create a new repository**.
4. Nome sugerido: `meu-agente-gemini` · deixe **Public** (vira portfólio!) · **Create repository**.

## 2. Clonar para o computador (terminal)
```bash
cd Desktop        # ou outra pasta onde você tenha permissão de escrita
git clone https://github.com/SEU_USUARIO/meu-agente-gemini.git
cd meu-agente-gemini
```

## 3. Identidade só neste repositório
Em computador compartilhado use `--local` (nunca `--global`):
```bash
git config --local user.name "Seu Nome"
git config --local user.email "SEU_USUARIO@users.noreply.github.com"
```
O e-mail `noreply` fica em https://github.com/settings/emails e protege seu e-mail real.

## 4. Checkpoint ao fim de cada módulo
```bash
git status                     # confira: o .env NÃO pode aparecer aqui
git add .
git commit -m "módulo 2: extração com structured outputs"
git push
```
**No primeiro `git push`:** o Git Credential Manager abre o navegador pedindo login no GitHub. Autorize e pronto.
Sem essa janela? Crie um token em https://github.com/settings/tokens (Fine-grained, acesso só a este repositório, permissão *Contents: Read and write*) e cole o token quando o terminal pedir a senha.

## 5. Antes de sair
```bash
python 00_setup/limpar_computador.py
```
Ele confere se está tudo enviado, apaga seu `.env`, remove o container e desconecta o GitHub. Depois, saia das contas no navegador.

## Em casa
```bash
git clone https://github.com/SEU_USUARIO/meu-agente-gemini.git
cd meu-agente-gemini
python -m venv .venv
# ative o venv, depois:
pip install -r requirements.txt
cp .env.example .env    # e cole sua chave
```
