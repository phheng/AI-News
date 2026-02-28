---
type: trd
version: v2-unconfirmed
updated_bjt: 2026-03-01 00:40
status: unconfirmed
---

# [未确认版本] TRD v2

## 1. 技术栈
- Backend: Node.js + TypeScript + Express
- Storage: SQLite（MVP），后续可升级 PostgreSQL
- Frontend: Web Console（后续可升级 React 架构）
- Test: Vitest + Supertest

## 2. API 契约
- GET /api/health
- GET/POST /api/tasks
- GET /api/recommendations
- POST /api/approvals/request
- POST /api/approvals/:id/resolve
- GET /api/approvals
- POST /api/metrics/ingest
- GET /api/metrics
- GET /api/events

## 3. 数据契约
### 事件
- event_id, task_code, action_type, risk_tier, status, timestamp, evidence_links

### 指标
- token_in, token_out, token_total
- cost_per_run, cost_ratio
- success_rate, error_rate, p95_latency
- adoption_rate, retention_30d
- acos_delta, roas_delta, oos_delta

## 4. 风控与治理
- 默认 Observe
- 高风险必须 Approve
- Auto 仅白名单
- 强制审计记录与回滚路径

## 5. 非功能要求
- API 成功率 >=95%
- 报告完整率 >=98%
- Token 成本占月费 <=25%
- 故障可定位（run_id 全链路）

## 6. 上线门禁
- 自动化测试通过
- 风险策略生效验证通过
- 关键页面可用性验收通过
- 关键指标采集可回看
