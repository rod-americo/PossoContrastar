# AGENTS.md

Este arquivo define regras de colaboracao para agentes e autores neste
repositorio. Ele vale para a raiz inteira.

## Ordem minima de leitura

Antes de fazer mudancas significativas, leia nesta ordem:

1. `README.md`
2. `PROJECT_GATE.md`
3. `docs/ARCHITECTURE.md`
4. `docs/CONTRACTS.md`
5. `docs/OPERATIONS.md`
6. `docs/DECISIONS.md`
7. `docs/meios_de_contraste/README.md`
8. `docs/identidade_visual/README.md`

## Politica de idioma

- Documentacao humana em `pt-BR`.
- Identificadores tecnicos em `en-US`.
- Mensagens de commit em `en-US`, preferencialmente
  `type(scope): summary`.

Preserve nomes de marcas, farmacos, siglas clinicas, titulos de fonte e nomes
de arquivos ja existentes quando eles forem parte do contrato documental.

## Escopo

Este repositorio guarda diretrizes e kits documentais. Nao transforme o acervo
em aplicacao, API, motor de decisao clinica ou produto assistencial sem criar
contratos, validacao e decisao arquitetural correspondentes.

Regras praticas:

- `docs/meios_de_contraste/` e o corpus Markdown canonico versionado.
- O PDF de origem nao deve ser versionado neste repositorio.
- `docs/identidade_visual/` contem kits cromaticos neutros para materiais,
  prototipos e adaptadores, sem marcas, logos ou nomes institucionais.
- `app/` contem uma aplicacao local whitelabel de apoio à decisão, com backend
  Python, regras deterministicas e Q&A restrita ao corpus local via Ollama.
- Mudancas clinicas devem citar fonte, capitulo e motivo.
- Nao inserir dados de pacientes, credenciais, logs assistenciais ou payloads
  sensiveis.

## Camadas documentais

- Raiz: governanca, fronteira, gate, changelog e scripts de validacao.
- `docs/ARCHITECTURE.md`: mapa do acervo e fluxo de manutencao.
- `docs/CONTRACTS.md`: entradas, saidas, invariantes e limites clinicos.
- `docs/OPERATIONS.md`: validacao, revisao, backup e troubleshooting.
- `docs/DECISIONS.md`: decisoes estruturais que condicionam evolucao.
- `docs/meios_de_contraste/`: capitulos canonicamente editaveis em Markdown.
- `docs/identidade_visual/`: kits de identidade visual e previews.
- `app/`: runtime local, API, UI whitelabel e contratos estruturados de regras.

## Validacao minima

- comando de validacao minima: `python3 scripts/project_doctor.py`
- gate check local: `python3 scripts/check_project_gate.py`
- doctor estrutural: `python3 scripts/project_doctor.py`
- doctor estrito: `python3 scripts/project_doctor.py --strict`
- doctor audit: `python3 scripts/project_doctor.py --audit-config`
- checagem sintatica: `python3 -m py_compile scripts/check_project_gate.py scripts/project_doctor.py`
- checagem sintatica do app: `python3 -m py_compile app/server.py`
- policy do doctor: `config/doctor.json`

## Hotspots conhecidos

- Conteudo clinico convertido para Markdown pode perder semantica de tabelas,
  notas de rodape e hierarquia visual.
- `docs/meios_de_contraste/proposta_apresentacao_dinamica.md` e proposta de
  produto; `app/` implementa uma v1 local de apoio à decisão, ainda sem
  validacao assistencial formal.
- Kits em `docs/identidade_visual/` sao cromaticos e anonimos; nao adicionar
  nomes institucionais, logos, URLs de origem ou assets proprietarios.
- O repositorio ainda nao tem teste de equivalencia entre corpus Markdown e a
  publicacao original externa.

## Guardrails

- Nao declarar prontidao assistencial sem revisao clinica formal.
- Nao substituir texto fonte por resumo gerado sem manter rastreabilidade.
- Calculadoras, doses e fluxos de conduta devem permanecer em contrato
  deterministico, citados por fonte e tratados como apoio à decisão ate revisao
  especializada.
- Nao versionar `.DS_Store`, caches, dumps, exports temporarios ou runtime
  mutavel.
- Atualize `README.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md` e
  `docs/OPERATIONS.md` quando a fronteira ou a rotina de manutencao mudar.
