# ARCHITECTURE

## 1. Objetivo

Descrever a arquitetura real do repositório como acervo documental governado e aplicação local whitelabel de apoio à decisão sobre meios de contraste.

## 2. Escopo

- Acervo Markdown sobre meios de contraste, importado de publicação técnica
externa não versionada neste repo, com metadado bibliográfico estruturado em `docs/meios_de_contraste/source.json`.
- Governança documental para fronteira, validação e revisão por diff.
- Kits de identidade visual usados como referência para materiais e protótipos.
- Scripts locais de gate e doctor para consistência estrutural.
- Aplicação local em `app/`, com backend Python, frontend estático, regras
determinísticas, calculadoras e módulo de Perguntas e Respostas restrito ao corpus local.
- Exclusão explícita de aplicação assistencial em produção, dados de pacientes
e protocolos institucionais finais.

## 3. Não escopo

- Decisão clínica automatizada ou recomendação personalizada para pacientes.
- Deploy web, autenticação corporativa, prontuário, PACS, RIS ou auditoria
clínica formal.
- Persistência operacional de dados, logs clínicos ou dados de pacientes. A
exceção local da v1 é o log de perguntas do Q&A em JSONL, usado para melhorar RAG e mantido fora do Git.
- Sistema oficial de design de marcas externas.

## 4. Layout atual

```text . ├── README.md ├── AGENTS.md ├── PROJECT_GATE.md ├── START_CHECKLIST.md ├── CHANGELOG.md ├── .githooks/ │   └── pre-commit ├── .github/ │   └── workflows/ │       └── ci.yml ├── config/ │   └── doctor.json ├── docs/ │   ├── ARCHITECTURE.md │   ├── CONTRACTS.md │   ├── OPERATIONS.md │   ├── DECISIONS.md │   ├── APP_REVIEW.md │   ├── meios_de_contraste/ │   └── identidade_visual/ ├── scripts/ │   ├── check_project_gate.py │   ├── smoke_app.py │   ├── install_git_hooks.sh │   └── project_doctor.py ├── app/ │   ├── README.md │   ├── server.py │   ├── data/ │   └── static/ ├── tests/ │   └── test_app_rules.py
```

## 5. Fluxo principal

1. O conteúdo clínico vive em `docs/meios_de_contraste/`, separado por
   capítulo e indexado por `docs/meios_de_contraste/README.md`.
2. Kits cromáticos neutros vivem em `docs/identidade_visual/` e são tratados
   como apoio documental para apresentações, páginas e protótipos.
3. Mudanças passam por leitura dos documentos estruturais, revisão de diff e
   validação com `python3 scripts/project_doctor.py`.
4. O app local em `app/` consome o corpus e os contratos estruturados para
   apresentar regras, calculadoras, biblioteca, busca e Perguntas e Respostas.
5. Qualquer uso assistencial exige validação clínica e aprovação institucional
   fora da v1.

## 6. Composition root e runtime

`app/server.py` é o composition root real da aplicação v1. Ele concentra:

- carregamento de configuração versionada e local:
  `app/data/app_config.example.json`, `app/data/app_config.json` e variáveis
  `APP_*`/`OLLAMA_*`;
- leitura do corpus em `docs/meios_de_contraste/`;
- cache em memória de capítulos e chunks de busca/RAG;
- leitura de regras determinísticas em `app/data/rules.json`;
- cálculo renal, decisão, intervalos, pediatria e extravasamento;
- endpoints HTTP locais sob `/api/...`;
- entrega de `app/static/index.html`, `app/static/app.js` e
  `app/static/styles.css`.

Não há framework web, worker, banco, fila ou camada de autenticação nesta fase.
Essa simplicidade é consciente: o app é local e whitelabel, não um serviço
assistencial remoto.

## 7. Interfaces reais

### HTTP local

Endpoints `GET`:

- `/api/health`: estado básico do app, Q&A e corpus carregado.
- `/api/chapters`: capítulos Markdown carregados para biblioteca.
- `/api/source`: metadados bibliográficos da obra-fonte.
- `/api/app-config`: configuração efetiva do app.
- `/api/rules`: regras determinísticas versionadas.
- `/api/search?q=...`: recuperação lexical sobre o corpus local.

Endpoints `POST`:

- `/api/decision`: apoio à decisão com cards explicáveis.
- `/api/renal-function`: cálculo renal isolado.
- `/api/calculators/renal`: hidratação/metformina e função renal.
- `/api/calculators/interval`: intervalo entre contrastes e coleta laboratorial.
- `/api/calculators/pediatric`: doses pediátricas e medicamentos de emergência.
- `/api/extravasation`: condutas estruturadas de extravasamento.
- `/api/qa`: Perguntas e Respostas, apenas quando habilitado.

### Interface estática

`app/static/app.js` orquestra navegação, chamadas HTTP, renderização de
Markdown, cards de decisão, biblioteca, busca, calculadoras e Q&A. A UI não é
fonte de regra clínica; ela consome o backend local e `app/data/rules.json`.

## 8. Módulos documentais e de código

| Área | Responsabilidade | Observação |
| --- | --- | --- |
| raiz | Identidade, governança e validação | Não deve receber runtime mutável |
| `docs/meios_de_contraste/` | Capítulos Markdown, índice e metadado da obra-fonte | Fonte canônica editável do guia convertido |
| `docs/identidade_visual/` | Kits cromáticos neutros e previews | Apoio, não design system oficial |
| `app/` | Backend local, UI whitelabel, regras e Perguntas e Respostas | Apoio à decisão, não produção |
| `scripts/` | Validação estrutural | Biblioteca padrão do Python |
| `tests/` | Regressão técnica do app local | Não valida verdade clínica |
| `.github/workflows/ci.yml` | Gate remoto de validação | Sem deploy |
| `config/doctor.json` | Política local do doctor | Versionado e auditável |

## 9. Persistência e estado

- Persistência versionada: Markdown, JSON de regras, config example, scripts,
  kits cromáticos e docs estruturais.
- Persistência local ignorada: `app/data/app_config.json` e
  `app/data/qa_questions.jsonl`.
- Caches de execução: `__pycache__/`, `.pytest_cache/`, `.playwright-mcp/` e
  arquivos equivalentes devem permanecer fora do Git.
- Logs persistentes gerais: inexistentes. O servidor escreve requisições no
  stderr; o Q&A pode gravar somente perguntas e metadados mínimos em JSONL.

## 10. Hotspots

- Tabelas clínicas densas podem perder nuance durante conversão para Markdown.
- Doses, limiares e condutas exigem revisão especializada antes de reuso
  operacional.
- `app/data/rules.json` precisa permanecer alinhado aos capítulos citados.
- Fórmulas renais e limiares ficam em código Python e JSON; há regressão
  técnica versionada, mas não validação clínica especializada.
- Perguntas e Respostas via Ollama pode falhar por modelo ausente; fallback deve
  ser conservador.
- `app/data/qa_questions.jsonl` pode conter texto sensível digitado pelo
  usuário; não versionar nem compartilhar sem revisão.
- Fontes de identidade visual podem mudar fora deste repositório.

## 11. Fronteiras de layout

O app já está em `app/`, que funciona como módulo principal do runtime. Não há
requisito atual para `src/`, packaging Python, monorepo ou separação formal em
`domain/application/infrastructure/interfaces`. Qualquer reorganização deve
nascer de uma necessidade real: testes, reutilização, deploy ou redução de
acoplamento demonstrada por código.

## 12. Direção de evolução

Para evoluir produto clínico, preservar separação:

- corpus documental e citações
- motor determinístico de regras
- interface e experiência de uso
- validação clínica, testes de cenários e auditoria
- logs, segurança e operação
