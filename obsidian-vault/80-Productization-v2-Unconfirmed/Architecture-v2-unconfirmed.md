---
type: architecture
version: v2.1-unconfirmed
updated_bjt: 2026-03-01 00:55
status: unconfirmed
source_ref: LinkFoxAgent 立项与路线资料（用户提供）
---

# [未确认版本] Architecture v2.1（NA 形态，LinkFox 对齐）

## 1) 战略核心
从“单点工具价值验证”进化到“多工具协同智能涌现”，最终成为卖家的主动决策大脑。

## 2) 三阶段架构演进
### 阶段1：单工具价值验证（快 + 准）
- 目标：10秒级响应、95%任务成功率
- 核心：对话式单工具调用 + LLM结构化解读

### 阶段2：多工具智能工作流（流畅 + 智能）
- 目标：从“用户指挥工具”到“AI规划并执行任务”
- 核心：工具编排、步骤执行、过程可追踪

### 阶段3：主动决策辅助（前瞻 + 个性化）
- 目标：从被动回答到主动洞察与策略提醒
- 核心：预警、优先级、个性化建议与复盘闭环

## 3) 分层架构
1. Interaction Layer：Web Console + Discord/IM
2. Orchestration Layer：OpenClaw（agent/workspace/cron/subagent）
3. Capability Layer：Selection Intelligence / Procurement Signals / Ops Context
4. Data Layer：垂类数据源 + 事件日志 + 指标仓
5. Governance Layer：Observe/Approve/Auto + 审计 + 回滚

## 4) 能力边界（MVP）
### 包含
- 用户输入需求 -> 生成选品方案 -> 执行 agent -> 输出候选商品与建议
- 多数据源聚合（趋势、竞品、平台信号）
- AI 解读 + 结构化输出 + 可追溯来源

### 不包含（本阶段）
- 自动上架
- 库存系统托管
- 广告系统自动投放

## 5) 角色分工
- henk：架构/ICP/决策与项目管理
- Atlas：架构确认后的产品与程序开发、测试
- Pulse：SEO内容、外部增长、可发现性运营

## 6) 风险控制
- 默认 Observe
- 中高风险 Approve
- Auto 仅白名单
- 每次执行记录 run_id / evidence / operator / rollback_ref

## 7) 架构验收门槛
- API 成功率 >= 95%
- 回答准确率（人工标注口径） >= 80%
- 周活跃用户比例 >= 40%（MVP目标）
- 高风险动作可审计可回滚
