# OpenSpec: Strategy Design Agent

- **状态**：Draft v0.3.8
- **目标 workspace（开发目录）**：`~/.openclaw/workspace-crypto-intel-strategy-agent`
- **技术栈**：Python + uv

## 1. 目标

将新闻（含分析结果）与行情融合，生成可回测的策略定义与信号逻辑；消费 Backtest/Paper Trading 周期结果并通过 OpenClaw 能力参与策略优化决策（不单独引入外部模型），并作为 OpenViking 记忆系统的主要承载 Agent。

## 2. 范围

### In Scope
- 策略模板管理（趋势/均值回归/事件驱动）
- 参数空间定义
- 风控约束定义（仓位、止损、最大回撤阈值）
- 生成标准化策略配置（供 Backtest Agent）
- OpenViking 记忆读写（L0/L1/L2 + P 标签），用于策略上下文持续化
- 复用旧 `workspace-crypto-trading-agent` 中可迁移的策略/指标/任务编排设计
- 消费回测 + paper trading 结果，执行自主策略优化（OpenClaw 交互式优化）
- 支持动态更新节奏：按策略生效窗口/失效窗口触发，而非固定时点机械更新

### Out of Scope（v0）
- 自动上线实盘
- 强化学习闭环

## 3. 输入/输出

### 输入
- News Agent 事件流
- Market Data Agent 历史行情
- 用户策略偏好/约束

### 输出
- `strategy_spec/*.yaml`
- `signals_preview/*.json`
- `strategy_optimization/*.json`（含调参与更新建议）

## 4. 接口契约

- 向 Backtest Agent 发送 `strategy_spec`
- 接收 Backtest Agent 的回测 + paper trading 周期结果
- 生成优化后的策略版本并回推 Backtest Agent 进入下一轮验证
- 在“策略完成设计 -> 回测 -> paper trading”完整周期结束后，通过 Telegram DM 推送摘要给你

## 5. 非功能要求

- 每个策略定义可复现实验
- 参数与版本可追踪
- 支持回滚到旧策略定义

## 6. 验收标准

- 至少 3 种模板能产出合法策略定义
- Backtest Agent 可无人工修补直接消费
- 输出包含必要风控参数
\n## 7. 运维与命名约束\n
- workspace：`~/.openclaw/workspace-crypto-intel-strategy-agent`
- 定时任务前缀：`crypto-intel: strategy`
- MySQL 主表（v0 草案）：`strategy_specs`, `strategy_versions`
- Redis（v0 草案）：用于信号计算缓存、参数搜索任务编排
