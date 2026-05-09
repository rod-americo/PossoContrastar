# AGENTS.md

Este arquivo define regras de colaboração para agentes e autores neste
repositório. Ele vale para a raiz inteira.

## Ordem mínima de leitura

Antes de fazer mudanças significativas, leia nesta ordem:

1. `README.md`
2. `PROJECT_GATE.md`
3. `docs/ARCHITECTURE.md`
4. `docs/CONTRACTS.md`
5. `docs/OPERATIONS.md`
6. `docs/DECISIONS.md`
7. `START_CHECKLIST.md`
8. `docs/meios_de_contraste/README.md`
9. `docs/identidade_visual/README.md`
10. `app/README.md` quando a mudança tocar o app local

## Política de idioma

- Documentação humana em `pt-BR`, com acentuação gráfica e cedilha.
- Identificadores técnicos em `en-US`.
- Mensagens de commit em `en-US`, preferencialmente
  `type(scope): summary`.

Preserve nomes de marcas, fármacos, siglas clínicas, títulos de fonte e nomes
de arquivos já existentes quando eles forem parte do contrato documental.

## Nomenclatura operacional

Use a mesma nomenclatura em UI, docs e fluxos de apoio à decisão:

- **Equipe de sala:** técnicos de radiologia, técnicos de enfermagem,
  tecnólogos, enfermeiros e biomédicos.
- **Residentes de radiologia:** R1, R2, R3 ou R4.
- **Radiologista responsável:** radiologista que valida exceções,
  risco-benefício e condutas fora do fluxo.

Evite rótulos genéricos como “operação”, “enfermagem” ou “técnico” quando o
contexto exigir identificar o papel.

## Escopo

Este repositório guarda diretrizes e kits documentais. Não transforme o acervo
em aplicação, API, motor de decisão clínica ou produto assistencial sem criar
contratos, validação e decisão arquitetural correspondentes.

Regras práticas:

- `docs/meios_de_contraste/` é o corpus Markdown canônico versionado.
- O PDF de origem não deve ser versionado neste repositório.
- `docs/identidade_visual/` contém kits cromáticos neutros para materiais,
  protótipos e adaptadores, sem marcas, logos ou nomes institucionais.
- `app/` contém uma aplicação local whitelabel de apoio à decisão, com backend
  Python, regras determinísticas e módulo de Perguntas e Respostas restrito ao
  corpus local via Ollama.
- `app/server.py` é o composition root real da v1: carrega configuração,
  corpus, regras, calculadoras, endpoints HTTP e arquivos estáticos.
- `app/data/rules.json` é contrato determinístico versionado; não transforme
  regra clínica em inferência livre de LLM.
- Mudanças clínicas devem citar fonte, capítulo e motivo.
- Não inserir dados de pacientes, credenciais, logs assistenciais ou payloads
  sensíveis.

## Camadas documentais

- Raiz: governança, fronteira, gate, changelog e scripts de validação.
- `docs/ARCHITECTURE.md`: mapa do acervo e fluxo de manutenção.
- `docs/CONTRACTS.md`: entradas, saídas, invariantes e limites clínicos.
- `docs/OPERATIONS.md`: validação, revisão, backup e troubleshooting.
- `docs/DECISIONS.md`: decisões estruturais que condicionam evolução.
- `START_CHECKLIST.md`: estado honesto da baseline, pendências e próximas
  rodadas seguras.
- `docs/meios_de_contraste/`: capítulos canonicamente editáveis em Markdown.
- `docs/identidade_visual/`: kits de identidade visual e previews.
- `app/`: runtime local, API, UI whitelabel e contratos estruturados de regras.

## Validação mínima

- comando de validação mínima: `python3 scripts/project_doctor.py`
- gate check local: `python3 scripts/check_project_gate.py`
- doctor estrutural: `python3 scripts/project_doctor.py`
- doctor estrito: `python3 scripts/project_doctor.py --strict`
- doctor audit: `python3 scripts/project_doctor.py --audit-config`
- checagem sintática: `python3 -m py_compile scripts/check_project_gate.py scripts/project_doctor.py`
- checagem sintática do app: `python3 -m py_compile app/server.py`
- policy do doctor: `config/doctor.json`

## Fluxo Git

- Quando uma tarefa gerar mudanças versionáveis, revisar o diff, executar a
  validação mínima aplicável, criar commit e fazer push para o remoto.
- Mensagens de commit devem seguir a política de idioma deste arquivo:
  `en-US`, preferencialmente `type(scope): summary`.
- Não incluir arquivos temporários, caches, dumps, dados sensíveis ou runtime
  mutável no commit.
- Se houver mudanças não relacionadas feitas por outra pessoa, preservá-las e
  commitar apenas o escopo da tarefa.

## Hotspots conhecidos

- Conteúdo clínico convertido para Markdown pode perder semântica de tabelas,
  notas de rodapé e hierarquia visual.
- `docs/meios_de_contraste/proposta_apresentacao_dinamica.md` é proposta de
  produto; `app/` implementa uma v1 local de apoio à decisão, ainda sem
  validação assistencial formal.
- Kits em `docs/identidade_visual/` são cromáticos e anônimos; não adicionar
  nomes institucionais, logos, URLs de origem ou assets proprietários.
- O repositório ainda não tem teste de equivalência entre corpus Markdown e a
  publicação original externa.

## Guardrails

- Não declarar prontidão assistencial sem revisão clínica formal.
- Não substituir texto fonte por resumo gerado sem manter rastreabilidade.
- Não mover o app para `src/` nem criar camadas artificiais só para aparentar
  maturidade arquitetural.
- Não habilitar Perguntas e Respostas por padrão sem decisão operacional
  explícita e atualização de contratos.
- Calculadoras, doses e fluxos de conduta devem permanecer em contrato
  determinístico, citados por fonte e tratados como apoio à decisão até revisão
  especializada.
- Não versionar `.DS_Store`, caches, dumps, exports temporários, logs
  `.playwright-mcp`, `app/data/app_config.json`, `app/data/qa_questions.jsonl`
  ou runtime mutável.
- Atualize `README.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md` e
  `docs/OPERATIONS.md` quando a fronteira ou a rotina de manutenção mudar.
