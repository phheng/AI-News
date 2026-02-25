# OpenSpec v0.3: Cross-Agent Data Contracts（场景化共享数据契约）

- 状态：Draft v0.3.1
- 原则：按场景共享最小数据面（不是全量共享）
- 基础设施：MySQL + Redis

## 1. 场景与数据 Owner

1) News → Strategy
- Owner: News Agent
- Consumer: Strategy Agent
- 数据：`news_events`, `news_event_tags`, `news_analysis_outputs`, `news_embeddings`(可选)

2) Market → Strategy
- Owner: Market Agent
- Consumer: Strategy Agent
- 数据：`market_ohlcv`, `market_features`（v0.3.1 默认主来源：Bybit API）

3) Strategy → Backtest
- Owner: Strategy Agent
- Consumer: Backtest Agent
- 数据：`strategy_specs`, `strategy_versions`, `strategy_signal_snapshots`

4) Market → Backtest
- Owner: Market Agent
- Consumer: Backtest Agent
- 数据：`market_ohlcv`（按 symbol/timeframe/time-range 切片）

5) Backtest → Frontend
- Owner: Backtest Agent
- Consumer: Frontend
- 数据：`backtest_runs`, `backtest_metrics`, `backtest_artifacts`

## 2. MySQL 表草案（最小集）

### 2.1 新闻域
- `news_events`
  - `id` (pk)
  - `event_uid` (unique, 幂等键)
  - `source`
  - `published_at`
  - `title`
  - `summary`
  - `url`
  - `sentiment_score` (nullable)
  - `created_at`, `updated_at`

- `news_event_tags`
  - `id` (pk)
  - `event_uid` (fk -> news_events.event_uid)
  - `tag_type` (`symbol|topic|risk`)
  - `tag_value`

- `news_analysis_outputs`
  - `id` (pk)
  - `event_uid` (fk -> news_events.event_uid)
  - `analysis_version`
  - `impact_direction` (`bullish|bearish|neutral`)
  - `confidence`
  - `reasoning_summary`
  - `created_at`

### 2.2 行情域
- `market_ohlcv`
  - `id` (pk)
  - `venue`, `symbol`, `timeframe`, `ts` (unique composite)
  - `open`, `high`, `low`, `close`, `volume`
  - `ingested_at`

- `market_features`
  - `id` (pk)
  - `venue`, `symbol`, `timeframe`, `ts` (index)
  - `feature_set_version`
  - `payload_json`

### 2.3 策略域
- `strategy_specs`
  - `id` (pk)
  - `strategy_id` (unique)
  - `name`
  - `template_type`
  - `owner_agent_id`
  - `created_at`

- `strategy_versions`
  - `id` (pk)
  - `strategy_id` (index)
  - `version` (composite unique with strategy_id)
  - `spec_json`
  - `risk_json`
  - `created_at`

- `strategy_signal_snapshots`（可选）
  - `id` (pk)
  - `strategy_id`, `version`
  - `window_start`, `window_end`
  - `summary_json`

### 2.4 回测域
- `backtest_runs`
  - `id` (pk)
  - `run_id` (unique)
  - `strategy_id`, `strategy_version`
  - `status` (`queued|running|success|failed|canceled`)
  - `started_at`, `ended_at`

- `backtest_metrics`
  - `id` (pk)
  - `run_id` (fk)
  - `total_return`, `annual_return`, `max_drawdown`, `sharpe`, `win_rate`, `trade_count`

- `backtest_artifacts`
  - `id` (pk)
  - `run_id` (fk)
  - `artifact_type` (`trades_csv|equity_curve_csv|report_json`)
  - `path_or_url`

## 3. Redis 约定（最小集）

- 队列（Streams 或 Lists）
  - `crypto-intel:q:news-ingest`
  - `crypto-intel:q:market-sync`
  - `crypto-intel:q:strategy-eval`
  - `crypto-intel:q:backtest-run`

- 幂等键（SETNX + TTL）
  - `crypto-intel:idempotency:news:{event_uid}`
  - `crypto-intel:idempotency:market:{venue}:{symbol}:{tf}:{ts}`
  - 默认 TTL：7d

- 运行态缓存
  - `crypto-intel:run:{agent}:{job_id}:status`（TTL 24h）

- 分布式锁
  - `crypto-intel:lock:{resource}`（短 TTL + watchdog）

## 4. API 约束（FastAPI）

- 每个 Agent 内部 API：FastAPI
- 对前端聚合 API：FastAPI（主 workspace）
- 统一健康检查：`/healthz`
- 统一就绪检查：`/readyz`
- 统一版本：`/version`

## 5. 幂等与审计

- 写 MySQL 前先校验幂等键
- 每个跨 Agent 事件都带 `trace_id`
- 关键变更写审计表（后续 v0.4 细化）

## 6. 待 v0.4 细化

- 分区策略（market_ohlcv 的时间分区）
- 索引优化与冷热分层
- 失败补偿与重放窗口
