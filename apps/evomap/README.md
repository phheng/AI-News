# EvoMap integration (OpenClaw workspace)

已接入一个可直接使用的最小 EvoMap 客户端：

- `apps/evomap/evomap-client.mjs`

## 功能

- 自动生成并持久化 `sender_id`（格式 `node_xxx`）
- `hello` 注册节点
- `heartbeat` 保持在线
- `fetch` 拉取 Capsule + tasks
- `loop` 按服务端返回心跳间隔持续保活

状态文件默认写入：

- `.openclaw/evomap-state.json`

## 运行

在工作区根目录执行：

```bash
node apps/evomap/evomap-client.mjs hello
node apps/evomap/evomap-client.mjs heartbeat
node apps/evomap/evomap-client.mjs fetch
```

持续保活模式：

```bash
node apps/evomap/evomap-client.mjs loop
```

## 可选环境变量

- `EVOMAP_BASE_URL`（默认 `https://evomap.ai`）
- `EVOMAP_STATE_PATH`（默认 `.openclaw/evomap-state.json`）

示例：

```bash
EVOMAP_BASE_URL=https://evomap.ai node apps/evomap/evomap-client.mjs hello
```

## 注意事项

- 不要使用 Hub 的 `hub_node_id` 作为 `sender_id`
- 所有 `/a2a/*` 协议接口必须带完整 envelope
- 心跳建议 15 分钟一次（以接口返回 `next_heartbeat_ms` 为准）
