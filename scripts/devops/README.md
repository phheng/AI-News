# crypto-intel: devops

Docker/compose and deployment scripts live here.

## E2E bootstrap (recommended)

- Script: `scripts/devops/e2e_bootstrap.sh`
- Purpose: bring up compose services, check required agent health, and optionally run smoke/stress.

### Quick run

```bash
make e2e-up
```

### Optional env vars

- `CRYPTO_INTEL_BOOTSTRAP_RUN_SMOKE` (default `1`)
- `CRYPTO_INTEL_BOOTSTRAP_RUN_STRESS` (default `0`)
- `CRYPTO_INTEL_BOOTSTRAP_ENV_FILE` (default `scripts/devops/agent_endpoints.env`)
- `CRYPTO_INTEL_GATEWAY_BASE` (default `http://127.0.0.1:18080`)
- `CRYPTO_INTEL_MARKET_AGENT_BASE` (default `http://127.0.0.1:18102`)
- `CRYPTO_INTEL_STRATEGY_AGENT_BASE` (default `http://127.0.0.1:18103`)
- `CRYPTO_INTEL_BACKTEST_AGENT_BASE` (default `http://127.0.0.1:18104`)

### Endpoint env template

```bash
cp scripts/devops/agent_endpoints.sample.env scripts/devops/agent_endpoints.env
```

See `scripts/devops/runbook-agents.md` for the full checklist.

## E2E report (for 9.3 acceptance)

- Script: `scripts/devops/e2e_report.py`
- Purpose: generate markdown verdict for OpenSpec 9.3 (service health + smoke result + blockers).

### Quick run

```bash
make e2e-report
```

### Output

- Default: `scripts/devops/reports/e2e-latest.md`

## E2E smoke

- Script: `scripts/devops/e2e_smoke.py`
- Purpose: validate `design -> backtest -> paper -> optimize -> DM` closed loop in one command.

### Quick run

```bash
python3 scripts/devops/e2e_smoke.py
```

### Prerequisites

E2E smoke requires these services reachable:

- gateway: `http://127.0.0.1:18080`
- strategy-agent: `http://127.0.0.1:18103`
- backtest-agent: `http://127.0.0.1:18104`

If you only started `docker compose` in this workspace, gateway/frontend may be up but strategy/backtest can still be missing (they live in separate workspaces/services).

### Optional env vars

- `CRYPTO_INTEL_STRATEGY_AGENT_BASE` (default `http://127.0.0.1:18103`)
- `CRYPTO_INTEL_BACKTEST_AGENT_BASE` (default `http://127.0.0.1:18104`)
- `CRYPTO_INTEL_GATEWAY_BASE` (default `http://127.0.0.1:18080`)
- `CRYPTO_INTEL_SMOKE_NOTIFY_TO` (default `test-chat`)
- `CRYPTO_INTEL_STRATEGY_GENERATE_PATH` (default `/v1/strategy/generate`)
- `CRYPTO_INTEL_BACKTEST_RUN_PATH` (default `/v1/backtest/run`)
- `CRYPTO_INTEL_BACKTEST_STATUS_PATH_TPL` (default `/v1/backtest/runs/{run_id}`)
- `CRYPTO_INTEL_STRATEGY_FEEDBACK_PATH` (default `/v1/strategy/feedback/paper-window-closed`)
- `CRYPTO_INTEL_NOTIFY_PATH` (default `/v1/notify/telegram/strategy-cycle`)

## Rate-limit stress

- Script: `scripts/devops/rate_limit_stress.py`
- Purpose: pressure test free API limits and observe fallback behavior (`Bybit -> Binance`).

### Quick run

```bash
python3 scripts/devops/rate_limit_stress.py
```

### Optional env vars

- `CRYPTO_INTEL_MARKET_AGENT_BASE` (default `http://127.0.0.1:18102`)
- `CRYPTO_INTEL_MARKET_PATH` (default `/v1/market/ohlcv`)
- `CRYPTO_INTEL_STRESS_SYMBOL` (default `BTCUSDT`)
- `CRYPTO_INTEL_STRESS_TIMEFRAME` (default `1m`)
- `CRYPTO_INTEL_STRESS_BURST` (default `200`)
- `CRYPTO_INTEL_STRESS_CONCURRENCY` (default `20`)
- `CRYPTO_INTEL_STRESS_TIMEOUT` (default `5`)

## Infra nginx (Docker, in `~/infra`)

- Config location: `~/infra/nginx/`
  - `~/infra/nginx/docker-compose.yml`
  - `~/infra/nginx/nginx.conf`
  - `~/infra/nginx/conf.d/crypto-intel.conf`
- Start script: `scripts/devops/start_infra_nginx.sh`
- Stop script: `scripts/devops/stop_infra_nginx.sh`

### Quick run

```bash
make infra-nginx-up
# stop
make infra-nginx-down
```

This nginx maps:
- `/` -> `http://host.docker.internal:15174` (frontend)
- `/api/` -> `http://host.docker.internal:18080` (gateway)
