---
type: multi-agent-topology
version: v1
updated_bjt: 2026-02-28 13:25
---

# Multi-Agent Topology v1

## 主控 Agent
- 名字：**henk**
- 职责：
  - 架构设计（103-A 主责）
  - ICP 研究与决策（102-A 主责）
  - 与你对话、收集需求、发起审核与决策
  - 统一管理历史遗留任务（无法明确分配的任务默认归 henk）

## 子 Agent 1（研发执行）
- 名字：**Atlas**
- 职责：
  - 在 henk 给出架构/需求后执行产品开发与程序开发
  - Coding、测试、修复、验证
  - 输出工程变更与测试报告

## 子 Agent 2（营销执行）
- 名字：**Pulse**
- 职责：
  - SEO 内容生产与分发
  - 外部营销活动策划与执行
  - 曝光/转化数据跟踪与复盘

## 共享记忆机制
- 共享日志：`obsidian-vault/00-Inbox/Agent-Shared-Log.md`
- 文档落盘：按任务目录写入（32-ICP / 41-Architecture / 20-Content-Factory / scripts）
- 主控汇总：henk 每轮输出“进展 + 风险 + 待决策项”
