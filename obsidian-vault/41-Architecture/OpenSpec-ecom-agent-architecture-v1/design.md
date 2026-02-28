# Design: E-commerce Agent Platform Architecture v1 (Design-only)

## 1. Context
This design transforms existing top-level strategy into a development-ready architecture package.

Role model:
- **henk**: architecture + ICP + decision governance + stakeholder dialog
- **Atlas**: implementation execution after architecture sign-off
- **Pulse**: SEO/content distribution and external growth operations

## 2. Architecture Overview

### 2.1 Logical layers
1. **Interaction Layer**
   - IM surfaces (Discord initially)
   - Future web console for approvals and analytics
2. **Orchestration Layer (OpenClaw-native)**
   - Agent turns
   - Cron schedules
   - Subagent jobs (when runtime allows)
3. **Capability Layer**
   - 101-A news intelligence
   - 102-A ICP intelligence
   - 103-A governance/metrics intelligence
   - 105-A market asset operations (EvoMap/OpenClawMP)
4. **Data & Memory Layer**
   - Obsidian markdown knowledge base
   - Task index + shared logs
   - Event/metric contracts for analytics backend
5. **Governance Layer**
   - Observe/Approve/Auto execution policy
   - Audit trail and rollback policies

### 2.2 Core data contracts

#### Event contract
- `event_id`
- `task_code`
- `agent_role`
- `action_type`
- `risk_tier`
- `status`
- `timestamp`
- `evidence_links[]`

#### Metrics contract
- Outcome: ACOS delta, ROAS delta, OOS delta, saved_hours
- Reliability: success_rate, error_rate, p95_latency
- Cost: token_in, token_out, token_total, cost_per_run, cost_ratio

## 3. Workflow design

### 3.1 Strategic workflow (henk-owned)
1. Intake user objective
2. Map to task code (101/102/103/105/106)
3. Decide: direct execution vs delegated execution
4. Run review gate before write/push (except explicit auto-write tasks)
5. Publish decision log and next-step queue

### 3.2 Delivery workflow (Atlas-owned after sign-off)
1. Consume architecture package
2. Implement module-by-module
3. Run tests by contract
4. Report results + unresolved risks to henk

### 3.3 Growth workflow (Pulse-owned)
1. Convert architecture and ICP outputs into distribution assets
2. Run SEO/content cadence
3. Track discoverability metrics (AI mention/citation/lead signals)
4. Feed market insights back to henk

## 4. UI interaction architecture (reference-inspired)

Note: tryclair/scout page content was minimally accessible from current environment, so this section uses interaction principles rather than pixel-level cloning.

### 4.1 Principles
- Decision-first cards (priority actions)
- Evidence-first expansion (source + confidence + timestamp)
- One-click escalation (Approve / Reject / Defer)
- Clear daily/weekly operator modes

### 4.2 Information architecture
- **Home**: Today’s priorities, blockers, approvals
- **Tasks**: 101/102/103/105/106 status by SLA
- **Insights**: ICP, market, AI discoverability
- **Governance**: risk policies, audit logs, rollback events
- **Assets**: Skill/Plugin/Trigger/Channel/Experience inventory

## 5. Security and risk model
- Default mode: Observe
- Approve required for medium/high-risk actions
- Human-only for threshold-breaking actions
- Mandatory evidence links for action proposals
- Immutable audit records for executed actions

## 6. Delivery phases (design to build)
- **Phase A**: finalize contracts and review gate
- **Phase B**: implementation planning handoff to Atlas
- **Phase C**: pilot run with metric instrumentation
- **Phase D**: iterate based on outcome and cost efficiency

## 7. Open questions
1. Persistent subagent thread support in current Discord config
2. Unified auth path for external tools (Memos/Brave/OpenClawMP)
3. Minimal web console scope before broader UI build
