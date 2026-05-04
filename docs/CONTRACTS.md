# CONTRACTS

## 1. Objetivo

Registrar entradas, saídas, invariantes e limites do acervo documental e do app
local de apoio à decisão. Estes contratos protegem a rastreabilidade do
material e evitam que a v1 seja confundida com protocolo institucional aprovado.

## 2. Entradas canônicas

| Entrada | Origem | Formato | Obrigatória | Observação |
| --- | --- | --- | --- | --- |
| Capítulos Markdown | `docs/meios_de_contraste/` | `.md` | sim | Fonte editável e revisável por diff |
| Índice dos capítulos | `docs/meios_de_contraste/README.md` | Markdown | sim | Mapa de leitura do material principal |
| Metadado da obra-fonte | `docs/meios_de_contraste/source.json` | JSON | sim | Título, subtítulo, versão, editores e nota de corpus |
| Kits cromáticos | `docs/identidade_visual/` | Markdown, CSS, HTML, JSON | não | Apoio visual neutro, sem marcas ou logos |
| Proposta dinâmica | `docs/meios_de_contraste/proposta_apresentacao_dinamica.md` | Markdown | não | Planejamento, não implementação |
| Configuração do doctor | `config/doctor.json` | JSON | sim | Política versionada de warnings e aliases |
| Regras estruturadas | `app/data/rules.json` | JSON | sim para app | Regras determinísticas citadas por fonte local |
| Configuração do app | `app/data/app_config.json` | JSON | sim para app | Tema padrão, seletor de adaptador, Q&A, conector e modelo sem alterar regras clínicas |

## 3. Saídas canônicas

| Saída | Destino | Formato | Garantia | Observação |
| --- | --- | --- | --- | --- |
| Acervo revisável | Git e leitores Markdown | Markdown | Texto versionado e diffs legíveis | Não substitui publicação original externa |
| Diagnóstico de gate | Terminal local | Texto | Falha quando gate está fraco | Usa regras semânticas simples |
| Diagnóstico do doctor | Terminal local | Texto | Verifica arquivos e coerência mínima | Não valida conteúdo clínico |
| Previews visuais | Navegador local | HTML/CSS | Referência visual manual | Não é deploy oficial |
| Propostas futuras | Markdown | Texto estruturado | Planejamento rastreável | Não é runtime assistencial |
| App local | Navegador local | HTML/CSS/JS + API Python | Apoio à decisão | Não é protocolo aprovado |
| Perguntas e Respostas | Navegador local | Resposta textual citada | Restrito ao corpus local | Usa Ollama opcional; fallback com trechos |

## 4. Invariantes

- Capítulos clínicos não devem receber alteração substantiva sem fonte e motivo.
- Conteúdo clínico, identidade visual e produto futuro devem permanecer
  distinguíveis.
- Scripts de governança não devem exigir dependência externa além do Python
  padrão.
- Dados de pacientes, credenciais e logs assistenciais não pertencem ao repo.
- Regras determinísticas devem citar arquivo fonte local e ser testáveis por
  cenários de fronteira.
- LLM não pode emitir resposta sem contexto recuperado do corpus local.

## 5. Identificadores

| Entidade | Identificador | Regra |
| --- | --- | --- |
| Capítulo | Prefixo numérico `01_` a `11_` | Preservar ordem do guia convertido |
| Kit visual | Slug em `docs/identidade_visual/<slug>/` | Usar nomes estáveis em minúsculas |
| Warning do doctor | Código estável | Registrar aliases ou ignores em `config/doctor.json` |
| Regra estruturada | Chave em `app/data/rules.json` | Preservar fonte e limiar explícito |
| Endpoint local | Caminho `/api/...` | Não depender de dados sensíveis |

## 6. Quebras de contrato

Mudanças abaixo exigem atualização de README, arquitetura, contratos e operação:

- Alterar a estrutura dos capítulos ou slugs de identidade visual.
- Alterar runtime de aplicação, API, calculadora, RAG ou dashboard.
- Passar a consumir dados reais, sensíveis ou assistenciais.
- Declarar validação clínica ou protocolo institucional final.

## 7. Validação clínica

O doctor valida estrutura documental, não verdade clínica. Qualquer uso em
decisão assistencial exige revisão humana especializada, protocolo institucional
e checagem contra publicação original, diretrizes vigentes e bulas oficiais.

## 8. Contrato do app local

- `app/server.py` deve rodar com biblioteca padrão do Python.
- `app/static/` não deve exigir build step.
- `app/data/rules.json` é fonte de regras determinísticas da v1.
- `app/data/app_config.json` controla tema manual, visibilidade do seletor de
  adaptador, ativação de Perguntas e Respostas, conector e modelo.
- O endpoint `/api/qa` deve recuperar trechos locais antes de chamar Ollama.
- O app não deve persistir perguntas, payloads ou respostas.
- Qualquer integração com dados reais exige novo contrato.
