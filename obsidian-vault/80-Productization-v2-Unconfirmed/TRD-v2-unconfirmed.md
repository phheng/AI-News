---
type: trd
version: v2.1-unconfirmed
updated_bjt: 2026-03-01 00:55
status: unconfirmed
---

# [未确认版本] TRD v2.1

## 1) 技术路线
- Backend: Node.js + TypeScript
- Orchestration: OpenClaw runtime (agent/workspace/cron/subagent)
- Storage: SQLite (MVP) -> PostgreSQL (later)
- Test: contract + integration + smoke

## 2) 数据源能力（MVP抽象）
- 垂类选品数据源（趋势、竞品、平台信号）
- 扩展源：browser automation / plugin adapters
- 输出：统一结构化候选对象

## 3) 任务执行模型
User intent -> Planner -> Tool calls -> Scoring -> Insight rendering -> Action recommendation

## 4) 结构化输出契约
- request_id
- query_intent
- candidate_items[]
- score_breakdown
- recommendation
- confidence
- evidence_links[]
- generated_at

## 5) 关键API（MVP）
- `/api/tasks`
- `/api/recommendations`
- `/api/approvals/*`
- `/api/metrics/*`
- `/api/events`

## 6) 性能与可靠性指标
- task success rate >= 95%
- response latency target: 10s class for common task
- answer accuracy target: >80% (label-based)

## 7) 安全与治理
- Observe/Approve/Auto
- 审计日志必填字段
- 高风险动作回滚路径强制存在

## 8) 实施顺序
1. 单工具稳定链路
2. 多工具编排
3. 主动洞察引擎
