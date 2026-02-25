#!/usr/bin/env bash
set -euo pipefail

MYSQL_CONTAINER="${CRYPTO_INTEL_MYSQL_CONTAINER:-mysql}"
MYSQL_USER="${CRYPTO_INTEL_MYSQL_USER:-root}"
MYSQL_PASSWORD="${CRYPTO_INTEL_MYSQL_PASSWORD:-nzh278799}"
MYSQL_DATABASE="${CRYPTO_INTEL_MYSQL_DATABASE:-crypto_intel}"

run_sql() {
  local file="$1"
  echo "[migrate] applying $file"
  docker exec -i "$MYSQL_CONTAINER" sh -lc \
    "mysql -u\"$MYSQL_USER\" -p\"$MYSQL_PASSWORD\" \"$MYSQL_DATABASE\"" < "$file"
}

# create DB if not exists

docker exec -i "$MYSQL_CONTAINER" sh -lc \
  "mysql -u\"$MYSQL_USER\" -p\"$MYSQL_PASSWORD\" -e 'CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'"

for f in scripts/db/migrations/V*.sql; do
  run_sql "$f"
done

echo "[migrate] done"
