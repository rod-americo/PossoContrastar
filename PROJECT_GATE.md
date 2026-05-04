# PROJECT GATE

Este gate documenta por que o repositorio existe como acervo proprio e quais
fronteiras impedem crescimento indefinido.

## 1. Por que este projeto existe?

- problema real: Centralizar diretrizes sobre meios de contraste em Markdown
  revisavel, reduzindo dependencia de material fechado para leitura, busca,
  citacao e evolucao documental.
- usuario ou operador alvo: Radiologistas, liderancas assistenciais,
  enfermagem, tecnicos de imagem e autores que mantem materiais clinicos e
  operacionais derivados.
- resultado esperado: Um acervo governado e uma aplicacao local de apoio à
  decisão, capazes de apoiar consulta, treinamento e prototipagem sem confundir
  a v1 com protocolo institucional aprovado.

## 2. Por que isto NAO deveria ser um modulo?

- repositorio candidato que poderia absorver isso: Repositorios de dashboards,
  coordenacao radiologica ou automacoes clinicas poderiam consumir este acervo.
- por que esse acoplamento seria inadequado: Acoplar as diretrizes a uma
  aplicacao especifica faria conteudo clinico, identidade visual e produto
  evoluirem no mesmo ciclo, dificultando revisao independente e reutilizacao.
- fronteira que justifica um repositório separado: A fronteira principal e a
  curadoria documental de diretrizes, fontes e kits auxiliares, com governanca
  propria antes de qualquer interface ou motor de regras.

## 3. O que este projeto compartilha com o ecossistema?

- configuracao: `config/doctor.json` para doctor e variaveis opcionais
  `OLLAMA_URL`, `OLLAMA_MODEL`, `APP_HOST` e `APP_PORT` para o app local.
- logging: O app nao persiste logs; validacoes imprimem diagnostico no terminal
  e o servidor local registra apenas requisicoes no stderr.
- runtime: Python padrao para scripts de governanca e `app/server.py`, com
  Ollama opcional para Q&A restrita ao corpus local.
- contratos: Contratos documentais sobre corpus Markdown, kits cromaticos,
  regras deterministicas, limites clinicos e Q&A local.
- autenticacao ou transporte: O app v1 nao implementa autenticacao; roda local
  via HTTP em `127.0.0.1` por padrao.

## 4. O que este projeto NAO pode carregar?

- responsabilidades fora de escopo: Prescricao clinica, protocolo final sem aprovacao, producao assistencial e armazenamento de dados de pacientes.
- integrações que pertencem a outro sistema: Prontuario, PACS, RIS, deploy web,
  autenticacao corporativa, auditoria clinica formal e consumo de dados reais
  pertencem a projetos consumidores com validacao propria.
- dados que nao devem morar aqui: PHI, PII, credenciais, logs clinicos, sessoes
  de usuario, exports temporarios e dados operacionais sensiveis.

## 5. Qual E O Custo De Manutencao Esperado?

- host ou ambiente principal: Worktree local versionado em Git, com app local em
  Python e revisao por diff.
- dependencia externa mais fragil: A publicacao fonte, diretrizes oficiais que
  podem mudar, modelo Ollama local para Q&A e revisao clinica especializada.
- necessidade de restart: Mudancas em `app/server.py`, `app/data/` ou
  `app/static/` exigem reiniciar o servidor local.
- necessidade de backup: Git deve preservar historico; capitulos Markdown,
  regras estruturadas e kits cromaticos devem permanecer versionados para
  rastreabilidade.
- risco operacional: O maior risco e interpretar as saidas da v1 ou material
  convertido como protocolo clinico pronto sem validacao institucional.

## 6. Condicao de saida

Este repositorio so deveria existir se:

- houver fronteira de escopo defensavel
- houver contrato de entrada e saida identificavel
- houver operacao propria ou ciclo de evolucao independente
- o custo de mais um repo for menor que o custo de acoplamento
