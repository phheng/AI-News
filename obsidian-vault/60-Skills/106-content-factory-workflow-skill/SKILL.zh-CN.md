---
name: content-factory-workflow-skill
description: 基于 content-factory 用例的三段式内容流水线（Research -> Writing -> Creative）。用于将选题研究、写作产出、创意方案按定时任务或手动触发方式稳定落盘到 Obsidian。
version: 1.0.0
task_code: 106-A
language: zh-CN
---

# Content Factory Workflow Skill（中文）

## 目标
将内容生产流程拆分为 3 个可独立迭代的步骤：
1. Research（研究）
2. Writing（写作）
3. Creative（创意）

并保证输出结构化、可追踪、可复盘。

## 目录约定
- Research 输出：`obsidian-vault/20-Content-Factory/Research/Research-YYYY-MM-DD.md`
- Writing 输出：`obsidian-vault/20-Content-Factory/Writing/Writing-YYYY-MM-DD.md`
- Creative 输出：`obsidian-vault/20-Content-Factory/Creative/Creative-YYYY-MM-DD.md`

## 触发方式
- 定时触发（cron）：每天固定时段依次执行
- 手动触发：按需单次运行某一阶段

## 阶段规范

### 1) Research
最小输出要求：
- 5 个候选选题
- 每个选题至少 1 个来源 URL
- 每个选题包含：受众、价值点、风险点

### 2) Writing
输入：最新 Research 文件
最小输出要求：
- 1 篇核心稿（短文/线程）
- 3 个标题备选
- 关键结论可追溯到 Research 来源

### 3) Creative
输入：最新 Writing 文件
最小输出要求：
- 3 套创意方案
- 每套包含：主标题、副标题、画面说明、CTA

## 质量门槛
- 不允许无来源结论
- 不允许 `~` 路径写入，必须绝对路径
- 输出优先简洁（控制篇幅），保证可执行性

## 失败回退策略
- 某阶段失败时，不阻塞其他任务，但记录失败状态
- 下次运行优先重试失败阶段
- 连续失败 >= 3 次，触发人工检查

## 来源
- usecase: https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/content-factory.md
- raw: https://raw.githubusercontent.com/hesamsheikh/awesome-openclaw-usecases/main/usecases/content-factory.md
