#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "app" / "server.py"


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request_json(url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_health(base_url: str, deadline: float) -> dict[str, Any]:
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            return request_json(f"{base_url}/api/health")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            time.sleep(0.1)
    raise RuntimeError(f"app não respondeu ao healthcheck: {last_error}")


def run_smoke(port: int) -> None:
    base_url = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    env.update(
        {
            "APP_HOST": "127.0.0.1",
            "APP_PORT": str(port),
            "APP_QA_ENABLED": "false",
            "APP_QA_LOG_QUESTIONS": "false",
        }
    )
    process = subprocess.Popen(
        [sys.executable, str(SERVER), "--host", "127.0.0.1", "--port", str(port)],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        health = wait_for_health(base_url, time.monotonic() + 8)
        if health.get("ok") is not True:
            raise AssertionError(f"healthcheck inesperado: {health}")
        if health.get("qa_enabled") is not False:
            raise AssertionError("smoke deve rodar com Q&A desabilitado")

        source = request_json(f"{base_url}/api/source")
        if source.get("corpus_path") != "docs/meios_de_contraste":
            raise AssertionError("source.json não retornou corpus esperado")

        rules = request_json(f"{base_url}/api/rules")
        if rules.get("status") != "decision-support-draft":
            raise AssertionError("rules.json não retornou status esperado")

        renal = request_json(
            f"{base_url}/api/renal-function",
            {
                "creatinine_mg_dl": 1.0,
                "age_years": 45,
                "sex": "female",
                "weight_kg": 70,
            },
        )
        renal_function = renal.get("renal_function") or {}
        if renal_function.get("egfr_bucket") != "normal":
            raise AssertionError(f"função renal inesperada: {renal_function}")

        decision = request_json(
            f"{base_url}/api/decision",
            {
                "contrast_class": "iodinated",
                "route": "iv",
                "creatinine_mg_dl": 1.0,
                "age_years": 45,
                "sex": "female",
                "weight_kg": 70,
            },
        )
        if "cards" not in decision or "renal_function" not in decision:
            raise AssertionError(f"decisão inesperada: {decision}")
    finally:
        process.terminate()
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=5)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke HTTP do app local")
    parser.add_argument("--port", type=int, default=0, help="porta local; 0 escolhe uma porta livre")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    port = args.port or find_free_port()
    run_smoke(port)
    print(f"Smoke HTTP passou em http://127.0.0.1:{port}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
