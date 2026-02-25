# OpenSpec v0.3.6: Review Checklist（你 Review 用）

- 状态：Draft v0.3.6
- 目标：让你快速检查文档是否能直接指导开发

## A. 架构边界

- [ ] OpenSpec 全在主 workspace
- [ ] 4 个 Agent 各自独立 workspace
- [ ] 前端与 gateway 在主 workspace

## B. 关键决策一致性

- [ ] 命名前缀统一 `crypto-intel`
- [ ] Market 主来源明确为 Bybit
- [ ] News 不止展示，包含分析处理
- [ ] OpenViking 重点落在 Strategy Agent

## C. 数据与存储

- [ ] MySQL 表设计覆盖 news/market/strategy/backtest
- [ ] Redis keyspace 定义完整（队列/幂等/状态/锁）
- [ ] Owner/Consumer 读写边界明确

## D. API 与前端

- [ ] 全部 API 采用 FastAPI
- [ ] 前端只调用 gateway，不直连 agent
- [ ] 多标签页结构与数据源对应清晰
- [ ] antd + Apple 风规范可执行

## E. 部署与运维

- [ ] Dockerfile 模板规范明确
- [ ] Compose dev/prod 拓扑明确
- [ ] 健康检查与发布回滚流程明确

## F. 可开发性

- [ ] Roadmap 分 phase 可按顺序执行
- [ ] 每 phase 都有验收标准
- [ ] 旧系统迁移与下线路径清楚

## G. 你可直接给我的反馈格式（建议）

```text
[通过] 章节：...
[修改] 章节：...（原因 + 期望）
[新增] 需要补充：...
[删除] 不需要：...
```
