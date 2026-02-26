import React, { useEffect, useMemo, useState } from 'react'
import { Card, Col, ConfigProvider, Layout, Row, Select, Space, Table, Tabs, Tag, Typography, Button, Alert } from 'antd'
import { api } from './api'
import TradingViewChart from './components/TradingViewChart'
import StreamsChart from './components/StreamsChart'
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
  if (loading) return <LoadingBlock tip="Loading news" />
  if (error) return <ErrorBlock error={error} />

  const latest = data?.latest || []
  const urgent = data?.urgent || []
  const analysis = data?.analysis || []
  const analysisMap = useMemo(() => {
    const m = {}
    for (const a of analysis) m[a.event_uid] = a
    return m
  }, [analysis])

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
  const { loading, data, error, reload } = useLoad(api.strategy, [], 15000)
  if (loading) return <LoadingBlock tip="Loading strategy" />
  if (error) return <ErrorBlock error={error} />
  const candidates = data?.candidates || []
  const optimized = data?.optimized || []

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Panel title="Strategy Candidates" extra={<Space><Text type="secondary">Auto refresh: 15s</Text><Button size="small" onClick={reload}>Refresh</Button></Space>}>
        <Table
          size="small"
          rowKey={(r, i) => r.strategy_id ? `${r.strategy_id}-${r.strategy_version}-${i}` : `c-${i}`}
          dataSource={candidates}
          expandable={{
            expandedRowRender: (r) => (
              <Space direction="vertical" style={{ width: '100%' }}>
                <Text>Spec: <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(r.spec_json, null, 2)}</pre></Text>
                <Text>Risk: <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(r.risk_json, null, 2)}</pre></Text>
                <Text>Anti liquidation: <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(r.anti_liquidation_json, null, 2)}</pre></Text>
              </Space>
            ),
          }}
          columns={[
            { title: 'strategy_id', dataIndex: 'strategy_id' },
            { title: 'version', dataIndex: 'strategy_version' },
            { title: 'name', dataIndex: 'name' },
            { title: 'template', dataIndex: 'template_type' },
            { title: 'window_start', dataIndex: 'effective_window_start' },
            { title: 'window_end', dataIndex: 'effective_window_end' },
          ]}
          locale={{ emptyText: 'No strategy candidates yet' }}
          pagination={{ pageSize: 8 }}
        />
      </Panel>
      <Panel title="Optimized Strategies">
        <Table
          size="small"
          rowKey={(r, i) => r.strategy_id ? `${r.strategy_id}-${r.strategy_version}-${r.created_at}-${i}` : `o-${i}`}
          dataSource={optimized}
          columns={[
            { title: 'strategy_id', dataIndex: 'strategy_id' },
            { title: 'version', dataIndex: 'strategy_version' },
            { title: 'action', dataIndex: 'optimization_action' },
            { title: 'status', dataIndex: 'status' },
            { title: 'summary', render: (_, r) => <Text ellipsis style={{ maxWidth: 300 }}>{typeof r.summary_json === 'object' ? JSON.stringify(r.summary_json) : String(r.summary_json || '')}</Text> },
            { title: 'created_at', dataIndex: 'created_at' },
          ]}
          locale={{ emptyText: 'No optimized records yet' }}
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
  const { loading, data, error } = useLoad(api.streams, [], 10000)
  if (loading) return <LoadingBlock tip="Loading streams" />
  if (error) return <ErrorBlock error={error} />
  const hasErr = (data?.items || []).some((x) => x.error)
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      {hasErr ? <Alert type="warning" message="Some streams have errors (infra redis connectivity or stream init)." showIcon /> : null}
      <Panel title="Stream backlog (ECharts)"><StreamsChart items={data?.items || []} /></Panel>
      <Panel title="Streams table"><Table size="small" rowKey="stream" dataSource={data?.items || []} columns={[{ title: 'stream', dataIndex: 'stream' }, { title: 'length', dataIndex: 'length' }, { title: 'pending', dataIndex: 'pending' }, { title: 'consumers', dataIndex: 'consumers' }, { title: 'error', dataIndex: 'error' }]} pagination={false} /></Panel>
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
