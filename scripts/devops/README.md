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
