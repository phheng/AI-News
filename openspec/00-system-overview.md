# OpenSpec: Crypto Intelligence System（四 Agent 拆分总览）

- **状态**：Draft v0.3.9（已补齐事件流契约、DM模板与执行任务拆解）
- **主 workspace**：`~/.openclaw/workspace`
- **核心原则**：
  1. OpenSpec 文档统一放在主 workspace（本目录）
  2. 各 Agent 代码仅放在各自独立 workspace
  3. 前端（React + TailwindCSS）放在主 workspace
  4. 四个 Agent 虽分开部署，但逻辑上属于一个系统
  5. 命名前缀统一（workspace / agentId / cron name）

---

## 1) 目标

把现有 `workspace-crypto-trading-agent` 拆分为四个职责清晰的 Agent：

1. News & Sentiment Agent
2. Market Data & Indicators Agent
3. Strategy Design Agent
4. Backtest Agent

并由主 workspace 前端统一展示结果（多标签页）。

---

## 2) 统一命名规范（已确认）

> 你要求“四个 Agent 虽然分开，但逻辑上一个系统”，因此统一前缀。

- **系统前缀**：`crypto-intel`
- **命令/任务统一前缀**：`crypto-intel:`（主 workspace 与所有 Agent workspace 一致）
- **workspace 命名**：
  - `~/.openclaw/workspace-crypto-intel-news-agent`
  - `~/.openclaw/workspace-crypto-intel-market-agent`
  - `~/.openclaw/workspace-crypto-intel-strategy-agent`
  - `~/.openclaw/workspace-crypto-intel-backtest-agent`
- **agentId 建议**：
  - `crypto-intel-news-agent`
  - `crypto-intel-market-agent`
  - `crypto-intel-strategy-agent`
  - `crypto-intel-backtest-agent`
- **cron name 前缀**：统一 `crypto-intel:`，例如：
  - `crypto-intel: news incremental`
  - `crypto-intel: market ohlcv sync`

---

## 3) Agent 划分（高层）

### A. News Collector Agent
- 输入：新闻源配置、抓取周期、关键词/白名单
- 输出：标准化新闻事件流（时间、来源、标签、情绪可选）

### B. Market Data Collector Agent
- 输入：交易所/标的配置、K 线粒度、采样频率
- 输出：标准化行情数据（OHLCV、funding、OI 可扩展）

### C. Strategy Design Agent
- 输入：新闻事件 + 行情数据 + 策略模板/约束
- 输出：策略定义（参数、信号逻辑、风控规则，含防爆仓约束）

### D. Backtest Agent
- 输入：策略定义 + 历史行情数据 + 实时价格流
- 输出：回测报告 + paper trading 结果（收益、回撤、交易明细、稳健性指标，含防爆仓校验结果）

---

## 4) 数据共享策略（已更新）

你明确说“共享是抽象需求，要看场景”，因此本规范采用：

- **先定义场景，再定义共享数据**（而非先定死全量共享）
- **数据底座**：
  - 持久化：MySQL（你已在 VPS 部署）
  - 缓存/队列/分布式锁：Redis（你已在 VPS 部署）

### 4.1 共享场景矩阵（v0）

1. `News -> Strategy`
   - 共享：新闻事件、标签、情绪、事件时间
2. `Market -> Strategy`
   - 共享：特征窗口所需 K 线与衍生指标
3. `Strategy -> Backtest`
   - 共享：策略定义、参数组合、风控约束
4. `Market -> Backtest`
   - 共享：历史数据切片
5. `Backtest -> Frontend`
   - 共享：报告摘要、排名、关键指标、回测工单状态

### 4.2 原则

- 不做“全库互相读写”，而是按场景开放最小数据面
- 每条跨 Agent 数据有 owner（写入方）与 consumer（只读方）
- 优先通过“标准化表结构 + 版本化契约”实现稳定共享

---

## 5) 工作区规划（目录与边界）

- 主 workspace：`~/.openclaw/workspace`
  - `openspec/`（仅规格）
  - `apps/frontend/`（React + TailwindCSS）
  - `contracts/`（跨 Agent 数据契约）

- 独立 Agent workspaces（后续创建）
  - `~/.openclaw/workspace-crypto-intel-news-agent`
  - `~/.openclaw/workspace-crypto-intel-market-agent`
  - `~/.openclaw/workspace-crypto-intel-strategy-agent`
  - `~/.openclaw/workspace-crypto-intel-backtest-agent`

---

## 6) 技术栈约束（已确认）

- Agent 端：`uv + python`
- 前端：`React + Ant Design + TailwindCSS`（图表：TradingView + ECharts）
- 存储：`MySQL + Redis`

---

## 7) 前端信息架构（已确认）

- 模式：**多标签页**
- 初版建议标签：
  1. Overview（系统总览）
  2. News
  3. Market Data
  4. Strategy
  5. Backtest

---

## 8) 迁移计划（阶段）

1. 冻结旧 crypto 定时任务（✅ 已完成）
2. 定稿四份 Agent OpenSpec（进行中）
3. 创建四个新 workspace + 初始化骨架
4. 按 Agent 分步迁移旧功能
5. 联调 MySQL/Redis + 前端多标签页
6. 验收后删除旧 workspace 与旧 cron

---

## 9) 验收门槛（系统级）

- 四 Agent 均可独立运行
- 按场景共享数据而非全量耦合
- 前端多标签页可展示四 Agent 最新结果
- 旧 `workspace-crypto-trading-agent` 完成替代后再下线

---

## 10) 下一步（我来做）

- 把 01~04 四份 Agent 规范升级到 v0.2：
  - 增加 MySQL 表与 Redis key/queue 设计草案
  - 明确每个 Agent 的输入/输出契约版本
  - 明确 cron 命名前缀 `crypto-intel:` 规范

## 11) v0.3 新决策（已确认）

- 前后端 API 统一采用 **FastAPI（Python）**
- 多 Agent 记忆系统采用 **OpenViking** 思路：L0/L1/L2 分层 + P0/P1/P2 生命周期
- 跨 Agent 共享记忆作为系统能力，不再依赖手工重复输入背景
- v0.3 先定规范，v0.4 进入脚本化与自动化落地

## 12) v0.3.1 新决策（已确认）

- OpenViking 记忆系统优先落在 **Strategy Design Agent**；其余 Agent 使用轻量记忆即可
- 价格数据主来源固定为 **Bybit API**（保留后续扩展交易所能力）
- 新闻链路不仅用于展示，必须包含“新闻分析处理”并输入策略设计

## 13) v0.3.2 新增设计（本轮）

- 明确 MySQL DDL 草案与 Redis keyspace 规范
- 明确主 workspace + 四 Agent workspace 的目录骨架
- 明确 consumer 对 owner 数据只读，按场景最小共享
- 明确 Strategy Agent 为 OpenViking 重点落地区

## 14) v0.3.3 新增设计（本轮）

- 增加数据库迁移 Playbook（版本命名、执行规则、回滚规则、迁移元数据表）
- 增加 Bybit 字段映射契约（API 字段到内部标准模型）
- 明确 Bybit 数据质量校验与幂等 upsert 规则

## 15) v0.3.4 新增设计（本轮）

- 前端组件库确定为 **Ant Design**
- 视觉方向确定为 **Apple 风（简洁、克制、轻量动效）**
- 所有代码服务支持镜像化，并可通过 **Docker** 部署

## 16) v0.3.5 新增设计（本轮）

- 增加 Docker Compose 拓扑规范（dev/prod 分层、网络、端口、依赖、健康检查）
- 增加 Dockerfile 模板规范（Python 服务 + Frontend 多阶段构建）
- 明确镜像安全基线与 CI/CD 构建发布约定

## 17) v0.3.6 新增设计（本轮）

- 增加实施路线图（Phase 0~7）及每阶段验收标准
- 增加 Review 清单，便于你逐条审阅与反馈
- 明确从“设计完成”到“开始开发”的执行顺序

## 18) v0.3.7 新增设计（按 review 补充）

- News Agent 升级为 **News & Sentiment Agent**，新增紧急新闻识别
- Market Agent 升级为 **Market Data & Indicators Agent**，新增多指标分析
- 前端必须展示新闻结果（含紧急新闻）与技术指标看板
- 跨 Agent 通信采用分层：MySQL + FastAPI + Redis Streams（gRPC 作为后续可选）
- 市场采集与指标计算按免费 API 预算设计频率，并支持 Binance 兜底
- Strategy Agent 增加 Grid Search 与策略平原等初步验证工具

## 19) v0.3.8 新增设计（本轮）

- Backtest Agent 增加“基于实时价格的 paper trading”能力
- Backtest/Paper Trading 周期结果必须回传 Strategy Agent
- Strategy Agent 使用 OpenClaw 参与优化决策（不单独引入外部大模型）
- 策略更新节奏采用“按策略生效窗口动态触发”，不使用机械固定时段
- 完整策略周期（设计 -> 回测 -> paper trading）结束后自动 Telegram DM 推送摘要

## 20) v0.3.9 新增设计（本轮）

- 增加 Redis Streams 事件 topics 与 payload 契约
- 增加 Telegram DM 模板字段规范与发送幂等规则
- 增加闭环实施任务拆解（事件流、paper、优化、通知、联调）

## 21) v0.3.10 补充设计（本轮）

- Strategy Agent 策略定义必须包含防爆仓约束（保证金安全、杠杆上限、降风险触发）
- Backtest / Paper Trading 必须执行防爆仓模拟与校验，并输出风险结果
