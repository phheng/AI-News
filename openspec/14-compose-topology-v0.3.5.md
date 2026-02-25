# OpenSpec v0.3.5: Docker Compose Topology

- 状态：Draft v0.3.5
- 目标：定义本地/服务器一体化编排拓扑（开发优先，兼容生产）

## 1) 服务拓扑

- `frontend`（React + antd，Nginx 托管）
- `api-gateway`（FastAPI 聚合层）
- `news-agent`（FastAPI + jobs）
- `market-agent`（FastAPI + Bybit jobs）
- `strategy-agent`（FastAPI + OpenViking memory jobs）
- `backtest-agent`（FastAPI + runner jobs）

可选（dev）：
- `mysql`（若不用外部 VPS MySQL）
- `redis`（若不用外部 VPS Redis）

## 2) 网络与端口

- 网络：`crypto-intel-net`
- 对外暴露：
  - frontend: `:80` / `:443`
  - api-gateway: `:18080`（可仅内网）
- 其余 agent 默认仅内网可达

## 3) compose 分层文件

- `docker-compose.yml`：基础服务定义
- `docker-compose.dev.yml`：开发覆盖（挂载源码、热更新、内置 mysql/redis）
- `docker-compose.prod.yml`：生产覆盖（固定镜像 tag、资源限制、重启策略）

## 4) 依赖与启动顺序

- gateway depends_on: all agent healthz
- frontend depends_on: gateway readyz
- migration job 在 gateway 启动前执行（或作为独立 one-shot service）

## 5) 健康检查与重启策略

- 每服务 healthcheck：`curl -f http://localhost:<port>/healthz`
- 重启策略：`unless-stopped`
- gateway/strategy/backtest 建议设置较高重试容忍

## 6) 数据卷与持久化

- 前端静态资源：镜像内置（无需卷）
- Strategy OpenViking memory：挂载持久卷
- 可选 dev 卷：mysql data / redis data

## 7) 环境变量约定

- 全局：`APP_ENV`, `LOG_LEVEL`, `TZ=Asia/Shanghai`
- 数据：`MYSQL_DSN`, `REDIS_URL`
- 市场：`BYBIT_API_BASE`, `BYBIT_API_KEY`, `BYBIT_API_SECRET`
- 追踪：`SERVICE_NAME`, `SERVICE_VERSION`

## 8) 发布与回滚

- 发布：按服务灰度替换（agents -> gateway -> frontend）
- 回滚：回退镜像 tag + 必要时执行 migration rollback
- 禁止使用 `latest` 作为生产 tag
