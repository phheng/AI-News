# OpenSpec v0.3.3: Bybit Field Mapping Contract

- 状态：Draft v0.3.3
- 目标：定义 Bybit API -> 内部标准模型 的字段映射契约
- 适用：Market Data Collector Agent（主来源：Bybit）

## 1) 标准 K 线模型（内部）

```json
{
  "venue": "bybit",
  "symbol": "BTCUSDT",
  "timeframe": "1m|5m|1h|4h|1d",
  "ts": "datetime(UTC)",
  "open": 0,
  "high": 0,
  "low": 0,
  "close": 0,
  "volume": 0,
  "turnover": 0
}
```

## 2) Bybit 到内部映射（Kline）

> 以 Bybit v5 Kline 响应为参考（数组字段位置映射）

- `startTime` -> `ts`
- `openPrice` -> `open`
- `highPrice` -> `high`
- `lowPrice` -> `low`
- `closePrice` -> `close`
- `volume` -> `volume`
- `turnover` -> `turnover`
- 请求参数 `category/symbol/interval` -> `venue/symbol/timeframe`

## 3) timeframes 归一化

- Bybit interval `1` -> `1m`
- `5` -> `5m`
- `60` -> `1h`
- `240` -> `4h`
- `D` -> `1d`

## 4) 精度与类型

- API 原始字符串先转 `Decimal`
- 入库时使用 `DECIMAL(30,10)`
- 禁止直接用 float 写库

## 5) 数据质量规则

- `high >= max(open, close)`
- `low <= min(open, close)`
- `volume >= 0`
- 时间连续性检查：允许短时缺口，但必须入补拉队列

## 6) 幂等写入规则

- 幂等键：`(venue, symbol, timeframe, ts)`
- 写入策略：`INSERT ... ON DUPLICATE KEY UPDATE`
- 仅当新数据版本时间更新时覆盖（避免旧数据回刷）

## 7) 错误处理

- `BYBIT_RATE_LIMIT`：退避重试（指数退避 + 抖动）
- `BYBIT_TIMEOUT`：重试 + 告警阈值
- `BYBIT_SCHEMA_CHANGED`：进入死信队列并触发人工检查

## 8) 扩展预留

- 预留 funding / OI / index price 映射章节
- 新交易所接入必须先提供同等级“字段映射契约”
