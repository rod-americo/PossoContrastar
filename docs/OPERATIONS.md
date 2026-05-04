# OPERATIONS

## 1. Objetivo

Este documento descreve como validar, diagnosticar e manter o repositorio
documental e o app local de apoio à decisão. Nao ha deploy, autenticacao ou
runtime assistencial em producao nesta fase.

## 2. Ambientes

| Ambiente | Objetivo | Runtime | Observacoes |
| --- | --- | --- | --- |
| `local` | edicao e validacao | `python3` | Usa biblioteca padrao |
| `app-local` | UI e API local | `python3 app/server.py` | Ollama opcional para Perguntas e Respostas |
| `git` | historico e revisao | `git` | Preserva Markdown, regras e kits |
| `consumer` | repositorios que reutilizam o acervo | variavel | Deve validar uso proprio |

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

## 4. Configuracao operacional

- arquivo local: `config/doctor.json`
- variaveis de ambiente criticas: nenhuma obrigatoria
- variaveis opcionais do app: `APP_HOST`, `APP_PORT`, `OLLAMA_URL`,
  `OLLAMA_MODEL`, `OLLAMA_KEEP_ALIVE`, `OLLAMA_NUM_PREDICT`
- path de runtime state: nenhum
- path de logs: nenhum

O repositorio nao deve depender de caminhos locais implicitos. Kits cromaticos
nao devem carregar nomes institucionais, logos, URLs de origem ou assets
proprietarios.

## 5. Validacao minima

Depois de alterar a baseline ou documentos estruturais:

```bash
python3 scripts/project_doctor.py
```

Validacao completa recomendada:

```bash
python3 scripts/check_project_gate.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --audit-config
python3 -m py_compile scripts/check_project_gate.py scripts/project_doctor.py
python3 -m py_compile app/server.py
```

Conferir:

- gate preenchido e defensavel
- docs estruturais sem marcadores de scaffolding
- comando principal coerente entre README e OPERATIONS
- diff sem `.DS_Store`, cache ou export temporario
- ausencia de dados de pacientes ou segredos
- app sobe localmente e endpoints principais respondem

## 6. Logs E Diagnostico

- logger principal: nao ha logger persistente de aplicacao
- formato dos logs: saida textual dos scripts e requisicoes locais do servidor
- onde ler logs:
  - terminal local
- sinais de falha comuns:
  - `PROJECT_GATE.md` com resposta curta, vaga ou pendente
  - divergencia entre README, AGENTS e OPERATIONS
  - placeholders de scaffolding em documentos principais
  - arquivo obrigatorio ausente
  - Ollama indisponivel ou modelo local ausente no endpoint `/api/qa`
  - JSON invalido em `app/data/`

## 7. Restart policy

Ao mudar:

- `docs/meios_de_contraste/`: reiniciar app para Perguntas e Respostas e
  regras refletirem corpus;
  exige revisao documental e, quando clinico, revisao especializada.
- `docs/identidade_visual/`: nenhum restart; exige revisar previews afetados.
- `scripts/`: nenhum restart; exige `py_compile` e execucao do doctor.
- `config/`: nenhum restart; exige `project_doctor.py --audit-config`.
- `docs/` estruturais apenas: nenhum restart; exige doctor e revisao de diff.
- `app/server.py`, `app/data/`, `app/static/`: reiniciar servidor local.

## 8. Persistencia, backup e limpeza

- armazenamento principal: Git.
- backup: remoto Git e copia local independente da publicacao original externa,
  quando necessaria para auditoria clinica.
- retencao: historico Git conforme politica do repositorio.
- limpeza segura: `.DS_Store`, caches, arquivos temporarios e exports locais
  nao versionados.

Nunca remova sem decisao explicita:

- `docs/meios_de_contraste/`
- historico de decisoes em `docs/DECISIONS.md`

## 9. Incidentes

Checklist minimo:

1. confirmar que o corpus Markdown ainda existe
2. confirmar que o capitulo alterado esta indexado
3. confirmar que o doctor passa
4. revisar se a mudanca altera contrato clinico ou apenas formatacao
5. confirmar se ha dado sensivel ou material temporario no diff

## 10. Mudancas que exigem update deste documento

- novo entrypoint
- nova dependencia operacional
- novo path de runtime
- nova regra de validacao
- nova rotina de backup, publicacao ou limpeza
