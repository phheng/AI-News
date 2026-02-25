# OpenSpec v0.3.9: Event Topics & Payload Contracts

- 状态：Draft v0.3.9
- 目标：把闭环流程拆成可执行事件流契约（Redis Streams）

## 1) Topic 命名

统一前缀：`crypto-intel:stream:`

- `crypto-intel:stream:news.events`
- `crypto-intel:stream:news.urgent`
- `crypto-intel:stream:market.ohlcv`
- `crypto-intel:stream:market.indicators`
- `crypto-intel:stream:strategy.generated`
- `crypto-intel:stream:backtest.completed`
- `crypto-intel:stream:paper.window.closed`
- `crypto-intel:stream:strategy.optimized`
- `crypto-intel:stream:notification.telegram`

## 2) 通用事件头

```json
{
  "event_id": "uuid",
  "event_type": "string",
  "trace_id": "string",
  "producer": "crypto-intel-xxx-agent",
  "occurred_at": "2026-02-25T09:00:00Z",
  "version": "1.0"
}
```

## 3) 关键 payload 草案

### 3.1 `paper.window.closed`
```json
{
  "strategy_id": "strat_x",
  "strategy_version": 7,
  "window_start": "...",
  "window_end": "...",
  "metrics": {
    "pnl": 0.0,
    "max_drawdown": 0.0,
    "win_rate": 0.0,
    "trade_count": 0
  },
  "trigger_flags": ["under_threshold", "regime_shift"]
}
```

### 3.2 `strategy.optimized`
```json
{
  "strategy_id": "strat_x",
  "from_version": 7,
  "to_version": 8,
  "reason": "paper_trading_underperform",
  "optimization_summary": "...",
  "next_effective_window": {
    "start": "...",
    "end": "..."
  }
}
```

### 3.3 `notification.telegram`
```json
{
  "to": "8215621524",
  "template": "strategy_cycle_summary_v1",
  "context": {
    "strategy_id": "strat_x",
    "version": 8
  }
}
```

## 4) 消费保障

- 每 topic 建 consumer group
- 消费幂等：`event_id` 去重
- 失败消息进死信流：`crypto-intel:stream:dlq:<topic>`
