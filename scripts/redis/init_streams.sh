#!/usr/bin/env bash
set -euo pipefail

REDIS_CONTAINER="${CRYPTO_INTEL_REDIS_CONTAINER:-redis}"
GROUP="${CRYPTO_INTEL_STREAM_GROUP:-crypto-intel-group}"

TOPICS=(
  "crypto-intel:stream:news.events"
  "crypto-intel:stream:news.urgent"
  "crypto-intel:stream:market.ohlcv"
  "crypto-intel:stream:market.indicators"
  "crypto-intel:stream:strategy.generated"
  "crypto-intel:stream:backtest.completed"
  "crypto-intel:stream:paper.window.closed"
  "crypto-intel:stream:strategy.optimized"
  "crypto-intel:stream:notification.telegram"
)

for stream in "${TOPICS[@]}"; do
  docker exec "$REDIS_CONTAINER" redis-cli XADD "$stream" '*' bootstrap 1 MAXLEN '~' 1 >/dev/null
  set +e
  out=$(docker exec "$REDIS_CONTAINER" redis-cli XGROUP CREATE "$stream" "$GROUP" '$' MKSTREAM 2>&1)
  code=$?
  set -e
  if [[ $code -ne 0 ]] && [[ "$out" != *BUSYGROUP* ]]; then
    echo "failed create group on $stream: $out"
    exit 1
  fi
  echo "ok $stream"
done

echo "redis streams initialized"
