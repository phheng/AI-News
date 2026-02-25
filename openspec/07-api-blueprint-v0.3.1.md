# OpenSpec v0.3.1: FastAPI Blueprint（前后端 + 四 Agent）

- 状态：Draft v0.3.1
- 目标：给开发阶段提供可直接落地的 API 草图

## 1) 统一约束

- 框架：FastAPI（Python）
- 返回格式：
  - 成功：`{ "ok": true, "data": ... }`
  - 失败：`{ "ok": false, "error": { "code": "...", "message": "..." } }`
- 基础接口：`GET /healthz` `GET /readyz` `GET /version`
- trace：请求头支持 `X-Trace-Id`

## 2) News Agent API

- `POST /v1/news/ingest`
  - 入参：source 批次/抓取窗口
  - 出参：写入条数、去重条数
- `GET /v1/news/events`
  - 查询：time range / symbol / topic
- `GET /v1/news/analysis`
  - 查询：impact_direction / confidence

## 3) Market Agent API（Bybit 优先）

- `POST /v1/market/sync`
  - 入参：`venue(bybit)`, `symbol`, `timeframe`, `from`, `to`
- `GET /v1/market/ohlcv`
  - 查询：`symbol`, `timeframe`, `from`, `to`
- `GET /v1/market/features`
  - 查询：`feature_set_version`, `symbol`, `timeframe`

## 4) Strategy Agent API（记忆重点）

- `POST /v1/strategy/generate`
  - 入参：策略模板 + 约束 + 新闻/行情窗口
  - 出参：`strategy_id`, `version`
- `GET /v1/strategy/specs/{strategy_id}`
- `POST /v1/strategy/memory/query`
  - OpenViking L0/L1/L2 按需读取入口
- `POST /v1/strategy/memory/write`
  - 写入 P0/P1/P2 记忆条目

## 5) Backtest Agent API

- `POST /v1/backtest/run`
  - 入参：`strategy_id`, `version`, `market_range`, `cost_model`
  - 出参：`run_id`
- `GET /v1/backtest/runs/{run_id}`
- `GET /v1/backtest/runs/{run_id}/metrics`
- `GET /v1/backtest/runs/{run_id}/artifacts`

## 6) Frontend Aggregator API（主 workspace）

- `GET /v1/dashboard/overview`
- `GET /v1/dashboard/news`
- `GET /v1/dashboard/market`
- `GET /v1/dashboard/strategy`
- `GET /v1/dashboard/backtest`

> 前端采用多标签页，对应以上 5 个聚合接口。
