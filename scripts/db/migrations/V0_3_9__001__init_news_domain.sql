CREATE TABLE IF NOT EXISTS news_events (
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

CREATE TABLE IF NOT EXISTS news_event_tags (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  event_uid VARCHAR(128) NOT NULL,
  tag_type ENUM('symbol','topic','risk') NOT NULL,
  tag_value VARCHAR(128) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_news_tags_event_uid (event_uid),
  KEY idx_news_tags_type_value (tag_type, tag_value)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS news_analysis_outputs (
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

CREATE TABLE IF NOT EXISTS news_alerts (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  event_uid VARCHAR(128) NOT NULL,
  alert_level ENUM('urgent','high','normal') NOT NULL,
  alert_reason VARCHAR(255) NOT NULL,
  created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY idx_news_alerts_event_uid (event_uid),
  KEY idx_news_alerts_level_created (alert_level, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
