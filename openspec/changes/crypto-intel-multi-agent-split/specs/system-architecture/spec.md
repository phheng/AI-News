## ADDED Requirements

### Requirement: Four-agent split architecture
The system SHALL split crypto capabilities into four isolated agents: news-sentiment, market-indicators, strategy, and backtest, with unified naming prefix `crypto-intel`.

#### Scenario: Agent boundaries are enforced
- **WHEN** workspaces and services are initialized
- **THEN** each agent runs in its own workspace and service boundary

### Requirement: Main workspace as orchestration surface
The system SHALL keep OpenSpec docs and frontend/gateway code in the main workspace.

#### Scenario: Main workspace content is validated
- **WHEN** repository structure is reviewed
- **THEN** `openspec/`, `apps/frontend`, and `apps/api-gateway` exist in main workspace

### Requirement: Strategy-focused memory system
The system SHALL prioritize OpenViking memory features for the strategy agent and keep other agents lightweight.

#### Scenario: Memory scope is applied
- **WHEN** memory architecture is implemented
- **THEN** strategy agent has L0/L1/L2 + P0/P1/P2 workflow while other agents only write lightweight shared summaries

### Requirement: Bybit-first with Binance fallback
The market-indicators architecture SHALL use Bybit as primary source and support Binance fallback under outage or free-tier rate constraints.

#### Scenario: Primary source degraded
- **WHEN** Bybit API is unavailable or rate-limited beyond threshold
- **THEN** fallback source is enabled for continuity with source tags persisted

### Requirement: Closed-loop strategy lifecycle
The architecture SHALL run a closed loop of strategy design, backtest, paper trading, and strategy re-optimization, with anti-liquidation checks in both design and evaluation stages.

#### Scenario: End-to-end strategy cycle
- **WHEN** a strategy version completes backtest and paper trading windows
- **THEN** results are fed back to strategy service for next optimization decisions

### Requirement: Mature backtest engine baseline
The backtest architecture SHALL use a mature backtesting engine as the historical simulation core (MVP: backtrader).

#### Scenario: Historical simulation execution
- **WHEN** strategy backtest is triggered
- **THEN** execution is performed by the configured mature backtest engine and result metrics are returned

### Requirement: Telegram DM final delivery
The system SHALL push a Telegram DM summary after each completed full strategy lifecycle.

#### Scenario: Lifecycle completion notification
- **WHEN** a lifecycle reaches design -> backtest -> paper trading completion
- **THEN** a concise summary is sent to the configured Telegram DM recipient

### Requirement: Event-driven lifecycle orchestration
The architecture SHALL use stream events to orchestrate transitions between design, backtest, paper-trading, optimization, and notification steps.

#### Scenario: Lifecycle stage transition
- **WHEN** a stage-completion event arrives
- **THEN** the next stage is triggered by event consumption rather than fixed cron-only scheduling
