# OpenSpec v0.3: OpenViking Memory Architecture（多 Agent 共享记忆）

- 状态：Draft v0.3.1
- 目标：以 Strategy Design Agent 为主构建可持续、可共享、可控成本的记忆系统（其他 Agent 仅保留轻量记忆）
- 方案：OpenViking（L0/L1/L2 + P0/P1/P2）

## 1. 设计目标

1) 重点解决 Strategy Agent 的长期上下文连续性
2) 在必要范围内解决跨 Agent “互相不认识”问题
3) 降低每轮加载 token 成本
4) 支持生命周期管理（保鲜 + 归档）

## 2. 三层记忆模型

- L0：目录索引（`.abstract`）
  - 作用：快速判断是否需要深入读取
  - 成本最低

- L1：摘要层（每个主题文件的摘要）
  - 作用：确认相关性

- L2：全文层（详细记录）
  - 作用：仅在需要时加载原始细节

## 3. 生命周期标签

- P0：核心信息（永久保留）
- P1：活跃项目（90 天后归档）
- P2：临时信息（30 天后归档/清理）

## 4. 目录结构（逻辑）

```text
memory/
  .abstract              # L0 索引
  p0-core/
  p1-active/
  p2-temp/
  archive/
shared-memory/
  .abstract              # 跨 Agent 共享 L0 索引
  user-profile.md        # P0
  active-tasks.md        # P1
  cross-agent-log.md     # P1/P2
```

## 5. Agent 行为约束

- **Strategy Agent（重点）**：完整执行 L0 -> L1 -> L2 按需加载与 P 标签维护
- **News/Market/Backtest Agent（轻量）**：默认只写共享结论与必要运行摘要，不维护大体量私有记忆
- 完成关键任务后，写入 `shared-memory/cross-agent-log.md`
- 记录规则：只写结论，不写过程；每条 ≤ 2 行
- 每日归档任务（主要针对 Strategy 记忆层）：
  - P1 超 90 天转 `archive/`
  - P2 超 30 天转 `archive/` 或清理

## 6. 与 OpenClaw memory 的关系

- OpenClaw 原生 `memory/*.md` 继续保留（兼容当前能力）
- OpenViking 层作为“项目记忆子系统”
- 对 Agent 来说，优先读取 OpenViking L0 索引，再按需深入

## 7. 实现边界（当前阶段）

- v0.3 是架构规范与目录/脚本设计，不立即大规模迁移旧记忆
- v0.4 再实施自动化脚本与迁移工具

## 8. 风险与缓解

- 风险：摘要失真导致检索偏差
  - 缓解：摘要文件保留 `source_ref` 与更新时间
- 风险：共享日志膨胀
  - 缓解：按周滚动 + 索引重建
