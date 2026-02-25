CREATE TABLE IF NOT EXISTS schema_migrations (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  version_tag VARCHAR(32) NOT NULL,
  seq INT NOT NULL,
  filename VARCHAR(255) NOT NULL,
  checksum_sha256 CHAR(64) NOT NULL,
  applied_by VARCHAR(64) NOT NULL,
  applied_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  status ENUM('applied','rolled_back','failed') NOT NULL,
  error_message TEXT NULL,
  UNIQUE KEY uk_migration_filename (filename),
  KEY idx_migration_version_seq (version_tag, seq)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
