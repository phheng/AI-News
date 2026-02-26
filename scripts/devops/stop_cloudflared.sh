#!/usr/bin/env bash
set -euo pipefail

INFRA_DIR="${INFRA_CLOUDFLARED_DIR:-/root/infra/cloudflared}"
cd "$INFRA_DIR"
docker compose down

echo "[cloudflared] stopped"
