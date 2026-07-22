"""Benchmark authorized OpenAI-compatible AI API providers."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return round(ordered[max(0, math.ceil(len(ordered) * fraction) - 1)], 2)


def request_payload(model: str, prompt: str) -> dict:
    return {"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 32, "temperature": 0}


def call_once(provider: dict, prompt: str, timeout: int) -> dict:
    api_key = os.getenv(provider["api_key_env"])
    if not api_key:
        return {"ok": False, "error": f"missing environment variable {provider['api_key_env']}"}
    request = urllib.request.Request(
        f"{provider['base_url'].rstrip('/')}/chat/completions",
        data=json.dumps(request_payload(provider["model"], prompt)).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode())
        return {"ok": bool(body.get("choices")), "http_status": response.status, "latency_ms": round((time.perf_counter() - started) * 1000, 2)}
    except urllib.error.HTTPError as error:
        error.read()
        return {"ok": False, "http_status": error.code, "latency_ms": round((time.perf_counter() - started) * 1000, 2)}
    except Exception as error:
        return {"ok": False, "error": type(error).__name__, "latency_ms": round((time.perf_counter() - started) * 1000, 2)}


def summarize(provider: dict, runs: list[dict]) -> dict:
    latencies = [run["latency_ms"] for run in runs if run.get("ok") and "latency_ms" in run]
    return {
        "provider": provider["name"],
        "model": provider["model"],
        "requests": len(runs),
        "successes": len(latencies),
        "success_rate": round(len(latencies) / len(runs), 4) if runs else 0,
        "latency_ms": {
            "mean": round(sum(latencies) / len(latencies), 2) if latencies else None,
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
        },
        "runs": runs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark authorized AI API providers")
    parser.add_argument("config", type=Path)
    parser.add_argument("--requests", type=int, default=5)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--prompt", default="Reply with OK")
    parser.add_argument("--output", type=Path, default=Path("results/latest.json"))
    args = parser.parse_args()
    if args.requests < 1 or args.concurrency < 1:
        parser.error("requests and concurrency must be positive")

    providers = json.loads(args.config.read_text(encoding="utf-8"))
    reports = []
    for provider in providers:
        with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            runs = list(executor.map(lambda _: call_once(provider, args.prompt, args.timeout), range(args.requests)))
        reports.append(summarize(provider, runs))
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "prompt_sha256": hashlib.sha256(args.prompt.encode()).hexdigest(),
        "methodology": {"requests": args.requests, "concurrency": args.concurrency, "timeout_seconds": args.timeout},
        "reports": reports,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
