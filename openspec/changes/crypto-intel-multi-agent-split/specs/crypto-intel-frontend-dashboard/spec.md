## ADDED Requirements

### Requirement: Multi-tab dashboard information architecture
The frontend SHALL provide tabs for Overview, News, Market Data, Strategy, Backtest, and System, and render outputs from news-sentiment and market-indicators agents.

#### Scenario: User switches tabs
- **WHEN** user opens each tab
- **THEN** relevant metrics and lists are loaded and rendered

### Requirement: Ant Design + Apple-style UI system
The frontend SHALL use Ant Design components with a lightweight Apple-style visual system.

#### Scenario: Visual consistency check
- **WHEN** dashboard pages are reviewed
- **THEN** spacing, typography, cards, and interaction styles follow unified design tokens

### Requirement: Charting strategy by data type
The frontend SHALL use TradingView for price and selected technical-indicator charting, and use ECharts for other analytical/operational charts.

#### Scenario: Price chart rendering
- **WHEN** user opens market tab for symbol/timeframe
- **THEN** TradingView renders price candles and selected indicators

#### Scenario: Non-price analytics rendering
- **WHEN** user opens overview/news/strategy/backtest analytics panels
- **THEN** ECharts renders non-price statistical and operational visualizations

#### Scenario: Visual consistency check
- **WHEN** dashboard pages are reviewed
- **THEN** spacing, typography, cards, and interaction styles follow unified design tokens

### Requirement: Resilient data-state UX
The frontend SHALL implement loading, empty, and error states for all data panels.

#### Scenario: API timeout or empty response
- **WHEN** backend fails or returns no data
- **THEN** the page shows proper fallback states instead of broken UI
