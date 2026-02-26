#!/usr/bin/env bash
set -euo pipefail

INFRA_DIR="${INFRA_NEWS_COLLECTOR_DIR:-/root/infra/news-collector}"
cd "$INFRA_DIR"
docker compose down

echo "[news-collector] stopped"
