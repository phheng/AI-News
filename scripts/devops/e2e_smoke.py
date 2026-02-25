#!/usr/bin/env python3
"""
crypto-intel E2E smoke test (design -> backtest -> paper -> optimize -> DM)

Pure-stdlib version (no third-party deps).
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass


@dataclass
class Cfg:
    strategy_base: str = os.getenv("CRYPTO_INTEL_STRATEGY_AGENT_BASE", "http://127.0.0.1:18103")
    backtest_base: str = os.getenv("CRYPTO_INTEL_BACKTEST_AGENT_BASE", "http://127.0.0.1:18104")
    gateway_base: str = os.getenv("CRYPTO_INTEL_GATEWAY_BASE", "http://127.0.0.1:18080")

    strategy_generate_path: str = os.getenv("CRYPTO_INTEL_STRATEGY_GENERATE_PATH", "/v1/strategy/generate")
    backtest_run_path: str = os.getenv("CRYPTO_INTEL_BACKTEST_RUN_PATH", "/v1/backtest/run")
    backtest_status_path_tpl: str = os.getenv(
        "CRYPTO_INTEL_BACKTEST_STATUS_PATH_TPL", "/v1/backtest/runs/{run_id}"
    )
    strategy_feedback_path: str = os.getenv(
        "CRYPTO_INTEL_STRATEGY_FEEDBACK_PATH", "/v1/strategy/feedback/paper-window-closed"
    )
    notify_path: str = os.getenv("CRYPTO_INTEL_NOTIFY_PATH", "/v1/notify/telegram/strategy-cycle")

    timeout_sec: float = float(os.getenv("CRYPTO_INTEL_SMOKE_TIMEOUT", "8"))
    poll_interval_sec: float = float(os.getenv("CRYPTO_INTEL_SMOKE_POLL_INTERVAL", "2"))
    poll_max_rounds: int = int(os.getenv("CRYPTO_INTEL_SMOKE_POLL_MAX_ROUNDS", "30"))
    notify_to: str = os.getenv("CRYPTO_INTEL_SMOKE_NOTIFY_TO", "test-chat")


def _request_json(method: str, url: str, timeout_sec: float, body: dict | None = None) -> dict:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            code = getattr(resp, "status", 200)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
        raise RuntimeError(f"request failed: {method} {url} status={e.code} body={raw[:500]}")
    except Exception as e:
        raise RuntimeError(f"request failed: {method} {url} error={e}")

    if not (200 <= code < 300):
        raise RuntimeError(f"request failed: {method} {url} status={code} body={raw[:500]}")

    try:
        payload = json.loads(raw) if raw else {}
    except Exception:
        payload = {"raw": raw}

    if isinstance(payload, dict) and payload.get("ok") is False:
        raise RuntimeError(f"request failed: {method} {url} body={str(payload)[:500]}")

    return payload if isinstance(payload, dict) else {"data": payload}


def main() -> int:
    cfg = Cfg()
    corr = f"smoke-{uuid.uuid4().hex[:10]}"
    print(f"[smoke] correlation={corr}")

    # 0) health
    _request_json("GET", f"{cfg.gateway_base}/healthz", cfg.timeout_sec)
    _request_json("GET", f"{cfg.strategy_base}/healthz", cfg.timeout_sec)
    _request_json("GET", f"{cfg.backtest_base}/healthz", cfg.timeout_sec)
    print("[ok] health checks passed")

    # 1) design
    gen_req = {
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "risk_profile": "balanced",
        "tags": ["smoke", corr],
    }
    gen = _request_json("POST", f"{cfg.strategy_base}{cfg.strategy_generate_path}", cfg.timeout_sec, gen_req)
    gen_data = gen.get("data", gen)
    strategy_id = gen_data.get("strategy_id") or f"smoke_strategy_{corr}"
    strategy_version = int(gen_data.get("strategy_version", 1))
    print(f"[ok] strategy generated: {strategy_id} v{strategy_version}")

    # 2) backtest
    run_req = {
        "strategy_id": strategy_id,
        "strategy_version": strategy_version,
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "period": "90d",
    }
    run = _request_json("POST", f"{cfg.backtest_base}{cfg.backtest_run_path}", cfg.timeout_sec, run_req)
    run_data = run.get("data", run)
    run_id = run_data.get("run_id")
    if not run_id:
        raise RuntimeError(f"backtest run_id missing: {run}")
    print(f"[ok] backtest started: {run_id}")

    # 2.5) poll backtest finish (best effort)
    final_status = "unknown"
    for _ in range(cfg.poll_max_rounds):
        st_path = cfg.backtest_status_path_tpl.format(run_id=run_id)
        st = _request_json("GET", f"{cfg.backtest_base}{st_path}", cfg.timeout_sec)
        st_data = st.get("data", st)
        final_status = str(st_data.get("status", "unknown")).lower()
        if final_status in {"completed", "success", "done", "finished"}:
            break
        if final_status in {"failed", "error", "cancelled", "canceled"}:
            raise RuntimeError(f"backtest failed status={final_status}")
        time.sleep(cfg.poll_interval_sec)
    print(f"[ok] backtest status: {final_status}")

    # 3) paper closed -> optimize trigger
    now = int(time.time())
    feed_req = {
        "strategy_id": strategy_id,
        "strategy_version": strategy_version,
        "window_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 3600)),
        "window_end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "metrics": {
            "pnl": 12.34,
            "max_drawdown": 0.07,
            "sharpe": 1.12,
            "win_rate": 0.56,
        },
        "trigger_flags": ["smoke-check"],
    }
    _request_json("POST", f"{cfg.strategy_base}{cfg.strategy_feedback_path}", cfg.timeout_sec, feed_req)
    print("[ok] paper window feedback submitted")

    # 4) queue DM
    notify_req = {
        "to": cfg.notify_to,
        "strategy_id": strategy_id,
        "strategy_version": strategy_version,
        "backtest_summary": f"run {run_id} status={final_status}",
        "paper_summary": "smoke cycle paper window closed",
        "optimization_action": "triggered-by-smoke",
        "next_window": "next 1h",
        "risk_notice": "smoke only",
    }
    notify = _request_json("POST", f"{cfg.gateway_base}{cfg.notify_path}", cfg.timeout_sec, notify_req)
    event_id = notify.get("data", notify).get("event_id", "unknown")
    print(f"[ok] notification queued event_id={event_id}")

    print("[smoke] PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"[smoke] FAIL: {e}", file=sys.stderr)
        raise SystemExit(1)
