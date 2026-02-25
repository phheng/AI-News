# OpenSpec v0.3.4: Docker Packaging & Deployment

- 状态：Draft v0.3.4
- 目标：所有代码服务可镜像化，并通过 Docker 部署

## 1) 组件清单（容器化）

- `crypto-intel-news-agent`（FastAPI + jobs）
- `crypto-intel-market-agent`（FastAPI + Bybit sync jobs）
- `crypto-intel-strategy-agent`（FastAPI + OpenViking memory jobs）
- `crypto-intel-backtest-agent`（FastAPI + runner jobs）
- `crypto-intel-api-gateway`（主 workspace 聚合 API）
- `crypto-intel-frontend`（React + antd）

> MySQL 与 Redis 可复用你 VPS 现有实例；也支持 compose 内自带实例（dev）

## 2) 镜像规范

- 镜像命名：`crypto-intel/<service>:<version>`
- 基础镜像：Python 服务使用 `python:3.12-slim`（建议）
- 多阶段构建：
  - 前端：node build -> nginx runtime
  - Python：builder 安装依赖 -> runtime 拷贝产物

## 3) 配置注入

- 使用环境变量注入：
  - `MYSQL_DSN`
  - `REDIS_URL`
  - `BYBIT_API_KEY` / `BYBIT_API_SECRET`（若需要）
  - `APP_ENV`, `LOG_LEVEL`
- Secrets 禁止写入镜像层

## 4) 健康检查

- 每个服务提供：`/healthz` `/readyz`
- Docker `HEALTHCHECK` 调用 `/healthz`

## 5) 网络与编排

- 统一 bridge network：`crypto-intel-net`
- 服务间通过容器名访问
- 对外仅暴露：
  - frontend
  - api-gateway

## 6) 发布策略

- 开发：`docker compose up -d`
- 生产：
  - 镜像版本固定（不可用 `latest`）
  - 滚动替换（先 gateway，再 frontend，再 agents）
  - 数据库迁移前后做 smoke check

## 7) 日志与观测

- stdout 结构化日志（JSON）
- 每服务注入 `service_name`, `version`, `trace_id`
- 可选接入 Loki/Prometheus（v0.5）
