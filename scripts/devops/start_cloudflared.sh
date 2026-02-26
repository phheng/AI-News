#!/usr/bin/env bash
set -euo pipefail

INFRA_DIR="${INFRA_CLOUDFLARED_DIR:-/root/infra/cloudflared}"
cd "$INFRA_DIR"
docker compose up -d

sleep 2
URL=$(docker logs infra-cloudflared 2>&1 | grep -oE 'https://[a-zA-Z0-9.-]+\.trycloudflare\.com' | tail -n 1 || true)
echo "[cloudflared] started"
if [[ -n "$URL" ]]; then
  echo "[cloudflared] url: $URL"
fi
