import React, { useEffect, useState } from 'react'
import { Alert, Card, Col, Layout, Row, Select, Space, Spin, Table, Tabs, Tag, Typography } from 'antd'
import { api } from './api'

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
  if (loading) return <Spin />
  if (error) return <Alert type="error" message={error} />
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
  if (loading) return <Spin />
  if (error) return <Alert type="error" message={error} />
  return (
    <Row gutter={[12, 12]}>
      <Col span={24}><Panel title="Urgent News"><Table size="small" rowKey="event_uid" dataSource={data?.urgent || []} columns={[{title:'Level',dataIndex:'alert_level'},{title:'Title',dataIndex:'title'},{title:'Source',dataIndex:'source'}]} pagination={false} /></Panel></Col>
      <Col span={24}><Panel title="Latest News"><Table size="small" rowKey="event_uid" dataSource={data?.latest || []} columns={[{title:'Time',dataIndex:'published_at'},{title:'Title',dataIndex:'title'},{title:'Sentiment',dataIndex:'sentiment_score'}]} pagination={false} /></Panel></Col>
    </Row>
  )
}

function MarketTab() {
  const [symbol, setSymbol] = useState('BTCUSDT')
  const [timeframe, setTf] = useState('1h')
  const { loading, data, error } = useLoad(() => api.market(symbol, timeframe), [symbol, timeframe])
  if (loading) return <Spin />
  if (error) return <Alert type="error" message={error} />
  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Space>
        <Select value={symbol} onChange={setSymbol} options={[{value:'BTCUSDT'},{value:'ETHUSDT'}]} style={{width:140}} />
        <Select value={timeframe} onChange={setTf} options={[{value:'15m'},{value:'1h'},{value:'4h'},{value:'1d'}]} style={{width:120}} />
      </Space>
      <Alert type="info" message="TradingView chart integration pending (Phase 7.2). Current view uses tabular fallback." />
      <Panel title="Candles (fallback table)">
        <Table size="small" rowKey={(r)=>`${r.ts}`} dataSource={data?.candles || []} columns={[{title:'ts',dataIndex:'ts'},{title:'open',dataIndex:'open'},{title:'high',dataIndex:'high'},{title:'low',dataIndex:'low'},{title:'close',dataIndex:'close'}]} pagination={{pageSize:10}} />
      </Panel>
      <Panel title="Indicators (persisted)">
        <Table size="small" rowKey={(r)=>`${r.ts}-${r.indicator_name}`} dataSource={data?.indicators || []} columns={[{title:'ts',dataIndex:'ts'},{title:'name',dataIndex:'indicator_name'},{title:'value',dataIndex:'indicator_value'}]} pagination={{pageSize:10}} />
      </Panel>
    </Space>
  )
}

function StrategyTab() { return <Panel title="Strategy"><Text>Strategy panel scaffold ready.</Text></Panel> }
function BacktestTab() { return <Panel title="Backtest"><Text>Backtest panel scaffold ready.</Text></Panel> }

function SystemTab() {
  const { loading, data, error } = useLoad(api.streams, [])
  if (loading) return <Spin />
  if (error) return <Alert type="error" message={error} />
  return <Panel title="Streams"><Table size="small" rowKey="stream" dataSource={data?.items || []} columns={[{title:'stream',dataIndex:'stream'},{title:'length',dataIndex:'length'},{title:'pending',dataIndex:'pending'},{title:'consumers',dataIndex:'consumers'}]} pagination={false} /></Panel>
}

export default function App() {
  return (
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
  )
}
