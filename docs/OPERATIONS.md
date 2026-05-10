# OPERATIONS

## 1. Objetivo

Este documento descreve como validar, diagnosticar e manter o repositório
documental e o app local de apoio à decisão. Não há deploy, autenticação ou
runtime assistencial em produção nesta fase.

## 2. Ambientes

| Ambiente | Objetivo | Runtime | Observações |
| --- | --- | --- | --- |
| `local` | edição e validação | `python3` | Usa biblioteca padrão |
| `app-local` | UI e API local | `python3 app/server.py` | Ollama opcional para Perguntas e Respostas |
| `git` | histórico e revisão | `git` | Preserva Markdown, regras e kits |
| `consumer` | repositórios que reutilizam o acervo | variável | Deve validar uso próprio |

## 3. Como executar

### Boot local

```bash
python3 --version
```

### Boot principal

```bash
python3 app/server.py
```

### App local

```bash
python3 app/server.py
```

Abrir `http://127.0.0.1:8765`.

Para Ollama:

```bash
OLLAMA_MODEL=gemma4:e4b python3 app/server.py
```

Para Ollama em outra máquina:

```bash
APP_QA_OLLAMA_URL=http://192.168.1.50:11434 python3 app/server.py
```

O app também aceita `APP_QA_OLLAMA_URL=192.168.1.50:11434` e assume `http://`.
No host remoto, o Ollama precisa escutar na rede, por exemplo:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

### Smoke HTTP local

Automatizado:

```bash
python3 scripts/smoke_app.py
```

O script escolhe uma porta livre, sobe `app/server.py` com Q&A desabilitado e
valida `/api/health`, `/api/source`, `/api/rules`, `/api/renal-function` e
`/api/decision`.

Manual, quando for necessário inspecionar o servidor:

```bash
python3 app/server.py --port 8765
curl -fsS http://127.0.0.1:8765/api/health
curl -fsS http://127.0.0.1:8765/api/source
curl -fsS http://127.0.0.1:8765/api/rules
curl -fsS -X POST http://127.0.0.1:8765/api/renal-function \
  -H 'Content-Type: application/json' \
  -d '{"creatinine_mg_dl":1.0,"age_years":45,"sex":"female","weight_kg":70}'
```

O smoke não valida segurança clínica; ele confirma bootstrap, JSON válido e
contratos HTTP básicos.

## 4. Configuração operacional

- arquivo local: `config/doctor.json`
- template versionado do app: `app/data/app_config.example.json`
- configuração local do app: `app/data/app_config.json`, ignorada pelo Git.
  Copie o template para esse caminho quando precisar fixar tema, branding,
  conector ou modelo em um ambiente específico.
- log local de perguntas do Q&A: `app/data/qa_questions.jsonl`, ignorado pelo
  Git. Use apenas para análise local, pois perguntas podem conter dados
  sensíveis digitados pelo usuário.
- variáveis de ambiente críticas: nenhuma obrigatória
- variáveis opcionais do app: `APP_HOST`, `APP_PORT`, `OLLAMA_URL`,
  `OLLAMA_MODEL`, `OLLAMA_KEEP_ALIVE`, `OLLAMA_NUM_PREDICT`, `APP_THEME`,
  `APP_SHOW_THEME_PICKER`, `APP_QA_ENABLED`, `APP_QA_CONNECTOR`,
  `APP_QA_MODEL`, `APP_QA_OLLAMA_URL`, `APP_QA_KEEP_ALIVE`,
  `APP_QA_NUM_PREDICT`, `APP_QA_LOG_QUESTIONS`, `APP_BRAND_TITLE`, `APP_BRAND_SUBTITLE`,
  `APP_BRAND_SHOW_MARK`, `APP_BRAND_MARK_TEXT`, `APP_BRAND_LOGO_SRC`
- path de runtime state: `app/data/qa_questions.jsonl` quando log de perguntas
  estiver habilitado
- path de logs: `app/data/qa_questions.jsonl` para perguntas do Q&A; não há
  log persistente geral de aplicação
- paths mutáveis ignorados: `runtime/`, `.playwright-mcp/`, `__pycache__/`,
  `app/data/app_config.json`, `app/data/qa_questions.jsonl`, caches de testes e
  arquivos temporários

O repositório não deve depender de caminhos locais implícitos. Kits cromáticos
não devem carregar nomes institucionais, logos, URLs de origem ou assets
proprietários.

## 5. Validação mínima

Depois de alterar a baseline ou documentos estruturais:

```bash
python3 scripts/project_doctor.py
```

Validação completa recomendada:

```bash
python3 scripts/check_project_gate.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --audit-config
python3 -m py_compile scripts/check_project_gate.py scripts/project_doctor.py scripts/smoke_app.py
python3 -m py_compile app/server.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/smoke_app.py
```

A suíte automatizada cobre regressões técnicas de regras, calculadoras,
recuperação e contratos HTTP básicos. Ela não valida verdade clínica, equivalência
com a publicação original nem prontidão assistencial.

Conferir:

- gate preenchido e defensável
- docs estruturais sem marcadores de scaffolding
- comando principal coerente entre README e OPERATIONS
- diff sem `.DS_Store`, cache ou export temporário
- ausência de dados de pacientes ou segredos
- app sobe localmente e endpoints principais respondem
- testes unitários passam
- smoke HTTP automatizado passa
- `START_CHECKLIST.md` continua refletindo o que está completo, parcial e fora
  de escopo

## 6. Logs e diagnóstico

- logger principal: não há logger persistente geral de aplicação; o módulo de
  Perguntas e Respostas grava perguntas em JSONL local quando habilitado.
- formato dos logs: saída textual dos scripts e requisições locais do servidor
  e eventos JSONL de perguntas do Q&A.
- onde ler logs:
  - terminal local
  - `app/data/qa_questions.jsonl` para perguntas feitas ao Q&A
- sinais de falha comuns:
  - `PROJECT_GATE.md` com resposta curta, vaga ou pendente
  - divergência entre README, AGENTS e OPERATIONS
  - placeholders de scaffolding em documentos principais
  - arquivo obrigatório ausente
  - `START_CHECKLIST.md` otimista demais ou desatualizado
  - Ollama indisponível ou modelo local ausente no endpoint `/api/qa`
  - `APP_QA_OLLAMA_URL` apontando para host/porta sem acesso de rede
  - JSON inválido em `app/data/`

## 7. Restart policy

Ao mudar:

- `docs/meios_de_contraste/`: reiniciar app para Perguntas e Respostas e
  regras refletirem corpus;
  exige revisão documental e, quando clínico, revisão especializada.
- `docs/identidade_visual/`: nenhum restart; exige revisar previews afetados.
- `scripts/`: nenhum restart; exige `py_compile` e execução do doctor.
- `config/`: nenhum restart; exige `project_doctor.py --audit-config`.
- `docs/` estruturais apenas: nenhum restart; exige doctor e revisão de diff.
- `app/server.py`, `app/data/`, `app/static/`: reiniciar servidor local.

## 8. Persistência, backup e limpeza

- armazenamento principal: Git.
- armazenamento local não versionado: `app/data/qa_questions.jsonl` para massa
  de perguntas do Q&A.
- backup: remoto Git e cópia local independente da publicação original externa,
  quando necessária para auditoria clínica.
- retenção: histórico Git conforme política do repositório.
- retenção de perguntas Q&A: manter `app/data/qa_questions.jsonl` apenas pelo
  tempo necessário à análise local; revisar manualmente antes de qualquer
  compartilhamento; remover o arquivo ao encerrar a rodada de análise ou em até
  30 dias, o que ocorrer primeiro.
- limpeza segura: `.DS_Store`, caches, arquivos temporários, exports locais e
  logs de perguntas quando não forem mais necessários. Não limpar arquivos
  locais de outra pessoa sem confirmação.

Nunca remova sem decisão explícita:

- `docs/meios_de_contraste/`
- histórico de decisões em `docs/DECISIONS.md`

## 9. Incidentes

Checklist mínimo:

1. confirmar que o corpus Markdown ainda existe
2. confirmar que o capítulo alterado está indexado
3. confirmar que o doctor passa
4. revisar se a mudança altera contrato clínico ou apenas formatação
5. confirmar se há dado sensível ou material temporário no diff

## 10. Mudanças que exigem update deste documento

- novo entrypoint
- nova dependência operacional
- novo path de runtime
- nova regra de validação
- nova rotina de backup, publicação ou limpeza
