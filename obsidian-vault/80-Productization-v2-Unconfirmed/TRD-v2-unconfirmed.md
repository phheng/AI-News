---
type: trd
version: v2-unconfirmed
updated_bjt: 2026-03-01 01:20
status: unconfirmed
---

# [未确认版本] TRD v2

## 1) Technical Baseline
- Backend: Node.js + TypeScript + Express
- Storage: SQLite (MVP baseline), PostgreSQL-ready schema path
- Frontend: Web console (evolvable to React component architecture)
- Test stack: Vitest + Supertest

## 2) API Contract (MVP)
- `GET /api/health`
- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/recommendations`
- `POST /api/approvals/request`
- `POST /api/approvals/:id/resolve`
- `GET /api/approvals`
- `POST /api/metrics/ingest`
- `GET /api/metrics`
- `GET /api/events`

## 3) Data Contracts
### Event schema
- `event_id`
- `task_code`
- `action_type`
- `risk_tier`
- `status`
- `timestamp`
- `evidence_links`
- `run_id`

### Metric schema
- Cost: `token_in`, `token_out`, `token_total`, `cost_per_run`, `cost_ratio`
- Reliability: `success_rate`, `error_rate`, `p95_latency`
- Product: `adoption_rate`, `retention_30d`, `pilot_to_paid`
- Business: `acos_delta`, `roas_delta`, `oos_delta`, `saved_hours`

## 4) Governance-by-Design
- Default execution mode: Observe
- Approval mandatory for medium/high-risk actions
- Auto execution only for explicit low-risk whitelist
- Rollback references required before execution for risky actions

## 5) Non-Functional Requirements
- API success rate >= 95%
- Report completeness >= 98%
- Token cost ratio <= 25%
- Full traceability for all executed actions

## 6) Test Strategy
- Contract tests for core endpoints
- Regression tests for approval flow and metrics ingest
- Smoke checks for UI route availability
- Failure-path tests for invalid approvals and missing evidence

## 7) Release Gates
- Tests green
- Approval policy enforcement verified
- Metrics ingestion + dashboard visibility verified
- Audit events generated for all resolved approvals
