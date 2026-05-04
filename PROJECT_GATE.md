# PROJECT GATE

Este gate documenta por que o repositório existe como acervo próprio e quais
fronteiras impedem crescimento indefinido.

## 1. Por que este projeto existe?

- problema real: Centralizar diretrizes sobre meios de contraste em Markdown
  revisável, reduzindo dependência de material fechado para leitura, busca,
  citação e evolução documental.
- usuário ou operador-alvo: Técnico de radiologia, técnico de enfermagem,
  enfermeiro, R1, R2, R3, R4, radiologista formado, lideranças assistenciais e
  autores que mantêm materiais clínicos e operacionais derivados.
- resultado esperado: Um acervo governado e uma aplicação local de apoio à
  decisão, capazes de apoiar consulta, treinamento e prototipagem sem confundir
  a v1 com protocolo institucional aprovado.

## 2. Por que isto NÃO deveria ser um módulo?

- repositório candidato que poderia absorver isso: Repositórios de dashboards,
  coordenação radiológica ou automações clínicas poderiam consumir este acervo.
- por que esse acoplamento seria inadequado: Acoplar as diretrizes a uma
  aplicação específica faria conteúdo clínico, identidade visual e produto
  evoluírem no mesmo ciclo, dificultando revisão independente e reutilização.
- fronteira que justifica um repositório separado: A fronteira principal é a
  curadoria documental de diretrizes, fontes e kits auxiliares, com governança
  própria antes de qualquer interface ou motor de regras.

## 3. O que este projeto compartilha com o ecossistema?

- configuração: `config/doctor.json` para doctor e variáveis opcionais
  `OLLAMA_URL`, `OLLAMA_MODEL`, `APP_HOST` e `APP_PORT` para o app local.
- logging: O app não persiste logs; validações imprimem diagnóstico no terminal
  e o servidor local registra apenas requisições no stderr.
- runtime: Python padrão para scripts de governança e `app/server.py`, com
  Ollama opcional para módulo de Perguntas e Respostas restrito ao corpus local.
- contratos: Contratos documentais sobre corpus Markdown, kits cromáticos,
  regras determinísticas, limites clínicos e Perguntas e Respostas.
- autenticação ou transporte: O app v1 não implementa autenticação; roda local
  via HTTP em `127.0.0.1` por padrão.

## 4. O que este projeto NÃO pode carregar?

- responsabilidades fora de escopo: Prescrição clínica, protocolo final sem aprovação, produção assistencial e armazenamento de dados de pacientes.
- integrações que pertencem a outro sistema: Prontuário, PACS, RIS, deploy web,
  autenticação corporativa, auditoria clínica formal e consumo de dados reais
  pertencem a projetos consumidores com validação própria.
- dados que não devem morar aqui: PHI, PII, credenciais, logs clínicos, sessões
  de usuário, exports temporários e dados operacionais sensíveis.

## 5. Qual é o custo de manutenção esperado?

- host ou ambiente principal: Worktree local versionado em Git, com app local em
  Python e revisão por diff.
- dependência externa mais frágil: A publicação fonte, diretrizes oficiais que
  podem mudar, modelo Ollama local para Perguntas e Respostas e revisão clínica
  especializada.
- necessidade de restart: Mudanças em `app/server.py`, `app/data/` ou
  `app/static/` exigem reiniciar o servidor local.
- necessidade de backup: Git deve preservar histórico; capítulos Markdown,
  regras estruturadas e kits cromáticos devem permanecer versionados para
  rastreabilidade.
- risco operacional: O maior risco é interpretar as saídas da v1 ou material
  convertido como protocolo clínico pronto sem validação institucional.

## 6. Condição de saída

Este repositório só deveria existir se:

- houver fronteira de escopo defensável
- houver contrato de entrada e saída identificável
- houver operação própria ou ciclo de evolução independente
- o custo de mais um repo for menor que o custo de acoplamento
