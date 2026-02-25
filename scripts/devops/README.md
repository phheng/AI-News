# crypto-intel: devops

Docker/compose and deployment scripts live here.

## E2E smoke

- Script: `scripts/devops/e2e_smoke.py`
- Purpose: validate `design -> backtest -> paper -> optimize -> DM` closed loop in one command.

### Quick run

```bash
python3 scripts/devops/e2e_smoke.py
```

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
