# OpenSpec v0.3.6: Implementation Roadmap（实施路线图）

- 状态：Draft v0.3.6
- 目标：把 v0.3.1 ~ v0.3.5 的设计收敛成可执行步骤

## Phase 0: 冻结与基线（已完成）

- [x] 暂停旧 crypto 定时任务
- [x] 明确四 Agent 拆分目标与命名前缀
- [x] 明确主 workspace / 子 workspace 边界

## Phase 1: 工程骨架初始化

1. 创建四个 workspace 目录
2. 各 workspace 初始化 Python + uv 工程
3. 主 workspace 初始化：
   - `apps/api-gateway`（FastAPI）
   - `apps/frontend`（React + antd + Tailwind）
4. 初始化共享脚本目录：`scripts/db`, `scripts/redis`, `scripts/devops`

**验收**：
- 五个代码服务目录结构符合 `09-workspace-bootstrap-v0.3.2.md`

## Phase 2: 存储与迁移落地

1. 建立 migration 目录与版本命名
2. 按域拆分 DDL（news/market/strategy/backtest）
3. 创建 `schema_migrations` 元数据表
4. 在 dev 环境执行全量 migrate + 基础回滚演练

**验收**：
- MySQL 表结构与 `08-storage-ddl-and-redis-v0.3.2.md` 一致
- 回滚脚本至少演练 1 次成功

## Phase 3: Agent 最小可运行 API（MVP）

1. News Agent：`/v1/news/ingest`, `/v1/news/events`, `/v1/news/analysis`
2. Market Agent：`/v1/market/sync`, `/v1/market/ohlcv`
3. Strategy Agent：`/v1/strategy/generate`, memory query/write
4. Backtest Agent：`/v1/backtest/run`, run/metrics/artifacts 查询
5. Gateway：`/v1/dashboard/*` 聚合接口

**验收**：
- 全部服务 `healthz/readyz/version` 可用
- 前端可通过 gateway 拿到 mock/真实数据

## Phase 4: 关键能力接入

1. Bybit 映射契约实现（按 `11-bybit-field-mapping-v0.3.3.md`）
2. 新闻分析处理链路接入（impact/confidence）
3. Strategy OpenViking 记忆层接入（L0/L1/L2 + P 标签）
4. Redis 队列与幂等键接入

**验收**：
- Bybit 数据可稳定入库并幂等更新
- 新闻分析结果可被策略生成接口消费
- Strategy 记忆查询可命中历史上下文

## Phase 5: 前端多标签页与设计系统

1. antd + Apple 风主题 token 落地
2. 6 个标签页页面壳完成
3. 关键组件封装：PanelCard / MetricStat / 状态态组件
4. 数据刷新与错误态处理

**验收**：
- 页面完整展示 Overview + 4 Agent + System
- 视觉风格统一，交互可用

## Phase 6: Docker 化与部署联调

1. 六服务 Dockerfile 按模板实现
2. compose 基础 + dev + prod 三层文件落地
3. 配置注入与 secrets 规范检查
4. 联调 smoke：ingest -> strategy -> backtest -> frontend

**验收**：
- `docker compose` 一键拉起（dev）
- 生产模板可按固定 tag 部署

## Phase 7: 旧系统退役

1. 功能映射核对（旧->新）
2. 观察窗运行（建议 3~7 天）
3. 删除旧 workspace 与旧 cron

**验收**：
- 新系统覆盖旧能力并稳定运行
- 旧资源安全下线
