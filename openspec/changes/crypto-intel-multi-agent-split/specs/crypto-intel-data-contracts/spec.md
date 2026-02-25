## ADDED Requirements

### Requirement: Scenario-based data sharing boundaries
The system SHALL share data between agents by scenario-specific contracts with explicit owner and consumer roles.

#### Scenario: Consumer reads owner data
- **WHEN** an agent consumes cross-agent data
- **THEN** it reads from owner-defined tables/interfaces and does not mutate owner-owned records

### Requirement: MySQL as persistence backbone
The system SHALL persist core domains (news, market, strategy, backtest) in MySQL with versioned migration rules.

#### Scenario: Domain tables exist after migration
- **WHEN** migrations are applied
- **THEN** required domain tables are created and queryable

### Requirement: Redis for queueing and idempotency
The system SHALL use Redis Streams for event queues, plus idempotency keys, runtime state cache, and distributed locks.

#### Scenario: Duplicate event ingestion
- **WHEN** the same business event is retried
- **THEN** idempotency keys prevent duplicate writes

### Requirement: Hybrid integration channels
The system SHALL support table persistence, API query/control, and message-stream event propagation between agents.

#### Scenario: Cross-agent async analysis trigger
- **WHEN** market-indicators agent publishes a new indicator snapshot
- **THEN** news-sentiment and strategy agents can consume the event stream without polling only from tables

### Requirement: Paper-trading feedback contracts
The system SHALL define persistent and event contracts for paper-trading runs and feed those outputs back to strategy service, including anti-liquidation risk fields.

#### Scenario: Paper-trading window closes
- **WHEN** a paper-trading evaluation window ends
- **THEN** results are written to contract tables and published on event stream for strategy consumption

### Requirement: Versioned event-topic contracts
The system SHALL define versioned topic names and payload schemas for Redis Streams event exchange.

#### Scenario: Topic payload evolution
- **WHEN** payload fields change
- **THEN** event schema version is bumped and consumers remain backward compatible
