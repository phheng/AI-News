---
type: architecture
version: v2-unconfirmed
updated_bjt: 2026-03-01 01:20
status: unconfirmed
---

# [未确认版本] Architecture v2（North America, OpenClaw-native）

## 1) Architecture Objective
Build a production-feasible agent platform for North American Amazon operators with:
- Decision-first execution
- Human-governed risk control
- Measurable business + cost outcomes

## 2) Explicit System Boundary
### In Scope
- Web operations console + IM interaction
- Recommendation + approval + execution feedback loop
- Observability for outcome/reliability/token-cost
- Asset governance (skills/plugins/triggers/channels/experience)

### Out of Scope (v2)
- Full autonomous high-risk execution
- Enterprise-grade multi-tenant IAM/SSO
- Cross-cloud HA deployment automation

## 3) Layered Architecture
1. **Interaction Layer**
   - Web UI (operator console)
   - Discord/IM for async actions and alerts
2. **Orchestration Layer**
   - OpenClaw agent/workspace/cron/subagent
   - Task routing and stage gates
3. **Capability Layer**
   - Ads Intelligence
   - Stock Risk
   - Competitor Pulse
   - News/Market Watch
   - Asset Ops (EvoMap/OpenClawMP)
4. **Data Layer**
   - Operational DB (tasks/recommendations/approvals/events/metrics)
   - Knowledge docs (Obsidian)
5. **Governance Layer**
   - Observe/Approve/Auto policy
   - Audit + rollback
   - Threshold gate checks

## 4) Role Architecture
- **henk (Control Plane Owner)**
  - architecture, ICP, sequencing, decision governance
- **Atlas (Build Plane Owner)**
  - feature implementation/testing after architecture sign-off
- **Pulse (Growth Plane Owner)**
  - SEO/distribution/discoverability execution + market feedback

## 5) Core Runtime Flows
### A. Decision Flow
Signal -> Recommendation -> Risk tiering -> Approve/Auto decision -> Action result -> Metric/event update

### B. Governance Flow
Action request -> threshold check -> policy gate -> audit record -> rollback path if failed

### C. Product Learning Flow
Usage telemetry + business delta + token cost -> weekly review -> strategy adjustment

## 6) Risk & Control Model
- Default execution: **Observe**
- Medium/high-risk: **Approve required**
- Auto only for low-risk white-listed actions
- Mandatory execution metadata:
  - `run_id`
  - `operator/agent`
  - `evidence_links`
  - `risk_tier`
  - `rollback_ref`

## 7) Environment Topology (Current)
- Design/docs workspace: `/root/.openclaw/workspace`
- Build workspace: `/root/.openclaw/workspace-amazon-agent-platform`
- Completed archive: `/root/.openclaw/projects/completed/amazon-agent-platform-v1-tested`

## 8) Architecture Acceptance Gates
- API reliability >= 95%
- Recommendation evidence coverage >= 98%
- Token cost ratio <= 25% of monthly fee target
- High-risk actions are fully auditable and reversible

## 9) Evolution Path
- Phase 1: single-tool value proof (speed + accuracy)
- Phase 2: multi-tool orchestrated workflows
- Phase 3: proactive personalized decision co-pilot
