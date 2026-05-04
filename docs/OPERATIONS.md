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

## 4. Configuração operacional

- arquivo local: `config/doctor.json`
- variáveis de ambiente críticas: nenhuma obrigatória
- variáveis opcionais do app: `APP_HOST`, `APP_PORT`, `OLLAMA_URL`,
  `OLLAMA_MODEL`, `OLLAMA_KEEP_ALIVE`, `OLLAMA_NUM_PREDICT`, `APP_THEME`,
  `APP_SHOW_THEME_PICKER`, `APP_QA_ENABLED`, `APP_QA_CONNECTOR`,
  `APP_QA_MODEL`, `APP_QA_OLLAMA_URL`, `APP_QA_KEEP_ALIVE`,
  `APP_QA_NUM_PREDICT`
- path de runtime state: nenhum
- path de logs: nenhum

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
python3 -m py_compile scripts/check_project_gate.py scripts/project_doctor.py
python3 -m py_compile app/server.py
```

Conferir:

- gate preenchido e defensável
- docs estruturais sem marcadores de scaffolding
- comando principal coerente entre README e OPERATIONS
- diff sem `.DS_Store`, cache ou export temporário
- ausência de dados de pacientes ou segredos
- app sobe localmente e endpoints principais respondem

## 6. Logs e diagnóstico

- logger principal: não há logger persistente de aplicação
- formato dos logs: saída textual dos scripts e requisições locais do servidor
- onde ler logs:
  - terminal local
- sinais de falha comuns:
  - `PROJECT_GATE.md` com resposta curta, vaga ou pendente
  - divergência entre README, AGENTS e OPERATIONS
  - placeholders de scaffolding em documentos principais
  - arquivo obrigatório ausente
  - Ollama indisponível ou modelo local ausente no endpoint `/api/qa`
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
- backup: remoto Git e cópia local independente da publicação original externa,
  quando necessária para auditoria clínica.
- retenção: histórico Git conforme política do repositório.
- limpeza segura: `.DS_Store`, caches, arquivos temporários e exports locais
  não versionados.

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
