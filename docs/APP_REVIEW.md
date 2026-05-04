# Avaliação do app e próximas rodadas

## Veredito

O app está adequado para publicação como **MVP interno de apoio à decisão e
coleta de opinião**, desde que a comunicação deixe claro que não é protocolo
institucional aprovado, prescrição médica, dispositivo médico ou substituto de
validação clínica.

Como protótipo operacional, a v1 está forte: organiza o corpus, calcula função
renal, oferece regras determinísticas, renderiza a biblioteca, permite busca e
restringe Perguntas e Respostas ao texto local. Como ferramenta institucional
pronta, ainda depende de validação clínica formal, matriz de equivalência com a
obra-fonte e testes por cenários.

## Publicação agora

Pode publicar para um grupo pequeno e identificado de usuários, com objetivo de
colher feedback sobre clareza, utilidade, lacunas e fluxo de trabalho.

Condições recomendadas para essa publicação:

- Usar linguagem de **apoio à decisão** em todas as comunicações.
- Informar que as saídas devem ser conferidas contra protocolos locais, bulas e
  julgamento clínico.
- Não coletar dados reais de pacientes.
- Pedir que os usuários informem perfil profissional, cenário testado, dúvida,
  resultado esperado e resultado observado.
- Separar feedback de usabilidade de feedback clínico.
- Não incorporar sugestões clínicas diretamente sem revisão por radiologista
  responsável e registro da fonte.

## Principais forças

- Fluxo “Posso Contrastar?” cobre os eixos operacionais certos: classe, via,
  contexto, função renal, metformina, diálise, gestação, lactação e reação
  prévia.
- Cálculo renal está mais correto para a v1: TFGe é estimada por CKD-EPI 2021 e
  Cockcroft-Gault aparece separado como clearance.
- Biblioteca e busca tornam o corpus navegável sem depender do PDF original.
- Perguntas e Respostas está restrita ao corpus local e pode ser desligada por
  configuração.
- Whitelabel, branding, tema e kits visuais estão desacoplados das regras
  clínicas.
- O app não persiste perguntas, respostas ou payloads.

## Fragilidades atuais

- O motor de regras ainda cobre uma fração do corpus; não deve ser interpretado
  como completude clínica.
- Falta suíte automatizada de cenários clínicos esperados.
- Falta matriz “regra estruturada -> trecho fonte -> revisão clínica”.
- Busca/RAG ainda é lexical e pode trazer trechos longos ou ruído.
- Modo emergência ainda parece lista de condutas; precisa virar fluxo de ação
  com hierarquia, dose, passo atual e reavaliação.
- A UI ainda é única para todos os perfis; deve evoluir para modos de uso.
- `app/server.py` concentra configuração, RAG, regras, calculadoras e HTTP; a
  próxima fase deve modularizar.

## Backlog para rodadas de codificação

### 1. Validação clínica por cenários

Criar `app/data/scenarios.json` ou estrutura equivalente com casos esperados:

- iodado IV eletivo com TFGe normal, moderada e < 30
- iodado IA primeira passagem com TFGe < 45
- IRA conhecida ou suspeita
- diálise anúrica e diálise com diurese residual
- metformina com e sem risco renal
- gestante com iodado e com MCBG
- lactante com iodado e com MCBG
- MCBG Grupo I em paciente de risco
- reação prévia leve, moderada e grave
- asma instável e betabloqueador
- pediatria com peso, idade, creatinina e altura

Resultado esperado: testes automatizados contra `/api/decision`,
`/api/renal-function` e calculadoras.

### 2. Matriz de rastreabilidade

Criar uma tabela versionada para cada regra:

- id da regra
- condição de entrada
- saída esperada
- arquivo fonte
- trecho ou seção fonte
- status de revisão
- responsável pela revisão
- data da revisão

Resultado esperado: nenhuma regra crítica sem fonte e status.

### 3. Modo emergência

Transformar a tela em fluxo de ação:

- cartões grandes por síndrome
- passo atual destacado
- dose adulta e pediátrica separadas
- timer de reavaliação
- botão para copiar resumo do evento
- supressão de conteúdo não urgente quando houver anafilaxia

Resultado esperado: menos texto corrido e mais ação segura em crise.

### 4. Perfis de uso

Criar modos de navegação por tarefa:

- equipe de sala: triagem, checklist, preparo, extravasamento e emergência
- residentes de radiologia: consulta orientada e documentação
- radiologistas: risco-benefício, exceções, MCBG, gestação, renal
- biblioteca: leitura, busca, fonte e capítulos

Resultado esperado: reduzir carga cognitiva sem mudar o motor de regras.

### 5. RAG e busca

Melhorar recuperação local:

- chunking com títulos hierárquicos mais estáveis
- score por seção e não apenas token lexical
- resposta com citações mais compactas
- aviso explícito quando a pergunta pedir algo fora do corpus
- teste de perguntas frequentes contra trechos esperados

Resultado esperado: respostas mais curtas, citadas e com menos ruído.

### 6. Modularização técnica

Separar `app/server.py` em módulos:

- configuração
- funções renais
- regras de decisão
- calculadoras
- RAG/Perguntas e Respostas
- HTTP

Resultado esperado: manutenção mais segura antes de ampliar regras.

## Perguntas para feedback dos usuários

1. Qual é seu perfil profissional?
2. Em que situação você usaria esta ferramenta?
3. A saída foi clara o suficiente para apoiar sua próxima ação?
4. Alguma recomendação pareceu excessiva, fraca ou ambígua?
5. Faltou algum campo de entrada?
6. Faltou alguma fonte, explicação ou citação?
7. O que você esperava encontrar e não encontrou?
8. Você confiaria neste fluxo apenas como apoio, sabendo que ainda exige
   validação institucional?

## Critério para sair de MVP opinativo

O app só deve avançar para piloto institucional quando houver:

- cenários clínicos automatizados passando
- revisão especializada das regras críticas
- matriz de rastreabilidade completa
- processo de aprovação local definido
- texto de limitação e responsabilidade aprovado
- decisão explícita sobre logs, auditoria e dados de pacientes
