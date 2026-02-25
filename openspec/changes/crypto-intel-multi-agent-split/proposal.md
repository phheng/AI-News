## Why

现有 `workspace-crypto-trading-agent` 职责耦合，导致数据、策略、回测、展示混在一起，迭代和扩展成本高。需要拆分为四个独立 Agent，并在统一规范下实现数据流通、前端聚合、事件驱动闭环优化和可部署性。

## What Changes

- 将旧 crypto agent 拆分为四个独立 Agent：
  - News & Sentiment Agent
  - Market Data & Indicators Agent
  - Strategy Design Agent
  - Backtest Agent（含实时价格 paper trading + 防爆仓校验）
- 统一命名前缀 `crypto-intel`（workspace、agentId、cron、stream、command）
- 数据底座统一为 MySQL + Redis（场景化最小共享）
- API 统一为 FastAPI，前端只调用主 workspace 的 gateway
- 前端采用多标签页（React + Ant Design + Tailwind，Apple 风）
- 图表策略：TradingView（价格与技术指标同图，默认 15m/1h/4h/1d + EMA/Bollinger/RSI/MACD/Volume）+ ECharts（其他分析图）
- 引入 Redis Streams 事件流：设计 -> 回测 -> paper -> 优化 -> 通知
- 重点在 Strategy Agent 引入 OpenViking 记忆分层（L0/L1/L2 + P0/P1/P2）
- Strategy Agent 使用 OpenClaw 参与优化推理（不引入独立外部大模型）
- 策略设计与评估必须执行防爆仓约束（设计侧约束 + 回测/纸交易侧校验）
- 市场数据 Bybit 为主，Binance 兜底
- 完整策略周期结束自动 Telegram DM 推送
- 全服务支持 Docker 镜像化与 compose 编排

## Capabilities

### New Capabilities
- `crypto-intel-system-architecture`: 四 Agent 体系、闭环编排与通知
- `crypto-intel-data-contracts`: 跨 Agent 数据/事件契约（MySQL/Redis Streams）
- `crypto-intel-api-gateway`: FastAPI 聚合 API + 通知派发入口
- `crypto-intel-strategy-memory`: Strategy Agent 的 OpenViking 记忆与动态优化
- `crypto-intel-docker-deployment`: 镜像化与 Docker Compose 部署规范
- `crypto-intel-frontend-dashboard`: 前端多标签页与图表策略

### Modified Capabilities
- 无（旧能力以拆分迁移方式实现，不做原地改造）

## Impact

- 影响代码仓结构：新增四个 agent workspace + 主 workspace 的 gateway/frontend
- 影响运行方式：由单体脚本任务改为多服务 + 事件流协作
- 影响数据层：引入标准化 schema、迁移体系、幂等与审计规则
- 影响决策层：引入 paper trading 反馈驱动的策略动态优化
- 影响交付层：完整生命周期结果自动 Telegram DM 推送
- 影响部署层：服务镜像化、compose 分层部署、健康检查/回滚流程