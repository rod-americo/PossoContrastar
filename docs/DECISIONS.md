# DECISIONS

## 1. Bootstrap estrutural como acervo documental

- contexto: O repositorio de origem continha capitulos Markdown convertidos,
  kits visuais e historico de governanca, mas o novo repositorio precisava de
  baseline propria.
- decisao: Aplicar Skidbladnir como recuperacao estrutural de repositorio
  existente, sem criar runtime de aplicacao.
- impacto: O repo passa a ter gate, doctor, contratos, operacao e guardrails
  para evolucao documental.
- tradeoff: A validacao automatica cobre coerencia estrutural, mas nao valida
  equivalencia clinica entre publicacao externa e Markdown.
- alternativas rejeitadas: Gerar projeto greenfield, criar app de consulta
  nesta rodada ou mover todo conteudo para um modulo de outro sistema.

## 2. Nao versionar PDF no novo repositorio

- contexto: O material Markdown depende de uma publicacao local identificavel.
- decisao: Manter apenas o corpus Markdown no repositorio `PossoContrastar`; a
  publicacao original deve ser consultada fora do Git quando necessaria.
- impacto: O repositorio fica leve e textual, sem binario grande ou arquivo de
  distribuicao externa.
- tradeoff: Revisoes de equivalencia clinica precisam ter acesso separado à
  publicacao original.

## 3. Nao declarar produto assistencial

- contexto: Existe uma proposta de apresentacao dinamica com ideias de motor de
  regras, RAG, cards e calculadoras.
- decisao: Tratar a proposta como planejamento, nao como arquitetura
  implementada ou promessa operacional.
- impacto: Evita misturar acervo documental com decisao clinica automatizada.
- tradeoff: Um produto futuro precisara de decisao, contrato e validacao
  proprios antes de ser implementado.

## 4. Implementar app local whitelabel de apoio à decisão

- contexto: O usuario explicitou que a primeira versao deve nascer em `app/`,
  com backend, escopo completo, LLM restrita à documentacao local via Ollama,
  whitelabel com adaptadores e trilha para protocolo aprovado.
- decisao: Criar app local em Python sem dependencias externas obrigatorias,
  frontend estatico, regras deterministicas em JSON, Perguntas e Respostas com
  RAG restrita ao corpus local, biblioteca, busca e calculadoras.
- impacto: O repositorio deixa de ser apenas acervo documental e passa a ter
  runtime local de apoio à decisão.
- tradeoff: A v1 evita banco, autenticacao e deploy para manter refatoracao
  posterior simples, mas ainda nao cobre auditoria clinica formal.
- alternativas rejeitadas: App puramente estatico sem backend, LLM livre sem
  corpus local, acoplamento direto aos kits visuais e persistencia de dados.

## 5. Retirar construtor de guidelines da v1

- contexto: O construtor de guidelines ficava proximo demais de geracao de
  protocolo institucional, enquanto a v1 deve ser ferramenta de apoio à decisao
  e consulta explicavel.
- decisao: Remover a secao Guidelines, seus templates e endpoints do app local.
- impacto: A interface fica mais enxuta e reduz o risco de interpretar a v1
  como geradora de protocolo aprovado.
- tradeoff: Rascunhos institucionais ficam fora do runtime; quando necessarios,
  devem nascer em fluxo proprio de governanca e aprovacao.
