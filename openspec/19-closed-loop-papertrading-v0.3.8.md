# OpenSpec v0.3.8: Closed-loop Strategy with Paper Trading

- 状态：Draft v0.3.8
- 目标：形成“设计 -> 回测 -> paper trading -> 优化 -> 通知”的完整闭环

## 1) 生命周期流程

1. Strategy Agent 生成策略版本 `S.vN`
2. Backtest Agent 执行历史回测
3. Backtest Agent 按策略定义周期执行实时价格 paper trading
4. 结果（回测 + paper）回传 Strategy Agent
5. Strategy Agent 结合 OpenViking 记忆 + OpenClaw 交互进行优化
6. 完整周期结果通过 Telegram DM 推送

## 2) Paper Trading 关键规则

- 使用实时价格流驱动模拟成交
- 模拟成本模型与回测成本模型保持一致或可映射
- 支持按策略周期窗口结束产出阶段性报告
- 强制执行防爆仓检查（保证金安全阈值、杠杆上限、强平前降风险动作）
- 结果分为：执行质量、收益质量、稳健性质量（含爆仓风险维度）

## 3) 结果回传契约（草案）

- `paper_trading_runs`
  - `run_id`, `strategy_id`, `strategy_version`, `window_start`, `window_end`, `status`
- `paper_trading_metrics`
  - `run_id`, `pnl`, `max_drawdown`, `win_rate`, `trade_count`, `slippage_impact`
- `paper_trading_events`
  - 异步流事件：`paper.window.closed`, `paper.alert.risk`, `paper.run.completed`

## 4) 动态优化触发器（Strategy Agent）

- 周期触发：策略生效窗口结束前/后
- 性能触发：
  - 连续 N 窗口低于阈值
  - 回撤超过阈值
  - 市场结构变化（波动/相关性 regime shift）

## 5) OpenClaw 交互定位

- 不引入独立模型服务
- 通过 OpenClaw 进行策略优化推理与动作编排
- OpenViking 提供证据链记忆（历史假设、参数、失败案例）

## 6) Telegram DM 交付模板（草案）

- 标题：`[Strategy Cycle Completed] <strategy_id> v<version>`
- 内容：
  - Backtest 核心指标
  - Paper trading 核心指标
  - 是否触发优化 / 新版本号
  - 下一观察窗口与风险提示
