"""
ANTES DE SAIR DO LABORATÓRIO — limpa seus dados deste computador compartilhado.

Rode com:  python 00_setup/limpar_computador.py

O que ele faz:
  1. Confere se todo o seu código já foi enviado para o GitHub (para você não perder nada)
  2. Apaga o arquivo .env (sua chave da API)
  3. Para e remove o container/imagem Docker da oficina
  4. Tenta desconectar sua conta do GitHub neste computador
  5. Lembra você do que falta fazer à mão
"""
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def rodar(args):
    try:
        return subprocess.run(args, cwd=RAIZ, capture_output=True, text=True, timeout=60)
    except Exception:
        return None


print("\n🧹 Limpando seus dados deste computador\n")

# 1) Código salvo no GitHub?
status = rodar(["git", "status", "--porcelain"])
pendente = rodar(["git", "log", "@{u}..", "--oneline"])
if status and status.stdout.strip():
    print("⚠ Você tem alterações que NÃO foram commitadas:")
    print(status.stdout)
    print("  Rode:  git add .  &&  git commit -m \"meu agente\"  &&  git push")
    if input("  Continuar mesmo assim? (s/N) ").strip().lower() != "s":
        sys.exit(0)
elif pendente is None or pendente.returncode != 0:
    print("⚠ Não consegui confirmar se o código foi enviado (repositório sem 'origin'?).")
    if input("  Continuar mesmo assim? (s/N) ").strip().lower() != "s":
        sys.exit(0)
elif pendente.stdout.strip():
    print("⚠ Há commits que ainda não foram enviados (git push):")
    print(pendente.stdout)
    if input("  Continuar mesmo assim? (s/N) ").strip().lower() != "s":
        sys.exit(0)
else:
    print("✔ Todo o código está no GitHub")

# 2) Chave da API
env = RAIZ / ".env"
if env.exists():
    env.unlink()
    print("✔ Arquivo .env (sua chave) apagado")
agenda = RAIZ / "04_agente" / "dados" / "minha_agenda.json"
if agenda.exists():
    agenda.unlink()

# 3) Docker
if shutil.which("docker"):
    for c in ["docker compose down", "docker rmi -f guia-recnplay"]:
        rodar(c.split())
    print("✔ Container e imagem Docker da oficina removidos")

# 4) Credenciais do GitHub neste computador
if shutil.which("git-credential-manager") or shutil.which("git"):
    r = rodar(["git", "credential-manager", "github", "logout"])
    if r and r.returncode == 0:
        print("✔ Conta do GitHub desconectada do Git Credential Manager")
    else:
        print("⚠ Não consegui desconectar o GitHub automaticamente (veja o passo 2 abaixo)")
rodar(["git", "config", "--local", "--unset", "user.email"])

print("""
📋 Falta fazer à mão (1 minuto):
  1. Saia da sua conta Google e do GitHub no navegador (ou feche a janela anônima)
  2. Windows: Painel de Controle › Gerenciador de Credenciais › Credenciais do Windows
     › remova as entradas "git:https://github.com" (se existirem)
  3. Opcional: apague esta pasta do computador
  4. Se sua chave vazou em algum lugar, revogue em https://aistudio.google.com/apikey

Seu código está seguro no seu GitHub. Até a próxima! 👋
""")
