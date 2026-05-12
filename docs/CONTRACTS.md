# CONTRACTS

## 1. Objetivo

Registrar entradas, saídas, invariantes e limites do acervo documental e do app local de apoio à decisão. Estes contratos protegem a rastreabilidade do material e evitam que a v1 seja confundida com protocolo institucional aprovado.

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
| Template de configuração do app | `app/data/app_config.example.json` | JSON | sim para app | Defaults versionados de branding, tema, seletor, Perguntas e Respostas, conector, modelo e URL do Ollama |
| Configuração local do app | `app/data/app_config.json` | JSON | não versionar | Arquivo local ignorado pelo Git para ajustes de ambiente sem alterar regras clínicas |

## 3. Saídas canônicas

| Saída | Destino | Formato | Garantia | Observação |
| --- | --- | --- | --- | --- |
| Acervo revisável | Git e leitores Markdown | Markdown | Texto versionado e diffs legíveis | Não substitui publicação original externa |
| Diagnóstico de gate | Terminal local | Texto | Falha quando gate está fraco | Usa regras semânticas simples |
| Diagnóstico do doctor | Terminal local | Texto | Verifica arquivos e coerência mínima | Não valida conteúdo clínico |
| Testes automatizados | Terminal local e CI | `unittest` | Regressão técnica de regras locais | Não valida verdade clínica |
| Smoke HTTP | Terminal local e CI | Processo local + HTTP | Verifica bootstrap e contratos básicos | Q&A roda desabilitado no smoke |
| Previews visuais | Navegador local | HTML/CSS | Referência visual manual | Não é deploy oficial |
| Propostas futuras | Markdown | Texto estruturado | Planejamento rastreável | Não é runtime assistencial |
| App local | Navegador local | HTML/CSS/JS + API Python | Apoio à decisão | Não é protocolo aprovado |
| Perguntas e Respostas | Navegador local | Resposta textual citada | Restrito ao corpus local | Usa Ollama opcional; fallback com trechos |
| Log local de perguntas | `app/data/qa_questions.jsonl` | JSONL | Perguntas feitas ao Q&A | Não versionar; pode conter texto sensível informado pelo usuário |

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

## 6. Contratos HTTP locais

O app é local, sem autenticação e sem promessa de compatibilidade externa. Os endpoints abaixo são contratos internos relevantes porque a UI e os smokes dependem deles.

| Endpoint | Método | Entrada | Saída | Observação |
| --- | --- | --- | --- | --- |
| `/api/health` | `GET` | nenhuma | JSON com `ok`, Q&A, modelo e corpus | Healthcheck local, não readiness assistencial |
| `/api/source` | `GET` | nenhuma | JSON de `source.json` | Metadado bibliográfico |
| `/api/rules` | `GET` | nenhuma | JSON de `rules.json` | Regras determinísticas versionadas |
| `/api/chapters` | `GET` | nenhuma | Lista de capítulos com conteúdo | Exclui README e proposta dinâmica do corpus clínico |
| `/api/search` | `GET` | query `q` | Resultados recuperados do corpus | Busca lexical simples |
| `/api/renal-function` | `POST` | creatinina, idade, sexo, peso/altura opcionais | CKD-EPI 2021, Cockcroft-Gault, Schwartz quando aplicável | Apoio ao limiar, não prescrição |
| `/api/decision` | `POST` | campos clínicos estruturados da UI | nível, cards, entradas e função renal | Deve citar fonte local em cada card |
| `/api/calculators/renal` | `POST` | campos renais e peso | hidratação, função renal, cards de metformina | Usa `rules.json` |
| `/api/calculators/interval` | `POST` | contraste anterior/próximo e função renal | intervalos mínimos/ótimos e coleta laboratorial | Usa fallback conservador quando função renal é desconhecida |
| `/api/calculators/pediatric` | `POST` | peso, idade, creatinina, altura e cateter | volume iodado, dose MCBG, taxa e medicações | Exige revisão clínica antes de uso assistencial |
| `/api/extravasation` | `POST` | volume e sinais graves | nível, ações e follow-up | Apoio estruturado local |
| `/api/qa` | `POST` | pergunta textual | resposta citada e chunks recuperados | Bloqueado quando `qa.enabled` é falso |

## 7. Invariantes do app

- `app/server.py` deve continuar executável com biblioteca padrão do Python.
- `app/static/` deve continuar sem build step.
- `app/data/rules.json` deve conter `source` ou capítulo local para regras
clínicas usadas pela UI.
- O Q&A deve recuperar contexto local antes de chamar Ollama.
- O Q&A não deve responder livremente quando não houver contexto recuperado.
- `app/data/app_config.json` e `app/data/qa_questions.jsonl` não entram no Git.
- `app/data/qa_questions.jsonl` deve ser retido apenas localmente, revisado
antes de compartilhamento e removido ao fim da análise ou em até 30 dias.

## 8. Assunções ainda não validadas

- O corpus Markdown ainda não tem teste de equivalência com a publicação
original externa.
- As regras clínicas estruturadas têm regressão técnica automatizada, mas ainda
não têm validação clínica especializada contra a obra-fonte.
- O desempenho do RAG lexical é adequado apenas para uso local exploratório; não
há avaliação formal de recall, precisão ou segurança clínica.
- Não há contrato de autenticação, auditoria, multiusuário, deploy remoto ou
retenção institucional de logs.

## 9. Quebras de contrato

Mudanças abaixo exigem atualização de README, arquitetura, contratos e operação:

- Alterar a estrutura dos capítulos ou slugs de identidade visual.
- Alterar runtime de aplicação, API, calculadora, RAG ou dashboard.
- Passar a consumir dados reais, sensíveis ou assistenciais.
- Declarar validação clínica ou protocolo institucional final.

## 10. Validação clínica

O doctor valida estrutura documental, não verdade clínica. Qualquer uso em decisão assistencial exige revisão humana especializada, protocolo institucional e checagem contra publicação original, diretrizes vigentes e bulas oficiais.

## 11. Contrato do app local

- `app/server.py` deve rodar com biblioteca padrão do Python.
- `app/static/` não deve exigir build step.
- `app/data/rules.json` é fonte de regras determinísticas da v1.
- `app/data/app_config.example.json` fornece defaults versionados de branding
whitelabel, tema manual, visibilidade do seletor de adaptador, ativação de Perguntas e Respostas, conector, modelo, URL base do Ollama e log local de perguntas.
- `app/data/app_config.json`, quando existir, controla os mesmos campos no
ambiente local e não deve ser versionado.
- O endpoint `/api/qa` deve recuperar trechos locais antes de chamar Ollama.
- O endpoint `/api/qa` deve registrar cada pergunta em
`app/data/qa_questions.jsonl` quando `qa.log_questions` estiver ativo.
- O app não deve persistir respostas, payloads completos, cabeçalhos, IP ou
identificadores do usuário.
- Perguntas podem conter dados sensíveis digitados pelo usuário; o log local não
deve ser versionado nem compartilhado sem revisão.
- Qualquer integração com dados reais exige novo contrato.
