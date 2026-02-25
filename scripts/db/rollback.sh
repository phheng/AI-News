#!/usr/bin/env bash
set -euo pipefail

MYSQL_CONTAINER="${CRYPTO_INTEL_MYSQL_CONTAINER:-mysql}"
MYSQL_USER="${CRYPTO_INTEL_MYSQL_USER:-root}"
MYSQL_PASSWORD="${CRYPTO_INTEL_MYSQL_PASSWORD:-nzh278799}"
MYSQL_DATABASE="${CRYPTO_INTEL_MYSQL_DATABASE:-crypto_intel}"

run_sql() {
  local file="$1"
  echo "[rollback] applying $file"
  docker exec -i "$MYSQL_CONTAINER" sh -lc \
    "mysql -u\"$MYSQL_USER\" -p\"$MYSQL_PASSWORD\" \"$MYSQL_DATABASE\"" < "$file"
}

for f in scripts/db/rollback/R*.sql; do
  run_sql "$f"
done

echo "[rollback] done"
