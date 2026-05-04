# Proposta de apresentação dinâmica: Meios de contraste

## Objetivo

Transformar o guia em Markdown em uma experiência clínica operacional: rápida para a equipe de sala, confiável para residentes de radiologia e radiologistas na decisão, clara para treinamento e auditável para governança institucional.

O material local é especialmente adequado para isso porque contém:

- Catálogo de meios de contraste e propriedades físico-químicas.
- Regras de risco renal, TFGe, diálise, metformina e hidratação.
- Algoritmos de reação adversa, incluindo doses e condutas.
- Regras pediátricas por idade, peso e calibre de acesso.
- Intervalos entre contrastes e coleta laboratorial.
- Condições especiais: gestação, amamentação, tireoide, mieloma, anemia falciforme, miastenia e medicamentos.
- Fluxo de extravasamento e documentação.

## Premissa de segurança

Separar o sistema em duas camadas:

1. **Motor determinístico de regras** para tudo que envolve limiares, doses, contraindicações, urgência e condutas.
2. **LLM restrita ao texto** apenas para explicar, resumir e responder perguntas diretas com citação do trecho usado.

Essa separação é importante: a literatura recente de suporte à decisão em contraste descreve bons resultados ao converter ACR/ESUR em regras auditáveis com cartões de ação, sem depender de dados de pacientes e com rastreabilidade por fonte. Estudos de RAG em diretrizes clínicas também mostram que a qualidade melhora muito quando tabelas/fluxos são convertidos para texto estruturado e quando a resposta é ancorada em corpus local.

## Arquitetura de informação

### Primeira tela

Quatro entradas, sem hero institucional:

- **Decidir conduta**: fluxo guiado para caso real.
- **Emergência**: tratamento de reação aguda, sempre visível.
- **Calculadoras**: TFGe, hidratação, dose pediátrica, intervalo, medicações.
- **Biblioteca**: capítulos, tabelas, cards e busca citada.

### Perfis de uso

- **Equipe de sala:** técnicos de radiologia, técnicos de enfermagem, tecnólogos, enfermeiros e biomédicos na triagem pré-exame, acesso, jejum, extravasamento e reação aguda.
- **Residentes de radiologia:** R1, R2, R3 e R4 em consulta orientada, documentação, preparo de discussão e aplicação supervisionada dos fluxos.
- **Radiologistas:** decisão de risco-benefício, contraste alternativo, risco renal, MCBG, gestação e exceções fora do fluxo.
- **Coordenação:** protocolos institucionais, checklists, indicadores, auditoria.
- **Paciente/atendimento:** explicações simples sobre jejum, amamentação e preparo, sem decisões complexas.

## Módulos propostos

### 1. Seletor “Posso contrastar?”

Fluxo de 6 perguntas:

- Classe pretendida: iodado, MCBG, bário, microbolhas, Lipiodol.
- Via: IV, IA primeira passagem, IA segunda passagem, oral, retal, intrauterina, intralinfática.
- Contexto: eletivo, urgência, emergência/risco de vida.
- Perfil: adulto, pediátrico, gestante, lactante, dialítico.
- Função renal/risco: TFGe, IRA conhecida/suspeita, DRC, diálise, função residual.
- Histórico: reação prévia à mesma classe, severidade, asma instável, betabloqueador, metformina.

Saída:

- Semáforo: `prosseguir`, `prosseguir com precauções`, `radiologista deve avaliar`, `evitar/contraindicação relativa`.
- Cards de ação: “fazer agora”, “documentar”, “orientar paciente”, “considerar alternativa”.
- Citações por capítulo e linha/fonte.

### 2. Catálogo de meios de contraste

Converter o capítulo 1 em uma tabela filtrável e cards comparativos.

Filtros:

- Classe.
- Fabricante.
- Nome comercial/genérico.
- Osmolalidade.
- Ionicidade.
- Estrutura: monômero/dímero, linear/macrocíclico.
- Classificação ACR para MCBG.
- Via aprovada.
- Excreção renal/hepatobiliar.

Interações úteis:

- “Comparar 2 produtos”.
- “Mostrar apenas MCBG Grupo II”.
- “Mostrar alternativas de outra classe”.
- “Mostrar viscosidade a 37 °C” para orientar aquecimento/fluxo.

### 3. Risco renal, TFGe e metformina

Um wizard dedicado, porque capítulos 3, 4 e 6 se cruzam.

Entradas:

- Idade, sexo, creatinina, altura se pediátrico.
- Adulto: CKD-EPI; criança: Bedside Schwartz.
- TFGe conhecida ou calculada.
- IRA suspeita/conhecida.
- DRC, diálise, diurese residual > 100 mL/dia.
- Via de administração e exposição renal de primeira/segunda passagem.
- Uso de metformina.

Saídas:

- Necessidade de creatinina/TFGe antes do exame.
- Risco de IRA-AC.
- Recomendação de hidratação profilática com volume por peso: `1-3 mL/kg/h`, início e pós-exame.
- Conduta de metformina: manter ou suspender, com retorno em até 48h se função renal normal quando aplicável.
- Aviso de não usar hemodiálise/hemofiltração como profilaxia.

### 4. MCBG, FSN e retenção de gadolínio

Seletor específico para RM com contraste.

Entradas:

- MCBG pretendido.
- Grupo ACR.
- TFGe/IRA/diálise.
- Pediatria, gestação, lactação.
- Histórico de múltiplas injeções.

Saídas:

- Preferir Grupo II quando houver risco.
- Contraindicar Grupo I em pacientes de risco.
- Recomendação de menor dose diagnóstica.
- Explicação separada para FSN versus retenção tecidual.
- Card de consentimento/informação quando aplicável.

### 5. Reações adversas: triagem pré-exame

Um módulo de anamnese estruturada.

Entradas:

- Reação prévia: mesma classe ou outra classe.
- Tipo: quimiotóxica/fisiológica, hipersensibilidade, desconhecida.
- Severidade: leve, moderada, grave.
- Tempo: aguda, tardia, muito tardia.
- Asma instável, betabloqueador, miastenia, interleucina-2.
- Urgência do exame.

Saídas:

- Contraste alternativo e/ou troca de classe.
- Necessidade de alergologista, com flag mandatória em reação grave.
- Pré-medicação somente como segurança adicional, não rotina.
- Regime eletivo/urgência quando indicado.
- Observação mínima pós-contraste.

### 6. Modo emergência: reação aguda

Deve ser um botão fixo, não enterrado no menu.

Design:

- Tela escura ou vermelha de alto contraste.
- Pergunta inicial: “qual quadro predominante?”.
- Cards grandes: náuseas/vômitos, urticária, broncoespasmo, edema laríngeo, hipotensão/bradicardia, hipotensão/taquicardia, anafilaxia, edema pulmonar, convulsão, hipoglicemia, ansiedade.
- Fluxo passo a passo com checklist e timer.
- Doses adultas por padrão e botão explícito para pediatria.
- Reavaliação a cada 5-15 min quando adrenalina for usada.
- Log automático do evento: horário, contraste, dose, sinais, medicações, acionamento de emergência.

Regra de segurança:

- Se houver critério de anafilaxia, o sistema suprime recomendações não urgentes e exibe apenas ABC, oxigênio, acesso, volume, adrenalina e acionamento de suporte.

### 7. Calculadora pediátrica

Entradas:

- Peso.
- Idade.
- Tipo de contraste.
- Região/exame.
- Calibre do acesso.
- Situação: rotina ou reação aguda.

Saídas:

- Iodado: faixa `1,0-2,0 mL/kg`.
- MCBG: dose em mmol/kg e volume estimado se concentração conhecida.
- Taxa máxima de injeção por calibre: 24G, 22G, 20G, 16-18G.
- Doses de emergência: adrenalina IM, SF, atropina, salbutamol, respeitando máximos.
- Avisos de aprovação pediátrica por produto.
- Monitorização tireoidiana pós-iodado para crianças < 3 anos com fatores de risco, com indicação de individualização.

### 8. Intervalômetro

Calculadora dos capítulos 8 e 4.

Entradas:

- Contraste anterior: iodado ou MCBG.
- Próximo contraste: iodado ou MCBG.
- TFGe: > 60, 30-60, < 30.
- Diálise sem função residual.
- Coleta pretendida: sangue ou urina.
- Emergência/risco de vida.

Saídas:

- Intervalo mínimo.
- Intervalo ótimo.
- Nota: RM antes da TC, exceto TC de vias urinárias.
- Para diálise sem função residual: considerar pelo menos 3 sessões entre administrações sucessivas.
- Para laboratório: intervalo por tipo de amostra.

### 9. Jejum inteligente

Interface curta para equipe de agendamento.

Entradas:

- Exame abdominal ou não abdominal.
- Envolve alças, vesícula ou vias biliares.
- Sólidos/líquidos e protocolo local.

Saídas:

- “Sem jejum necessário” para não abdominais.
- “Jejum conforme protocolo institucional; usualmente 4h” para abdominais.
- Explicação do racional: reduzir jejum desnecessário, desconforto, hipoglicemia e desidratação.

### 10. Condições especiais em cards

Cards filtráveis:

- Amamentação.
- Gestação.
- Disfunção tireoidiana.
- Tumores produtores de catecolaminas.
- Anemia falciforme.
- Mieloma múltiplo.
- Miastenia gravis.
- Medicamentos.

Cada card deve ter:

- “Pode usar?”
- “Qual classe?”
- “Precaução principal”
- “Quando chamar radiologista?”
- “Texto de orientação ao paciente/equipe”

### 11. Extravasamento

Fluxo operacional com documentação.

Entradas:

- Volume estimado.
- Local.
- Sintomas neurovasculares/motores.
- Tipo de contraste.
- Injeção manual/automática.
- Taxa/pressão.

Saídas:

- Interromper injeção, retirar acesso, elevar membro, compressa fria.
- Avaliação cirúrgica se grave ou volume > 150 mL.
- Follow-up em 24h e 48h.
- Documento estruturado do evento.
- Farmacovigilância: fabricante e/ou ANVISA.

### 12. Perguntas e Respostas com LLM restrita ao texto

Função: responder perguntas diretas sem substituir os módulos determinísticos.

Exemplos:

- “Preciso suspender metformina?”
- “Paciente lactante pode fazer RM com gadolínio?”
- “Qual intervalo entre dois contrastes com TFGe 45?”
- “Quais MCBG são Grupo II?”
- “O que fazer no extravasamento de 180 mL?”

Regras de implementação:

- Corpus único: arquivos em `docs/meios_de_contraste`.
- Responder somente com trechos recuperados do corpus.
- Citar capítulo/arquivo e trecho.
- Se a pergunta pedir conduta que dependa de dados ausentes, pedir os campos faltantes.
- Se houver risco imediato, redirecionar ao Modo Emergência.
- Se houver conflito entre texto local e fonte externa, declarar conflito e priorizar protocolo institucional vigente.
- Temperatura baixa, saída curta, sem “criatividade”.
- Logar pergunta, chunks recuperados, resposta e versão do corpus.

### 13. Protocolização institucional futura

Esta frente deve ficar fora da v1 do app. Transformar o guia em política local
versionada exige governança própria, responsáveis técnicos e aprovação formal.

Saídas possíveis:

- **Protocolo de triagem renal pré-contraste**: quem precisa creatinina, validade do exame, TFGe, grupos de risco.
- **Protocolo de contraste iodado em risco renal**: contraindicação relativa, hidratação, dose mínima, via IA/IV, metformina.
- **Protocolo de MCBG/FSN**: formulary por Grupo I/II, restrições, diálise, gestação, pediatria.
- **Protocolo de reações adversas**: anamnese, alto risco, troca de contraste, pré-medicação, observação e documentação.
- **Protocolo de reação aguda na sala**: kit de emergência, treinamento, doses adultas/pediátricas, acionamentos.
- **Protocolo de extravasamento**: prevenção, manejo, documentação, follow-up e farmacovigilância.
- **Protocolo de jejum**: reduzir jejum desnecessário e padronizar exceções abdominais.
- **Protocolo de condições especiais**: gestação, lactação, tireoide, mieloma, miastenia, anemia falciforme, medicamentos.
- **Política de IA/RAG para diretrizes**: escopo, limites, revisão humana, versionamento, auditoria e atualização.

Um fluxo futuro, separado do runtime de apoio à decisão, poderia permitir:

- Escolher postura institucional: conservadora, balanceada ou permissiva dentro do texto.
- Definir responsáveis: radiologia, enfermagem, qualidade, farmácia, alergologia, nefrologia.
- Gerar checklist por setor.
- Exportar Markdown, PDF e versão “cartão de bolso”.
- Registrar versão, data, aprovador e fonte.

## Modelo de dados recomendado

Converter Markdown para objetos:

```json
{
  "id": "renal.metformin.iodado.akiorgfrlt30",
  "chapter": "03_injuria_renal_aguda_associada_ao_contraste.md",
  "domain": "renal",
  "inputs": ["contrast_class", "route", "egfr", "aki", "metformin"],
  "condition": "contrast_class == 'iodado' && (aki || egfr < 30 || route == 'ia_primeira_passagem') && metformin",
  "recommendation": "Suspender metformina a partir da injeção e retornar em até 48h pós-exame se função renal normal.",
  "severity": "precaution",
  "source_text": "Nesses casos, suspender a metformina...",
  "version": "2026-05-04"
}
```

Princípios:

- Tabelas grandes viram JSON/CSV.
- Cada recomendação tem `id`, `fonte`, `condição`, `saída`, `exceções`.
- Limiares ficam explícitos e testáveis.
- Toda regra tem teste de fronteira: TFGe 29/30, 44/45, 59/60; peso pediátrico; volume 150 mL; intervalo 24h.

## Design de interface

Três temas úteis:

- **noturno** para operação clínica: dark mode, alta densidade, emergência e auditoria.
- **botanico** para dashboards institucionais: verde operacional, KPIs e painéis.
- **lilas** para material público/educacional: linguagem clara, cards e perguntas para paciente.

Recomendação: construir a ferramenta profissional em `noturno` e gerar páginas públicas/educacionais em `lilas`.

## MVP sugerido

### Fase 1: Base navegável

- Biblioteca com capítulos.
- Busca textual.
- Cards por domínio.
- Catálogo filtrável de contrastes.

### Fase 2: Regras determinísticas

- Risco renal/metformina.
- Reações prévias.
- Intervalos.
- Extravasamento.
- Pediatria básica.

### Fase 3: Emergência

- Modo reação aguda.
- Timers.
- Doses adultas/pediátricas.
- Log estruturado.

### Fase 4: LLM restrita ao texto

- RAG sobre Markdown estruturado.
- Respostas citadas.
- Abstenção quando faltar dado.
- Avaliação com perguntas sintéticas.

### Fase 5: Protocolização institucional futura

- Fluxo separado para protocolos.
- Aprovação/versionamento.
- Exportação para PDF/cartão.
- Indicadores de uso, divergência e atualização.

## Métricas de qualidade

- Tempo para achar uma conduta.
- Percentual de respostas com citação válida.
- Percentual de perguntas em que o sistema abstém corretamente por dado ausente.
- Concordância com gabarito de cenários sintéticos.
- Uso do modo emergência em simulações.
- Aderência a documentação obrigatória.
- Número de exceções institucionais registradas.

## Referências externas usadas para calibrar a proposta

- ACR Manual on Contrast Media: lista capítulos atualizados e tabelas de reações, tratamento, especificações, CA-AKI, pediatria, gestação, lactação, metformina, extravasamento e gadolínio.  
  https://www.acr.org/clinical-resources/clinical-tools-and-reference/contrast-manual
- ESUR Guidelines 2025: organiza módulos de hipersensibilidade, CA-AKI, gadolínio, diálise, extravasamento, intervalos, interferência laboratorial, gestação/lactação, pediatria e doenças sistêmicas.  
  https://www.esur.org/esur-guidelines-2025/
- FDA, iodinated contrast and thyroid monitoring in children: recomenda individualizar monitorização tireoidiana em crianças de até 3 anos conforme fatores de risco.  
  https://www.fda.gov/drugs/drug-safety-and-availability/fda-recommends-thyroid-monitoring-babies-and-young-children-who-receive-injections-iodine-containing
- ACR statement on thyroid monitoring: discute a recomendação da FDA e limitações da evidência.  
  https://www.acr.org/Advocacy/Position-Statements/Use-of-Iodinated-Contrast-Material-for-Medical-Imaging-in-Young-Children
- Contrast Media Decision Support Simulator: descreve conversão de ACR/ESUR em regras auditáveis, triagem por semáforo, cards de ação, caminho de emergência e testes sintéticos.  
  https://acamedicine.org/article/contrast-media-decision-support-simulator-cmds-in-radiology-practice/
- RAG em diretrizes clínicas: estudo em diretrizes de hepatologia mostrando ganho de acurácia com corpus estruturado, conversão de tabelas/figuras para texto e prompt engineering.  
  https://www.nature.com/articles/s41746-024-01091-y
