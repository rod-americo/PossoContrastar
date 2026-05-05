#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
STATIC_DIR = APP_DIR / "static"
DATA_DIR = APP_DIR / "data"
DOCS_DIR = ROOT / "docs" / "meios_de_contraste"
RULES_PATH = DATA_DIR / "rules.json"
APP_CONFIG_PATH = DATA_DIR / "app_config.json"
APP_CONFIG_EXAMPLE_PATH = DATA_DIR / "app_config.example.json"
SOURCE_PATH = DOCS_DIR / "source.json"
CHAPTERS_CACHE: list[dict[str, Any]] | None = None
CHUNKS_CACHE: list[dict[str, Any]] | None = None
SUPPORTED_THEMES = {"whitelabel", "noturno", "botanico", "cobalto", "lilas"}
SUPPORTED_QA_CONNECTORS = {"ollama"}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool_env(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "sim", "on"}:
        return True
    if normalized in {"0", "false", "no", "nao", "não", "off"}:
        return False
    return None


def parse_int(value: Any, default: int) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


def normalize_base_url(value: str, default: str) -> str:
    raw = (value or default).strip()
    if "://" not in raw:
        raw = f"http://{raw}"
    parsed = urllib.parse.urlparse(raw)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"URL do Ollama inválida: {value}")
    return raw.rstrip("/")


def app_config() -> dict[str, Any]:
    config_path = APP_CONFIG_PATH if APP_CONFIG_PATH.exists() else APP_CONFIG_EXAMPLE_PATH
    config = read_json(config_path)
    branding = dict(config.get("branding") or {})
    theme = dict(config.get("theme") or {})
    qa = dict(config.get("qa") or {})

    brand_show_mark = parse_bool_env(os.environ.get("APP_BRAND_SHOW_MARK"))
    if brand_show_mark is None:
        configured_brand_show_mark = branding.get("show_mark", False)
        if isinstance(configured_brand_show_mark, bool):
            brand_show_mark = configured_brand_show_mark
        else:
            brand_show_mark = parse_bool_env(str(configured_brand_show_mark))
        if brand_show_mark is None:
            brand_show_mark = False
    brand_title = str(os.environ.get("APP_BRAND_TITLE") or branding.get("title") or "Posso Contrastar?").strip()
    brand_subtitle = str(
        os.environ.get("APP_BRAND_SUBTITLE")
        or branding.get("subtitle")
        or "Apoio à decisão baseado em documentação local"
    ).strip()
    brand_mark_text = str(os.environ.get("APP_BRAND_MARK_TEXT") or branding.get("mark_text") or "").strip()
    brand_logo_src = str(os.environ.get("APP_BRAND_LOGO_SRC") or branding.get("logo_src") or "").strip()

    default_theme = str(os.environ.get("APP_THEME") or theme.get("default_theme") or "whitelabel")
    if default_theme not in SUPPORTED_THEMES:
        default_theme = "whitelabel"
    show_picker = parse_bool_env(os.environ.get("APP_SHOW_THEME_PICKER"))
    if show_picker is None:
        configured_picker = theme.get("show_theme_picker", True)
        if isinstance(configured_picker, bool):
            show_picker = configured_picker
        else:
            show_picker = parse_bool_env(str(configured_picker))
        if show_picker is None:
            show_picker = True
    available = [
        str(item)
        for item in theme.get("available_themes", sorted(SUPPORTED_THEMES))
        if str(item) in SUPPORTED_THEMES
    ]
    if default_theme not in available:
        available.insert(0, default_theme)

    qa_enabled = parse_bool_env(os.environ.get("APP_QA_ENABLED"))
    if qa_enabled is None:
        configured_qa_enabled = qa.get("enabled", True)
        if isinstance(configured_qa_enabled, bool):
            qa_enabled = configured_qa_enabled
        else:
            qa_enabled = parse_bool_env(str(configured_qa_enabled))
        if qa_enabled is None:
            qa_enabled = True
    qa_connector = str(os.environ.get("APP_QA_CONNECTOR") or qa.get("connector") or "ollama").strip().lower()
    if qa_connector not in SUPPORTED_QA_CONNECTORS:
        qa_connector = "ollama"
    qa_model = str(
        os.environ.get("APP_QA_MODEL")
        or os.environ.get("OLLAMA_MODEL")
        or qa.get("model")
        or "gemma4:e4b"
    ).strip()
    ollama_url = normalize_base_url(
        str(
            os.environ.get("APP_QA_OLLAMA_URL")
            or os.environ.get("OLLAMA_URL")
            or qa.get("ollama_url")
            or "http://localhost:11434"
        ),
        "http://localhost:11434",
    )
    keep_alive = str(
        os.environ.get("APP_QA_KEEP_ALIVE")
        or os.environ.get("OLLAMA_KEEP_ALIVE")
        or qa.get("keep_alive")
        or "10m"
    ).strip()
    num_predict = parse_int(
        os.environ.get("APP_QA_NUM_PREDICT")
        or os.environ.get("OLLAMA_NUM_PREDICT")
        or qa.get("num_predict"),
        384,
    )

    return {
        "branding": {
            "title": brand_title,
            "subtitle": brand_subtitle,
            "show_mark": brand_show_mark,
            "mark_text": brand_mark_text,
            "logo_src": brand_logo_src,
        },
        "theme": {
            "default_theme": default_theme,
            "show_theme_picker": show_picker,
            "available_themes": available,
        },
        "qa": {
            "enabled": qa_enabled,
            "connector": qa_connector,
            "model": qa_model,
            "ollama_url": ollama_url,
            "keep_alive": keep_alive,
            "num_predict": num_predict,
        },
    }


def source_metadata() -> dict[str, Any]:
    return read_json(SOURCE_PATH)


def markdown_files() -> list[Path]:
    excluded = {"README.md", "proposta_apresentacao_dinamica.md"}
    return sorted(path for path in DOCS_DIR.glob("*.md") if path.name not in excluded)


def chapter_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def load_chapters() -> list[dict[str, Any]]:
    global CHAPTERS_CACHE
    if CHAPTERS_CACHE is not None:
        return CHAPTERS_CACHE

    chapters: list[dict[str, Any]] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        sections = [
            {"level": len(match.group(1)), "title": match.group(2).strip()}
            for match in re.finditer(r"^(#{2,4})\s+(.+)$", text, flags=re.M)
        ]
        chapters.append(
            {
                "file": path.name,
                "title": chapter_title(text, path.stem),
                "sections": sections,
                "content": text,
            }
        )
    CHAPTERS_CACHE = chapters
    return chapters


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.strip().lower())
    ascii_text = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", ascii_text)


TOKEN_ALIASES = {
    "amamentacao": {"amamentacao", "amamentando", "amamentar", "aleitamento", "lactacao", "lactante", "lactantes", "lactente", "lactentes"},
    "gestacao": {"gestacao", "gestante", "gravidez", "gravida", "pregnancy"},
    "gadolínio": {"gadolínio", "gadolinio", "gbca", "mcbg"},
    "iodado": {"iodado", "iodados", "iodinated"},
    "rim": {"rim", "renal", "tfge", "creatinina", "ckd", "drc"},
    "metformina": {"metformina", "metformin"},
    "extravasamento": {"extravasamento", "extravasou", "extravasado", "extravasation"},
    "reacao": {"reacao", "reacoes", "alergia", "anafilaxia", "hipersensibilidade"},
}

TOKEN_TO_GROUP = {
    alias: {group, *aliases}
    for group, aliases in TOKEN_ALIASES.items()
    for alias in aliases
}


def tokens(value: str) -> set[str]:
    stop = {
        "para",
        "com",
        "sem",
        "uma",
        "que",
        "dos",
        "das",
        "por",
        "mais",
        "menos",
        "deve",
        "de",
        "da",
        "do",
        "em",
        "ao",
        "ou",
        "e",
        "a",
        "o",
    }
    found = set()
    for token in re.findall(r"[A-Za-z0-9_-]{3,}", normalize(value)):
        if token not in stop:
            found.add(token)
            found.update(TOKEN_TO_GROUP.get(token, set()))
    return found


def build_chunks() -> list[dict[str, Any]]:
    global CHUNKS_CACHE
    if CHUNKS_CACHE is not None:
        return CHUNKS_CACHE

    chunks: list[dict[str, Any]] = []
    for chapter in load_chapters():
        parts = re.split(r"\n(?=##+ )", chapter["content"])
        for index, part in enumerate(parts):
            clean = part.strip()
            if not clean:
                continue
            title = chapter["title"]
            first = clean.splitlines()[0].strip("# ").strip()
            if first and first != title:
                title = f"{title} > {first}"
            chunks.append(
                {
                    "id": f"{chapter['file']}#{index}",
                    "file": chapter["file"],
                    "title": title,
                    "text": clean[:3500],
                    "tokens": list(tokens(clean + " " + title)),
                    "title_tokens": list(tokens(title)),
                }
            )
    CHUNKS_CACHE = chunks
    return chunks


def retrieve(query: str, limit: int = 6) -> list[dict[str, Any]]:
    query_tokens = tokens(query)
    if not query_tokens:
        return []
    scored: list[tuple[int, dict[str, Any]]] = []
    for chunk in build_chunks():
        chunk_tokens = set(chunk["tokens"])
        title_tokens = set(chunk["title_tokens"])
        score = len(query_tokens & chunk_tokens)
        score += 3 * len(query_tokens & title_tokens)
        lower_text = normalize(chunk["text"])
        lower_query = normalize(query)
        if lower_query and lower_query in lower_text:
            score += 5
        if score:
            scored.append((score, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    results = []
    for score, chunk in scored[:limit]:
        text = re.sub(r"\s+", " ", chunk["text"]).strip()
        results.append(
            {
                "id": chunk["id"],
                "file": chunk["file"],
                "title": chunk["title"],
                "score": score,
                "snippet": text[:650] + ("..." if len(text) > 650 else ""),
                "text": chunk["text"],
            }
        )
    return results


def focus_retrieved_chunks(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not chunks:
        return []
    top_score = chunks[0]["score"]
    if top_score >= 10:
        threshold = max(2, top_score * 0.5)
        focused = [chunk for chunk in chunks if chunk["score"] >= threshold]
        return focused[:4] or chunks[:1]
    return chunks


def parse_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def normalize_sex(value: Any) -> str:
    normalized = str(value or "").strip().lower()
    if normalized in {"female", "feminino", "f", "mulher"}:
        return "female"
    if normalized in {"male", "masculino", "m", "homem"}:
        return "male"
    return ""


def ckd_epi_2021_creatinine(creatinine: float, age: float, sex: str) -> float | None:
    if creatinine <= 0 or age <= 0 or sex not in {"female", "male"} or age < 18:
        return None
    kappa = 0.7 if sex == "female" else 0.9
    alpha = -0.241 if sex == "female" else -0.302
    sex_factor = 1.012 if sex == "female" else 1.0
    ratio = creatinine / kappa
    return 142 * (min(ratio, 1) ** alpha) * (max(ratio, 1) ** -1.2) * (0.9938**age) * sex_factor


def cockcroft_gault(creatinine: float, age: float, weight: float, sex: str) -> float | None:
    if creatinine <= 0 or age <= 0 or weight <= 0 or sex not in {"female", "male"}:
        return None
    sex_factor = 0.85 if sex == "female" else 1.0
    return ((140 - age) * weight * sex_factor) / (72 * creatinine)


def bedside_schwartz(creatinine: float, height_cm: float) -> float | None:
    if creatinine <= 0 or height_cm <= 0:
        return None
    return (0.41 * height_cm) / creatinine


def renal_function(payload: dict[str, Any]) -> dict[str, Any]:
    creatinine = parse_float(payload.get("creatinine_mg_dl") or payload.get("creatinine"))
    age = parse_float(payload.get("age_years") or payload.get("age"))
    weight = parse_float(payload.get("weight_kg"))
    height = parse_float(payload.get("height_cm"))
    sex = normalize_sex(payload.get("sex"))
    manual_egfr = parse_float(payload.get("egfr"))

    ckd_epi = None
    crcl = None
    schwartz = None
    threshold_value = None
    threshold_method = None
    notes = []

    if creatinine and age and sex:
        ckd_epi = ckd_epi_2021_creatinine(creatinine, age, sex)
    if creatinine and age and weight and sex:
        crcl = cockcroft_gault(creatinine, age, weight, sex)
    if creatinine and height and age is not None and age < 18:
        schwartz = bedside_schwartz(creatinine, height)

    if ckd_epi is not None:
        threshold_value = ckd_epi
        threshold_method = "CKD-EPI 2021 creatinina"
    elif schwartz is not None:
        threshold_value = schwartz
        threshold_method = "Bedside Schwartz"
    elif manual_egfr is not None:
        threshold_value = manual_egfr
        threshold_method = "TFGe informada manualmente"

    if threshold_value is None:
        missing = []
        if creatinine is None:
            missing.append("creatinina")
        if age is None:
            missing.append("idade")
        if not sex:
            missing.append("sexo")
        notes.append("Função renal não calculada; informe " + ", ".join(missing) + ".")
    if crcl is not None:
        notes.append("Cockcroft-Gault é clearance de creatinina em mL/min, não TFGe indexada.")
    if age is not None and age < 18 and schwartz is None:
        notes.append("Para estimar TFGe pediátrica por Schwartz, informe altura em cm.")

    return {
        "creatinine_mg_dl": creatinine,
        "age_years": age,
        "sex": sex,
        "weight_kg": weight,
        "height_cm": height,
        "egfr_ckd_epi_2021": round(ckd_epi, 1) if ckd_epi is not None else None,
        "crcl_cockcroft_gault_ml_min": round(crcl, 1) if crcl is not None else None,
        "egfr_bedside_schwartz": round(schwartz, 1) if schwartz is not None else None,
        "manual_egfr": manual_egfr,
        "egfr_for_thresholds": round(threshold_value, 1) if threshold_value is not None else None,
        "egfr_method": threshold_method,
        "egfr_bucket": egfr_bucket(threshold_value),
        "notes": notes,
    }


def egfr_bucket(egfr: float | None) -> str:
    if egfr is None:
        return "unknown"
    if egfr > 60:
        return "normal"
    if egfr >= 30:
        return "moderate"
    return "severe"


def add_result(
    output: dict[str, Any],
    level: str,
    title: str,
    message: str,
    source: str,
) -> None:
    severity_order = {"ok": 0, "attention": 1, "caution": 2, "high": 3, "stop": 4}
    if severity_order[level] > severity_order[output["level"]]:
        output["level"] = level
    output["cards"].append({"level": level, "title": title, "message": message, "source": source})


def decision_support(payload: dict[str, Any]) -> dict[str, Any]:
    rules = read_json(RULES_PATH)
    contrast = str(payload.get("contrast_class", "")).lower()
    route = str(payload.get("route", "")).lower()
    setting = str(payload.get("setting", "")).lower()
    renal = renal_function(payload)
    egfr = renal["egfr_for_thresholds"]
    bucket = renal["egfr_bucket"]
    weight = renal["weight_kg"]
    output: dict[str, Any] = {
        "level": "ok",
        "summary": "Apoio à decisão baseado no corpus local. Não substitui validação clínica.",
        "cards": [],
        "inputs": payload,
        "renal_function": renal,
    }

    if setting in {"emergency", "risco_vida"}:
        add_result(
            output,
            "attention",
            "Emergência/risco de vida",
            "O texto local permite encurtar intervalos em emergências, sempre considerando segurança do paciente. Registre justificativa clínica.",
            rules["chapters"]["intervals"],
        )

    if payload.get("pregnant"):
        if contrast == "gbca":
            add_result(
                output,
                "high",
                "Gestação e MCBG",
                rules["special_conditions"]["pregnancy_gbca"],
                rules["chapters"]["special"],
            )
        elif contrast == "iodinated":
            add_result(
                output,
                "caution",
                "Gestação e iodado",
                rules["special_conditions"]["pregnancy_iodinated"],
                rules["chapters"]["special"],
            )

    if payload.get("lactating"):
        key = "lactation_gbca" if contrast == "gbca" else "lactation_iodinated"
        add_result(output, "ok", "Amamentação", rules["special_conditions"][key], rules["chapters"]["special"])

    dialysis = bool(payload.get("dialysis"))
    residual = bool(payload.get("residual_diuresis"))
    aki = bool(payload.get("aki"))

    if contrast == "iodinated":
        if egfr is None and route in {"iv", "ia_first_pass", "ia_second_pass"} and not dialysis and not aki:
            add_result(
                output,
                "attention",
                "Função renal não calculada",
                "Informe creatinina, idade, sexo e peso para estimar função renal e aplicar limiares com segurança.",
                rules["chapters"]["renal_screening"],
            )
        if dialysis and not residual:
            add_result(output, "attention", "Dialítico anúrico", rules["dialysis"]["iodinated_anuric"], rules["chapters"]["dialysis"])
        elif dialysis and residual:
            add_result(output, "high", "Diálise com função residual", rules["dialysis"]["iodinated_non_anuric"], rules["chapters"]["dialysis"])
        elif aki:
            add_result(output, "high", "IRA conhecida ou suspeita", "Injeção intravascular de iodado constitui contraindicação relativa e exige avaliação risco/benefício.", rules["chapters"]["renal"])
        elif egfr is not None and egfr < 30:
            add_result(output, "high", "TFGe < 30", "DRC grave sem diálise de manutenção é condição de alto risco para IRA-AC com iodado intravascular.", rules["chapters"]["renal"])
        elif egfr is not None and egfr < 45 and route == "ia_first_pass":
            add_result(output, "high", "IA primeira passagem e TFGe < 45", "DRC moderada é alto risco quando há exposição renal de primeira passagem.", rules["chapters"]["renal"])

        if payload.get("metformin"):
            if aki or (egfr is not None and egfr < 30) or route == "ia_first_pass":
                add_result(output, "caution", "Metformina", rules["renal"]["metformin"]["restart"], rules["chapters"]["renal"])
            elif egfr is None:
                add_result(output, "attention", "Metformina", "Função renal não calculada; informe creatinina, idade, sexo e peso antes de aplicar a regra.", rules["chapters"]["renal"])
            else:
                add_result(output, "ok", "Metformina", rules["renal"]["metformin"]["default"], rules["chapters"]["renal"])

    if contrast == "gbca":
        group = str(payload.get("gbca_group", "")).lower()
        if egfr is None and not dialysis and not aki:
            add_result(output, "attention", "Função renal não calculada", "Informe creatinina, idade e sexo para estimar TFGe antes de aplicar limiares de risco renal.", rules["chapters"]["renal_screening"])
        if group == "group_i" and (dialysis or aki or (egfr is not None and egfr < 30)):
            add_result(output, "stop", "MCBG Grupo I", rules["dialysis"]["gbca_group_i"], rules["chapters"]["dialysis"])
        elif aki or (egfr is not None and egfr < 30):
            add_result(output, "caution", "Risco de FSN", "Preferir MCBG Grupo II, na menor dose diagnóstica possível; Grupo I é contraindicado em pacientes de risco.", rules["chapters"]["gadolinium"])

    if payload.get("prior_reaction"):
        severity = str(payload.get("reaction_severity", "unknown")).lower()
        if severity == "severe":
            add_result(output, "high", "Reação prévia grave", "Usar contraste alternativo, realizar em ambiente hospitalar, recomendar alergologista e considerar pré-medicação como segurança adicional.", rules["chapters"]["reactions"])
        elif severity == "moderate":
            add_result(output, "caution", "Reação prévia moderada", "Usar contraste alternativo e considerar pré-medicação como medida de segurança adicional.", rules["chapters"]["reactions"])
        else:
            add_result(output, "attention", "Reação prévia leve/desconhecida", "Preferir contraste alternativo; reação quimiotóxica/fisiológica não prediz hipersensibilidade futura.", rules["chapters"]["reactions"])

    if payload.get("unstable_asthma"):
        add_result(output, "attention", "Asma instável", "Pode aumentar risco de reação adversa, principalmente broncoespasmo.", rules["chapters"]["reactions"])

    if payload.get("beta_blocker"):
        add_result(output, "attention", "Betabloqueador", "Pode dificultar resposta à adrenalina em eventual broncoespasmo/reação.", rules["chapters"]["reactions"])

    if weight and output["level"] in {"high", "caution"} and contrast == "iodinated" and not dialysis:
        h = rules["renal"]["hydration"]
        add_result(
            output,
            "attention",
            "Hidratação profilática",
            f"Se indicada e sem risco de sobrecarga: {h['fluid']} {h['rate_ml_kg_h_min'] * weight:.0f}-{h['rate_ml_kg_h_max'] * weight:.0f} mL/h, iniciar pelo menos {h['start_before_h']}h antes e manter por {h['continue_after_h']}h após.",
            rules["chapters"]["renal"],
        )

    if not output["cards"]:
        add_result(output, "ok", "Sem alerta pelos campos informados", "Nenhum bloqueio foi identificado pelas regras estruturadas da v1. Confirmar indicação, bula e protocolo local.", "docs/meios_de_contraste/README.md")

    output["egfr_bucket"] = bucket
    return output


def renal_calculator(payload: dict[str, Any]) -> dict[str, Any]:
    rules = read_json(RULES_PATH)
    renal = renal_function(payload)
    weight = renal["weight_kg"]
    bucket = renal["egfr_bucket"]
    h = rules["renal"]["hydration"]
    hydration = None
    if weight:
        hydration = {
            "fluid": h["fluid"],
            "rate_min_ml_h": round(weight * h["rate_ml_kg_h_min"]),
            "rate_max_ml_h": round(weight * h["rate_ml_kg_h_max"]),
            "start_before_h": h["start_before_h"],
            "continue_after_h": h["continue_after_h"],
            "note": "Individualizar para evitar sobrecarga de volume.",
        }
    return {
        "renal_function": renal,
        "bucket": bucket,
        "hydration": hydration,
        "metformin": decision_support({**payload, "contrast_class": "iodinated"}).get("cards", []),
        "source": rules["chapters"]["renal"],
    }


def interval_calculator(payload: dict[str, Any]) -> dict[str, Any]:
    rules = read_json(RULES_PATH)["intervals"]
    renal = renal_function(payload)
    bucket = payload.get("egfr_bucket") or renal["egfr_bucket"]
    fallback_note = None
    if bucket == "unknown":
        bucket = "moderate"
        fallback_note = "Função renal não calculada; usando faixa 30-60 como fallback conservador da v1."
    same_class = payload.get("previous_class") == payload.get("next_class")
    table = rules["between_injections"]["same_class" if same_class else "different_class"]
    sample_type = payload.get("sample_type", "blood")
    lab = rules["lab_collection"].get(sample_type, rules["lab_collection"]["blood"]).get(bucket)
    return {
        "egfr_bucket": bucket,
        "renal_function": renal,
        "between_injections": table[bucket],
        "lab_collection": lab,
        "same_class": same_class,
        "note": fallback_note or "Em emergência ou risco de vida, o intervalo pode ser encurtado considerando a segurança do paciente.",
        "source": rules["source"],
    }


def pediatric_calculator(payload: dict[str, Any]) -> dict[str, Any]:
    rules = read_json(RULES_PATH)["pediatrics"]
    weight = parse_float(payload.get("weight_kg")) or 0
    catheter = payload.get("catheter", "22G")
    return {
        "renal_function": renal_function(payload),
        "iodinated_volume_ml": {
            "min": round(weight * rules["iodinated_dose_ml_kg"]["min"], 1),
            "max": round(weight * rules["iodinated_dose_ml_kg"]["max"], 1),
        },
        "gbca_dose_mmol": round(weight * rules["gbca_dose_mmol_kg"], 3),
        "max_injection_rate": rules["injection_rate_by_catheter"].get(catheter, "Calibre não mapeado na v1"),
        "emergency_meds": rules["emergency_meds"],
        "source": rules["source"],
    }


def extravasation_support(payload: dict[str, Any]) -> dict[str, Any]:
    rules = read_json(RULES_PATH)["extravasation"]
    volume = parse_float(payload.get("volume_ml"))
    severe = bool(payload.get("severe_signs"))
    actions = list(rules["actions"])
    level = "attention"
    if severe or (volume is not None and volume > rules["surgical_eval_if_volume_gt_ml"]):
        level = "high"
        actions.append("Encaminhar para avaliação cirúrgica.")
    if volume is not None and volume > rules["document_if_volume_gt_ml"]:
        actions.append("Documentar detalhadamente o evento, contraste, volume, local, tipo de injeção, taxa/pressão, data e hora.")
    return {"level": level, "actions": actions, "follow_up": rules["follow_up"], "source": rules["source"]}


def build_qa_prompt(question: str, chunks: list[dict[str, Any]]) -> str:
    context = "\n\n".join(
        f"[{index + 1}] {chunk['title']} ({chunk['file']})\n{chunk['text']}"
        for index, chunk in enumerate(chunks)
    )
    return f"""Você é um assistente clínico local para equipe de sala, residentes de radiologia e radiologista responsável.
Responda em pt-BR, de forma natural, direta e acolhedora, como em uma conversa profissional curta.

Regras obrigatórias:
- Use somente o CONTEXTO local abaixo.
- Não invente doses, limiares, classes, contraindicações ou recomendações.
- Não transforme a resposta em protocolo institucional nem prescrição.
- Se a resposta não estiver no CONTEXTO, diga: "Não encontrei isso na documentação local."
- Se faltarem dados do paciente ou do exame para orientar a conduta, diga quais dados faltam em uma frase objetiva.
- Cite as fontes no formato [1], [2] no próprio texto.

Formato preferido:
1. Comece com uma resposta curta em linguagem natural.
2. Depois, se ajudar, use até 3 bullets com pontos práticos.
3. Termine com uma frase de cautela quando houver incerteza, exceção ou necessidade de validação pelo radiologista responsável.
4. Evite jargão desnecessário e listas longas.

CONTEXTO:
{context}

PERGUNTA:
{question}

RESPOSTA:"""


def ask_ollama(question: str, chunks: list[dict[str, Any]], qa: dict[str, Any]) -> dict[str, Any]:
    if not chunks:
        return {
            "answer": "Não encontrei isso na documentação local.",
            "model": qa["model"],
            "connector": qa["connector"],
            "available": False,
        }
    prompt = build_qa_prompt(question, chunks)
    body = json.dumps(
        {
            "model": qa["model"],
            "prompt": prompt,
            "stream": False,
            "keep_alive": qa["keep_alive"],
            "options": {"temperature": 0.1, "num_predict": qa["num_predict"]},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{qa['ollama_url'].rstrip('/')}/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = json.loads(response.read().decode("utf-8"))
            return {"answer": raw.get("response", "").strip(), "model": qa["model"], "connector": qa["connector"], "available": True}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        fallback = "Não consegui chamar o Ollama agora. Enquanto isso, encontrei estes trechos locais que parecem mais relevantes:\n\n"
        fallback += "\n".join(f"- [{index + 1}] {chunk['title']}: {chunk['snippet']}" for index, chunk in enumerate(chunks[:3]))
        return {"answer": fallback, "model": qa["model"], "connector": qa["connector"], "available": False, "error": str(exc)}


class Handler(BaseHTTPRequestHandler):
    server_version = "PossoContrastar/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format % args))

    def send_json(self, payload: Any, status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if not length:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/api/health":
            qa = app_config()["qa"]
            self.send_json(
                {
                    "ok": True,
                    "qa_enabled": qa["enabled"],
                    "qa_connector": qa["connector"],
                    "qa_model": qa["model"],
                    "qa_ollama_url": qa["ollama_url"],
                    "qa_keep_alive": qa["keep_alive"],
                    "qa_num_predict": qa["num_predict"],
                    "corpus": str(DOCS_DIR.relative_to(ROOT)),
                }
            )
        elif path == "/api/chapters":
            self.send_json({"chapters": load_chapters()})
        elif path == "/api/source":
            self.send_json(source_metadata())
        elif path == "/api/app-config":
            self.send_json(app_config())
        elif path == "/api/rules":
            self.send_json(read_json(RULES_PATH))
        elif path == "/api/search":
            query = ""
            if "?" in self.path:
                from urllib.parse import parse_qs, urlparse

                query = parse_qs(urlparse(self.path).query).get("q", [""])[0]
            self.send_json({"query": query, "results": retrieve(query, limit=10)})
        elif path.startswith("/api/"):
            self.send_json({"error": "endpoint not found"}, status=404)
        else:
            self.serve_static(path)

    def do_POST(self) -> None:
        try:
            payload = self.read_body()
            if self.path == "/api/decision":
                self.send_json(decision_support(payload))
            elif self.path == "/api/renal-function":
                self.send_json({"renal_function": renal_function(payload)})
            elif self.path == "/api/calculators/renal":
                self.send_json(renal_calculator(payload))
            elif self.path == "/api/calculators/interval":
                self.send_json(interval_calculator(payload))
            elif self.path == "/api/calculators/pediatric":
                self.send_json(pediatric_calculator(payload))
            elif self.path == "/api/extravasation":
                self.send_json(extravasation_support(payload))
            elif self.path == "/api/qa":
                qa = app_config()["qa"]
                if not qa["enabled"]:
                    self.send_json({"error": "Perguntas e Respostas desativado em app_config.json."}, status=403)
                    return
                if qa["connector"] != "ollama":
                    self.send_json({"error": f"Conector de Perguntas e Respostas não suportado: {qa['connector']}"}, status=400)
                    return
                question = str(payload.get("question", "")).strip()
                chunks = focus_retrieved_chunks(retrieve(question, limit=6))
                self.send_json({"question": question, "citations": chunks, **ask_ollama(question, chunks, qa)})
            else:
                self.send_json({"error": "endpoint not found"}, status=404)
        except json.JSONDecodeError:
            self.send_json({"error": "invalid json"}, status=400)
        except Exception as exc:  # noqa: BLE001 - surfacing local development errors as JSON.
            self.send_json({"error": str(exc)}, status=500)

    def serve_static(self, request_path: str) -> None:
        rel = request_path.lstrip("/") or "index.html"
        if rel.startswith("static/"):
            rel = rel[len("static/") :]
        target = (STATIC_DIR / rel).resolve()
        if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.exists() or target.is_dir():
            target = STATIC_DIR / "index.html"
        content_type = "text/html; charset=utf-8"
        if target.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif target.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        data = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Posso Contrastar local app")
    parser.add_argument("--host", default=os.environ.get("APP_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("APP_PORT", "8765")))
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    qa = app_config()["qa"]
    print(f"Serving app on http://{args.host}:{args.port}")
    print(
        f"Q&A: enabled={qa['enabled']} connector={qa['connector']} "
        f"model={qa['model']} ollama_url={qa['ollama_url']}"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
