#!/usr/bin/env python3
"""
crypto-intel notification worker
- Consumes Redis stream: crypto-intel:stream:notification.telegram
- Idempotency: event_id + recipient composite key
- Retry + DLQ on repeated failures

Current sender implementation prints rendered message.
Hook actual telegram dispatch in send_telegram_message().
"""

from __future__ import annotations

import json
import os
import time
from redis import Redis

STREAM = os.getenv("CRYPTO_INTEL_NOTIFY_STREAM", "crypto-intel:stream:notification.telegram")
GROUP = os.getenv("CRYPTO_INTEL_STREAM_GROUP", "crypto-intel-group")
CONSUMER = os.getenv("CRYPTO_INTEL_STREAM_CONSUMER", "notify-worker-1")
REDIS_URL = os.getenv("CRYPTO_INTEL_REDIS_URL", "redis://127.0.0.1:6379/0")
DLQ_STREAM = os.getenv("CRYPTO_INTEL_NOTIFY_DLQ", "crypto-intel:stream:dlq:notification.telegram")
MAX_RETRY = int(os.getenv("CRYPTO_INTEL_NOTIFY_MAX_RETRY", "3"))
BLOCK_MS = int(os.getenv("CRYPTO_INTEL_NOTIFY_BLOCK_MS", "5000"))


def send_telegram_message(to: str, text: str) -> bool:
    # TODO: integrate real delivery bridge.
    print(f"[telegram:send] to={to}\n{text}\n")
    return True


def render_summary(payload: dict) -> str:
    return (
        f"[Strategy Cycle Completed] {payload.get('strategy_id')} v{payload.get('strategy_version')}\n\n"
        f"Backtest: {payload.get('backtest_summary')}\n"
        f"Paper: {payload.get('paper_summary')}\n"
        f"Optimization: {payload.get('optimization_action')}\n"
        f"Next Window: {payload.get('next_window')}\n"
        f"Risk: {payload.get('risk_notice')}"
    )


def main() -> None:
    r = Redis.from_url(REDIS_URL, decode_responses=True)

    # Ensure group exists
    try:
        r.xgroup_create(STREAM, GROUP, id="$", mkstream=True)
    except Exception as e:
        if "BUSYGROUP" not in str(e):
            raise

    print(f"[worker] listening stream={STREAM} group={GROUP} consumer={CONSUMER}")

    while True:
        entries = r.xreadgroup(groupname=GROUP, consumername=CONSUMER, streams={STREAM: ">"}, count=10, block=BLOCK_MS)
        if not entries:
            continue

        for _, records in entries:
            for message_id, fields in records:
                try:
                    event_id = fields.get("event_id")
                    payload_raw = fields.get("payload", "{}")
                    payload = json.loads(payload_raw)
                    to = payload.get("to")
                    dedup_key = f"crypto-intel:idem:notify:{event_id}:{to}"

                    if r.setnx(dedup_key, "1"):
                        r.expire(dedup_key, 7 * 24 * 3600)
                    else:
                        r.xack(STREAM, GROUP, message_id)
                        continue

                    text = render_summary(payload)
                    ok = send_telegram_message(to=to, text=text)
                    if ok:
                        r.xack(STREAM, GROUP, message_id)
                        continue

                    raise RuntimeError("telegram send failed")

                except Exception as e:
                    retry_key = f"crypto-intel:retry:notify:{message_id}"
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
