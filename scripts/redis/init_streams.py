#!/usr/bin/env python3
import os
from redis import Redis

REDIS_URL = os.getenv("CRYPTO_INTEL_REDIS_URL", "redis://127.0.0.1:6379/0")
GROUP = os.getenv("CRYPTO_INTEL_STREAM_GROUP", "crypto-intel-group")

TOPICS = [
    "crypto-intel:stream:news.events",
    "crypto-intel:stream:news.urgent",
    "crypto-intel:stream:market.ohlcv",
    "crypto-intel:stream:market.indicators",
    "crypto-intel:stream:strategy.generated",
    "crypto-intel:stream:backtest.completed",
    "crypto-intel:stream:paper.window.closed",
    "crypto-intel:stream:strategy.optimized",
    "crypto-intel:stream:notification.telegram",
]


def ensure_stream_and_group(client: Redis, stream: str, group: str) -> None:
    client.xadd(stream, {"bootstrap": "1"}, id="*", maxlen=1, approximate=True)
    try:
        client.xgroup_create(stream, group, id="$", mkstream=True)
        print(f"created group {group} on {stream}")
    except Exception as e:
        msg = str(e)
        if "BUSYGROUP" in msg:
            print(f"group exists {group} on {stream}")
        else:
            raise


def main():
    client = Redis.from_url(REDIS_URL, decode_responses=True)
    for topic in TOPICS:
        ensure_stream_and_group(client, topic, GROUP)
    print("done")


if __name__ == "__main__":
    main()
