#!/usr/bin/env python3
"""
crypto-intel E2E smoke test (design -> backtest -> paper -> optimize -> DM)

This script validates the closed loop in a lightweight way:
1) generate strategy (strategy-agent)
2) run backtest (backtest-agent)
3) submit paper-window feedback (strategy-agent optimize trigger)
4) queue DM notification (api-gateway -> notification stream)

All endpoint paths are configurable via env vars for compatibility.
"""

from __future__ import annotations

import os
import sys
import time
import uuid
from dataclasses import dataclass

import httpx


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
    notify_path: str = os.getenv(
        "CRYPTO_INTEL_NOTIFY_PATH", "/v1/notify/telegram/strategy-cycle"
    )

    timeout_sec: float = float(os.getenv("CRYPTO_INTEL_SMOKE_TIMEOUT", "8"))
    poll_interval_sec: float = float(os.getenv("CRYPTO_INTEL_SMOKE_POLL_INTERVAL", "2"))
    poll_max_rounds: int = int(os.getenv("CRYPTO_INTEL_SMOKE_POLL_MAX_ROUNDS", "30"))
    notify_to: str = os.getenv("CRYPTO_INTEL_SMOKE_NOTIFY_TO", "test-chat")


def _ok(resp: httpx.Response) -> bool:
    try:
        data = resp.json()
    except Exception:
        return False
    if isinstance(data, dict) and data.get("ok") is False:
        return False
    return 200 <= resp.status_code < 300


def _must(client: httpx.Client, method: str, url: str, *, json: dict | None = None) -> dict:
    resp = client.request(method, url, json=json)
    if not _ok(resp):
        raise RuntimeError(f"request failed: {method} {url} status={resp.status_code} body={resp.text[:500]}")
    try:
        return resp.json()
    except Exception:
        return {"raw": resp.text}


def main() -> int:
    cfg = Cfg()
    corr = f"smoke-{uuid.uuid4().hex[:10]}"
    print(f"[smoke] correlation={corr}")

    with httpx.Client(timeout=cfg.timeout_sec) as client:
        # 0) health
        _must(client, "GET", f"{cfg.gateway_base}/healthz")
        _must(client, "GET", f"{cfg.strategy_base}/healthz")
        _must(client, "GET", f"{cfg.backtest_base}/healthz")
        print("[ok] health checks passed")

        # 1) design
        gen_req = {
            "symbol": "BTCUSDT",
            "timeframe": "1h",
            "risk_profile": "balanced",
            "tags": ["smoke", corr],
        }
        gen = _must(client, "POST", f"{cfg.strategy_base}{cfg.strategy_generate_path}", json=gen_req)
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
        run = _must(client, "POST", f"{cfg.backtest_base}{cfg.backtest_run_path}", json=run_req)
        run_data = run.get("data", run)
        run_id = run_data.get("run_id")
        if not run_id:
            raise RuntimeError(f"backtest run_id missing: {run}")
        print(f"[ok] backtest started: {run_id}")

        # 2.5) poll backtest finish (best effort)
        final_status = "unknown"
        for _ in range(cfg.poll_max_rounds):
            st_path = cfg.backtest_status_path_tpl.format(run_id=run_id)
            st = _must(client, "GET", f"{cfg.backtest_base}{st_path}")
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
        _must(client, "POST", f"{cfg.strategy_base}{cfg.strategy_feedback_path}", json=feed_req)
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
        notify = _must(client, "POST", f"{cfg.gateway_base}{cfg.notify_path}", json=notify_req)
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
