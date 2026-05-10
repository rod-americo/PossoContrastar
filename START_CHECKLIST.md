# Start Checklist

Checklist de continuidade para um repositório existente. Este arquivo não
declara prontidão operacional; ele registra o que já está consolidado, o que
continua parcial e o que não deve ser feito na próxima rodada.

## 0. Identidade e fronteira

- [x] O repositório tem fronteira explícita em `PROJECT_GATE.md`.
- [x] O corpus canônico vive em `docs/meios_de_contraste/`.
- [x] O PDF de origem fica fora do Git.
- [x] O app local está isolado em `app/`, sem espalhar runtime de produção na
  raiz.
- [ ] Existe validação formal de equivalência entre corpus Markdown e
  publicação original externa.
- [ ] Existe protocolo institucional aprovado para uso assistencial.

## 1. Baseline documental

- [x] `README.md` descreve identidade, não escopo, entrypoints e maturidade.
- [x] `AGENTS.md` registra leitura mínima, idioma, camadas e guardrails.
- [x] `PROJECT_GATE.md` justifica a existência do repo separado.
- [x] `CHANGELOG.md` concentra histórico de mudanças relevantes.
- [x] `docs/ARCHITECTURE.md` descreve o layout e fluxo reais.
- [x] `docs/CONTRACTS.md` registra entradas, saídas, invariantes e limites.
- [x] `docs/OPERATIONS.md` registra execução, validação, restart e diagnóstico.
- [x] `docs/DECISIONS.md` registra decisões arquiteturais já assumidas.
- [x] `app/README.md` documenta o runtime local do app.

## 2. Código e runtime

- [x] Entrypoint principal real: `python3 app/server.py`.
- [x] Backend local usa biblioteca padrão do Python.
- [x] Frontend estático fica em `app/static/`, sem build step.
- [x] Regras determinísticas ficam em `app/data/rules.json`.
- [x] Configuração local não versionada: `app/data/app_config.json`.
- [x] Log local de perguntas do Q&A ignorado pelo Git:
  `app/data/qa_questions.jsonl`.
- [x] Existe suíte automatizada de regressão técnica para regras e endpoints
  locais.
- [x] Existe CI remoto configurado neste repositório.
- [ ] Existe autenticação, auditoria clínica formal ou deploy assistencial.

## 3. Operação mínima

- [x] Gate local: `python3 scripts/check_project_gate.py`.
- [x] Doctor estrutural: `python3 scripts/project_doctor.py`.
- [x] Auditoria de policy: `python3 scripts/project_doctor.py --audit-config`.
- [x] Checagem sintática de scripts e app documentada em `docs/OPERATIONS.md`.
- [x] Hook local versionado em `.githooks/pre-commit`.
- [x] Instalador de hooks local em `scripts/install_git_hooks.sh`.
- [ ] Hook local instalado automaticamente em todos os clones.
- [ ] Smoke de Q&A com Ollama é obrigatório; por enquanto é opcional porque o
  Q&A vem desabilitado no template versionado.

## 4. Hotspots que permanecem

- [ ] Tabelas e hierarquia visual do corpus convertido ainda podem divergir da
  publicação original.
- [ ] `app/data/rules.json` precisa de revisão clínica especializada contra os
  capítulos citados.
- [ ] Perguntas registradas em `app/data/qa_questions.jsonl` podem conter dados
  sensíveis digitados pelo usuário e não devem ser compartilhadas sem revisão.
- [ ] O fallback do Q&A depende da qualidade de recuperação lexical do corpus.
- [x] Há testes automatizados de regressão técnica para endpoints HTTP e
  cenários de fronteira das calculadoras.

## 5. Próxima rodada segura

- [x] Criar testes pequenos para funções puras de `app/server.py`, começando
  por cálculo renal, intervalômetro, pediatria e extravasamento.
- [x] Automatizar smoke HTTP que suba o servidor em porta temporária e cheque
  `/api/health`, `/api/source`, `/api/rules` e uma chamada `/api/decision`.
- [ ] Revisar `app/data/rules.json` contra a publicação original e registrar
  fonte, capítulo e motivo para qualquer ajuste clínico.
- [x] Decidir se haverá CI remoto antes de exigir checks de pull request.
- [x] Definir política de retenção local para `app/data/qa_questions.jsonl`.

## 6. O que não fazer

- [ ] Não mover o app para `src/` nem criar camadas artificiais sem necessidade
  demonstrada.
- [ ] Não transformar `docs/meios_de_contraste/` em resumo gerado sem
  rastreabilidade.
- [ ] Não habilitar Q&A por padrão sem decisão operacional explícita.
- [ ] Não declarar o app como produto assistencial, protocolo aprovado ou
  dispositivo médico.
- [ ] Não versionar PDF, dumps, logs, caches, perguntas reais ou configuração
  local.
