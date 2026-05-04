# Posso Contrastar? App

Aplicação local whitelabel para apresentação dinâmica das diretrizes de meios de
contraste.

## Estado

- `v1`: apoio à decisão, não protocolo institucional aprovado.
- Backend: Python com biblioteca padrão.
- Frontend: HTML/CSS/JS sem build step.
- LLM: endpoint RAG restrito ao corpus local, usando Ollama quando disponível.
- Persistência: nenhuma. A aplicação não grava perguntas, respostas ou dados.

## Como rodar

```bash
python3 app/server.py
```

Abrir:

```text
http://127.0.0.1:8765
```

Configuração opcional do servidor e do Ollama:

```bash
APP_HOST=127.0.0.1 APP_PORT=8765 OLLAMA_MODEL=gemma4:e4b python3 app/server.py
```

O modelo padrão da v1 é `gemma4:e4b`. Use `OLLAMA_MODEL=<modelo>` para trocar.
`OLLAMA_KEEP_ALIVE` e `OLLAMA_NUM_PREDICT` controlam aquecimento e tamanho das
respostas do Q&A local.

## Estrutura

```text
app/
├── README.md
├── server.py
├── data/
│   ├── guideline_templates.json
│   └── rules.json
└── static/
    ├── app.js
    ├── index.html
    └── styles.css
```

## Contratos de segurança

- Regras críticas são determinísticas e ficam em `app/data/rules.json`.
- O Q&A recupera trechos apenas de `docs/meios_de_contraste`.
- Capítulos e chunks de RAG ficam em cache de memória até reiniciar o servidor.
- A referência bibliográfica da obra-fonte vem de
  `docs/meios_de_contraste/source.json`.
- Se o Ollama estiver indisponível, o Q&A retorna trechos recuperados sem
  inventar resposta.
- Não inserir dados reais de pacientes em ambiente não governado.
- Toda saída mantém fonte local quando possível.

## Função renal

O app não pede mais TFGe como entrada primária. Em `Posso contrastar?`,
`Renal / hidratação` e `Intervalômetro`, a função renal é calculada no backend a
partir de creatinina sérica, idade, sexo e peso:

- `CKD-EPI 2021 creatinina`: usado como TFGe de referência para limiares em
  adultos.
- `Cockcroft-Gault`: exibido como clearance de creatinina secundário, porque
  usa peso, mas não é TFGe indexada.
- `Bedside Schwartz`: disponível para pediatria quando idade, creatinina e
  altura são informadas.

O peso continua sendo usado diretamente para hidratação e doses ponderais.

## Referências de desenho

A v1 foi desenhada como apoio à decisão explicável: mostra entradas, recomendações
e fonte local, em vez de emitir ordem automática. Esse desenho segue a lógica de
manuais estruturados por cenário, como ACR e ESUR, e os princípios gerais de CDS
explicável descritos por FDA/AHRQ. Essas referências orientam a experiência, mas
as respostas do RAG continuam restritas ao corpus local.

- ACR Manual on Contrast Media: <https://www.acr.org/clinical-resources/clinical-tools-and-reference/contrast-manual>
- ESUR Guidelines 2025: <https://www.esur.org/esur-guidelines-2025/>
- FDA Clinical Decision Support Software FAQ: <https://www.fda.gov/medical-devices/software-medical-device-samd/clinical-decision-support-software-frequently-asked-questions-faqs>
- AHRQ Clinical Decision Support: <https://www.ahrq.gov/cpi/about/otherwebsites/clinical-decision-support/index.html>
- NIDDK CKD-EPI 2021: <https://www.niddk.nih.gov/research-funding/research-programs/kidney-clinical-research-epidemiology/laboratory/glomerular-filtration-rate-equations/adults>
- NKF Cockcroft-Gault: <https://www.kidney.org/professionals/gfr_calculatorCoc>
- NIDDK Bedside Schwartz: <https://www.niddk.nih.gov/health-information/professionals/clinical-tools-patient-management/kidney-disease/identify-manage-patients/evaluate-ckd/considerations-pediatric>

## Adaptação visual

A v1 é whitelabel. O frontend usa variáveis CSS e `html[data-theme]` para
adaptadores:

- `whitelabel`
- `noturno`
- `botanico`
- `lilas`

Os kits completos vivem em `docs/identidade_visual/<slug>/` e podem ser
conectados depois por build/theme loader sem mexer no motor de regras.
