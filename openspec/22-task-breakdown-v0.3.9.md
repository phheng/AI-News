# OpenSpec v0.3.9: Execution Task Breakdown

- 状态：Draft v0.3.9
- 目标：把 v0.3.8 闭环落成可执行任务清单

## 1. 事件流实施

- [ ] 1.1 创建 Redis Streams topics 与 consumer groups
- [ ] 1.2 落地通用事件头封装与 trace 透传
- [ ] 1.3 实现 event_id 幂等去重与 DLQ

## 2. Paper Trading 闭环

- [ ] 2.1 Backtest Agent 增加实时 paper trading runner
- [ ] 2.2 实现 `paper.window.closed` 事件发布
- [ ] 2.3 持久化 paper_trading_runs / metrics

## 3. Strategy 动态优化

- [ ] 3.1 实现窗口触发器（effectiveness window + degradation threshold）
- [ ] 3.2 实现 OpenClaw 驱动优化流程
- [ ] 3.3 产出 `strategy.optimized` 事件与版本落库

## 4. Telegram 交付

- [ ] 4.1 实现 `strategy_cycle_summary_v1` 模板渲染
- [ ] 4.2 接入 notification topic -> telegram sender
- [ ] 4.3 幂等发送与失败重试

## 5. 联调与验收

- [ ] 5.1 E2E: design -> backtest -> paper -> optimize -> DM
- [ ] 5.2 压测免费 API 限流场景（Bybit + Binance fallback）
- [ ] 5.3 验证 3 个策略周期连续稳定运行
