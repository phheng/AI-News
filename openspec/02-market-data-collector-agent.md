# OpenSpec: Market Data Collector Agent

- **状态**：Draft v0.3.1
- **目标 workspace（开发目录）**：`~/.openclaw/workspace-crypto-intel-market-agent`
- **技术栈**：Python + uv

## 1. 目标

收集并标准化行情数据（优先 OHLCV），作为策略设计与回测的统一数据底座。

## 2. 范围

### In Scope
- 多交易所行情抓取（**Bybit API 为主数据源**）
- 多周期 K 线（1m/5m/1h/4h/1d）
- 数据补齐与基础质量校验
- 可扩展字段（funding/OI）

### Out of Scope（v0）
- 高频 tick 级回放
- 订单簿深度持久化

## 3. 输入/输出

### 输入
- `markets.yaml`：交易所、交易对、周期配置（v0.3.1 默认 `venue=bybit`，后续可扩展）

### 输出
- `ohlcv_<venue>_<symbol>_<tf>.parquet`（或 SQLite 表）
- 统一字段：`ts, open, high, low, close, volume, venue, symbol, timeframe`

## 4. 接口契约

- 向 Strategy Design Agent 提供特征构建所需历史窗口数据
- 向 Backtest Agent 提供回测数据切片

## 5. 非功能要求

- 数据断档自动补拉
- 时间戳对齐一致
- 失败重试 + 死信日志

## 6. 验收标准

- 指定交易对在 24h 内无明显断档（允许短时 API 故障）
- 可按 symbol/timeframe 快速查询
- 可直接喂给 Backtest Agent
\n## 7. 运维与命名约束\n
- workspace：`~/.openclaw/workspace-crypto-intel-market-agent`
- 定时任务前缀：`crypto-intel: market`
- MySQL 主表（v0 草案）：`ohlcv_bars`
- Redis（v0 草案）：用于补拉任务队列、热数据缓存、分布式锁
