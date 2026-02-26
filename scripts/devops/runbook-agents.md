# crypto-intel agent runbook (for E2E 9.3)

This workspace only starts gateway/frontend.
To pass `9.3 E2E smoke`, you also need:

- market-agent (`:18102`)
- strategy-agent (`:18103`)
- backtest-agent (`:18104`)

## 1) Configure endpoints

```bash
cp scripts/devops/agent_endpoints.sample.env scripts/devops/agent_endpoints.env
# edit if your ports/hosts differ
```

## 2) Load env in current shell

```bash
set -a
source scripts/devops/agent_endpoints.env
set +a
```

## 3) Start gateway/frontend (this workspace)

```bash
make e2e-up
```

> `make e2e-up` will auto-check dependencies and run smoke only when required agents are available.

## 4) Start external agents

Start each agent in its own workspace/service manager so `/healthz` is reachable:

- `${CRYPTO_INTEL_MARKET_AGENT_BASE}/healthz`
- `${CRYPTO_INTEL_STRATEGY_AGENT_BASE}/healthz`
- `${CRYPTO_INTEL_BACKTEST_AGENT_BASE}/healthz`

## 5) Re-run full E2E

```bash
make e2e-up
```

## 6) Optional pressure test

```bash
make rate-limit-stress
```
