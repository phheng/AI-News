---
type: trd
version: v2
updated_bjt: 2026-03-01 00:30
---

# TRD v2

## 技术栈（当前可用）
- Backend: Node.js + TypeScript + Express
- Storage: SQLite
- Frontend: Web pages（后续可升级 React）
- Testing: Vitest + Supertest

## API 契约（MVP）
- GET /api/health
- GET/POST /api/tasks
- GET /api/recommendations
- POST /api/approvals/request
- POST /api/approvals/:id/resolve
- GET /api/approvals
- POST /api/metrics/ingest
- GET /api/metrics
- GET /api/events

## 数据与指标契约
- event: event_id, task_code, action_type, risk_tier, status, timestamp
- metrics: token_in/out/total, cost_per_run, success_rate, adoption_rate, acos_delta, roas_delta

## 非功能要求
- API 成功率 >=95%
- 报告完整率 >=98%
- token 成本占月费 <=25%
- 高风险动作可回滚可审计
