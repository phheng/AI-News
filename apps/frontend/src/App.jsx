import React, { useEffect, useState } from 'react'
import { Alert, Card, Col, ConfigProvider, Layout, Row, Select, Space, Table, Tabs, Tag, Typography } from 'antd'
import { api } from './api'
import TradingViewChart from './components/TradingViewChart'
import StreamsChart from './components/StreamsChart'
import { EmptyBlock, ErrorBlock, LoadingBlock } from './components/StateBlock'
import { appleLikeTheme, defaultChartConfig } from './theme'

const { Header, Content } = Layout
const { Title, Text } = Typography

function useLoad(fn, deps = []) {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  useEffect(() => {
    let on = true
    setLoading(true)
    setError(null)
    fn()
      .then((r) => on && setData(r.data || r))
      .catch((e) => on && setError(String(e)))
      .finally(() => on && setLoading(false))
    return () => {
      on = false
    }
  }, deps)
  return { loading, data, error }
}

function Panel({ title, children }) {
  return <Card title={title} style={{ borderRadius: 14 }}>{children}</Card>
}

function OverviewTab() {
  const { loading, data, error } = useLoad(api.overview, [])
  if (loading) return <LoadingBlock tip="Loading overview" />
  if (error) return <ErrorBlock error={error} />
  const agents = data?.agents || {}
  return (
    <Panel title="System Overview">
      <Space>
        {Object.entries(agents).map(([k, ok]) => <Tag key={k} color={ok ? 'green' : 'red'}>{k}:{ok ? 'up' : 'down'}</Tag>)}
      </Space>
    </Panel>
  )
}

function NewsTab() {
  const { loading, data, error } = useLoad(api.news, [])
  if (loading) return <LoadingBlock tip="Loading news" />
  if (error) return <ErrorBlock error={error} />
  if (!data?.latest?.length && !data?.urgent?.length) return <EmptyBlock desc="No news data" />
  return (
    <Row gutter={[12, 12]}>
      <Col span={24}><Panel title="Urgent News"><Table size="small" rowKey="event_uid" dataSource={data?.urgent || []} columns={[{title:'Level',dataIndex:'alert_level'},{title:'Title',dataIndex:'title'},{title:'Source',dataIndex:'source'}]} pagination={false} /></Panel></Col>
      <Col span={24}><Panel title="Latest News"><Table size="small" rowKey="event_uid" dataSource={data?.latest || []} columns={[{title:'Time',dataIndex:'published_at'},{title:'Title',dataIndex:'title'},{title:'Sentiment',dataIndex:'sentiment_score'}]} pagination={false} /></Panel></Col>
    </Row>
  )
}

function MarketTab() {
  const [symbol, setSymbol] = useState('BTCUSDT')
  const [timeframe, setTf] = useState(defaultChartConfig.timeframes[1])
  const { loading, data, error } = useLoad(() => api.market(symbol, timeframe), [symbol, timeframe])
  if (loading) return <LoadingBlock tip="Loading market data" />
  if (error) return <ErrorBlock error={error} />
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Space>
        <Select value={symbol} onChange={setSymbol} options={[{value:'BTCUSDT'},{value:'ETHUSDT'}]} style={{width:140}} />
        <Select value={timeframe} onChange={setTf} options={defaultChartConfig.timeframes.map((v)=>({value:v}))} style={{width:120}} />
      </Space>
      <Panel title="TradingView (Candles + Indicators)">
        <TradingViewChart symbol={symbol} timeframe={timeframe} />
      </Panel>
      <Panel title="Indicators (persisted)">
        <Table size="small" rowKey={(r)=>`${r.ts}-${r.indicator_name}`} dataSource={data?.indicators || []} columns={[{title:'ts',dataIndex:'ts'},{title:'name',dataIndex:'indicator_name'},{title:'value',dataIndex:'indicator_value'}]} pagination={{pageSize:10}} />
      </Panel>
    </Space>
  )
}

function StrategyTab() {
  const { loading, data, error } = useLoad(api.strategy, [])
  if (loading) return <LoadingBlock tip="Loading strategy" />
  if (error) return <ErrorBlock error={error} />
  const candidates = data?.candidates || []
  const optimized = data?.optimized || []
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Panel title="Strategy Candidates">
        {candidates.length ? (
          <Table
            size="small"
            rowKey={(r, i) => r.strategy_id || `c-${i}`}
            dataSource={candidates}
            columns={[
              { title: 'strategy_id', dataIndex: 'strategy_id' },
              { title: 'version', dataIndex: 'strategy_version' },
              { title: 'summary', dataIndex: 'summary' },
            ]}
            pagination={false}
          />
        ) : (
          <EmptyBlock desc="No strategy candidates yet" />
        )}
      </Panel>
      <Panel title="Optimized Strategies">
        {optimized.length ? (
          <Table
            size="small"
            rowKey={(r, i) => r.strategy_id || `o-${i}`}
            dataSource={optimized}
            columns={[
              { title: 'strategy_id', dataIndex: 'strategy_id' },
              { title: 'version', dataIndex: 'strategy_version' },
              { title: 'action', dataIndex: 'optimization_action' },
            ]}
            pagination={false}
          />
        ) : (
          <EmptyBlock desc="No optimized records yet" />
        )}
      </Panel>
    </Space>
  )
}

function BacktestTab() {
  const { loading, data, error } = useLoad(api.backtest, [])
  if (loading) return <LoadingBlock tip="Loading backtest" />
  if (error) return <ErrorBlock error={error} />

  const backtests = data?.backtests || []
  const paper = data?.paper || []
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Panel title="Backtest Runs">
        {backtests.length ? (
          <Table
            size="small"
            rowKey={(r, i) => r.run_id || `b-${i}`}
            dataSource={backtests}
            columns={[
              { title: 'run_id', dataIndex: 'run_id' },
              { title: 'strategy', dataIndex: 'strategy_id' },
              { title: 'status', dataIndex: 'status' },
            ]}
            pagination={false}
          />
        ) : (
          <EmptyBlock desc="No backtest runs yet" />
        )}
      </Panel>
      <Panel title="Paper Trading Windows">
        {paper.length ? (
          <Table
            size="small"
            rowKey={(r, i) => r.run_id || `p-${i}`}
            dataSource={paper}
            columns={[
              { title: 'run_id', dataIndex: 'run_id' },
              { title: 'window', dataIndex: 'window_end' },
              { title: 'pnl', dataIndex: 'pnl' },
            ]}
            pagination={false}
          />
        ) : (
          <EmptyBlock desc="No paper trading records yet" />
        )}
      </Panel>
    </Space>
  )
}

function SystemTab() {
  const { loading, data, error } = useLoad(api.streams, [])
  if (loading) return <LoadingBlock tip="Loading streams" />
  if (error) return <ErrorBlock error={error} />
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Panel title="Stream backlog (ECharts)"><StreamsChart items={data?.items || []} /></Panel>
      <Panel title="Streams table"><Table size="small" rowKey="stream" dataSource={data?.items || []} columns={[{title:'stream',dataIndex:'stream'},{title:'length',dataIndex:'length'},{title:'pending',dataIndex:'pending'},{title:'consumers',dataIndex:'consumers'}]} pagination={false} /></Panel>
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
              { key: 'system', label: 'System', children: <SystemTab /> },
            ]}
          />
        </Content>
      </Layout>
    </ConfigProvider>
  )
}
