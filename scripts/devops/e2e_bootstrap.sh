#!/usr/bin/env bash
set -euo pipefail

# crypto-intel e2e bootstrap helper
# - starts local compose services (gateway + frontend)
# - checks required dependencies for e2e-smoke
# - optionally runs smoke/stress

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

GATEWAY_URL="${CRYPTO_INTEL_GATEWAY_BASE:-http://127.0.0.1:18080}"
MARKET_URL="${CRYPTO_INTEL_MARKET_AGENT_BASE:-http://127.0.0.1:18102}"
STRATEGY_URL="${CRYPTO_INTEL_STRATEGY_AGENT_BASE:-http://127.0.0.1:18103}"
BACKTEST_URL="${CRYPTO_INTEL_BACKTEST_AGENT_BASE:-http://127.0.0.1:18104}"

RUN_SMOKE="${CRYPTO_INTEL_BOOTSTRAP_RUN_SMOKE:-1}"
RUN_STRESS="${CRYPTO_INTEL_BOOTSTRAP_RUN_STRESS:-0}"

log() { echo "[e2e-bootstrap] $*"; }
warn() { echo "[e2e-bootstrap][WARN] $*"; }

check_health() {
  local base="$1"
  local url="${base%/}/healthz"
  if curl -fsS --max-time 3 "$url" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

log "starting compose services (gateway + frontend)"
docker compose up -d crypto-intel-api-gateway crypto-intel-frontend >/dev/null

log "waiting gateway health"
for _ in $(seq 1 20); do
  if check_health "$GATEWAY_URL"; then
    log "gateway ok: $GATEWAY_URL"
    break
  fi
  sleep 1
done

missing=()

if ! check_health "$MARKET_URL"; then
  missing+=("market-agent ($MARKET_URL)")
fi
if ! check_health "$STRATEGY_URL"; then
  missing+=("strategy-agent ($STRATEGY_URL)")
fi
if ! check_health "$BACKTEST_URL"; then
  missing+=("backtest-agent ($BACKTEST_URL)")
fi

if ((${#missing[@]} > 0)); then
  warn "missing required services:"
  for m in "${missing[@]}"; do
    warn "- $m"
  done
  warn "Tip: start corresponding agent workspaces/services first, then rerun."
fi

if [[ "$RUN_SMOKE" == "1" ]]; then
  if ((${#missing[@]} == 0)); then
    log "running e2e smoke"
    make e2e-smoke
  else
    warn "skip e2e-smoke due to missing services"
  fi
fi

if [[ "$RUN_STRESS" == "1" ]]; then
  if check_health "$MARKET_URL"; then
    log "running rate-limit stress"
    make rate-limit-stress
  else
    warn "skip rate-limit-stress: market-agent unavailable"
  fi
fi

log "done"