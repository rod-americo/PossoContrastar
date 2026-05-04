# ARCHITECTURE

## 1. Objetivo

Descrever a arquitetura real do repositório como acervo documental governado e
aplicação local whitelabel de apoio à decisão sobre meios de contraste.

## 2. Escopo

- Acervo Markdown sobre meios de contraste, importado de publicação técnica
  externa não versionada neste repo, com metadado bibliográfico estruturado em
  `docs/meios_de_contraste/source.json`.
- Governança documental para fronteira, validação e revisão por diff.
- Kits de identidade visual usados como referência para materiais e protótipos.
- Scripts locais de gate e doctor para consistência estrutural.
- Aplicação local em `app/`, com backend Python, frontend estático, regras
  determinísticas, calculadoras e módulo de Perguntas e Respostas restrito ao
  corpus local.
- Exclusão explícita de aplicação assistencial em produção, dados de pacientes
  e protocolos institucionais finais.

## 3. Não escopo

- Decisão clínica automatizada ou recomendação personalizada para pacientes.
- Deploy web, autenticação corporativa, prontuário, PACS, RIS ou auditoria
  clínica formal.
- Persistência operacional de dados, logs clínicos ou dados de pacientes.
- Sistema oficial de design de marcas externas.

## 4. Layout atual

```text
.
├── README.md
├── AGENTS.md
├── PROJECT_GATE.md
├── CHANGELOG.md
├── config/
│   └── doctor.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONTRACTS.md
│   ├── OPERATIONS.md
│   ├── DECISIONS.md
│   ├── APP_REVIEW.md
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

## 6. Módulos documentais

| Área | Responsabilidade | Observação |
| --- | --- | --- |
| raiz | Identidade, governança e validação | Não deve receber runtime mutável |
| `docs/meios_de_contraste/` | Capítulos Markdown, índice e metadado da obra-fonte | Fonte canônica editável do guia convertido |
| `docs/identidade_visual/` | Kits cromáticos neutros e previews | Apoio, não design system oficial |
| `app/` | Backend local, UI whitelabel, regras e Perguntas e Respostas | Apoio à decisão, não produção |
| `scripts/` | Validação estrutural | Biblioteca padrão do Python |
| `config/doctor.json` | Política local do doctor | Versionado e auditável |

## 7. Hotspots

- Tabelas clínicas densas podem perder nuance durante conversão para Markdown.
- Doses, limiares e condutas exigem revisão especializada antes de reuso
  operacional.
- `app/data/rules.json` precisa permanecer alinhado aos capítulos citados.
- Perguntas e Respostas via Ollama pode falhar por modelo ausente; fallback deve
  ser conservador.
- Fontes de identidade visual podem mudar fora deste repositório.

## 8. Direção de evolução

Para evoluir produto clínico, preservar separação:

- corpus documental e citações
- motor determinístico de regras
- interface e experiência de uso
- validação clínica, testes de cenários e auditoria
- logs, segurança e operação
