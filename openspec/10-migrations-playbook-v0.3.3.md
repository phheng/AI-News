# OpenSpec v0.3.3: DB Migration Playbook

- 状态：Draft v0.3.3
- 目标：把 v0.3.2 的 DDL 变成可执行、可回滚、可审计的迁移规范

## 1) 迁移目录与命名

主 workspace：`~/.openclaw/workspace/scripts/db/migrations/`

命名规范：
- `V{major}_{minor}_{patch}__{seq}__{slug}.sql`
- 示例：
  - `V0_3_3__001__init_news_domain.sql`
  - `V0_3_3__002__init_market_domain.sql`
  - `V0_3_3__003__init_strategy_domain.sql`
  - `V0_3_3__004__init_backtest_domain.sql`

回滚脚本：
- `R{major}_{minor}_{patch}__{seq}__{slug}.sql`
- 与 V 脚本一一对应

## 2) 迁移执行规则

- 规则 1：按文件名字典序执行
- 规则 2：每个脚本必须“幂等安全”
  - `CREATE TABLE IF NOT EXISTS`
  - `CREATE INDEX` 需先检查是否存在（或使用可兼容写法）
- 规则 3：单脚本单事务（DDL 受引擎限制时按语句级兜底）
- 规则 4：迁移执行前自动备份 schema 快照

## 3) 元数据表（migration history）

```sql
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
```

## 4) 回滚策略

- 只允许“最近 N 个迁移”的受控回滚
- 数据破坏型变更（drop/rename）必须提供：
  - 备份路径
  - 回滚恢复步骤
  - 风险说明
- 回滚前强制确认：
  - 当前活跃任务数（backtest/strategy jobs）
  - 受影响表写流量

## 5) 环境策略

- `dev`：可重置、可快速回滚
- `staging`：必须全量跑过 `validate + smoke`
- `prod`：灰度执行（先只迁移低风险域，如 news）

## 6) 验证清单

- 结构验证：表、索引、约束存在
- 数据验证：抽样查询可命中索引
- 业务验证：
  - news ingest 正常写入
  - bybit ohlcv 正常 upsert
  - strategy version 正常落库
  - backtest run 正常状态流转

## 7) 与 v0.3.2 的关系

- 本文档是 v0.3.2 DDL 的“执行规范层”
- 业务字段以 `08-storage-ddl-and-redis-v0.3.2.md` 为源头
