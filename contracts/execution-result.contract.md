# Execution Result Contract（执行结果契约）

> 状态：Draft v0.1
> 目标：统一执行层回传给策略/监控/持仓引擎的结果事件。

## 1. 适用范围

- 发送方：执行引擎（真实交易）
- 接收方：策略引擎、持仓管理、PnL、告警系统
- 非目标：paper fill、模拟成交事件

## 2. 设计原则

1. **事件化**：支持 ACK / REJECT / PARTIAL_FILL / FILLED / CANCELED
2. **可对账**：必须含 venue_order_id / client_order_id / request_id 关联
3. **最终一致**：允许同一订单多次事件更新，最终状态可收敛

## 3. Schema（JSON）

```json
{
  "version": "1.0",
  "event_id": "uuid",
  "timestamp_ms": 0,
  "correlation": {
    "request_id": "uuid",
    "strategy_run_id": "string|null",
    "client_order_id": "string|null",
    "venue_order_id": "string|null"
  },
  "market": {
    "venue": "binance|bybit|okx|...",
    "symbol": "BTCUSDT"
  },
  "status": {
    "state": "ACKED|REJECTED|PARTIAL_FILLED|FILLED|CANCELED|EXPIRED",
    "reason_code": "string|null",
    "reason_msg": "string|null"
  },
  "execution": {
    "side": "buy|sell",
    "order_type": "market|limit|stop_market|stop_limit",
    "price": "number|null",
    "orig_qty": "number",
    "filled_qty": "number",
    "avg_fill_price": "number|null",
    "fees": [
      {
        "asset": "USDT",
        "amount": "number"
      }
    ]
  },
  "position_hint": {
    "position_delta": "number|null",
    "is_reduce": "boolean|null"
  },
  "meta": {
    "trace_id": "string|null",
    "raw_exchange_payload_ref": "string|null"
  }
}
```

## 4. 状态机约束

- 合法迁移示例：
  - `ACKED -> PARTIAL_FILLED -> FILLED`
  - `ACKED -> CANCELED`
  - `ACKED -> EXPIRED`
- `REJECTED` 为终态
- `FILLED` / `CANCELED` / `EXPIRED` 为终态

## 5. 幂等与去重

- 以 `event_id` 去重
- 以 `(venue, venue_order_id, state, filled_qty)` 做二次去重保护

## 6. 错误码建议

- `EXCHANGE_REJECT_MIN_NOTIONAL`
- `EXCHANGE_REJECT_PRICE_FILTER`
- `EXCHANGE_REJECT_RISK_LIMIT`
- `NETWORK_TIMEOUT`
- `UNKNOWN_ORDER_STATE`

## 7. 待确认（你拍板）

1. 是否要求每次 `PARTIAL_FILLED` 带“增量成交”字段？
2. `fees` 是否统一折算到 quote asset 再上报？
3. 是否把 `position_hint` 升级为强语义（由执行层计算）？
