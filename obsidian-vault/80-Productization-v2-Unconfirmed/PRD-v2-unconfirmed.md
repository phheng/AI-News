---
type: prd
version: v2-unconfirmed
updated_bjt: 2026-03-01 01:20
status: unconfirmed
---

# [未确认版本] PRD v2

## 1) Product Positioning
**Decision-first Agent Console** for North American Amazon operations.

## 2) MVP Scope
### Must Have
1. Task Hub (prioritized operational tasks)
2. Recommendation Hub (confidence + evidence + risk tier)
3. Approval Center (Observe/Approve/Auto handling)
4. Insights Dashboard (business + product + cost metrics)
5. Asset Inventory (skill/plugin/trigger/channel/experience)

### Should Have
- Segment-aware recommendation templates (Primary/Secondary)
- Weekly review output and action carry-over

### Could Have
- Public strategy template marketplace
- External AI discoverability monitoring panel

## 3) Core User Flows
### Daily Triage
Home -> top 3 recommendations -> approve/defer actions -> update status

### Controlled Execution
Recommendation -> risk classification -> approval action -> event logging -> outcome update

### Weekly Review
Insights -> KPI deltas -> accepted/rejected action analysis -> next-week plan

## 4) Functional Acceptance Criteria
- Recommendation-to-approval-to-event loop works end-to-end
- Evidence links and confidence visible for each recommendation
- Approval decisions are queryable and auditable
- Metrics update after action outcomes

## 5) UX Requirements
- Decision cards above tables
- Evidence-first detail expansion
- One-screen actionability for operator workflows
- Clear risk visualization and irreversible-action warning labels

## 6) Operational Constraints
- No high-risk auto execution in v2
- Every action requires traceable metadata
- Token-aware output strategy (concise by default, expand on demand)
