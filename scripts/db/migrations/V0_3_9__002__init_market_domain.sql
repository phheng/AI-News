CREATE TABLE IF NOT EXISTS market_ohlcv (
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
  turnover DECIMAL(30,10) NULL,
  ingested_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_market_ohlcv (venue, symbol, timeframe, ts),
  KEY idx_market_symbol_tf_ts (symbol, timeframe, ts)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS market_features (
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

CREATE TABLE IF NOT EXISTS technical_indicator_values (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  venue VARCHAR(32) NOT NULL,
  symbol VARCHAR(32) NOT NULL,
  timeframe VARCHAR(8) NOT NULL,
  ts DATETIME(3) NOT NULL,
  indicator_name VARCHAR(64) NOT NULL,
  indicator_params VARCHAR(128) NOT NULL,
  indicator_value DECIMAL(30,10) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_indicator_point (venue, symbol, timeframe, ts, indicator_name, indicator_params),
  KEY idx_indicator_lookup (symbol, timeframe, indicator_name, ts)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
