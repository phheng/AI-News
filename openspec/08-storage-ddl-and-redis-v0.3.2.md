# OpenSpec v0.3.2: Storage DDL & Redis Keyspace

- 状态：Draft v0.3.2
- 范围：MySQL DDL 草案 + Redis Key 规范 + 数据治理约束

## 1) MySQL 约束

- 字符集：`utf8mb4`
- 时区：统一存储 UTC（展示层再转 Asia/Shanghai）
- 主键：`BIGINT UNSIGNED AUTO_INCREMENT`
- 审计字段：`created_at`, `updated_at`
- 软删除：默认不启用（可在 v0.4 评估）

## 2) DDL 草案

```sql
CREATE TABLE news_events (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  event_uid VARCHAR(128) NOT NULL,
  source VARCHAR(64) NOT NULL,
  published_at DATETIME(3) NOT NULL,
  title VARCHAR(512) NOT NULL,
  summary TEXT,
  url VARCHAR(1024) NOT NULL,
  sentiment_score DECIMAL(6,4) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  updated_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_news_event_uid (event_uid),
  KEY idx_news_published_at (published_at),
  KEY idx_news_source (source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE news_event_tags (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  event_uid VARCHAR(128) NOT NULL,
  tag_type ENUM('symbol','topic','risk') NOT NULL,
  tag_value VARCHAR(128) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_news_tags_event_uid (event_uid),
  KEY idx_news_tags_type_value (tag_type, tag_value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE news_analysis_outputs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  event_uid VARCHAR(128) NOT NULL,
  analysis_version VARCHAR(32) NOT NULL,
  impact_direction ENUM('bullish','bearish','neutral') NOT NULL,
  confidence DECIMAL(6,4) NOT NULL,
  reasoning_summary TEXT,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_news_analysis_event_uid (event_uid),
  KEY idx_news_analysis_direction_conf (impact_direction, confidence)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE market_ohlcv (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  venue VARCHAR(32) NOT NULL,
  symbol VARCHAR(32) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  ts DATETIME(3) NOT NULL,
  open DECIMAL(30,10) NOT NULL,
  high DECIMAL(30,10) NOT NULL,
  low DECIMAL(30,10) NOT NULL,
  close DECIMAL(30,10) NOT NULL,
  volume DECIMAL(30,10) NOT NULL,
  ingested_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_market_ohlcv (venue, symbol, timeframe, ts),
  KEY idx_market_symbol_tf_ts (symbol, timeframe, ts)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE market_features (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  venue VARCHAR(32) NOT NULL,
  symbol VARCHAR(32) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  ts DATETIME(3) NOT NULL,
  feature_set_version VARCHAR(32) NOT NULL,
  payload_json JSON NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_market_features_lookup (symbol, timeframe, ts),
  KEY idx_market_features_version (feature_set_version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE strategy_specs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  strategy_id VARCHAR(64) NOT NULL,
  name VARCHAR(128) NOT NULL,
  template_type VARCHAR(64) NOT NULL,
  owner_agent_id VARCHAR(64) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_strategy_id (strategy_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE strategy_versions (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  strategy_id VARCHAR(64) NOT NULL,
  version INT NOT NULL,
  spec_json JSON NOT NULL,
  risk_json JSON NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_strategy_ver (strategy_id, version),
  KEY idx_strategy_ver_strategy (strategy_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE backtest_runs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  run_id VARCHAR(64) NOT NULL,
  strategy_id VARCHAR(64) NOT NULL,
  strategy_version INT NOT NULL,
  status ENUM('queued','running','success','failed','canceled') NOT NULL,
  started_at DATETIME(3) NULL,
  ended_at DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_backtest_run_id (run_id),
  KEY idx_backtest_strategy (strategy_id, strategy_version),
  KEY idx_backtest_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE backtest_metrics (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  run_id VARCHAR(64) NOT NULL,
  total_return DECIMAL(12,6) NOT NULL,
  annual_return DECIMAL(12,6) NOT NULL,
  max_drawdown DECIMAL(12,6) NOT NULL,
  sharpe DECIMAL(12,6) NULL,
  win_rate DECIMAL(12,6) NULL,
  trade_count INT NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_backtest_metrics_run_id (run_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE backtest_artifacts (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  run_id VARCHAR(64) NOT NULL,
  artifact_type ENUM('trades_csv','equity_curve_csv','report_json') NOT NULL,
  path_or_url VARCHAR(1024) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_backtest_artifacts_run_id (run_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 3) Redis Keyspace 规范

- 命名统一：`crypto-intel:<domain>:<type>:...`

### 3.1 队列
- `crypto-intel:q:news-ingest`
- `crypto-intel:q:market-sync`
- `crypto-intel:q:strategy-eval`
- `crypto-intel:q:backtest-run`

### 3.2 幂等键（SETNX）
- `crypto-intel:idem:news:{event_uid}`
- `crypto-intel:idem:market:{venue}:{symbol}:{tf}:{ts}`
- TTL：7 天

### 3.3 状态缓存
- `crypto-intel:run:{agent}:{job_id}:status`
- TTL：24 小时

### 3.4 分布式锁
- `crypto-intel:lock:{resource}`
- TTL：15~60 秒（按资源类型）

## 4) 数据治理

- Market 数据默认来源：Bybit API
- 所有跨 Agent 事件都带 `trace_id`
- 任何 consumer 禁止更新 owner 数据（只读）
- 归档策略：
  - `market_ohlcv` 按月归档（v0.4 做分区）
  - `news_analysis_outputs` 保留 180 天热数据
