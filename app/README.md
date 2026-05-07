# Posso Contrastar? App

Aplicação local whitelabel para apresentação dinâmica das diretrizes de meios de
contraste.

## Estado

- `v1`: apoio à decisão, não protocolo institucional aprovado.
- Backend: Python com biblioteca padrão.
- Frontend: HTML/CSS/JS sem build step.
- LLM: endpoint RAG restrito ao corpus local, usando Ollama quando disponível.
- Persistência: perguntas do módulo Perguntas e Respostas são gravadas em
  JSONL local para análise posterior. Respostas e payloads completos não são
  persistidos.

## Como rodar

```bash
python3 app/server.py
```

Abrir:

```text
http://127.0.0.1:8765
```

Configuração opcional do servidor e do conector de Perguntas e Respostas:

```bash
APP_HOST=127.0.0.1 APP_PORT=8765 APP_QA_MODEL=gemma4:e4b python3 app/server.py
```

O modelo padrão da v1 é `gemma4:e4b`, definido em
`app/data/app_config.example.json`. Para ajustes locais, copie esse arquivo para
`app/data/app_config.json`; o arquivo local é ignorado pelo Git. Use
`APP_QA_MODEL=<modelo>` para trocar em runtime. `OLLAMA_MODEL` continua aceito
por compatibilidade. `APP_QA_KEEP_ALIVE` e `APP_QA_NUM_PREDICT` controlam
aquecimento e tamanho das respostas de Perguntas e Respostas.

Para usar Ollama em outra máquina, aponte o app para a URL base desse servidor:

```bash
APP_QA_OLLAMA_URL=http://192.168.1.50:11434 python3 app/server.py
```

Também é aceito informar apenas `192.168.1.50:11434`; o app assume `http://`.
Na máquina que hospeda o Ollama, o serviço precisa escutar fora do loopback, por
exemplo com `OLLAMA_HOST=0.0.0.0:11434 ollama serve`, e a rede/firewall deve
permitir acesso à porta `11434`.

## Estrutura

```text
app/
├── README.md
├── server.py
├── data/
│   ├── app_config.example.json
│   └── rules.json
└── static/
    ├── app.js
    ├── index.html
    └── styles.css
```

## Contratos de segurança

- Regras críticas são determinísticas e ficam em `app/data/rules.json`.
- Perguntas e Respostas só aparece e responde quando `qa.enabled` está ativo na
  configuração carregada pelo app.
- Perguntas e Respostas recupera trechos apenas de `docs/meios_de_contraste`.
- Perguntas feitas ao módulo são registradas em `app/data/qa_questions.jsonl`
  quando `qa.log_questions` está ativo. Esse arquivo é local, ignorado pelo Git
  e pode conter dados sensíveis digitados pelo usuário.
- A Biblioteca renderiza Markdown local em HTML legível, incluindo tabelas com
  rolagem horizontal dentro do painel.
- Capítulos e chunks de RAG ficam em cache de memória até reiniciar o servidor.
- A referência bibliográfica da obra-fonte vem de
  `docs/meios_de_contraste/source.json`.
- Se o Ollama estiver indisponível, Perguntas e Respostas retorna trechos recuperados sem
  inventar resposta.
- Não inserir dados reais de pacientes em ambiente não governado.
- Toda saída mantém fonte local quando possível.

## Público operacional

A interface deve ser legível para técnicos de radiologia, técnicos de
enfermagem, tecnólogos, enfermeiros, biomédicos, residentes de radiologia e
radiologistas. Quando o texto usar “equipe de sala”, o termo cobre técnicos de
radiologia, técnicos de enfermagem, tecnólogos, enfermeiros e biomédicos;
decisões fora do fluxo devem apontar para o radiologista responsável.

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
- `cobalto`
- `lilas`

Os kits completos vivem em `docs/identidade_visual/<slug>/` e podem ser
conectados depois por build/theme loader sem mexer no motor de regras.

O adaptador padrão e a visibilidade do seletor no canto superior direito são
definidos na configuração do app, junto com o módulo de Perguntas e Respostas.
O template versionado é `app/data/app_config.example.json`; quando existir,
`app/data/app_config.json` sobrescreve localmente esse template e não entra no
Git:

```json
{
  "branding": {
    "title": "Posso Contrastar?",
    "subtitle": "Apoio à decisão baseado em documentação local",
    "show_mark": false,
    "mark_text": "",
    "logo_src": ""
  },
  "theme": {
    "default_theme": "whitelabel",
    "show_theme_picker": true
  },
  "qa": {
    "enabled": false,
    "connector": "ollama",
    "model": "gemma4:e4b",
    "ollama_url": "http://localhost:11434",
    "log_questions": true
  }
}
```

O bloco à esquerda do título é o lugar de logomarca institucional, tratado como
slot retangular horizontal. Por padrão, `show_mark` fica `false` para não exibir
placeholder. Use `logo_src` para uma imagem servida pelo app ou URL permitida,
ou `mark_text` para uma sigla temporária centralizada. Em runtime,
`APP_BRAND_TITLE`, `APP_BRAND_SUBTITLE`, `APP_BRAND_SHOW_MARK`,
`APP_BRAND_MARK_TEXT` e `APP_BRAND_LOGO_SRC` podem sobrescrever esses valores.

Use `show_theme_picker: false` no arquivo local para ocultar o seletor na interface e
`default_theme` para fixar manualmente `whitelabel`, `noturno`, `botanico`,
`cobalto` ou `lilas`. Em execução local, `APP_THEME` e `APP_SHOW_THEME_PICKER` podem
sobrescrever esses valores sem editar o template versionado.

Use `qa.enabled: false` para remover Perguntas e Respostas da navegação e
bloquear `/api/qa`. Use `qa.connector` para escolher o conector; a v1 suporta
`ollama`. Use `qa.model` para fixar o modelo e `qa.ollama_url` para apontar
para Ollama local ou remoto. Em runtime, `APP_QA_ENABLED`, `APP_QA_CONNECTOR`,
`APP_QA_MODEL`, `APP_QA_OLLAMA_URL`,
`APP_QA_KEEP_ALIVE`, `APP_QA_NUM_PREDICT` e `APP_QA_LOG_QUESTIONS` podem
sobrescrever a config.
