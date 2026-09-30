# 🚀 Publicar seu agente com link público (opcional, para fazer em casa)

Usamos o **Hugging Face Spaces**, que roda containers Docker de graça. O `Dockerfile` do projeto já funciona lá, e o `README.md` já tem o cabeçalho que o Spaces exige (aquele bloco entre `---` no topo).

> ⚠️ **Cota:** quem abrir seu link vai usar a SUA chave da API. Deixe o Space **privado** ou mantenha `MAX_MENSAGENS_POR_SESSAO` baixo.

## Passo a passo
1. Crie uma conta em https://huggingface.co
2. **New Space** › dê um nome (ex.: `meu-agente-gemini`) › **SDK: Docker** › **Blank** › escolha Public ou Private › **Create Space**.
3. No Space, vá em **Settings › Variables and secrets › New secret**:
   - Nome: `GEMINI_API_KEY` · Valor: sua chave
   - (opcional) variável `GEMINI_MODEL`, `AGENTE_NOME`
4. Crie um token de escrita em https://huggingface.co/settings/tokens (**Write**).
5. No terminal, dentro do seu projeto:
```bash
git remote add space https://huggingface.co/spaces/SEU_USUARIO_HF/meu-agente-gemini
git push --force space main
```
   Usuário: seu usuário do Hugging Face · Senha: o **token** do passo 4.
   (O `--force` substitui o README de exemplo que o Space cria.)
6. Aguarde o build (aba **Logs**) e abra o link `https://SEU_USUARIO_HF-meu-agente-gemini.hf.space`.

## Atualizar depois
```bash
git add . && git commit -m "melhorias" && git push && git push space main
```

## Problemas comuns
- **Build falhou:** veja a aba *Logs*. Geralmente é um erro de digitação em `requirements.txt`.
- **"Chave GEMINI_API_KEY não configurada":** o secret não foi criado ou tem outro nome.
- **Space "dormindo":** no plano gratuito ele hiberna sem uso; o primeiro acesso demora alguns segundos.
