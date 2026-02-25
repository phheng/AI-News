# OpenSpec v0.3.9: Telegram DM Template Contract

- 状态：Draft v0.3.9
- 目标：统一完整策略周期结束后的 DM 推送内容

## 1) 模板 ID

- `strategy_cycle_summary_v1`

## 2) 字段

- `strategy_id`
- `strategy_version`
- `backtest_metrics`（return, mdd, sharpe）
- `paper_metrics`（pnl, mdd, win_rate, trade_count）
- `optimization_action`（none|retune|replace）
- `next_window`
- `risk_notice`

## 3) 文案草案

```text
[Strategy Cycle Completed] {strategy_id} v{strategy_version}

Backtest: Return {bt_return}, MDD {bt_mdd}, Sharpe {bt_sharpe}
Paper: PnL {p_pnl}, MDD {p_mdd}, WinRate {p_wr}, Trades {p_trades}
Optimization: {optimization_action}
Next Window: {next_window}
Risk: {risk_notice}
```

## 4) 发送规则

- 仅在完整周期结束后发送
- 同一 `strategy_id + version + window_end` 只发一次
- 失败重试最多 3 次，仍失败写告警事件
