#!/usr/bin/env bash
set -euo pipefail

INFRA_DIR="${INFRA_NGINX_DIR:-/root/infra/nginx}"

if [[ ! -f "$INFRA_DIR/docker-compose.yml" ]]; then
  echo "[infra-nginx] docker-compose.yml not found in $INFRA_DIR" >&2
  exit 1
fi

cd "$INFRA_DIR"
docker compose up -d

echo "[infra-nginx] started"
echo "[infra-nginx] test: curl -I http://127.0.0.1/"
