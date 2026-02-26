#!/usr/bin/env bash
set -euo pipefail

INFRA_DIR="${INFRA_NGINX_DIR:-/root/infra/nginx}"
cd "$INFRA_DIR"
docker compose down

echo "[infra-nginx] stopped"
