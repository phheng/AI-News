from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_event(event_type: str, producer: str, payload: dict[str, Any], trace_id: str | None = None) -> dict[str, str]:
    envelope = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "trace_id": trace_id or str(uuid.uuid4()),
        "producer": producer,
        "occurred_at": now_iso(),
        "version": "1.0",
        "payload": json.dumps(payload, ensure_ascii=False),
    }
    return envelope
