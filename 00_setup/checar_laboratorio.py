"""
Checagem do LABORATÓRIO — para o técnico rodar em cada máquina ANTES da oficina.
Não precisa de chave de API.

Rode com:  python 00_setup/checar_laboratorio.py

Verifica: programas instalados (git, python, docker, node), Docker em execução,
e se a rede libera os sites que a oficina usa.
"""
import shutil
import socket
import subprocess
import sys

OK, FALHA, AVISO = "✔", "✖", "⚠"
problemas = 0


def comando(nome, args, obrigatorio=True):
    global problemas
    if not shutil.which(args[0]):
        print(f"{FALHA if obrigatorio else AVISO} {nome}: não encontrado no PATH")
        problemas += obrigatorio
        return
    try:
        saida = subprocess.run(args, capture_output=True, text=True, timeout=20)
        texto = (saida.stdout or saida.stderr).strip().splitlines()[0] if (saida.stdout or saida.stderr) else ""
        if saida.returncode != 0:
            print(f"{FALHA if obrigatorio else AVISO} {nome}: instalado, mas retornou erro → {texto[:100]}")
            problemas += obrigatorio
        else:
            print(f"{OK} {nome}: {texto[:100]}")
    except Exception as e:
        print(f"{FALHA} {nome}: {e}")
        problemas += obrigatorio


print("\n🔧 Programas")
print(f"{OK if sys.version_info >= (3, 10) else FALHA} Python {sys.version.split()[0]} (precisa ≥ 3.10)")
problemas += sys.version_info < (3, 10)
comando("pip", [sys.executable, "-m", "pip", "--version"])
comando("venv", [sys.executable, "-m", "venv", "--help"])
comando("git", ["git", "--version"])
comando("docker (cliente)", ["docker", "--version"])
comando("docker (serviço rodando)", ["docker", "info", "--format", "{{.ServerVersion}}"])
comando("imagem base python:3.12-slim", ["docker", "image", "inspect", "python:3.12-slim", "--format", "baixada ✓"], obrigatorio=False)
comando("node (opcional)", ["node", "--version"], obrigatorio=False)

print("\n🌐 Rede (porta 443)")
SITES = {
    "generativelanguage.googleapis.com": "Gemini API (essencial)",
    "aistudio.google.com": "gerar chave da API (essencial)",
    "pypi.org": "instalar bibliotecas (essencial)",
    "files.pythonhosted.org": "instalar bibliotecas (essencial)",
    "github.com": "clonar e enviar código (essencial)",
    "registry-1.docker.io": "Docker Hub (módulo 5)",
    "geocoding-api.open-meteo.com": "ferramenta de clima",
    "api.open-meteo.com": "ferramenta de clima",
    "viacep.com.br": "ferramenta de CEP",
    "huggingface.co": "deploy opcional",
    "colab.research.google.com": "plano B no navegador",
    "economia.awesomeapi.com.br": "desafio de câmbio",
}
for host, uso in SITES.items():
    try:
        socket.create_connection((host, 443), timeout=5).close()
        print(f"{OK} {host:36} {uso}")
    except OSError:
        essencial = "essencial" in uso
        print(f"{FALHA if essencial else AVISO} {host:36} {uso} — BLOQUEADO")
        problemas += essencial

print("\n" + ("🎉 Máquina pronta para a oficina!" if not problemas else f"❗ {problemas} problema(s) essencial(is). Veja docs/LABORATORIO.md"))
sys.exit(1 if problemas else 0)
