# OpenSpec v0.3.7: Review Enhancements（按你 review 补充）

- 状态：Draft v0.3.7
- 目标：补齐新闻/情绪、技术指标、数据交互机制、频率策略、策略验证工具

## 1) Agent 职责升级

### 1.1 新闻 Agent 升级
- 新名称：**News & Sentiment Agent**（新闻收集及市场情绪分析）
- 新增能力：
  - 紧急新闻识别（breaking/urgent）
  - 新闻情绪与事件影响分析（bullish/bearish/neutral + confidence）
  - 输出可直接用于策略特征

### 1.2 市场 Agent 升级
- 新名称：**Market Data & Indicators Agent**
- 新增能力：
  - 多技术指标计算（如 MA/EMA/RSI/MACD/ATR/Bollinger 等）
  - 指标结果可查询、可被前端看板展示
  - 指标结果可被 News & Sentiment Agent 消费做联合分析

## 2) 前端展示补充

- News 标签必须展示：
  - 最新新闻流
  - 紧急新闻（独立区域/告警样式）
  - 情绪与影响方向摘要
- Market Data 标签必须展示：
  - K线基础数据摘要（TradingView 图表）
  - 核心技术指标（可叠加在 TradingView）
  - 其他指标统计看板（ECharts）
- 形式先以“可用”为主（卡片+表格+图），后续逐步优化交互

## 3) 跨 Agent 交互机制（不局限于数据表）

采用分层通信策略：

1. **MySQL（事实层）**：持久化、可追溯结果
2. **FastAPI（查询/控制层）**：同步拉取与任务触发
3. **消息队列（事件层，优先 Redis Streams）**：异步事件广播与解耦
4. **gRPC（可选，性能层）**：在高吞吐低延迟场景按需引入

### 推荐落地顺序
- v0.x：MySQL + FastAPI + Redis Streams
- v1.x：若吞吐/延迟成为瓶颈，再增量引入 gRPC

## 4) 采集频率策略（免费 API 约束）

### 4.1 市场数据采集频率（建议）
- 高频对（核心交易对）：1m/5m 每 1~2 分钟拉取
- 中频对：15m/1h 每 5~10 分钟拉取
- 低频对：4h/1d 每 30~60 分钟拉取
- 指标计算：按对应 timeframe 触发（增量计算优先）

### 4.2 限流与降级
- 全局速率控制 + 指数退避
- 达到限流阈值时：优先核心 symbol，非核心延迟
- 兜底源：**Binance API**（Bybit 不可用或受限时切换）

## 5) Strategy Agent 增强（验证工具）

Strategy Agent 除消费前两个 Agent 结果外，新增初步验证工具：

1. **Grid Search**
   - 参数网格枚举与批量回测触发
2. **策略平原（Parameter Plateau）分析**
   - 识别参数鲁棒区而非单点最优
3. **初步稳健性校验**
   - 时间切片稳定性
   - 成本敏感性（滑点/手续费）
   - 关键指标阈值过滤

## 6) 新增数据产物（草案）

- `news_alerts`（紧急新闻）
- `sentiment_snapshots`（按 symbol/timeframe 聚合情绪）
- `technical_indicator_values`（多指标时序值）
- `strategy_validation_runs`（grid/plateau 验证结果）

## 7) 里程碑调整

- 将“新闻分析”和“技术指标”从可选项提升为 v0.x 必做项
- 将“消息队列事件流”从建议项提升为 v0.x 必做项（Redis Streams）
- gRPC 继续保留为后续性能演进选项
