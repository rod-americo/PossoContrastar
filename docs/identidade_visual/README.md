# Kits cromaticos

Kits neutros de cor para adaptar a interface whitelabel sem carregar nomes,
logos, URLs ou assets de instituicoes. Eles preservam apenas direcao cromatica,
tokens basicos e um preview simples.

## Kits disponiveis

| Slug | Nome | Uso sugerido |
| --- | --- | --- |
| `noturno` | Noturno | Interfaces densas, operacionais e de baixa luminosidade |
| `botanico` | Botânico | Painel claro com verde institucional neutro |
| `lilas` | Lilás | Experiencias educativas, publicas ou de leitura leve |

## Contrato

- Nao versionar marcas, logos, imagens, URLs institucionais ou nomes de origem.
- Cada kit deve manter `tokens.json`, `<slug>.css`, `preview.html` e `README.md`.
- Adaptadores podem mudar a apresentacao, mas nao devem alterar regras clinicas.
