# Posso Contrastar?

Repositório para organizar, governar e reutilizar diretrizes sobre meios de
contraste, com foco em leitura técnica, rastreabilidade de fonte e experiências
clínicas operacionais locais de apoio à decisão.

Este trabalho é baseado no livro **Meios de contraste: conceitos e diretrizes
(versão pocket)**. O repositório transforma o conteúdo em corpus Markdown,
contratos, regras explicáveis e uma aplicação local whitelabel de apoio à
decisão; ele não substitui o livro, não versiona o PDF original e não representa
protocolo institucional aprovado.

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
conversão Markdown local para leitura, busca, Perguntas e Respostas restrito ao
corpus quando habilitado e prototipagem de apoio à decisão.

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
  calculadoras, biblioteca, busca, renderização de Markdown e adaptadores
  visuais.
- Módulo de Perguntas e Respostas restrito ao corpus local, com Ollama opcional,
  atualmente desabilitado no template versionado e ativável por configuração.
- Metadado estruturado da obra-fonte em
  `docs/meios_de_contraste/source.json`, consumido pelo app e pela API local.
- Avaliação e backlog do app em `docs/APP_REVIEW.md`, orientados para rodadas
  futuras de codificação e validação.

## O que este repositório NÃO é

- Não é protocolo institucional final, prescrição médica, dispositivo médico ou
  substituto da publicação original, de bulas oficiais e de validação clínica
  local.
- Não é aplicação assistencial em produção nem serviço web público.
- Não deve carregar dados de pacientes, credenciais, sessões, logs clínicos ou
  artefatos derivados sem governança explícita.
- Não deve promover regras clínicas a protocolo final sem contrato, citação,
  revisão por responsável técnico e aprovação institucional.

Quando o módulo Perguntas e Respostas estiver habilitado, perguntas feitas ao
módulo são gravadas localmente em `app/data/qa_questions.jsonl` para melhoria
posterior do RAG. Esse arquivo não deve ser versionado e pode exigir revisão
antes de qualquer compartilhamento.

## Estado atual

- fase: `app local de apoio à decisão`
- runtime principal: `python3 app/server.py`, com `app/server.py` como
  composition root, API HTTP local e servidor de arquivos estáticos
- frontend: HTML/CSS/JS estático, sem build step
- backend: Python com biblioteca padrão
- contratos determinísticos: `app/data/rules.json`
- corpus canônico: `docs/meios_de_contraste/`
- Q&A: disponível por configuração, mas desabilitado por padrão em
  `app/data/app_config.example.json`
- entrypoints principais:
  - `python3 scripts/check_project_gate.py`
  - `python3 scripts/project_doctor.py`
  - `python3 scripts/project_doctor.py --audit-config`
  - `python3 -m unittest discover -s tests -p 'test_*.py'`
  - `python3 scripts/smoke_app.py`
  - `python3 app/server.py`
- dependência externa crítica:
  - Ollama opcional quando Perguntas e Respostas estiver habilitado.
  - Validação humana especializada para qualquer uso clínico. O PDF de origem
    não é versionado neste repositório.

## Conteúdo principal

```text
PossoContrastar/
├── README.md
├── AGENTS.md
├── PROJECT_GATE.md
├── START_CHECKLIST.md
├── CHANGELOG.md
├── .githooks/
│   └── pre-commit
├── .github/
│   └── workflows/
│       └── ci.yml
├── config/
│   └── doctor.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONTRACTS.md
│   ├── OPERATIONS.md
│   ├── DECISIONS.md
│   ├── APP_REVIEW.md
│   ├── identidade_visual/
│   └── meios_de_contraste/
├── scripts/
│   ├── check_project_gate.py
│   ├── smoke_app.py
│   ├── install_git_hooks.sh
│   └── project_doctor.py
├── app/
│   ├── README.md
│   ├── server.py
│   ├── data/
│   └── static/
├── tests/
│   └── test_app_rules.py
```

O layout atual deve ser preservado enquanto ele refletir o sistema real. A
aplicação principal já vive em `app/`; não há ganho em mover para `src/` ou
criar camadas `domain/application/infrastructure` artificiais nesta fase.

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
apenas biblioteca padrão do Python. Ollama é opcional e só é usado quando
Perguntas e Respostas estiver habilitado.

### 3. Configurar

```bash
test -f config/doctor.json
```

O template versionado do app fica em `app/data/app_config.example.json`.
Configuração local pode ser feita em `app/data/app_config.json`, que é ignorado
pelo Git, ou por variáveis de ambiente. O Q&A vem desabilitado por padrão; para
ativá-lo localmente use `APP_QA_ENABLED=true` e configure `APP_QA_OLLAMA_URL`
quando o Ollama estiver em outra máquina.

### 4. Rodar

```bash
python3 app/server.py
```

Abrir em `http://127.0.0.1:8765`.

Exemplo com Perguntas e Respostas habilitado:

```bash
APP_QA_ENABLED=true APP_QA_OLLAMA_URL=http://127.0.0.1:11434 python3 app/server.py
```

## Validação

Checklist mínimo antes de commitar:

- `python3 scripts/check_project_gate.py`
- `python3 scripts/project_doctor.py`
- `python3 scripts/project_doctor.py --audit-config`
- `python3 -m py_compile scripts/check_project_gate.py scripts/project_doctor.py scripts/smoke_app.py`
- `python3 -m py_compile app/server.py`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/smoke_app.py`
- revisão de `git diff`

O fluxo de colaboração do repositório espera commit e push quando uma tarefa
gerar mudança versionável, preservando alterações não relacionadas feitas por
outra pessoa.

A suíte versionada cobre regressões técnicas de cálculo, regras locais,
recuperação e contratos HTTP básicos. Ela não valida verdade clínica; mudanças
clínicas continuam exigindo revisão especializada contra a fonte citada.

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
