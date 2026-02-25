#!/usr/bin/env python3
"""
crypto-intel market API rate-limit stress tester (stdlib only)
"""

from __future__ import annotations

import concurrent.futures
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass


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

            for key in ("candles", "items", "rows"):
                arr = data.get(key)
                if isinstance(arr, list) and arr and isinstance(arr[0], dict):
                    v = arr[0].get("venue") or arr[0].get("source") or arr[0].get("exchange")
                    if isinstance(v, str) and v.strip():
                        candidates.append(v.strip().lower())

    if not candidates:
        return "unknown"
    c0 = candidates[0]
    if "bybit" in c0:
        return "bybit"
    if "binance" in c0:
        return "binance"
    return c0


def _one(url: str, timeout_sec: float) -> tuple[int, str, float, str]:
    req = urllib.request.Request(url=url, method="GET", headers={"Accept": "application/json"})
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            status = getattr(resp, "status", 200)
        latency_ms = (time.perf_counter() - t0) * 1000.0
        venue = "unknown"
        try:
            venue = _extract_venue(json.loads(raw))
        except Exception:
            pass
        return (status, venue, latency_ms, "")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
        latency_ms = (time.perf_counter() - t0) * 1000.0
        venue = "unknown"
        try:
            venue = _extract_venue(json.loads(raw))
        except Exception:
            pass
        return (e.code, venue, latency_ms, "")
    except Exception as e:
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return (0, "unknown", latency_ms, str(e))


def percentile(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    idx = int(p * (len(s) - 1))
    return s[idx]


def main() -> int:
    cfg = Cfg()
    params = urllib.parse.urlencode({"symbol": cfg.symbol, "timeframe": cfg.timeframe, "limit": 200})
    url = f"{cfg.base}{cfg.path}?{params}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=cfg.concurrency) as ex:
        futures = [ex.submit(_one, url, cfg.timeout_sec) for _ in range(cfg.burst)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    status_counter = Counter()
    venue_counter = Counter()
    latencies = []
    errors = []

    for status, venue, lat_ms, err in results:
        status_counter[status] += 1
        venue_counter[venue] += 1
        latencies.append(lat_ms)
        if err:
            errors.append(err)

    total = len(results)
    ok_2xx = sum(v for s, v in status_counter.items() if 200 <= s < 300)
    ratelimited = status_counter.get(429, 0)
    server_err = sum(v for s, v in status_counter.items() if 500 <= s < 600)
    net_err = status_counter.get(0, 0)

    p50 = percentile(latencies, 0.50)
    p95 = percentile(latencies, 0.95)
    p99 = percentile(latencies, 0.99)

    print("[stress] market free-api rate-limit test")
    print(f"target={url}")
    print(f"burst={cfg.burst} concurrency={cfg.concurrency} timeout={cfg.timeout_sec}s")
    print("---")
    print(f"total={total}")
    print(f"2xx={ok_2xx}")
    print(f"429={ratelimited}")
    print(f"5xx={server_err}")
    print(f"net_err={net_err}")
    print(f"latency_ms p50={p50:.1f} p95={p95:.1f} p99={p99:.1f}")
    print(f"venue_counts={dict(venue_counter)}")
    if errors:
        print(f"sample_errors={errors[:3]}")

    fail = False
    if ok_2xx == 0:
        print("[result] FAIL: no successful responses")
        fail = True
    if server_err > total * 0.5:
        print("[result] FAIL: 5xx ratio too high (>50%)")
        fail = True

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


if __name__ == "__main__":
    raise SystemExit(main())
