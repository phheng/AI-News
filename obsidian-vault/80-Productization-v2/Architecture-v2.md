---
type: architecture
version: v2
updated_bjt: 2026-03-01 00:30
---

# Architecture v2（OpenClaw-native）

## 分层
1. Interaction Layer：Web Console + IM
2. Orchestration Layer：agent/workspace/cron/subagent
3. Capability Layer：Ads/Stock/Competitor/Market Assets
4. Data Layer：events + metrics + audit + knowledge docs
5. Governance Layer：Observe/Approve/Auto + rollback

## 角色
- henk：架构/ICP/决策
- Atlas：研发与测试执行
- Pulse：营销与SEO执行

## 风险控制
- 默认 Observe
- 中高风险必须 Approve
- Auto 仅白名单低风险动作
- 所有执行动作必须留痕（run_id + evidence + operator）

## 演进阶段
- 阶段1（单工具价值验证）
- 阶段2（多工具智能工作流）
- 阶段3（主动决策辅助）
