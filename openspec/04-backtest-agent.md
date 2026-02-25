# OpenSpec: Backtest Agent

- **状态**：Draft v0.3.8
- **目标 workspace（开发目录）**：`~/.openclaw/workspace-crypto-intel-backtest-agent`
- **技术栈**：Python + uv

## 1. 目标

消费策略定义与历史数据，执行可复现回测；并基于实时价格进行 paper trading，输出可比较的评估结果并回传给 Strategy Agent 形成闭环优化。

## 2. 范围

### In Scope
- 单策略回测
- 批量参数回测
- 交易成本/滑点建模（基础版）
- 基于实时价格的 paper trading（按策略生效周期运行）
- 回测 + paper trading 结果汇总与排名
- 将周期结果回传 Strategy Agent

### Out of Scope（v0）
- 实盘执行
- 复杂组合优化器

## 3. 输入/输出

### 输入
- `strategy_spec/*.yaml`
- 历史行情切片

### 输出
- `backtests/<run_id>/report.json`
- `backtests/<run_id>/trades.csv`
- `backtests/<run_id>/equity_curve.csv`
- `paper_trading/<run_id>/paper_report.json`
- `paper_trading/<run_id>/paper_trades.csv`

## 4. 指标（最低集）

- 总收益率
- 年化收益率
- 最大回撤
- 夏普比率
- 胜率/盈亏比
- 交易次数

## 5. 非功能要求

- 同输入必须同输出（确定性）
- 回测参数与结果可追溯
- 支持失败重跑

## 6. 验收标准

- 单策略回测可在可接受时间内完成
- 多策略结果可排序比较
- 前端可读取报告并展示关键指标
\n## 7. 运维与命名约束\n
- workspace：`~/.openclaw/workspace-crypto-intel-backtest-agent`
- 定时任务前缀：`crypto-intel: backtest`
- MySQL 主表（v0 草案）：`backtest_runs`, `backtest_metrics`, `backtest_trades`
- Redis（v0 草案）：用于回测任务队列、运行状态缓存、并发控制锁
