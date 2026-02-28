## ADDED Requirements

### Requirement: Architecture SHALL be OpenClaw-native
The system SHALL define orchestration around OpenClaw primitives (agent, workspace, cron, subagent) rather than a generic controller-first backend.

#### Scenario: Orchestration mapping is complete
- GIVEN the architecture document
- WHEN reviewed by engineering
- THEN every major workflow maps to OpenClaw runtime primitives

### Requirement: Multi-agent role boundaries MUST be explicit
The design MUST define responsibilities and handoffs for `henk`, `Atlas`, and `Pulse` with clear decision ownership.

#### Scenario: Role conflict check
- GIVEN a task involving product, engineering, and marketing
- WHEN routing logic is evaluated
- THEN exactly one role is primary owner and escalation path is defined

### Requirement: Execution safety SHALL use risk tiers
The system SHALL classify actions into Observe/Approve/Auto with thresholds and audit logs.

#### Scenario: High-risk action
- GIVEN a high-risk commercial action (price/ads major change)
- WHEN an agent requests execution
- THEN the system requires human approval and records audit metadata

### Requirement: Architecture MUST include metrics contracts
The design MUST include data contracts for outcome, reliability, and cost metrics including token usage.

#### Scenario: Metrics compatibility review
- GIVEN the metric dictionary
- WHEN analytics integration is designed
- THEN each KPI has formula, source event, aggregation cadence, and threshold

### Requirement: UI SHALL be decision-first
The UI architecture SHALL prioritize “what to do now” actions and evidence traceability.

#### Scenario: Operator workflow
- GIVEN an operator opening dashboard
- WHEN viewing daily state
- THEN top recommendations, confidence, sources, and approval actions are visible in one screen flow

### Requirement: Design package SHALL be implementation-ready
The change artifacts SHALL provide enough detail for Atlas to implement without redefining architecture.

#### Scenario: Handoff readiness
- GIVEN design artifacts (proposal/spec/design/tasks)
- WHEN Atlas starts execution planning
- THEN no architecture-level ambiguity blocks implementation kickoff
