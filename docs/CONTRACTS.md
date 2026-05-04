# CONTRACTS

## 1. Objetivo

Registrar entradas, saidas, invariantes e limites do acervo documental e do app
local de apoio à decisão. Estes contratos protegem a rastreabilidade do
material e evitam que a v1 seja confundida com protocolo institucional aprovado.

## 2. Entradas canonicas

| Entrada | Origem | Formato | Obrigatoria | Observacao |
| --- | --- | --- | --- | --- |
| Capitulos Markdown | `docs/meios_de_contraste/` | `.md` | sim | Fonte editavel e revisavel por diff |
| Indice dos capitulos | `docs/meios_de_contraste/README.md` | Markdown | sim | Mapa de leitura do material principal |
| Metadado da obra-fonte | `docs/meios_de_contraste/source.json` | JSON | sim | Titulo, subtitulo, versao, editores e nota de corpus |
| Kits cromaticos | `docs/identidade_visual/` | Markdown, CSS, HTML, JSON | nao | Apoio visual neutro, sem marcas ou logos |
| Proposta dinamica | `docs/meios_de_contraste/proposta_apresentacao_dinamica.md` | Markdown | nao | Planejamento, nao implementacao |
| Configuracao do doctor | `config/doctor.json` | JSON | sim | Politica versionada de warnings e aliases |
| Regras estruturadas | `app/data/rules.json` | JSON | sim para app | Regras deterministicas citadas por fonte local |

## 3. Saidas canonicas

| Saida | Destino | Formato | Garantia | Observacao |
| --- | --- | --- | --- | --- |
| Acervo revisavel | Git e leitores Markdown | Markdown | Texto versionado e diffs legiveis | Nao substitui publicacao original externa |
| Diagnostico de gate | Terminal local | Texto | Falha quando gate esta fraco | Usa regras semanticas simples |
| Diagnostico do doctor | Terminal local | Texto | Verifica arquivos e coerencia minima | Nao valida conteudo clinico |
| Previews visuais | Navegador local | HTML/CSS | Referencia visual manual | Nao e deploy oficial |
| Propostas futuras | Markdown | Texto estruturado | Planejamento rastreavel | Nao e runtime assistencial |
| App local | Navegador local | HTML/CSS/JS + API Python | Apoio à decisão | Nao e protocolo aprovado |
| Q&A local | Navegador local | Resposta textual citada | Restrito ao corpus local | Usa Ollama opcional; fallback com trechos |

## 4. Invariantes

- Capitulos clinicos nao devem receber alteracao substantiva sem fonte e motivo.
- Conteudo clinico, identidade visual e produto futuro devem permanecer
  distinguiveis.
- Scripts de governanca nao devem exigir dependencia externa alem do Python
  padrao.
- Dados de pacientes, credenciais e logs assistenciais nao pertencem ao repo.
- Regras deterministicas devem citar arquivo fonte local e ser testaveis por
  cenarios de fronteira.
- LLM nao pode emitir resposta sem contexto recuperado do corpus local.

## 5. Identificadores

| Entidade | Identificador | Regra |
| --- | --- | --- |
| Capitulo | Prefixo numerico `01_` a `11_` | Preservar ordem do guia convertido |
| Kit visual | Slug em `docs/identidade_visual/<slug>/` | Usar nomes estaveis em minusculas |
| Warning do doctor | Codigo estavel | Registrar aliases ou ignores em `config/doctor.json` |
| Regra estruturada | Chave em `app/data/rules.json` | Preservar fonte e limiar explicito |
| Endpoint local | Caminho `/api/...` | Nao depender de dados sensiveis |

## 6. Quebras de contrato

Mudancas abaixo exigem atualizacao de README, arquitetura, contratos e operacao:

- Alterar a estrutura dos capitulos ou slugs de identidade visual.
- Alterar runtime de aplicacao, API, calculadora, RAG ou dashboard.
- Passar a consumir dados reais, sensiveis ou assistenciais.
- Declarar validacao clinica ou protocolo institucional final.

## 7. Validacao clinica

O doctor valida estrutura documental, nao verdade clinica. Qualquer uso em
decisao assistencial exige revisao humana especializada, protocolo institucional
e checagem contra publicacao original, diretrizes vigentes e bulas oficiais.

## 8. Contrato do app local

- `app/server.py` deve rodar com biblioteca padrao do Python.
- `app/static/` nao deve exigir build step.
- `app/data/rules.json` e fonte de regras deterministicas da v1.
- O endpoint `/api/qa` deve recuperar trechos locais antes de chamar Ollama.
- O app nao deve persistir perguntas, payloads ou respostas.
- Qualquer integracao com dados reais exige novo contrato.
