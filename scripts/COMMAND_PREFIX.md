# crypto-intel Command Prefix Convention

为保证主 workspace 与各 Agent workspace 在逻辑上属于同一项目，统一使用前缀：

- **命令前缀**：`crypto-intel:`
- **服务名**：`crypto-intel-<service>`
- **任务名/cron 名**：`crypto-intel: <domain> <action>`

## 示例

- `crypto-intel: db migrate`
- `crypto-intel: redis init-streams`
- `crypto-intel: gateway serve`
- `crypto-intel: market sync bybit`
- `crypto-intel: strategy optimize`

## 建议落地

- 主 workspace 和各 Agent 都提供同名入口脚本（如 `./bin/ci` 或 `make` 目标）
- 日志统一包含 `service_name=crypto-intel-...`
- 事件流 topic 统一前缀 `crypto-intel:stream:*`
