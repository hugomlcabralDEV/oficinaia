# 📦 Para o instrutor: publicar o template da oficina

1. Crie um repositório vazio no GitHub, por exemplo `gdgrecife/oficina-agentes-gemini` (sem README).
2. Na pasta do projeto:
```bash
git init -b main
git add .
git commit -m "Oficina Rec'n'Play 2026: agentes com Gemini API"
git remote add origin https://github.com/gdgrecife/oficina-agentes-gemini.git
git push -u origin main
```
3. No GitHub: **Settings › General › marque "Template repository"**. Isso habilita o botão *Use this template* para os participantes.
4. Confira se o link do template está correto no README, em `docs/GITHUB.md`, em `docs/LABORATORIO.md` e nos slides 9 e 51.
5. Gere um QR Code do link e coloque no slide 5.
6. Exporte os slides em PDF (Share › Export) e adicione em `docs/slides.pdf`, para a turma levar junto:
```bash
git add docs/slides.pdf && git commit -m "slides da oficina" && git push
```
7. Envie o link para a equipe técnica rodar `00_setup/checar_laboratorio.py` nas máquinas.
