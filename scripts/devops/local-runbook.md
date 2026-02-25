# crypto-intel local runbook

## 1) 初始化 Redis Streams

```bash
cd ~/.openclaw/workspace
make redis-init
```

## 2) 启动 API Gateway

```bash
cd ~/.openclaw/workspace
make gateway-run
```

## 2.1) 启动事件 worker（建议）

```bash
cd ~/.openclaw/workspace
make redis-notify-worker
make redis-paper-bridge
```

## 3) 启动四个 Agent（分别在各自 workspace）

```bash
cd ~/.openclaw/workspace-crypto-intel-news-agent/apps/news-agent && ./run.sh
cd ~/.openclaw/workspace-crypto-intel-market-agent/apps/market-agent && ./run.sh
cd ~/.openclaw/workspace-crypto-intel-strategy-agent/apps/strategy-agent && ./run.sh
cd ~/.openclaw/workspace-crypto-intel-backtest-agent/apps/backtest-agent && ./run.sh
```

默认端口：
- news: 18101
- market: 18102
- strategy: 18103
- backtest: 18104
- gateway: 18080
