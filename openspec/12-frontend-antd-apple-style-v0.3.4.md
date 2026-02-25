# OpenSpec v0.3.4: Frontend UI System（Ant Design + Apple 风）

- 状态：Draft v0.3.4
- 目标：统一前端组件体系与视觉语言，支持多标签页业务面板

## 1) 技术与组件

- 框架：React
- 组件库：Ant Design（antd）
- 样式：TailwindCSS（布局/间距）+ 设计 token（主题）
- 图表：
  - 价格与技术指标同图：TradingView（优先）
    - 默认周期：15m / 1h / 4h / 1d
    - 默认指标：EMA(20/50/200), Bollinger Bands, RSI(14), MACD(12,26,9), Volume
  - 其他运营/统计图表：ECharts

## 2) 视觉风格（Apple 风）

- 关键词：简洁、留白、层级克制、动效轻量、毛玻璃/半透明卡片（适度）
- 设计原则：
  - 大字号标题 + 小字号辅助信息
  - 弱边框、高对比可读性
  - 统一圆角（如 12/16）
  - 阴影极轻，避免“企业后台重阴影”

## 3) 主题 token 规范（草案）

- 主色：中性蓝灰（支持深浅两套）
- 成功/风险：低饱和绿/红
- 背景层：
  - Page: `#F5F7FA`
  - Card: `#FFFFFFCC`（支持半透明）
- 字体：优先系统字体栈（SF Pro / Inter / Segoe UI）

## 4) 信息架构（多标签页）

- `Overview`
- `News`
- `Market Data`
- `Strategy`
- `Backtest`
- `System`（健康状态、任务状态、版本）

## 5) 关键组件约定

- 顶栏：全局状态 + 最近刷新时间 + 环境标识
- 卡片：统一 `PanelCard` 封装（标题、副标题、右上角操作）
- 表格：统一空状态、加载状态、错误状态
- 指标：统一 `MetricStat`（数值、变化、解释）

## 6) 前端与 API 边界

- 前端只调用主 workspace 的 FastAPI Aggregator
- 不直连四 Agent API（避免前端耦合）
- 每个标签页一个聚合 endpoint

## 7) 可访问性与响应式

- 最低支持 1280 宽
- 平板视图降级为两列
- 颜色对比满足基础可读性
- 关键交互支持键盘操作
