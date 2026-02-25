# OpenSpec v0.3.2: Workspace Bootstrap Plan

- 状态：Draft v0.3.2
- 目标：定义四 Agent workspace 与主 workspace 的最小骨架

## 1) 主 workspace（~/.openclaw/workspace）

```text
apps/
  frontend/                 # React + TailwindCSS（多标签页）
  api-gateway/              # FastAPI 聚合层（给前端）
contracts/
openspec/
scripts/
  db/
  redis/
```

## 2) 四 Agent workspace 骨架

### 2.1 news agent
`~/.openclaw/workspace-crypto-intel-news-agent`

```text
apps/news-agent/
  pyproject.toml
  src/
    api/
    collectors/
    analysis/
    storage/
    jobs/
  tests/
  config/
```

### 2.2 market agent
`~/.openclaw/workspace-crypto-intel-market-agent`

```text
apps/market-agent/
  pyproject.toml
  src/
    api/
    bybit/
    features/
    storage/
    jobs/
  tests/
  config/
```

### 2.3 strategy agent（记忆重点）
`~/.openclaw/workspace-crypto-intel-strategy-agent`

```text
apps/strategy-agent/
  pyproject.toml
  src/
    api/
    engine/
    templates/
    memory_openviking/
    storage/
    jobs/
  memory/
    .abstract
    p0-core/
    p1-active/
    p2-temp/
    archive/
  shared-memory/
    .abstract
    user-profile.md
    active-tasks.md
    cross-agent-log.md
  tests/
  config/
```

### 2.4 backtest agent
`~/.openclaw/workspace-crypto-intel-backtest-agent`

```text
apps/backtest-agent/
  pyproject.toml
  src/
    api/
    runner/
    metrics/
    storage/
    jobs/
  tests/
  config/
```

## 3) Cron 前缀规范

- `crypto-intel: news ...`
- `crypto-intel: market ...`
- `crypto-intel: strategy ...`
- `crypto-intel: backtest ...`

## 4) 复用策略（旧 Agent）

- 来源：`workspace-crypto-trading-agent`
- 优先复用模块：
  - 市场抓取调度逻辑
  - 策略参数管理
  - 回测报告组织方式
- 迁移方式：复制后重构，不做“原地硬改”
