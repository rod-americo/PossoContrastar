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
7. `docs/meios_de_contraste/README.md`
8. `docs/identidade_visual/README.md`

## Política de idioma

- Documentação humana em `pt-BR`, com acentuação gráfica e cedilha.
- Identificadores técnicos em `en-US`.
- Mensagens de commit em `en-US`, preferencialmente
  `type(scope): summary`.

Preserve nomes de marcas, fármacos, siglas clínicas, títulos de fonte e nomes
de arquivos já existentes quando eles forem parte do contrato documental.

## Nomenclatura operacional

Use a mesma nomenclatura em UI, docs e fluxos de apoio à decisão:

- **Equipe de sala:** técnico de radiologia, técnico de enfermagem e
  enfermeiro.
- **Médico residente:** R1, R2, R3 ou R4.
- **Radiologista responsável:** radiologista formado que valida exceções,
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
- Mudanças clínicas devem citar fonte, capítulo e motivo.
- Não inserir dados de pacientes, credenciais, logs assistenciais ou payloads
  sensíveis.

## Camadas documentais

- Raiz: governança, fronteira, gate, changelog e scripts de validação.
- `docs/ARCHITECTURE.md`: mapa do acervo e fluxo de manutenção.
- `docs/CONTRACTS.md`: entradas, saídas, invariantes e limites clínicos.
- `docs/OPERATIONS.md`: validação, revisão, backup e troubleshooting.
- `docs/DECISIONS.md`: decisões estruturais que condicionam evolução.
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
- Calculadoras, doses e fluxos de conduta devem permanecer em contrato
  determinístico, citados por fonte e tratados como apoio à decisão até revisão
  especializada.
- Não versionar `.DS_Store`, caches, dumps, exports temporários ou runtime
  mutável.
- Atualize `README.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md` e
  `docs/OPERATIONS.md` quando a fronteira ou a rotina de manutenção mudar.
