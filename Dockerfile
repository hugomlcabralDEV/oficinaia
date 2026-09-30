# Imagem do Guia Rec'n'Play — roda a interface web do agente.
#   Construir:  docker build -t guia-recnplay .
#   Rodar:      docker run --rm -p 8000:8000 --env-file .env guia-recnplay
#   Abrir:      http://localhost:8000
FROM python:3.12-slim

# Não gera arquivos .pyc e mostra os logs na hora
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000

WORKDIR /app

# Instala as dependências primeiro (o Docker reaproveita essa camada se só o código mudar)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código. A chave NÃO vai para dentro da imagem (.dockerignore bloqueia o .env)
COPY . .

# Roda como usuário comum, não como administrador (boa prática de segurança)
RUN useradd --create-home agente && chown -R agente /app
USER agente

EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://localhost:{os.environ[\"PORT\"]}/saude')" || exit 1
CMD ["sh", "-c", "uvicorn app:app --app-dir 05_web --host 0.0.0.0 --port ${PORT}"]
