# Posso Contrastar?

Repositorio para organizar, governar e reutilizar diretrizes sobre meios de
contraste, com foco em leitura tecnica, rastreabilidade de fonte e experiencias
clinicas operacionais locais de apoio à decisão.

Este trabalho é baseado no livro **Meios de contraste: conceitos e diretrizes
(versão pocket)**. O repositorio transforma o conteudo em corpus Markdown,
contratos, regras explicáveis e uma aplicação local de apoio à decisão; ele não
substitui o livro, não versiona o PDF original e não representa protocolo
institucional aprovado.

## Base bibliográfica

Obra-fonte:

> Dutra BG, Bauab Jr T, editores. **Meios de contraste: conceitos e diretrizes
> (versão pocket)**. 1. ed. São Paulo, SP: Farol Editora; São Caetano do Sul,
> SP: Sociedade Paulista de Radiologia e Diagnóstico por Imagem (SPR); 2026.

- Publicado no Brasil em abril de 2026.
- ISBN: `978-65-989971-1-3`
- DOI: `10.29327/5827214`
- Metadado estruturado: `docs/meios_de_contraste/source.json`

Os direitos autorais da publicação original pertencem à Sociedade Paulista de
Radiologia e Diagnóstico por Imagem (SPR). Este repositorio guarda apenas uma
conversão Markdown local para leitura, busca, RAG restrito e prototipagem de
apoio à decisão.

## O que este repositorio e

- Acervo documental em Markdown derivado da publicacao **Meios de contraste:
  conceitos e diretrizes**, versao pocket, editada por Bruna Garbugio Dutra e
  Tufik Bauab Jr.
- Base de consulta para radiologia, enfermagem, operacao assistencial e
  governanca institucional sobre uso seguro de meios de contraste.
- Espaco para kits de identidade visual que apoiam paginas, documentos e
  prototipos relacionados ao material.
- Aplicacao local whitelabel de apoio à decisão, com regras deterministicas,
  RAG restrita ao corpus local e adaptadores visuais.
- Metadado estruturado da obra-fonte em
  `docs/meios_de_contraste/source.json`, consumido pelo app e pela API local.

## O que este repositorio NAO e

- Nao e protocolo institucional final, prescricao medica, dispositivo medico ou
  substituto da publicacao original, de bulas oficiais e de validacao clinica
  local.
- Nao e aplicacao em producao, protocolo institucional aprovado, prescricao,
  dispositivo medico ou substituto de revisao clinica.
- Nao deve carregar dados de pacientes, credenciais, sessoes, logs clinicos ou
  artefatos derivados sem governanca explicita.
- Nao deve promover regras clinicas a protocolo final sem contrato, citacao,
  revisao por responsavel tecnico e aprovacao institucional.

## Estado atual

- fase: `app local de apoio à decisão`
- runtime principal: `python3 app/server.py`
- entrypoints principais:
  - `python3 scripts/check_project_gate.py`
  - `python3 scripts/project_doctor.py`
  - `python3 scripts/project_doctor.py --audit-config`
  - `python3 app/server.py`
- dependencia externa critica:
  - Ollama opcional para Perguntas e Respostas e validacao humana especializada
    para uso clinico. O PDF de origem nao e versionado neste repositorio.

## Conteudo principal

```text
PossoContrastar/
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
│   ├── identidade_visual/
│   └── meios_de_contraste/
├── scripts/
│   ├── check_project_gate.py
│   └── project_doctor.py
├── app/
│   ├── server.py
│   ├── data/
│   └── static/
```

## Quick start

### 1. Clonar

```bash
git clone <repo-url>
cd PossoContrastar
```

### 2. Preparar ambiente

```bash
python3 --version
```

Nao ha instalacao obrigatoria de dependencias de aplicacao. O backend local usa
apenas biblioteca padrao do Python. Ollama e opcional para Perguntas e
Respostas.

### 3. Configurar

```bash
test -f config/doctor.json
```

### 4. Rodar

```bash
python3 app/server.py
```

## Validacao

Checklist minimo antes de commitar:

- `python3 scripts/check_project_gate.py`
- `python3 scripts/project_doctor.py`
- `python3 scripts/project_doctor.py --audit-config`
- `python3 -m py_compile scripts/check_project_gate.py scripts/project_doctor.py`
- `python3 -m py_compile app/server.py`
- revisao de `git diff`

## Fonte e seguranca clinica

O material em `docs/meios_de_contraste/` e um corpus Markdown versionado,
importado a partir de publicacao tecnica externa que nao mora neste repo. O app
em `app/` e apoio à decisão e prototipo operacional local. Para decisoes
clinicas, consulte sempre a publicacao original, protocolos institucionais
vigentes, bulas oficiais e responsaveis tecnicos habilitados.

## Proximos passos

1. Revisar os capitulos contra a publicacao original mantida fora do repo.
2. Definir ownership tecnico-clinico para mudancas de conteudo.
3. Evoluir validacao clinica, testes de cenarios e processo de aprovacao antes
   de qualquer uso assistencial institucional.
