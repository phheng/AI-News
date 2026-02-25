## 0. 命名统一基线

- [x] 0.1 定稿全局统一前缀：`crypto-intel` / `crypto-intel:`
- [ ] 0.2 校对主 workspace 与各 Agent workspace 的 command/cron/stream/service 命名一致

## 1. 文档对齐与基线

- [x] 1.1 校对 proposal/design/tasks 与 v0.3.9 一致性
- [x] 1.2 校对 change specs 与 18~22 文档一致性
- [x] 1.3 运行 OpenSpec validate 并修正格式问题

## 2. 工程骨架初始化

- [x] 2.1 创建四个 agent workspace 目录
- [x] 2.2 初始化四个 Python + uv 项目骨架
- [x] 2.3 在主 workspace 初始化 `apps/api-gateway` 与 `apps/frontend`
- [x] 2.4 初始化 `scripts/db` `scripts/redis` `scripts/devops`

## 3. 存储与迁移

- [x] 3.1 建立 migration 目录与命名体系（V/R）
- [x] 3.2 按域落地 news/market/strategy/backtest DDL 脚本
- [x] 3.3 增加 paper trading 相关表（runs/metrics）
- [x] 3.4 创建并验证 `schema_migrations` 元数据表
- [x] 3.5 演练一次受控回滚

## 4. 事件流与契约

- [x] 4.1 创建 Redis Streams topics 与 consumer groups
- [x] 4.2 落地通用事件头（event_id/trace_id/version）
- [x] 4.3 落地幂等消费与 DLQ 机制
- [x] 4.4 落地 `paper.window.closed` / `strategy.optimized` / `notification.telegram` payload

## 5. Agent API MVP

- [x] 5.1 落地 News & Sentiment Agent API（含 urgent news）
- [x] 5.2 落地 Market & Indicators Agent API（Bybit 主链路 + Binance fallback）
- [x] 5.3 落地 Strategy Agent API（generate/memory/query/optimize）
- [x] 5.4 落地 Backtest Agent API（backtest + realtime paper trading + 防爆仓评估字段）
- [x] 5.6 接入成熟回测引擎（MVP 先接 backtrader）
- [x] 5.5 落地 Gateway 聚合 API（dashboard tabs + notification dispatch）

## 6. 关键能力接入

- [x] 6.1 接入新闻情绪与影响分析
- [x] 6.2 接入技术指标计算与指标看板数据
- [ ] 6.3 接入 Strategy OpenViking（L0/L1/L2 + P 标签）
- [x] 6.4 接入 Strategy 动态触发优化（窗口+阈值+冷却期）
- [ ] 6.5 接入 Grid Search + 策略平原验证
- [ ] 6.6 接入防爆仓约束生成与回测/纸交易防爆仓校验

## 7. 前端实现

- [x] 7.1 搭建多标签页框架（Overview/News/Market/Strategy/Backtest/System）
- [x] 7.2 集成 TradingView（价格与技术指标同图）
- [x] 7.3 配置默认周期与指标（15m/1h/4h/1d + EMA/Bollinger/RSI/MACD/Volume）
- [x] 7.4 集成 ECharts（其他分析图）
- [x] 7.5 统一 antd + Apple 风 token 与状态态组件


## 8. 通知与交付

- [x] 8.1 实现 Telegram DM 模板 `strategy_cycle_summary_v1`
- [x] 8.2 实现同一周期幂等发送（strategy+version+window_end）
- [x] 8.3 实现失败重试与告警事件

## 9. 部署与联调

- [ ] 9.1 完成各服务 Dockerfile
- [ ] 9.2 完成 compose 基础/dev/prod 文件
- [ ] 9.3 完成 E2E smoke（design -> backtest -> paper -> optimize -> DM）
- [ ] 9.4 压测免费 API 限流场景

## 10. 迁移收尾

- [ ] 10.1 对照旧系统能力做覆盖验收
- [ ] 10.2 运行 3~7 天观察窗
- [ ] 10.3 删除旧 workspace 与旧 cron（最终下线）