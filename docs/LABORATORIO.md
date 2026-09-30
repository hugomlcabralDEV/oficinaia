# 🖥️ Preparação do laboratório — para a equipe técnica

**Oficina:** Agentes Autônomos com Gemini API · **Horário:** 13h–17h · **Responsável:** Petros Barreto

## Software em cada máquina
| Item | Versão | Observações |
|---|---|---|
| Python | 3.10 ou mais novo (3.12 recomendado) | Windows: marcar **Add Python to PATH**. `pip` e `venv` precisam funcionar sem administrador. |
| Git | 2.40+ | No Windows, o instalador padrão já inclui o **Git Credential Manager** (necessário para o `git push` abrir o login no navegador). |
| Docker | Docker Desktop (Windows/Mac) ou Docker Engine (Linux) | O serviço precisa estar **rodando** e o usuário do aluno precisa estar no grupo `docker-users` (Windows) ou `docker` (Linux). No Windows, WSL2 habilitado. |
| Editor | **VS Code** com a extensão Python (recomendado) | Sem editor, iniciantes não conseguem fazer os exercícios. |
| Navegador | Chrome ou Firefox atualizados | Janela anônima liberada. |
| Node.js | Opcional | Não é usado nesta versão da oficina. |

### Pré-baixar a imagem base (economiza a rede na hora)
```bash
docker pull python:3.12-slim
```

## Rede — liberar HTTPS (porta 443) para
- `generativelanguage.googleapis.com` e `aistudio.google.com` (Gemini API) — **essencial**
- `pypi.org` e `files.pythonhosted.org` (instalar bibliotecas) — **essencial**
- `github.com` e `*.githubusercontent.com` (clonar e enviar código) — **essencial**
- `registry-1.docker.io`, `auth.docker.io`, `production.cloudflare.docker.com` (Docker Hub)
- `api.open-meteo.com`, `geocoding-api.open-meteo.com`, `viacep.com.br` (ferramentas do agente)
- `huggingface.co`, `colab.research.google.com`, `economia.awesomeapi.com.br` (opcionais)
- `localhost:8000` precisa abrir no navegador (firewall local)

## Teste automático (rodar em 1 máquina de cada imagem, e de preferência em todas)
```bash
git clone https://github.com/petrosbarreto/oficina-agentes-gemini teste-oficina
cd teste-oficina
python 00_setup/checar_laboratorio.py
```
O script confere programas, se o Docker está rodando, se a imagem base foi baixada e se cada site está acessível. Resultado esperado: `🎉 Máquina pronta para a oficina!`

## Durante e depois
- Se as máquinas forem **restauradas ao reiniciar** (Deep Freeze ou similar), avise a turma: tudo que não for enviado ao GitHub se perde. Por isso fazemos `git push` a cada módulo.
- Ao final, cada aluno roda `python 00_setup/limpar_computador.py`, que apaga a chave de API e desconecta o GitHub.
- Sugestão: reiniciar/restaurar as máquinas depois da oficina.
