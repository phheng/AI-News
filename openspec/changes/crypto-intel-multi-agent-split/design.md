## Context

当前已完成 v0.1~v0.3.9 设计：四 Agent 拆分、Bybit 映射、MySQL/Redis、OpenViking、FastAPI、前端 antd+Apple 风、Docker、paper trading 闭环、Telegram DM 交付。需要将分散设计统一收敛为开发可执行蓝图。

## Goals / Non-Goals

**Goals:**
- 固化四 Agent + gateway + frontend 的边界与交互
- 固化“数据事实层 + API 控制层 + 事件流编排层”三层通信模型
- 形成策略闭环：设计 -> 回测 -> paper trading -> 优化 -> DM
- 明确 Strategy Agent 使用 OpenClaw 进行优化推理（不引入额外模型栈）
- 保证文档可直接指导开发与验收

**Non-Goals:**
- 本阶段不直接上线实盘交易
- 本阶段不引入独立 gRPC 服务（保留后续演进）
- 本阶段不扩展到非 crypto 主域

## Decisions

1. **Agent 拆分与命名统一**：news-sentiment / market-indicators / strategy / backtest，统一 `crypto-intel` 前缀。  
   - 理由：职责清晰、可运维、可扩展。

2. **三层通信模型**：MySQL（事实层）+ FastAPI（查询控制）+ Redis Streams（事件层）。  
   - 理由：兼顾可追溯、可调试与异步解耦。

3. **市场数据策略**：Bybit 为主，Binance 兜底；采集频率按免费 API 预算动态分层。  
   - 理由：在成本约束下确保连续性。

4. **策略闭环引擎**：Backtest 增加实时价格 paper trading，窗口结果回传 Strategy。  
   - 理由：让策略在“历史+准实时”双维度验证后迭代。

5. **优化智能路径**：Strategy 通过 OpenClaw 交互完成优化，不单独接第三方模型服务。  
   - 理由：减少系统复杂性，统一智能入口。

6. **记忆重点化**：OpenViking 深度落在 Strategy，其他 Agent 轻记忆 + shared log。  
   - 理由：收益最大化、复杂度最小化。

7. **前端图表双栈**：TradingView 用于价格/部分指标；ECharts 用于其余分析图。  
   - 理由：专业行情展示 + 通用可视化兼得。

8. **交付规范**：完整策略周期结束 Telegram DM 推送，带幂等发送规则。  
   - 理由：结果闭环可见、可追踪。

## Risks / Trade-offs

- [风险] 多 Agent + 事件流编排复杂度上升  
  → [缓解] 统一 topic 命名、payload 版本、DLQ、trace_id。

- [风险] 免费 API 限流导致数据空窗  
  → [缓解] 分级频率、优先级队列、Bybit->Binance 兜底。

- [风险] paper trading 与回测偏差误导优化  
  → [缓解] 成本模型对齐、窗口对比、异常窗口剔除规则。

- [风险] Strategy 自动优化过度频繁  
  → [缓解] 生效窗口 + 退化阈值双触发 + 冷却期。

## Migration Plan

1. Phase 0~2：骨架、迁移体系、数据层验证
2. Phase 3~4：四 Agent API MVP + 指标/情绪/事件流接入
3. Phase 5：paper trading 闭环 + Strategy 动态优化
4. Phase 6：前端多标签页（TradingView+ECharts）联通
5. Phase 7：Docker 部署联调 + Telegram DM 收敛
6. Phase 8：观察窗后旧系统下线

## Open Questions

- TradingView 指标叠加首批名单（MVP）最终定哪些？
- Strategy 优化冷却期默认值（例如 6h/12h/24h）
- DM 模板是否需要附带风险等级 emoji/颜色语义