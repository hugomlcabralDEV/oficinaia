# 🏆 Desafios — escolha um e mão na massa!

Todos os desafios mexem em `04_agente/ferramentas.py`. Lembre das duas partes: **função** + **declaração**, e registre nas listas `DECLARACOES` e `FUNCOES` no fim do arquivo.

## ⭐ Nível 1 — Remover da agenda (10 min)
Crie `remover_da_minha_agenda(id_atividade)`. Se o id não estiver na agenda, devolva `{"erro": ...}`.
*Dica:* copie `adicionar_na_minha_agenda` e use `agenda.remove(...)`.

## ⭐ Nível 1 — Filtro por nível
Adicione o parâmetro opcional `nivel` (`"iniciante"`, `"intermediário"`, `"todos"`) em `consultar_programacao`. Use `enum` na declaração.

## ⭐⭐ Nível 2 — Câmbio para visitantes
Crie `cotacao_moeda(moeda)` usando a AwesomeAPI (sem chave):
`https://economia.awesomeapi.com.br/json/last/USD-BRL` → campo `USDBRL.bid`.
Valide a moeda com `enum` (`USD`, `EUR`, `GBP`).

## ⭐⭐ Nível 2 — Confirmação humana antes de agir
Antes de executar `adicionar_na_minha_agenda`, pergunte no terminal `Confirmar? (s/n)`. Se o usuário negar, devolva `{"ok": false, "mensagem": "Usuário cancelou"}` ao modelo. Isso se chama **human-in-the-loop**.

## ⭐⭐⭐ Nível 3 — Exportar agenda para calendário
Crie `exportar_agenda_ics()` que gera um arquivo `.ics` com as atividades salvas (abre no Google Agenda). Teste perguntando "exporta minha agenda".

## ⭐⭐⭐ Nível 3 — Busca na web embutida
O Gemini tem ferramentas nativas. Adicione `{"type": "google_search"}` à lista `DECLARACOES` e pergunte algo atual sobre Recife. Compare quando ele usa a busca e quando usa as suas ferramentas.

## 🧪 Bônus para qualquer nível
Escreva um teste em `tests/test_ferramentas.py` para a ferramenta que você criou e rode `pytest -q`.
