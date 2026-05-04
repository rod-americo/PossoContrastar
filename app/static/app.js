const state = {
  rules: null,
  templates: [],
  chapters: [],
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function formPayload(form) {
  const data = new FormData(form);
  const payload = {};
  for (const [key, value] of data.entries()) payload[key] = value;
  for (const input of form.querySelectorAll('input[type="checkbox"]')) {
    payload[input.name] = input.checked;
  }
  return payload;
}

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: {"Content-Type": "application/json"},
    ...options,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

function card(item) {
  return `
    <article class="result-card ${item.level || "ok"}">
      <h3>${escapeHtml(item.title || item.file || "Resultado")}</h3>
      <p>${escapeHtml(item.message || item.snippet || "")}</p>
      ${item.source ? `<span class="source">${escapeHtml(item.source)}</span>` : ""}
    </article>
  `;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function pretty(value) {
  return JSON.stringify(value, null, 2)
    .replace(/[{}"]/g, "")
    .replace(/,\n/g, "\n");
}

function formatDecimal(value, digits = 1) {
  if (value === null || value === undefined || value === "") return "--";
  const number = Number(value);
  if (Number.isNaN(number)) return String(value);
  return number.toLocaleString("pt-BR", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

function bucketLabel(bucket) {
  return {
    normal: "TFGe > 60",
    moderate: "TFGe 30-60",
    severe: "TFGe < 30",
    unknown: "faixa não calculada",
  }[bucket] || bucket || "faixa não calculada";
}

function renalCard(renal) {
  if (!renal) return "";
  const value = renal.egfr_ckd_epi_2021 ?? renal.egfr_bedside_schwartz ?? renal.egfr_for_thresholds;
  const method = renal.egfr_method || "não calculada";
  const level = renal.egfr_bucket === "severe" ? "caution" : "ok";
  const displayValue = formatDecimal(value);
  const unit = value !== null && value !== undefined ? "mL/min/1,73 m²" : "";
  const crcl = renal.crcl_cockcroft_gault_ml_min !== null
    ? `<span>ClCr Cockcroft-Gault: <strong>${escapeHtml(formatDecimal(renal.crcl_cockcroft_gault_ml_min))} mL/min</strong></span>`
    : "";
  const notes = renal.notes?.length ? `<p>${escapeHtml(renal.notes.join(" "))}</p>` : "";
  return `
    <article class="result-card ${level}">
      <h3>Função renal calculada</h3>
      <div class="renal-metric">
        <span>TFGe</span>
        <strong>${escapeHtml(displayValue)}</strong>
        <em>${escapeHtml(unit)}</em>
      </div>
      <div class="renal-details">
        <span>Método: <strong>${escapeHtml(method)}</strong></span>
        <span>Faixa: <strong>${escapeHtml(bucketLabel(renal.egfr_bucket))}</strong></span>
        ${crcl}
      </div>
      ${notes}
      <span class="source">NIDDK/NKF + corpus local</span>
    </article>
  `;
}

function hydrationCard(hydration) {
  if (!hydration) return "";
  return card({
    level: "attention",
    title: "Hidratação",
    message: `${hydration.fluid}: ${hydration.rate_min_ml_h}-${hydration.rate_max_ml_h} mL/h; iniciar ${hydration.start_before_h}h antes e manter ${hydration.continue_after_h}h após. ${hydration.note}`,
  });
}

function intervalCards(result) {
  return [
    renalCard(result.renal_function),
    card({
      level: result.egfr_bucket === "severe" ? "caution" : "ok",
      title: "Intervalo entre injeções",
      message: `Mínimo: ${result.between_injections.minimum}. Ótimo: ${result.between_injections.optimal || result.between_injections.minimum}.`,
      source: result.source,
    }),
    card({
      level: "attention",
      title: "Coleta laboratorial",
      message: `Mínimo: ${result.lab_collection.minimum}. ${result.lab_collection.optimal ? `Ótimo: ${result.lab_collection.optimal}. ` : ""}${result.note}`,
      source: result.source,
    }),
  ].join("");
}

function setDecisionEgfr(renal) {
  const field = $("#decision-egfr");
  if (!field) return;
  const value = renal?.egfr_ckd_epi_2021 ?? renal?.egfr_bedside_schwartz ?? renal?.egfr_for_thresholds;
  field.value = value !== null && value !== undefined ? `${formatDecimal(value)} mL/min/1,73 m²` : "";
}

function canEstimateRenal(form) {
  return Boolean(form.creatinine_mg_dl.value && form.age_years.value && form.sex.value);
}

function bindDecisionEgfrPreview(form) {
  let timer = null;
  const refresh = () => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      if (!canEstimateRenal(form)) {
        setDecisionEgfr(null);
        return;
      }
      const data = await api("/api/renal-function", {method: "POST", body: JSON.stringify(formPayload(form))});
      setDecisionEgfr(data.renal_function);
    }, 180);
  };
  ["creatinine_mg_dl", "age_years", "sex", "weight_kg"].forEach((name) => {
    form.elements[name].addEventListener("input", refresh);
    form.elements[name].addEventListener("change", refresh);
  });
  form.addEventListener("reset", () => setTimeout(() => setDecisionEgfr(null), 0));
  return refresh;
}

function setView(viewId) {
  $$(".nav-tab").forEach((button) => button.classList.toggle("active", button.dataset.view === viewId));
  $$(".view").forEach((view) => view.classList.toggle("active", view.id === viewId));
}

async function init() {
  $$(".nav-tab").forEach((button) => button.addEventListener("click", () => setView(button.dataset.view)));
  $("#theme-select").addEventListener("change", (event) => {
    document.documentElement.dataset.theme = event.target.value;
  });

  const health = await api("/api/health");
  $("#health").textContent = `OK · Ollama: ${health.ollama_model}`;
  state.rules = await api("/api/rules");
  state.templates = (await api("/api/guideline-templates")).templates;
  state.chapters = (await api("/api/chapters")).chapters;

  bindDecision();
  bindEmergency();
  bindCalculators();
  bindLibrary();
  bindQa();
  bindGuidelines();
}

function bindDecision() {
  const form = $("#decision-form");
  const refreshEgfr = bindDecisionEgfrPreview(form);
  $("#sample-decision").addEventListener("click", () => {
    form.contrast_class.value = "iodinated";
    form.route.value = "iv";
    form.setting.value = "elective";
    form.creatinine_mg_dl.value = "2.4";
    form.age_years.value = "76";
    form.sex.value = "male";
    form.weight_kg.value = "70";
    form.metformin.checked = true;
    refreshEgfr();
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const result = await api("/api/decision", {method: "POST", body: JSON.stringify(formPayload(form))});
    setDecisionEgfr(result.renal_function);
    $("#decision-result").innerHTML = `
      <article class="result-card ${result.level}">
        <h3>Nível: ${escapeHtml(result.level)}</h3>
        <p>${escapeHtml(result.summary)}</p>
      </article>
      ${renalCard(result.renal_function)}
      ${result.cards.map(card).join("")}
    `;
  });
}

function bindEmergency() {
  const render = () => {
    const kind = $("#emergency-kind").value;
    const actions = state.rules.adverse_reactions.adult_emergency[kind] || [];
    $("#emergency-actions").innerHTML = actions
      .map((action, index) => `
        <article class="result-card high">
          <h3>Passo ${index + 1}</h3>
          <p>${escapeHtml(action)}</p>
          <span class="source">${escapeHtml(state.rules.adverse_reactions.source)}</span>
        </article>
      `)
      .join("");
  };
  $("#emergency-kind").addEventListener("change", render);
  render();
}

function bindCalculators() {
  $("#renal-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const result = await api("/api/calculators/renal", {method: "POST", body: JSON.stringify(formPayload(form))});
    form.querySelector("output").innerHTML = `
      ${renalCard(result.renal_function)}
      ${hydrationCard(result.hydration)}
      ${result.metformin.map(card).join("")}
    `;
  });
  $("#interval-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const result = await api("/api/calculators/interval", {method: "POST", body: JSON.stringify(formPayload(form))});
    form.querySelector("output").innerHTML = intervalCards(result);
  });
  $("#pediatric-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const result = await api("/api/calculators/pediatric", {method: "POST", body: JSON.stringify(formPayload(form))});
    form.querySelector("output").innerHTML = `
      ${renalCard(result.renal_function)}
      ${card({title: "Dose iodado", message: `${result.iodinated_volume_ml.min}-${result.iodinated_volume_ml.max} mL`})}
      ${card({title: "Dose gadolínio (MCBG)", message: `${result.gbca_dose_mmol} mmol`})}
      ${card({title: "Taxa máxima", message: result.max_injection_rate, source: result.source})}
    `;
  });
  $("#extravasation-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const result = await api("/api/extravasation", {method: "POST", body: JSON.stringify(formPayload(form))});
    form.querySelector("output").textContent = pretty(result);
  });
}

function bindLibrary() {
  $("#chapter-list").innerHTML = state.chapters.map((chapter) => `
    <article class="chapter-card">
      <h3>${escapeHtml(chapter.title)}</h3>
      <ul>
        ${chapter.sections.slice(0, 6).map((section) => `<li>${escapeHtml(section.title)}</li>`).join("")}
      </ul>
    </article>
  `).join("");

  $("#search-button").addEventListener("click", search);
  $("#search-input").addEventListener("keydown", (event) => {
    if (event.key === "Enter") search();
  });
}

async function search() {
  const query = encodeURIComponent($("#search-input").value);
  const data = await api(`/api/search?q=${query}`);
  $("#search-results").innerHTML = data.results.map(card).join("") || "<p>Nenhum resultado.</p>";
}

function bindQa() {
  $("#qa-button").addEventListener("click", async () => {
    const question = $("#qa-question").value.trim();
    if (!question) return;
    $("#qa-result").innerHTML = '<article class="result-card"><h3>Consultando...</h3><p>Recuperando trechos locais e chamando Ollama se disponível.</p></article>';
    const data = await api("/api/qa", {method: "POST", body: JSON.stringify({question})});
    $("#qa-result").innerHTML = `
      <article class="result-card ${data.available ? "ok" : "attention"}">
        <h3>Resposta ${data.available ? `(${escapeHtml(data.model)})` : "(fallback local)"}</h3>
        <p>${escapeHtml(data.answer)}</p>
      </article>
      ${data.citations.map((item, index) => card({title: `Fonte [${index + 1}] · ${item.title}`, message: item.snippet, source: item.file})).join("")}
    `;
  });
}

function bindGuidelines() {
  $("#guideline-options").innerHTML = state.templates.map((template) => `
    <label class="check">
      <input name="template_ids" type="checkbox" value="${escapeHtml(template.id)}" checked>
      ${escapeHtml(template.title)}
    </label>
  `).join("");

  $("#guidelines-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = formPayload(event.currentTarget);
    payload.template_ids = [...event.currentTarget.querySelectorAll('input[name="template_ids"]:checked')].map((input) => input.value);
    const result = await api("/api/guidelines/generate", {method: "POST", body: JSON.stringify(payload)});
    $("#guideline-output").value = result.markdown;
  });

  $("#copy-guideline").addEventListener("click", async () => {
    await navigator.clipboard.writeText($("#guideline-output").value);
  });
}

init().catch((error) => {
  $("#health").textContent = `Erro: ${error.message}`;
  console.error(error);
});
