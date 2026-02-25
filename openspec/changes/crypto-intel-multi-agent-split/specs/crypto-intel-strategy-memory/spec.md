## ADDED Requirements

### Requirement: Strategy-first OpenViking memory model
The system SHALL implement OpenViking L0/L1/L2 memory loading and P0/P1/P2 lifecycle management primarily in strategy agent.

#### Scenario: Context retrieval for strategy generation
- **WHEN** strategy agent needs historical context
- **THEN** it loads L0 first and escalates to L1/L2 only when needed

### Requirement: Shared summary logging
The system SHALL append concise cross-agent conclusions to shared memory logs.

#### Scenario: Important task completion
- **WHEN** an agent completes a key task
- **THEN** it appends a short conclusion entry to shared memory log

### Requirement: Memory lifecycle automation
The system SHALL enforce lifecycle transitions for P1/P2 memory records via scheduled cleanup/archive.

#### Scenario: Expired temporary memory
- **WHEN** a P2 record exceeds retention window
- **THEN** it is archived or cleaned according to policy

### Requirement: Built-in strategy validation toolkit
The strategy service SHALL provide grid search and parameter-plateau validation workflows before strategy promotion.

#### Scenario: Candidate strategy validation
- **WHEN** a candidate strategy is generated
- **THEN** grid search and plateau analysis results are produced for pass/fail gating

### Requirement: OpenClaw-mediated strategy optimization
The strategy service SHALL use OpenClaw interactions as the optimization intelligence path instead of introducing a separate external LLM stack.

#### Scenario: Optimization decision required
- **WHEN** backtest/paper-trading feedback indicates strategy adjustment
- **THEN** strategy optimization is executed through OpenClaw-driven reasoning with memory evidence

### Requirement: Dynamic strategy update cadence
The strategy service SHALL schedule updates based on strategy effectiveness windows and trigger conditions, not fixed mechanical time slots.

#### Scenario: Window-based update trigger
- **WHEN** a strategy nears end of its effective window or degrades by threshold
- **THEN** optimization/update pipeline is triggered dynamically
