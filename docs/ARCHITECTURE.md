# ARCHITECTURE

## 1. Objetivo

Descrever a arquitetura real do repositorio como acervo documental governado e
aplicacao local whitelabel de apoio à decisão sobre meios de contraste.

## 2. Escopo

- Acervo Markdown sobre meios de contraste, importado de publicacao tecnica
  externa nao versionada neste repo, com metadado bibliografico estruturado em
  `docs/meios_de_contraste/source.json`.
- Governanca documental para fronteira, validacao e revisao por diff.
- Kits de identidade visual usados como referencia para materiais e prototipos.
- Scripts locais de gate e doctor para consistencia estrutural.
- Aplicacao local em `app/`, com backend Python, frontend estatico, regras
  deterministicas, calculadoras e modulo de Perguntas e Respostas restrito ao
  corpus local.
- Exclusao explicita de aplicacao assistencial em producao, dados de pacientes
  e protocolos institucionais finais.

## 3. Nao escopo

- Decisao clinica automatizada ou recomendacao personalizada para pacientes.
- Deploy web, autenticacao corporativa, prontuario, PACS, RIS ou auditoria
  clinica formal.
- Persistencia operacional de dados, logs clinicos ou dados de pacientes.
- Sistema oficial de design de marcas externas.

## 4. Layout atual

```text
.
├── README.md
├── AGENTS.md
├── PROJECT_GATE.md
├── CHANGELOG.md
├── START_CHECKLIST.md
├── config/
│   └── doctor.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONTRACTS.md
│   ├── OPERATIONS.md
│   ├── DECISIONS.md
│   ├── meios_de_contraste/
│   └── identidade_visual/
├── scripts/
│   ├── check_project_gate.py
│   ├── install_git_hooks.sh
│   └── project_doctor.py
├── app/
│   ├── README.md
│   ├── server.py
│   ├── data/
│   └── static/
```

## 5. Fluxo principal

1. O conteudo clinico vive em `docs/meios_de_contraste/`, separado por
   capitulo e indexado por `docs/meios_de_contraste/README.md`.
2. Kits cromaticos neutros vivem em `docs/identidade_visual/` e sao tratados
   como apoio documental para apresentacoes, paginas e prototipos.
3. Mudancas passam por leitura dos documentos estruturais, revisao de diff e
   validacao com `python3 scripts/project_doctor.py`.
4. O app local em `app/` consome o corpus e os contratos estruturados para
   apresentar regras, calculadoras, biblioteca, busca e Perguntas e Respostas.
5. Qualquer uso assistencial exige validacao clinica e aprovacao institucional
   fora da v1.

## 6. Modulos documentais

| Area | Responsabilidade | Observacao |
| --- | --- | --- |
| raiz | Identidade, governanca e validacao | Nao deve receber runtime mutavel |
| `docs/meios_de_contraste/` | Capitulos Markdown, indice e metadado da obra-fonte | Fonte canonica editavel do guia convertido |
| `docs/identidade_visual/` | Kits cromaticos neutros e previews | Apoio, nao design system oficial |
| `app/` | Backend local, UI whitelabel, regras e Perguntas e Respostas | Apoio à decisão, nao producao |
| `scripts/` | Validacao estrutural | Biblioteca padrao do Python |
| `config/doctor.json` | Politica local do doctor | Versionado e auditavel |

## 7. Hotspots

- Tabelas clinicas densas podem perder nuance durante conversao para Markdown.
- Doses, limiares e condutas exigem revisao especializada antes de reuso
  operacional.
- `app/data/rules.json` precisa permanecer alinhado aos capitulos citados.
- Perguntas e Respostas via Ollama pode falhar por modelo ausente; fallback deve
  ser conservador.
- Fontes de identidade visual podem mudar fora deste repositorio.

## 8. Direcao de evolucao

Para evoluir produto clinico, preservar separacao:

- corpus documental e citacoes
- motor deterministico de regras
- interface e experiencia de uso
- validacao clinica, testes de cenarios e auditoria
- logs, seguranca e operacao
