# Changelog

Todas as mudanças relevantes deste repositório devem ser registradas aqui.

## Unreleased

- Normaliza acentuação, cedilha e nomenclatura operacional para técnicos de
  radiologia, técnicos de enfermagem, tecnólogos, enfermeiros, biomédicos,
  residentes de radiologia e radiologistas.
- Adiciona bootstrap estrutural Skidbladnir para governança documental.
- Registra fronteira, contratos, operação e decisões do acervo.
- Adiciona scripts locais de gate e project doctor.
- Adiciona `app/` whitelabel com backend local, regras determinísticas,
  calculadoras, módulo de Perguntas e Respostas restrito ao corpus local via
  Ollama, biblioteca e busca.
- Corrige fluxo renal do app para calcular TFGe/clearance a partir de
  creatinina, idade, sexo e peso, em vez de pedir TFGe como entrada principal.
- Destaca a TFGe calculada na UI de decisão e calculadoras, substituindo JSON
  bruto por cards clínicos.
- Renomeia campos de gadolínio na UI para explicar Grupo I/II como risco de
  FSN.
- Ajusta mensagem de bloqueio para MCBG Grupo I em pacientes de risco para FSN.
- Reorganiza o formulário de decisão e adiciona campo TFGe calculado em tempo
  de preenchimento.
- Reduz destaque visual da função renal calculada e formata decimais com
  vírgula na UI.
- Migra o projeto para `PossoContrastar`, remove PDF versionado, anonimiza kits
  cromáticos e adiciona cache em memória para chunks de RAG.
- Estrutura metadados da obra-fonte para app e API local.
- Remove painéis laterais de status, guardrail e corpus para reduzir ruído na
  tela principal.
- Padroniza os adaptadores visuais como Noturno, Botânico e Lilás.
- Atualiza o nome visível do produto para `Posso Contrastar?`.
- Explicita no README que o trabalho é baseado no livro-fonte, com ISBN e DOI.
- Remove a seção Guidelines da UI e do backend para manter a v1 focada em apoio
  à decisão.
- Renomeia o módulo local de perguntas para Perguntas e Respostas.
- Renderiza Markdown na Biblioteca, nos resultados de busca e nas fontes de
  Perguntas e Respostas.
- Exclui o README do corpus da lista de capítulos e da recuperação clínica.
- Remove o botão de preenchimento de exemplo do fluxo de decisão.
- Adiciona configuração versionada para tema padrão e exibição do seletor de
  adaptador visual.
- Move Perguntas e Respostas para configuração versionada, com liga/desliga,
  conector e modelo.
- Trata a área à esquerda do título como slot retangular de branding
  institucional configurável, sem placeholder por padrão.
- Adiciona kit visual Cobalto e expõe o adaptador correspondente na v1.
- Documenta avaliação do app, critérios de publicação opinativa e backlog de
  rodadas de codificação.
