#!/usr/bin/env python3
"""
crypto-intel market API rate-limit stress tester

Goal:
- pressure test free API quota behavior
- observe 429/5xx ratios
- verify fallback behavior (Bybit -> Binance) if exposed in response payload

Usage:
  python3 scripts/devops/rate_limit_stress.py

Key env vars:
  CRYPTO_INTEL_MARKET_AGENT_BASE=http://127.0.0.1:18102
  CRYPTO_INTEL_MARKET_PATH=/v1/market/ohlcv
  CRYPTO_INTEL_STRESS_SYMBOL=BTCUSDT
  CRYPTO_INTEL_STRESS_TIMEFRAME=1m
  CRYPTO_INTEL_STRESS_BURST=200
  CRYPTO_INTEL_STRESS_CONCURRENCY=20
  CRYPTO_INTEL_STRESS_TIMEOUT=5
"""

from __future__ import annotations

import asyncio
import os
import time
from collections import Counter
from dataclasses import dataclass

import httpx


@dataclass
class Cfg:
    base: str = os.getenv("CRYPTO_INTEL_MARKET_AGENT_BASE", "http://127.0.0.1:18102")
    path: str = os.getenv("CRYPTO_INTEL_MARKET_PATH", "/v1/market/ohlcv")
    symbol: str = os.getenv("CRYPTO_INTEL_STRESS_SYMBOL", "BTCUSDT")
    timeframe: str = os.getenv("CRYPTO_INTEL_STRESS_TIMEFRAME", "1m")
    burst: int = int(os.getenv("CRYPTO_INTEL_STRESS_BURST", "200"))
    concurrency: int = int(os.getenv("CRYPTO_INTEL_STRESS_CONCURRENCY", "20"))
    timeout_sec: float = float(os.getenv("CRYPTO_INTEL_STRESS_TIMEOUT", "5"))


def _extract_venue(payload: dict) -> str:
    """Best-effort venue extraction for fallback verification."""
    candidates = []

    if isinstance(payload, dict):
        for k in ("venue", "source", "source_venue", "exchange"):
            v = payload.get(k)
            if isinstance(v, str) and v.strip():
                candidates.append(v.strip().lower())

        data = payload.get("data")
        if isinstance(data, dict):
            for k in ("venue", "source", "source_venue", "exchange"):
                v = data.get(k)
                if isinstance(v, str) and v.strip():
                    candidates.append(v.strip().lower())

            # list payload support
            for key in ("candles", "items", "rows"):
                arr = data.get(key)
                if isinstance(arr, list) and arr:
                    first = arr[0]
                    if isinstance(first, dict):
                        v = first.get("venue") or first.get("source") or first.get("exchange")
                        if isinstance(v, str) and v.strip():
                            candidates.append(v.strip().lower())

    if not candidates:
        return "unknown"

    # normalize known aliases
    c0 = candidates[0]
    if "bybit" in c0:
        return "bybit"
    if "binance" in c0:
        return "binance"
    return c0


async def _one(client: httpx.AsyncClient, sem: asyncio.Semaphore, url: str, params: dict) -> tuple[int, str, float, str]:
    async with sem:
        t0 = time.perf_counter()
        try:
            resp = await client.get(url, params=params)
            latency_ms = (time.perf_counter() - t0) * 1000.0
            venue = "unknown"
            try:
                venue = _extract_venue(resp.json())
            except Exception:
                pass
            return (resp.status_code, venue, latency_ms, "")
        except Exception as e:
            latency_ms = (time.perf_counter() - t0) * 1000.0
            return (0, "unknown", latency_ms, str(e))


async def run(cfg: Cfg) -> int:
    url = f"{cfg.base}{cfg.path}"
    params = {"symbol": cfg.symbol, "timeframe": cfg.timeframe, "limit": 200}

    sem = asyncio.Semaphore(cfg.concurrency)
    results: list[tuple[int, str, float, str]] = []

    timeout = httpx.Timeout(cfg.timeout_sec)
    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [_one(client, sem, url, params) for _ in range(cfg.burst)]
        results = await asyncio.gather(*tasks)

    status_counter = Counter()
    venue_counter = Counter()
    latencies = []
    errors = []

    for status, venue, lat_ms, err in results:
        latencies.append(lat_ms)
        status_counter[status] += 1
        venue_counter[venue] += 1
        if err:
            errors.append(err)

    total = len(results)
    ok_2xx = sum(v for s, v in status_counter.items() if 200 <= s < 300)
    ratelimited = status_counter.get(429, 0)
    server_err = sum(v for s, v in status_counter.items() if 500 <= s < 600)
    net_err = status_counter.get(0, 0)

    lat_sorted = sorted(latencies)
    p50 = lat_sorted[int(0.5 * (total - 1))] if total else 0
    p95 = lat_sorted[int(0.95 * (total - 1))] if total else 0
    p99 = lat_sorted[int(0.99 * (total - 1))] if total else 0

    print("[stress] market free-api rate-limit test")
    print(f"target={url} symbol={cfg.symbol} timeframe={cfg.timeframe}")
    print(f"burst={cfg.burst} concurrency={cfg.concurrency} timeout={cfg.timeout_sec}s")
    print("---")
    print(f"total={total}")
    print(f"2xx={ok_2xx} ({ok_2xx/total*100:.1f}% if total else 0)")
    print(f"429={ratelimited} ({ratelimited/total*100:.1f}% if total else 0)")
    print(f"5xx={server_err} ({server_err/total*100:.1f}% if total else 0)")
    print(f"net_err={net_err} ({net_err/total*100:.1f}% if total else 0)")
    print(f"latency_ms p50={p50:.1f} p95={p95:.1f} p99={p99:.1f}")
    print(f"venue_counts={dict(venue_counter)}")

    if errors:
        sample = errors[:3]
        print(f"sample_errors={sample}")

    # simple pass criteria (tunable): service should remain mostly available
    # even under pressure and not collapse into pure failures.
    fail = False
    if ok_2xx == 0:
        print("[result] FAIL: no successful responses")
        fail = True
    if server_err > total * 0.5:
        print("[result] FAIL: 5xx ratio too high (>50%)")
        fail = True

    # fallback observation hint
    if venue_counter.get("binance", 0) > 0:
        print("[result] OBSERVED: Binance fallback traffic")
    elif venue_counter.get("bybit", 0) > 0:
        print("[result] OBSERVED: Bybit served responses")
    else:
        print("[result] WARN: venue source not observable in payload")

    if fail:
        return 1

    print("[result] PASS")
    return 0


def main() -> int:
    cfg = Cfg()
    return asyncio.run(run(cfg))


if __name__ == "__main__":
    raise SystemExit(main())
