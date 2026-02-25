# Trade Intent Contract（下单意图契约）

> 状态：Draft v0.1
> 目标：在**不保留 paper trading**前提下，统一策略层到执行层的“下单意图”输入。

## 1. 适用范围

- 发送方：策略引擎 / 信号引擎
- 接收方：执行引擎（真实交易）
- 非目标：回测、仿真撮合、paper trading

## 2. 设计原则

1. **意图优先，不含交易所细节**（如具体 endpoint、签名参数）
2. **幂等可追踪**（必须有 request_id / strategy_run_id）
3. **风险前置**（策略可携带风控建议，执行层拥有最终裁决）
4. **可扩展**（字段新增不破坏旧版本）

## 3. Schema（JSON）

```json
{
  "version": "1.0",
  "request_id": "uuid",
  "timestamp_ms": 0,
  "strategy": {
    "strategy_id": "string",
    "strategy_run_id": "string",
    "signal_id": "string"
  },
  "market": {
    "venue": "binance|bybit|okx|...",
    "symbol": "BTCUSDT",
    "instrument_type": "spot|perp|futures"
  },
  "intent": {
    "side": "buy|sell",
    "action": "open|close|reduce|reverse",
    "order_type": "market|limit|stop_market|stop_limit",
    "quantity": {
      "value": "number",
      "unit": "base|quote|contracts"
    },
    "price": "number|null",
    "time_in_force": "GTC|IOC|FOK|null",
    "post_only": false,
    "reduce_only": false
  },
  "risk": {
    "max_slippage_bps": 0,
    "max_notional": "number|null",
    "kill_switch_tag": "string|null"
  },
  "meta": {
    "reason": "string",
    "tags": ["string"],
    "trace_id": "string"
  }
}
```

## 4. 必填 / 可选

- 必填：`version` `request_id` `timestamp_ms` `strategy.strategy_id` `market.venue` `market.symbol` `intent.side` `intent.order_type` `intent.quantity`
- 条件必填：
  - `intent.order_type=limit|stop_limit` 时，`intent.price` 必填
- 可选：`risk.*` `meta.*`

## 5. 校验规则

- `timestamp_ms` 与执行层系统时间偏差不得超过 ±30s
- `quantity.value > 0`
- `max_slippage_bps >= 0`
- 同一 `request_id` 重复提交必须视为幂等重放，不得重复下单

## 6. 错误码建议

- `INTENT_VALIDATION_ERROR`
- `RISK_REJECTED`
- `IDEMPOTENT_REPLAY`
- `UNSUPPORTED_SYMBOL`
- `VENUE_UNAVAILABLE`

## 7. 版本策略

- 当前：`1.0`
- 兼容原则：新增字段仅允许 optional；删除/改语义需升级大版本

## 8. 待确认（你拍板）

1. 是否强制 `strategy_run_id`？
2. `quantity.unit` 是否限制为 `contracts`（做衍生品优先）？
3. 是否允许策略层直接下 `reduce_only=true`？
