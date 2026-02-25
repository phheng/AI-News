CREATE TABLE IF NOT EXISTS backtest_runs (
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

CREATE TABLE IF NOT EXISTS backtest_metrics (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  run_id VARCHAR(64) NOT NULL,
  total_return DECIMAL(12,6) NOT NULL,
  annual_return DECIMAL(12,6) NOT NULL,
  max_drawdown DECIMAL(12,6) NOT NULL,
  sharpe DECIMAL(12,6) NULL,
  win_rate DECIMAL(12,6) NULL,
  trade_count INT NOT NULL,
  anti_liquidation_score DECIMAL(12,6) NULL,
  liquidation_risk_events INT NOT NULL DEFAULT 0,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_backtest_metrics_run_id (run_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS paper_trading_runs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  run_id VARCHAR(64) NOT NULL,
  strategy_id VARCHAR(64) NOT NULL,
  strategy_version INT NOT NULL,
  window_start DATETIME(3) NOT NULL,
  window_end DATETIME(3) NOT NULL,
  status ENUM('queued','running','success','failed','canceled') NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_paper_run_id (run_id),
  KEY idx_paper_strategy_window (strategy_id, strategy_version, window_end)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS paper_trading_metrics (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  run_id VARCHAR(64) NOT NULL,
  pnl DECIMAL(12,6) NOT NULL,
  max_drawdown DECIMAL(12,6) NOT NULL,
  win_rate DECIMAL(12,6) NULL,
  trade_count INT NOT NULL,
  slippage_impact DECIMAL(12,6) NULL,
  anti_liquidation_score DECIMAL(12,6) NULL,
  liquidation_risk_events INT NOT NULL DEFAULT 0,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_paper_metrics_run_id (run_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
