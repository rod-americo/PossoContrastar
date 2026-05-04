# Posso Contrastar?

Repositório para organizar, governar e reutilizar diretrizes sobre meios de
contraste, com foco em leitura técnica, rastreabilidade de fonte e experiências
clínicas operacionais locais de apoio à decisão.

Este trabalho é baseado no livro **Meios de contraste: conceitos e diretrizes
(versão pocket)**. O repositório transforma o conteúdo em corpus Markdown,
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
Radiologia e Diagnóstico por Imagem (SPR). Este repositório guarda apenas uma
conversão Markdown local para leitura, busca, RAG restrito e prototipagem de
apoio à decisão.

## Licença

O código, scripts, configuração do app, kits visuais anônimos e documentação
original deste repositório são distribuídos sob a licença MIT; veja
[`LICENSE`](LICENSE).

A licença MIT não altera os direitos autorais da obra-fonte nem concede licença
de redistribuição independente da publicação **Meios de contraste: conceitos e
diretrizes (versão pocket)**. O corpus convertido em
`docs/meios_de_contraste/` deve ser usado respeitando a titularidade e as
condições da publicação original.

## Público-alvo e nomenclatura

A linguagem do app e dos documentos operacionais deve funcionar para técnicos
de radiologia, técnicos de enfermagem, tecnólogos, enfermeiros, biomédicos,
residentes de radiologia e radiologistas.

Neste repositório, **equipe de sala** significa técnicos de radiologia,
técnicos de enfermagem, tecnólogos, enfermeiros e biomédicos. **Residentes de
radiologia** inclui R1, R2, R3 e R4. **Radiologista responsável** significa
radiologista que valida exceções, risco-benefício e condutas fora do fluxo.

## O que este repositório é

- Acervo documental em Markdown derivado da publicação **Meios de contraste:
  conceitos e diretrizes**, versão pocket, editada por Bruna Garbugio Dutra e
  Tufik Bauab Jr.
- Base de consulta para equipe de sala, residentes de radiologia,
  radiologistas e governança institucional sobre uso seguro de meios de
  contraste.
- Espaço para kits de identidade visual que apoiam páginas, documentos e
  protótipos relacionados ao material.
- Aplicação local whitelabel de apoio à decisão, com regras determinísticas,
  RAG restrita ao corpus local e adaptadores visuais.
- Metadado estruturado da obra-fonte em
  `docs/meios_de_contraste/source.json`, consumido pelo app e pela API local.

## O que este repositório NÃO é

- Não é protocolo institucional final, prescrição médica, dispositivo médico ou
  substituto da publicação original, de bulas oficiais e de validação clínica
  local.
- Não é aplicação em produção, protocolo institucional aprovado, prescrição,
  dispositivo médico ou substituto de revisão clínica.
- Não deve carregar dados de pacientes, credenciais, sessões, logs clínicos ou
  artefatos derivados sem governança explícita.
- Não deve promover regras clínicas a protocolo final sem contrato, citação,
  revisão por responsável técnico e aprovação institucional.

## Estado atual

- fase: `app local de apoio à decisão`
- runtime principal: `python3 app/server.py`
- entrypoints principais:
  - `python3 scripts/check_project_gate.py`
  - `python3 scripts/project_doctor.py`
  - `python3 scripts/project_doctor.py --audit-config`
  - `python3 app/server.py`
- dependência externa crítica:
  - Ollama opcional para Perguntas e Respostas e validação humana especializada
    para uso clínico. O PDF de origem não é versionado neste repositório.

## Conteúdo principal

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

Não há instalação obrigatória de dependências de aplicação. O backend local usa
apenas biblioteca padrão do Python. Ollama é opcional para Perguntas e
Respostas.

### 3. Configurar

```bash
test -f config/doctor.json
```

### 4. Rodar

```bash
python3 app/server.py
```

## Validação

Checklist mínimo antes de commitar:

- `python3 scripts/check_project_gate.py`
- `python3 scripts/project_doctor.py`
- `python3 scripts/project_doctor.py --audit-config`
- `python3 -m py_compile scripts/check_project_gate.py scripts/project_doctor.py`
- `python3 -m py_compile app/server.py`
- revisão de `git diff`

## Fonte e segurança clínica

O material em `docs/meios_de_contraste/` é um corpus Markdown versionado,
importado a partir de publicação técnica externa que não mora neste repo. O app
em `app/` é apoio à decisão e protótipo operacional local. Para decisões
clínicas, consulte sempre a publicação original, protocolos institucionais
vigentes, bulas oficiais e responsáveis técnicos habilitados.

## Próximos passos

1. Revisar os capítulos contra a publicação original mantida fora do repo.
2. Definir ownership técnico-clínico para mudanças de conteúdo.
3. Evoluir validação clínica, testes de cenários e processo de aprovação antes
   de qualquer uso assistencial institucional.
