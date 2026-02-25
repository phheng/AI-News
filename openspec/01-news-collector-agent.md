# OpenSpec: News Collector Agent

- **状态**：Draft v0.3.1
- **目标 workspace（开发目录）**：`~/.openclaw/workspace-crypto-intel-news-agent`
- **技术栈**：Python + uv

## 1. 目标

稳定收集加密市场新闻并标准化，并产出新闻分析结果（主题/情绪/事件影响），供策略设计 Agent 直接使用。

## 2. 范围

### In Scope
- 多源抓取（RSS/API/网页抓取适配）
- 去重、清洗、标准化
- 标签提取（币种、主题）
- 新闻分析处理（事件分类、影响方向、置信度）
- 情绪打分（基础版）

### Out of Scope（v0）
- 深度 NLP 推理
- 自动下单决策

## 3. 输入/输出

### 输入
- `sources.yaml`：新闻源配置
- `rules.yaml`：过滤规则（关键词、语言、黑白名单）

### 输出（标准事件）
- `news_events.jsonl`
- `news_analysis.jsonl`
- 字段：`event_id, ts, source, title, summary, url, symbols[], tags[], sentiment, impact_direction, confidence`

## 4. 接口契约（与其他 Agent）

- 向 Strategy Design Agent 提供：按时间窗口查询的新闻事件流 + 分析结果
- 数据交换底座：MySQL + Redis（已拍板）

## 5. 非功能要求

- 单轮抓取失败不影响后续轮次
- 同一新闻去重率 > 95%
- 可观测日志（抓取数、入库数、去重数、失败数）

## 6. 验收标准

- 新增源可通过配置接入（无需改主流程）
- 产出事件可被 Strategy Agent 直接消费
- 24h 运行无崩溃
\n## 7. 运维与命名约束\n
- workspace：`~/.openclaw/workspace-crypto-intel-news-agent`
- 定时任务前缀：`crypto-intel: news`
- MySQL 主表（v0 草案）：`news_events`
- Redis（v0 草案）：用于抓取去重键、短期事件缓存、任务队列
