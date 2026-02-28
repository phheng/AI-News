---
type: completed-project
name: amazon-agent-platform-v1-tested
status: completed-tested
completed_bjt: 2026-02-28 17:01
test_result: pass
owner: henk
---

# Amazon Agent Platform v1（测试完成）

## 项目状态
- 状态：已完成并通过可用性测试
- 结论：项目机制可行（API 健康检查 200 OK，Web 可访问）

## 独立代码与文档目录
- `/root/.openclaw/projects/completed/amazon-agent-platform-v1-tested`

> 说明：已将项目代码与文档独立复制到 completed 目录（排除 `node_modules` 与 `dist`）。

## 核心内容
- OpenSpec 设计包（proposal/spec/design/tasks）
- Web MVP（Home/Tasks/Insights/Governance/Assets）
- 后端 API（任务、建议、审批、指标、事件）
- SQLite 本地数据层与 seed
- 测试脚本与验证流程

## 运行方式
```bash
cd /root/.openclaw/projects/completed/amazon-agent-platform-v1-tested
npm install
npm run build
npm start
```

## 验证方式
```bash
curl http://127.0.0.1:3000/api/health
```
应返回：`{"ok":true}`

## 关键提交记录
- Atlas MVP: `793b00c10d32de6ab13b6536469eb6ce58d04f04`
- Pulse 增长包: `0d8c491`
- UI/API 收敛修复: `76f9877`
