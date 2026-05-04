# Changelog

Todas as mudancas relevantes deste repositorio devem ser registradas aqui.

## Unreleased

- Adiciona bootstrap estrutural Skidbladnir para governanca documental.
- Registra fronteira, contratos, operacao e decisoes do acervo.
- Adiciona scripts locais de gate e project doctor.
- Adiciona `app/` whitelabel com backend local, regras deterministicas,
  calculadoras, Q&A restrita ao corpus local via Ollama e gerador de rascunhos
  de guidelines.
- Corrige fluxo renal do app para calcular TFGe/clearance a partir de
  creatinina, idade, sexo e peso, em vez de pedir TFGe como entrada principal.
- Destaca a TFGe calculada na UI de decisao e calculadoras, substituindo JSON
  bruto por cards clinicos.
- Renomeia campos de gadolinio na UI para explicar Grupo I/II como risco de
  FSN.
- Ajusta mensagem de bloqueio para MCBG Grupo I em pacientes de risco para FSN.
- Reorganiza o formulario de decisao e adiciona campo TFGe calculado em tempo
  de preenchimento.
- Reduz destaque visual da funcao renal calculada e formata decimais com
  virgula na UI.
- Migra o projeto para `PossoContrastar`, remove PDF versionado, anonimiza kits
  cromaticos e adiciona cache em memoria para chunks de RAG.
- Estrutura metadados da obra-fonte e exibe a referencia bibliografica no app.
