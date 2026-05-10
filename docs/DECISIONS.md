# DECISIONS

## 1. Bootstrap estrutural como acervo documental

- contexto: O repositório de origem continha capítulos Markdown convertidos,
  kits visuais, histórico de governança e depois incorporou um app local de
  apoio à decisão, mas precisava de baseline própria e coerente com a realidade
  atual.
- decisão: Aplicar Skidbladnir como recuperação estrutural de repositório
  existente, preservando o corpus em `docs/` e o runtime real em `app/`.
- impacto: O repo passa a ter gate, doctor, contratos, operação e guardrails
  para evolução documental e do app local.
- tradeoff: A validação automática cobre coerência estrutural, mas não valida
  equivalência clínica entre publicação externa e Markdown.
- alternativas rejeitadas: Gerar projeto greenfield, mover o app para `src/`,
  criar camadas artificiais ou deslocar todo conteúdo para um módulo de outro
  sistema.

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

## 6. Persistir perguntas do Q&A para melhoria do RAG

- contexto: Perguntas reais revelaram falhas de recuperação e linguagem natural
  no módulo de Perguntas e Respostas.
- decisão: Gravar cada pergunta em `app/data/qa_questions.jsonl`, arquivo local
  ignorado pelo Git, sem persistir respostas, payloads completos, headers, IP ou
  identificadores do usuário.
- impacto: O projeto passa a ter massa local de perguntas para análise,
  avaliação sintética e melhoria de aliases/recuperação.
- tradeoff: Perguntas podem conter dados sensíveis digitados pelo usuário; o log
  deve permanecer local e passar por revisão antes de compartilhamento.

## 7. Manter `app/` como módulo principal em vez de reorganizar para `src/`

- contexto: A aplicação real é pequena, local, sem packaging Python e com
  composition root claro em `app/server.py`.
- decisão: Preservar `app/` como runtime principal, com backend, contratos JSON
  e frontend estático no mesmo módulo, sem refatoração massiva de diretórios.
- impacto: A raiz continua enxuta, a operação documentada segue verdadeira e a
  recuperação estrutural não cria maturidade aparente que o código ainda não
  sustenta.
- tradeoff: `app/server.py` concentra responsabilidades e deve ganhar testes
  antes de ser separado; a separação futura precisa ser motivada por casos de
  uso reais.
- alternativas rejeitadas: Migrar para `src/`, criar pacotes
  `domain/application/infrastructure/interfaces` sem necessidade atual ou
  introduzir framework web apenas por padrão arquitetural.

## 8. Checklist de continuidade para repositório existente

- contexto: O template Skidbladnir traz checklist de projeto novo, mas este
  repositório já tem código, corpus, runtime e histórico.
- decisão: Adaptar `START_CHECKLIST.md` para continuidade, registrando itens
  concluídos, parciais, ausentes e proibidos na próxima rodada.
- impacto: A próxima manutenção consegue distinguir baseline pronta de lacunas
  reais, como falta de testes automatizados e validação clínica formal.
- tradeoff: O checklist fica menos genérico que o starter e mais preso à
  realidade deste repositório.
- alternativas rejeitadas: Copiar o checklist greenfield sem adaptação ou
  declarar como concluídos itens ainda não implementados, como CI e testes.

## 9. Regressão técnica com biblioteca padrão

- contexto: O app local ainda não tinha suíte versionada nem CI, mas o backend
  usa biblioteca padrão e expõe funções puras testáveis.
- decisão: Criar testes `unittest`, smoke HTTP automatizado e workflow de CI sem
  dependências externas obrigatórias.
- impacto: Cálculo renal, regras determinísticas, recuperação local e contratos
  HTTP básicos passam a ter proteção técnica local e remota.
- tradeoff: A suíte evita regressões de comportamento implementado, mas não
  valida verdade clínica, equivalência com a publicação original ou prontidão
  assistencial.
- alternativas rejeitadas: Introduzir pytest ou framework web só para testes,
  deixar smoke manual como único controle ou declarar revisão clínica sem fonte
  especializada.
