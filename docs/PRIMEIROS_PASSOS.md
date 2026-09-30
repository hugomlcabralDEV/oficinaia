# 👣 Primeiros passos — para quem nunca programou

## Onde o código vive e como ele roda
| Onde | Para quê | Como |
|---|---|---|
| **Editor (VS Code)** | Ler e escrever o código. Um arquivo `.py` é uma receita de passos. | *Arquivo › Abrir Pasta* e escolha a pasta do projeto |
| **Terminal** | Mandar o computador seguir a receita | *Terminal › Novo Terminal* e digite `python nome_do_arquivo.py` |
| **Resultado** | Ver o que o programa mostrou | Aparece no próprio terminal |

## O que é uma API?
Pense num restaurante: **você** (seu programa) faz o pedido, a **API** (o garçom) leva o pedido pela internet num formato combinado, e o **Gemini** (a cozinha, nos computadores do Google) prepara a resposta.
O Gemini **não roda** no seu computador. Seu programa só manda o pedido e recebe a resposta.

## O que é a chave de API?
É a sua **comanda**: diz ao Google quem está pedindo e controla quanto você pode usar. Para começar, é gratuita.

### Como conseguir a sua (2 minutos)
1. Abra **https://aistudio.google.com/apikey** (no laboratório, use janela anônima).
2. Entre com sua conta Google.
3. Aceite os termos, se aparecerem, e clique em **Create API key** (Criar chave de API).
4. Copie a chave: é um texto longo, parecido com `AIzaSy…`.

> ⚠️ A chave é como uma senha: não mande no grupo, não coloque em prints, não publique no GitHub.

### Onde guardar: o arquivo `.env`
1. No terminal, dentro da pasta do projeto: `copy .env.example .env` (Windows) ou `cp .env.example .env` (Linux/Mac).
2. Abra o `.env` no VS Code e cole a chave depois do `=`, **sem espaços e sem aspas**:
   ```
   GEMINI_API_KEY=AIzaSy...cole_a_sua_aqui
   ```
3. Salve (Ctrl+S). O arquivo `comum.py` lê a chave sozinho, e o `.gitignore` impede que ela vá para o GitHub.

## Python em 2 minutos
| Você vê | Nome | O que significa |
|---|---|---|
| `# um lembrete` | Comentário | O computador ignora; serve para explicar |
| `"Olá, Recife"` | Texto | Usado exatamente como está escrito |
| `nome = "Ana"` | Variável | Uma caixinha com nome que guarda um valor |
| `print("oi")` | Função | Um comando pronto; nos parênteses vai o que ele precisa |
| `from google import genai` | Import | Pega uma caixa de ferramentas que alguém já fez |
| `cliente.interactions.create()` | Ponto | Entra em algo: do cliente, pegue interactions e use create |

## O primeiro código, linha por linha (`01_primeira_chamada/ola_gemini.py`)
| Código | Em português |
|---|---|
| `from google import genai` | Pega a biblioteca do Google que conversa com o Gemini |
| `cliente = genai.Client(api_key=...)` | Cria a conexão com o Google usando a sua chave (no projeto, ela vem do `.env`) |
| `interaction = cliente.interactions.create(` | Envia o pedido e guarda a resposta na variável `interaction` |
| `model="gemini-3.8-flash"` | Escolhe qual modelo vai responder |
| `input="Explique o que é uma API..."` | O pedido em si: o prompt |
| `print(interaction.output_text)` | Mostra na tela o texto que o Gemini escreveu |

Para rodar: `python 01_primeira_chamada/ola_gemini.py` (com `(.venv)` aparecendo no começo da linha do terminal).
