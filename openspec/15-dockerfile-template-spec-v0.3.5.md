# OpenSpec v0.3.5: Dockerfile Template Spec

- 状态：Draft v0.3.5
- 目标：统一六类服务的镜像构建规范

## 1) Python 服务模板（FastAPI Agents / Gateway）

### 1.1 基本策略
- 使用多阶段构建
- builder 安装依赖，runtime 仅保留运行时
- 非 root 用户运行
- 启动命令统一走 `uvicorn`（或 gunicorn+uvicorn workers）

### 1.2 builder 阶段建议
- 基础镜像：`python:3.12-slim`
- 安装系统依赖（最小化）
- 复制 `pyproject.toml` / lock 文件后先装依赖（利用缓存）

### 1.3 runtime 阶段建议
- 仅复制 site-packages + app 源码
- 设置 `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`
- `HEALTHCHECK` 指向 `/healthz`

## 2) Frontend 模板（React + antd）

### 2.1 多阶段
- build: `node:lts` 执行构建
- runtime: `nginx:alpine` 托管 dist

### 2.2 运行时
- 配置 SPA fallback（history 路由）
- 静态资源 gzip/brotli（可选）
- 反向代理 API 到 `api-gateway`

## 3) 镜像元数据规范

- OCI labels：
  - `org.opencontainers.image.title`
  - `org.opencontainers.image.version`
  - `org.opencontainers.image.revision`
  - `org.opencontainers.image.created`

## 4) 安全基线

- 禁止把 secrets bake 进镜像
- 定期更新基础镜像
- 依赖漏洞扫描（CI）
- 最小权限文件系统（可写目录显式声明）

## 5) 性能与体积

- Python 镜像目标 < 350MB（初期）
- Frontend 镜像目标 < 150MB
- 清理缓存、移除无用构建工件

## 6) CI/CD 约定（草案）

- PR 阶段：lint + unit test + build test
- main 合并：打版本 tag -> 构建镜像 -> 推送仓库
- 生产发布：按 compose.prod.yml 进行有序拉起
