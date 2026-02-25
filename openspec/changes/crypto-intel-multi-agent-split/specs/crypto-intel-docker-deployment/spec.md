## ADDED Requirements

### Requirement: Containerized deployment for all code services
The system SHALL package all code services as Docker images.

#### Scenario: Build all services
- **WHEN** CI/CD build pipeline runs
- **THEN** images are produced for frontend, gateway, and four agents

### Requirement: Compose-based environment topology
The system SHALL provide base, dev, and prod compose configurations.

#### Scenario: Development startup
- **WHEN** developers run compose in dev mode
- **THEN** all required services start with valid network and env wiring

### Requirement: Health and rollback readiness
The deployment SHALL include health checks and versioned image tags for controlled rollout/rollback.

#### Scenario: Production rollback
- **WHEN** release health checks fail
- **THEN** operators can rollback to prior fixed image tags and recover service
