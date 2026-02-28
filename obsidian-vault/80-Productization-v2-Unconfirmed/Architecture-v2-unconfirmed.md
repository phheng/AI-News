---
type: architecture
version: v2-unconfirmed
updated_bjt: 2026-03-01 00:40
status: unconfirmed
---

# [未确认版本] Architecture v2（North America, OpenClaw-native）

## 1. 系统边界
### 做什么
- 提供“决策优先”的运营控制台（Web + IM）
- 将多工具数据转成可执行建议（带证据与置信度）
- 提供可审计的审批闭环（Observe / Approve / Auto）
- 提供业务/产品/成本（Token）统一指标

### 不做什么（当前阶段）
- 不做全自动高风险执行
- 不做复杂多租户企业权限系统（先保留扩展位）
- 不做过度重前端（先可用，再精美）

## 2. 分层架构
1) Interaction Layer：Web 控制台 + Discord
2) Orchestration Layer：OpenClaw agent/workspace/cron/subagent
3) Capability Layer：Ads / Stock / Competitor / News / Asset Ops
4) Data Layer：events + metrics + audit + knowledge docs
5) Governance Layer：risk tiers + approval gates + rollback

## 3. 角色边界
- henk：架构与ICP主责、任务调度、最终决策对话
- Atlas：架构确认后的研发与测试执行
- Pulse：SEO与外部增长执行，反馈可发现性指标

## 4. 决策流（主路径）
建议生成 → 风险分级 → 审批执行 → 指标回写 → 复盘优化

## 5. 风险控制
- 默认 Observe
- 中高风险必须 Approve
- Auto 仅白名单低风险动作
- 每次执行必须留痕（run_id / evidence / operator / timestamp）

## 6. 三阶段演进
- 阶段1：单工具价值验证（快+准）
- 阶段2：多工具智能工作流（流畅+智能）
- 阶段3：主动决策辅助（前瞻+个性化）

## 7. 验收锚点
- API 成功率 >=95%
- 报告完整率 >=98%
- Token 成本占月费 <=25%
- 高风险动作可审计可回滚
