CREATE TABLE IF NOT EXISTS strategy_specs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  strategy_id VARCHAR(64) NOT NULL,
  name VARCHAR(128) NOT NULL,
  template_type VARCHAR(64) NOT NULL,
  owner_agent_id VARCHAR(64) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_strategy_id (strategy_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS strategy_versions (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  strategy_id VARCHAR(64) NOT NULL,
  version INT NOT NULL,
  spec_json JSON NOT NULL,
  risk_json JSON NOT NULL,
  anti_liquidation_json JSON NOT NULL,
  effective_window_start DATETIME(3) NULL,
  effective_window_end DATETIME(3) NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uk_strategy_ver (strategy_id, version),
  KEY idx_strategy_ver_strategy (strategy_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS strategy_validation_runs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  strategy_id VARCHAR(64) NOT NULL,
  strategy_version INT NOT NULL,
  validation_type ENUM('grid_search','parameter_plateau','stress') NOT NULL,
  status ENUM('queued','running','success','failed') NOT NULL,
  summary_json JSON NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_strategy_validation_lookup (strategy_id, strategy_version, validation_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
