import React, { useEffect, useMemo, useState } from 'react'
import { Card, Col, ConfigProvider, Layout, Row, Select, Space, Table, Tabs, Tag, Typography, Button, Alert } from 'antd'
import { api } from './api'
import TradingViewChart from './components/TradingViewChart'
import StreamsChart from './components/StreamsChart'
import StrategyEvolutionChart from './components/StrategyEvolutionChart'
import StrategyTimelineChart from './components/StrategyTimelineChart'
import StrategyPerformanceChart from './components/StrategyPerformanceChart'
import PortfolioCorrelationHeatmap from './components/PortfolioCorrelationHeatmap'
import { EmptyBlock, ErrorBlock, LoadingBlock } from './components/StateBlock'
import { appleLikeTheme, defaultChartConfig } from './theme'

const { Header, Content } = Layout
const { Title, Text, Link } = Typography

function useLoad(fn, deps = [], refreshMs = 0) {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  const run = () => {
    setLoading(true)
    setError(null)
    fn()
      .then((r) => setData(r.data || r))
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    let on = true
    setLoading(true)
    setError(null)
    fn()
      .then((r) => on && setData(r.data || r))
      .catch((e) => on && setError(String(e)))
      .finally(() => on && setLoading(false))

    let t = null
    if (refreshMs > 0) {
      t = setInterval(() => {
        if (!on) return
        fn()
          .then((r) => on && setData(r.data || r))
          .catch((e) => on && setError(String(e)))
      }, refreshMs)
    }

    return () => {
      on = false
      if (t) clearInterval(t)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  return { loading, data, error, reload: run }
}

function Panel({ title, children, extra }) {
  return <Card title={title} extra={extra} style={{ borderRadius: 14 }}>{children}</Card>
}

function OverviewTab() {
  const { loading, data, error } = useLoad(api.overview, [], 10000)
  if (loading) return <LoadingBlock tip="Loading overview" />
  if (error) return <ErrorBlock error={error} />
  const agents = data?.agents || {}
  return (
    <Panel title="System Overview" extra={<Text type="secondary">Auto refresh: 10s</Text>}>
      <Space>
        {Object.entries(agents).map(([k, ok]) => <Tag key={k} color={ok ? 'green' : 'red'}>{k}:{ok ? 'up' : 'down'}</Tag>)}
      </Space>
    </Panel>
  )
}

function NewsTab() {
  const { loading, data, error, reload } = useLoad(api.news, [], 15000)

  const latest = data?.latest || []
  const urgent = data?.urgent || []
  const analysis = data?.analysis || []
  const analysisMap = useMemo(() => {
    const m = {}
    for (const a of analysis) m[a.event_uid] = a
    return m
  }, [analysis])

  if (loading) return <LoadingBlock tip="Loading news" />
  if (error) return <ErrorBlock error={error} />
  if (!latest.length && !urgent.length) return <EmptyBlock desc="No news data yet (collector may still warming up)" />

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Alert
        type="info"
        showIcon
        message={`Sentiment method: ${data?.meta?.sentiment_method || 'rule-based v1'}`}
      />
      <Panel title="Urgent News" extra={<Space><Text type="secondary">Auto refresh: 15s</Text><Button size="small" onClick={reload}>Refresh</Button></Space>}>
        <Table
          size="small"
          rowKey="event_uid"
          dataSource={urgent}
          columns={[
            { title: 'Level', dataIndex: 'alert_level' },
            { title: 'Title', dataIndex: 'title' },
            { title: 'Source', dataIndex: 'source' },
            { title: 'Link', render: (_, r) => (r?.url ? <Link href={r.url} target="_blank">open</Link> : <Text type="secondary">n/a</Text>) },
          ]}
          locale={{ emptyText: 'No urgent news currently' }}
          pagination={false}
        />
      </Panel>

      <Panel title="Latest News">
        <Table
          size="small"
          rowKey="event_uid"
          dataSource={latest}
          expandable={{
            expandedRowRender: (r) => {
              const a = analysisMap[r.event_uid]
              return (
                <Space direction="vertical">
                  <Text>Event: {r.event_uid}</Text>
                  <Text>Title: {r.title}</Text>
                  <Text>Summary: {r.summary || 'n/a'}</Text>
                  <Link href={r.url} target="_blank">Open source link</Link>
                  <Text>Sentiment score: {r.sentiment_score}</Text>
                  <Text>Impact: {a?.impact_direction || 'n/a'} | Confidence: {a?.confidence ?? 'n/a'}</Text>
                </Space>
              )
            },
          }}
          columns={[
            { title: 'Time', dataIndex: 'published_at' },
            { title: 'Title', dataIndex: 'title' },
            { title: 'Source', dataIndex: 'source' },
            { title: 'Sentiment', dataIndex: 'sentiment_score' },
          ]}
          pagination={{ pageSize: 10 }}
        />
      </Panel>
    </Space>
  )
}

function MarketTab() {
  const [symbol, setSymbol] = useState('BTCUSDT')
  const [timeframe, setTf] = useState(defaultChartConfig.timeframes[1])
  const { loading, data, error, reload } = useLoad(() => api.market(symbol, timeframe), [symbol, timeframe], 15000)
  if (loading) return <LoadingBlock tip="Loading market data" />
  if (error) return <ErrorBlock error={error} />
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Space>
        <Select value={symbol} onChange={setSymbol} options={[{ value: 'BTCUSDT' }, { value: 'ETHUSDT' }]} style={{ width: 140 }} />
        <Select value={timeframe} onChange={setTf} options={defaultChartConfig.timeframes.map((v) => ({ value: v }))} style={{ width: 120 }} />
        <Button size="small" onClick={reload}>Refresh</Button>
        <Text type="secondary">Auto refresh: 15s</Text>
      </Space>
      <Panel title="TradingView (Candles + Indicators)">
        <TradingViewChart symbol={symbol} timeframe={timeframe} />
      </Panel>
      <Panel title="Indicators (persisted)">
        <Table size="small" rowKey={(r) => `${r.ts}-${r.indicator_name}`} dataSource={data?.indicators || []} columns={[{ title: 'ts', dataIndex: 'ts' }, { title: 'name', dataIndex: 'indicator_name' }, { title: 'value', dataIndex: 'indicator_value' }]} pagination={{ pageSize: 10 }} locale={{ emptyText: 'Indicators are being collected, please wait ~1-2 minutes.' }} />
      </Panel>
    </Space>
  )
}

function StrategyTab() {
  const main = useLoad(api.strategy, [], 15000)
  const portfolio = useLoad(api.portfolioSummary, [], 15000)
  const decisions = useLoad(api.portfolioDecisions, [], 15000)

  const loading = main.loading || portfolio.loading || decisions.loading
  const error = main.error || portfolio.error || decisions.error
  const reload = () => { main.reload(); portfolio.reload(); decisions.reload() }

  const data = main.data
  const candidates = data?.candidates || []
  const optimized = data?.optimized || []

  const groups = useMemo(() => {
    const g = {}
    for (const c of candidates) {
      const id = c.strategy_id || 'unknown'
      let spec = c.spec_json
      if (typeof spec === 'string') {
        try { spec = JSON.parse(spec) } catch (_) { spec = {} }
      }
      const withSpec = { ...c, spec_json: spec }
      if (!g[id]) g[id] = { strategy_id: id, name: c.name, template_type: c.template_type, versions: [], optimizations: [] }
      g[id].versions.push(withSpec)
    }
    for (const o of optimized) {
      const id = o.strategy_id || 'unknown'
      if (!g[id]) g[id] = { strategy_id: id, name: '', template_type: '', versions: [], optimizations: [] }
      g[id].optimizations.push(o)
    }
    return Object.values(g).map((x) => ({
      ...x,
      versions: x.versions.sort((a, b) => (a.strategy_version || 0) - (b.strategy_version || 0)),
      latest_version: Math.max(0, ...x.versions.map((v) => v.strategy_version || 0)),
      optimize_count: x.optimizations.length,
    }))
  }, [candidates, optimized])

  if (loading) return <LoadingBlock tip="Loading strategy" />
  if (error) return <ErrorBlock error={error} />

  const ps = portfolio.data || {}

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Panel title="组合池总览（core_multi_asset_v1）" extra={<Space><Text type="secondary">Auto refresh: 15s</Text><Button size="small" onClick={reload}>Refresh</Button></Space>}>
        <Row gutter={12}>
          <Col span={8}><Card><Text type="secondary">组合收益</Text><Title level={4}>{ps.portfolio_return ?? 0}</Title></Card></Col>
          <Col span={8}><Card><Text type="secondary">组合回撤</Text><Title level={4}>{ps.portfolio_drawdown ?? 0}</Title></Card></Col>
          <Col span={8}><Card><Text type="secondary">组合Sharpe</Text><Title level={4}>{ps.portfolio_sharpe ?? 0}</Title></Card></Col>
        </Row>
        <Table
          size="small"
          rowKey="strategy_id"
          dataSource={ps.strategies || []}
          columns={[
            { title: 'strategy', dataIndex: 'strategy_id' },
            { title: 'version', dataIndex: 'latest_version' },
            { title: 'return', dataIndex: 'total_return' },
            { title: 'max_dd', dataIndex: 'max_drawdown' },
            { title: 'sharpe', dataIndex: 'sharpe' },
            { title: 'weight_suggest', dataIndex: 'weight_suggest' },
          ]}
          pagination={false}
        />
      </Panel>

      <Panel title="组合相关性热力图">
        <PortfolioCorrelationHeatmap labels={ps?.correlation?.labels || []} matrix={ps?.correlation?.matrix || []} />
      </Panel>

      <Panel title="组合决策日志（OpenViking Memory）">
        <Table
          size="small"
          rowKey={(r, i) => `${r.memory_key}-${r.created_at}-${i}`}
          dataSource={decisions.data?.items || []}
          columns={[
            { title: 'time', dataIndex: 'created_at' },
            { title: 'strategy', dataIndex: 'memory_key' },
            { title: 'category', dataIndex: 'category' },
            { title: 'decision', render: (_, r) => {
              let c = r.content_json
              if (typeof c === 'string') {
                try { c = JSON.parse(c) } catch (_) { c = {} }
              }
              return <Text ellipsis style={{ maxWidth: 560 }}>{c?.spec?.reason_cn || c?.spec?.next_actions_cn || JSON.stringify(c || {})}</Text>
            } },
          ]}
          pagination={{ pageSize: 6 }}
        />
      </Panel>

      <Panel title="Strategy Evolution Overview" extra={<Space><Text type="secondary">Auto refresh: 15s</Text><Button size="small" onClick={reload}>Refresh</Button></Space>}>
        <StrategyEvolutionChart groups={groups} />
      </Panel>
      <Panel title="Strategy Version Timeline">
        <StrategyTimelineChart groups={groups} />
      </Panel>

      <Panel title="Strategy Groups (logic + grid-search iterations)">
        <Table
          size="small"
          rowKey="strategy_id"
          dataSource={groups}
          expandable={{
            expandedRowRender: (r) => (
              <Space direction="vertical" style={{ width: '100%' }}>
                <Text strong>进化说明（中文）</Text>
                <Text>
                  {`该策略是组合池(core_multi_asset_v1)中的子策略，当前版本范围 v1 -> v${r.latest_version}。`}
                  {`优化记录数 ${r.optimize_count} 指的是该策略在验证表中累计的优化/验证条目（如 grid_search、stress 等），不是等于收益一定提升的次数。`}
                </Text>
                <Text>
                  {`策略含义：${r.template_type === 'trend_momentum' ? '趋势动量：跟随中期趋势，回避逆势交易。' : r.template_type === 'mean_reversion' ? '均值回归：价格偏离均值后博弈回归。' : '突破波动：在波动放大与关键位突破时参与。'}`}
                </Text>
                <Text strong>单策略参数/表现图</Text>
                <StrategyPerformanceChart versions={r.versions} optimizations={r.optimizations} />
                <Text strong>Versions</Text>
                <Table
                  size="small"
                  pagination={false}
                  rowKey={(x, i) => `${r.strategy_id}-${x.strategy_version}-${i}`}
                  dataSource={r.versions}
                  columns={[
                    { title: 'version', dataIndex: 'strategy_version' },
                    { title: 'window_start', dataIndex: 'effective_window_start' },
                    { title: 'window_end', dataIndex: 'effective_window_end' },
                    { title: 'spec', render: (_, x) => <Text ellipsis style={{ maxWidth: 320 }}>{JSON.stringify(x.spec_json || {})}</Text> },
                    { title: 'risk', render: (_, x) => <Text ellipsis style={{ maxWidth: 220 }}>{JSON.stringify(x.risk_json || {})}</Text> },
                  ]}
                />
                <Text strong>Optimizations (including grid-search)</Text>
                <Table
                  size="small"
                  pagination={false}
                  rowKey={(x, i) => `${r.strategy_id}-opt-${i}-${x.created_at}`}
                  dataSource={r.optimizations}
                  columns={[
                    { title: 'version', dataIndex: 'strategy_version' },
                    { title: 'action', dataIndex: 'optimization_action' },
                    { title: 'status', dataIndex: 'status' },
                    { title: 'summary', render: (_, x) => <Text ellipsis style={{ maxWidth: 360 }}>{typeof x.summary_json === 'object' ? JSON.stringify(x.summary_json) : String(x.summary_json || '')}</Text> },
                  ]}
                />
              </Space>
            ),
          }}
          columns={[
            { title: 'strategy_id', dataIndex: 'strategy_id' },
            { title: 'name', dataIndex: 'name' },
            { title: 'template', dataIndex: 'template_type' },
            { title: 'latest_version', dataIndex: 'latest_version' },
            { title: 'optimization_count', dataIndex: 'optimize_count' },
          ]}
          locale={{ emptyText: 'No strategy groups yet' }}
          pagination={{ pageSize: 8 }}
        />
      </Panel>
    </Space>
  )
}

function BacktestTab() {
  const { loading, data, error, reload } = useLoad(api.backtest, [], 15000)
  if (loading) return <LoadingBlock tip="Loading backtest" />
  if (error) return <ErrorBlock error={error} />

  const backtests = data?.backtests || []
  const paper = data?.paper || []
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Panel title="Backtest Runs" extra={<Space><Text type="secondary">Auto refresh: 15s</Text><Button size="small" onClick={reload}>Refresh</Button></Space>}>
        <Table
          size="small"
          rowKey={(r, i) => r.run_id || `b-${i}`}
          dataSource={backtests}
          columns={[
            { title: 'run_id', dataIndex: 'run_id' },
            { title: 'strategy', dataIndex: 'strategy_id' },
            { title: 'version', dataIndex: 'strategy_version' },
            { title: 'status', dataIndex: 'status' },
            { title: 'return', dataIndex: 'total_return' },
            { title: 'sharpe', dataIndex: 'sharpe' },
            { title: 'max_dd', dataIndex: 'max_drawdown' },
          ]}
          locale={{ emptyText: 'No backtest runs yet' }}
          pagination={{ pageSize: 8 }}
        />
      </Panel>
      <Panel title="Paper Trading Windows">
        <Table
          size="small"
          rowKey={(r, i) => r.run_id || `p-${i}`}
          dataSource={paper}
          columns={[
            { title: 'run_id', dataIndex: 'run_id' },
            { title: 'strategy', dataIndex: 'strategy_id' },
            { title: 'window_end', dataIndex: 'window_end' },
            { title: 'status', dataIndex: 'status' },
            { title: 'pnl', dataIndex: 'pnl' },
            { title: 'max_dd', dataIndex: 'max_drawdown' },
            { title: 'win_rate', dataIndex: 'win_rate' },
          ]}
          locale={{ emptyText: 'No paper trading records yet' }}
          pagination={{ pageSize: 8 }}
        />
      </Panel>
    </Space>
  )
}

function TokenTab() {
  const { loading, data, error, reload } = useLoad(api.tokenUsage, [], 20000)
  if (loading) return <LoadingBlock tip="Loading token usage" />
  if (error) return <ErrorBlock error={error} />
  const items = data?.items || []
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Panel title="Token Usage by Agent (estimated)" extra={<Space><Text type="secondary">Auto refresh: 20s</Text><Button size="small" onClick={reload}>Refresh</Button></Space>}>
        <Table
          size="small"
          rowKey="agent"
          dataSource={items}
          columns={[
            { title: 'agent', dataIndex: 'agent' },
            { title: 'events(24h)', dataIndex: 'events' },
            { title: 'tokens(estimated)', dataIndex: 'tokens' },
            { title: 'share', render: (_, r) => `${((r.share || 0) * 100).toFixed(1)}%` },
          ]}
          pagination={false}
        />
      </Panel>
      <Alert type="info" showIcon message={`24h total estimated tokens: ${data?.total_tokens || 0}`} description={data?.note} />
    </Space>
  )
}

function SystemTab() {
  const streams = useLoad(api.streams, [], 10000)
  const deps = useLoad(api.sysDeps, [], 10000)
  if (streams.loading || deps.loading) return <LoadingBlock tip="Loading streams" />
  if (streams.error) return <ErrorBlock error={streams.error} />
  if (deps.error) return <ErrorBlock error={deps.error} />
  const items = streams.data?.items || []
  const hasErr = items.some((x) => x.error)
  const totalLength = items.reduce((s, x) => s + (x.length || 0), 0)
  const totalPending = items.reduce((s, x) => s + (x.pending || 0), 0)
  const totalConsumers = items.reduce((s, x) => s + (x.consumers || 0), 0)

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      {hasErr ? <Alert type="warning" message="Some streams have errors (infra redis connectivity or stream init)." showIcon /> : null}
      {!items.length ? <Alert type="info" showIcon message="No stream stats yet" description="等待 agent 写入 redis stream 后这里会出现具体统计。" /> : null}
      <Row gutter={12}>
        <Col span={6}><Card><Text type="secondary">Total Stream Length</Text><Title level={4}>{totalLength}</Title></Card></Col>
        <Col span={6}><Card><Text type="secondary">Total Pending</Text><Title level={4}>{totalPending}</Title></Card></Col>
        <Col span={6}><Card><Text type="secondary">Total Consumers</Text><Title level={4}>{totalConsumers}</Title></Card></Col>
        <Col span={6}><Card><Text type="secondary">Deps</Text><Title level={4}>{deps.data?.ok ? 'OK' : 'WARN'}</Title><Text>mysql:{String(deps.data?.mysql)} redis:{String(deps.data?.redis)}</Text></Card></Col>
      </Row>
      <Panel title="Stream backlog (ECharts)"><StreamsChart items={items} /></Panel>
      <Panel title="Streams table"><Table size="small" rowKey="stream" dataSource={items} columns={[{ title: 'stream', dataIndex: 'stream' }, { title: 'length', dataIndex: 'length' }, { title: 'pending', dataIndex: 'pending' }, { title: 'consumers', dataIndex: 'consumers' }, { title: 'error', dataIndex: 'error' }]} pagination={false} /></Panel>
    </Space>
  )
}

export default function App() {
  return (
    <ConfigProvider theme={appleLikeTheme}>
      <Layout style={{ minHeight: '100vh', background: '#F5F7FA' }}>
        <Header style={{ background: '#fff', borderBottom: '1px solid #eee' }}>
          <Title level={4} style={{ margin: 0 }}>crypto-intel dashboard</Title>
        </Header>
        <Content style={{ padding: 16 }}>
          <Tabs
            items={[
              { key: 'overview', label: 'Overview', children: <OverviewTab /> },
              { key: 'news', label: 'News', children: <NewsTab /> },
              { key: 'market', label: 'Market Data', children: <MarketTab /> },
              { key: 'strategy', label: 'Strategy', children: <StrategyTab /> },
              { key: 'backtest', label: 'Backtest', children: <BacktestTab /> },
              { key: 'token', label: 'Token Usage', children: <TokenTab /> },
              { key: 'system', label: 'System', children: <SystemTab /> },
            ]}
          />
        </Content>
      </Layout>
    </ConfigProvider>
  )
}
