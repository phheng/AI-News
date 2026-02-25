#!/usr/bin/env python3
"""
crypto-intel paper->strategy bridge worker
Consumes: crypto-intel:stream:paper.window.closed
Calls: strategy-agent /v1/strategy/feedback/paper-window-closed
"""

from __future__ import annotations

import json
import os
import time
import httpx
from redis import Redis

REDIS_URL = os.getenv("CRYPTO_INTEL_REDIS_URL", "redis://127.0.0.1:6379/0")
STREAM = os.getenv("CRYPTO_INTEL_PAPER_STREAM", "crypto-intel:stream:paper.window.closed")
GROUP = os.getenv("CRYPTO_INTEL_STREAM_GROUP", "crypto-intel-group")
CONSUMER = os.getenv("CRYPTO_INTEL_STREAM_CONSUMER", "paper-bridge-1")
DLQ_STREAM = os.getenv("CRYPTO_INTEL_PAPER_DLQ", "crypto-intel:stream:dlq:paper.window.closed")
MAX_RETRY = int(os.getenv("CRYPTO_INTEL_PAPER_MAX_RETRY", "3"))
BLOCK_MS = int(os.getenv("CRYPTO_INTEL_PAPER_BLOCK_MS", "5000"))
STRATEGY_BASE = os.getenv("CRYPTO_INTEL_STRATEGY_AGENT_BASE", "http://127.0.0.1:18103")


def main() -> None:
    r = Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        r.xgroup_create(STREAM, GROUP, id="$", mkstream=True)
    except Exception as e:
        if "BUSYGROUP" not in str(e):
            raise

    print(f"[bridge] stream={STREAM} group={GROUP} consumer={CONSUMER}")

    while True:
        entries = r.xreadgroup(groupname=GROUP, consumername=CONSUMER, streams={STREAM: ">"}, count=10, block=BLOCK_MS)
        if not entries:
            continue

        for _, records in entries:
            for message_id, fields in records:
                try:
                    payload = json.loads(fields.get("payload", "{}"))
                    event_id = fields.get("event_id", message_id)

                    dedup_key = f"crypto-intel:idem:paper-bridge:{event_id}"
                    if not r.setnx(dedup_key, "1"):
                        r.xack(STREAM, GROUP, message_id)
                        continue
                    r.expire(dedup_key, 7 * 24 * 3600)

                    req = {
                        "strategy_id": payload.get("strategy_id"),
                        "strategy_version": int(payload.get("strategy_version", 0)),
                        "window_start": payload.get("window_start"),
                        "window_end": payload.get("window_end"),
                        "metrics": payload.get("metrics", {}),
                        "trigger_flags": payload.get("anti_liquidation", {}).get("risk_flags", []),
                    }

                    with httpx.Client(timeout=5) as client:
                        resp = client.post(f"{STRATEGY_BASE}/v1/strategy/feedback/paper-window-closed", json=req)
                        resp.raise_for_status()

                    r.xack(STREAM, GROUP, message_id)

                except Exception as e:
                    retry_key = f"crypto-intel:retry:paper-bridge:{message_id}"
                    retry = r.incr(retry_key)
                    r.expire(retry_key, 24 * 3600)
                    if retry >= MAX_RETRY:
                        r.xadd(
                            DLQ_STREAM,
                            {
                                "source_stream": STREAM,
                                "source_id": message_id,
                                "error": str(e),
                                "fields": json.dumps(fields, ensure_ascii=False),
                                "ts": str(int(time.time())),
                            },
                        )
                        r.xack(STREAM, GROUP, message_id)


if __name__ == "__main__":
    main()
