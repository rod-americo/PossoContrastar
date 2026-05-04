# DECISIONS

## 1. Bootstrap estrutural como acervo documental

- contexto: O repositório de origem continha capítulos Markdown convertidos,
  kits visuais e histórico de governança, mas o novo repositório precisava de
  baseline própria.
- decisão: Aplicar Skidbladnir como recuperação estrutural de repositório
  existente, sem criar runtime de aplicação.
- impacto: O repo passa a ter gate, doctor, contratos, operação e guardrails
  para evolução documental.
- tradeoff: A validação automática cobre coerência estrutural, mas não valida
  equivalência clínica entre publicação externa e Markdown.
- alternativas rejeitadas: Gerar projeto greenfield, criar app de consulta
  nesta rodada ou mover todo conteúdo para um módulo de outro sistema.

## 2. Não versionar PDF no novo repositório

- contexto: O material Markdown depende de uma publicação local identificável.
- decisão: Manter apenas o corpus Markdown no repositório `PossoContrastar`; a
  publicação original deve ser consultada fora do Git quando necessária.
- impacto: O repositório fica leve e textual, sem binário grande ou arquivo de
  distribuição externa.
- tradeoff: Revisões de equivalência clínica precisam ter acesso separado à
  publicação original.

## 3. Não declarar produto assistencial

- contexto: Existe uma proposta de apresentação dinâmica com ideias de motor de
  regras, RAG, cards e calculadoras.
- decisão: Tratar a proposta como planejamento, não como arquitetura
  implementada ou promessa operacional.
- impacto: Evita misturar acervo documental com decisão clínica automatizada.
- tradeoff: Um produto futuro precisará de decisão, contrato e validação
  próprios antes de ser implementado.

## 4. Implementar app local whitelabel de apoio à decisão

- contexto: O usuário explicitou que a primeira versão deve nascer em `app/`,
  com backend, escopo completo, LLM restrita à documentação local via Ollama,
  whitelabel com adaptadores e trilha para protocolo aprovado.
- decisão: Criar app local em Python sem dependências externas obrigatórias,
  frontend estático, regras determinísticas em JSON, Perguntas e Respostas com
  RAG restrita ao corpus local, biblioteca, busca e calculadoras.
- impacto: O repositório deixa de ser apenas acervo documental e passa a ter
  runtime local de apoio à decisão.
- tradeoff: A v1 evita banco, autenticação e deploy para manter refatoração
  posterior simples, mas ainda não cobre auditoria clínica formal.
- alternativas rejeitadas: App puramente estático sem backend, LLM livre sem
  corpus local, acoplamento direto aos kits visuais e persistência de dados.

## 5. Retirar construtor de guidelines da v1

- contexto: O construtor de guidelines ficava próximo demais de geração de
  protocolo institucional, enquanto a v1 deve ser ferramenta de apoio à decisão
  e consulta explicável.
- decisão: Remover a seção Guidelines, seus templates e endpoints do app local.
- impacto: A interface fica mais enxuta e reduz o risco de interpretar a v1
  como geradora de protocolo aprovado.
- tradeoff: Rascunhos institucionais ficam fora do runtime; quando necessários,
  devem nascer em fluxo próprio de governança e aprovação.
