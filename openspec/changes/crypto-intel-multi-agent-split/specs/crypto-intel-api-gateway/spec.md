## ADDED Requirements

### Requirement: FastAPI standard across services
The system SHALL implement FastAPI for all agent APIs and the frontend-facing gateway API.

#### Scenario: Service interface consistency
- **WHEN** services start
- **THEN** each service exposes `/healthz`, `/readyz`, and `/version`

### Requirement: Frontend single-entry API access
The frontend SHALL access backend data only via gateway endpoints and not call agent services directly.

#### Scenario: Frontend network policy
- **WHEN** frontend is configured for production
- **THEN** requests target gateway base URL only, without direct calls to agent service URLs

### Requirement: Urgent news and indicators dashboard endpoints
The gateway SHALL expose aggregated endpoints for urgent news and technical indicator dashboard data.

#### Scenario: Urgent news panel refresh
- **WHEN** frontend requests urgent news
- **THEN** gateway returns prioritized breaking news items with sentiment/impact metadata

### Requirement: Telegram notification dispatch endpoint
The gateway SHALL provide a controlled dispatch path for strategy-cycle Telegram DM notifications.

#### Scenario: Lifecycle summary send request
- **WHEN** strategy lifecycle completion event is received
- **THEN** gateway dispatches a single idempotent Telegram DM using approved template fields

#### Scenario: Dashboard data request
- **WHEN** frontend requests dashboard tabs data
- **THEN** gateway aggregates/forwards responses from relevant agents

### Requirement: Unified response envelope
The system SHALL return standardized success/error envelopes for API responses.

#### Scenario: API failure response
- **WHEN** an endpoint fails validation or execution
- **THEN** it returns structured error code and message in the standard envelope
