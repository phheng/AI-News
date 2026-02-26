const BASE = import.meta.env.VITE_GATEWAY_BASE || '/api'

async function getJson(path) {
  const resp = await fetch(`${BASE}${path}`)
  if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`)
  return resp.json()
}

export const api = {
  overview: () => getJson('/v1/dashboard/overview'),
  news: () => getJson('/v1/dashboard/news?limit=20'),
  market: (symbol = 'BTCUSDT', timeframe = '1h') =>
    getJson(`/v1/dashboard/market?symbol=${symbol}&timeframe=${timeframe}`),
  strategy: () => getJson('/v1/dashboard/strategy'),
  backtest: () => getJson('/v1/dashboard/backtest'),
  streams: () => getJson('/v1/system/streams'),
  sysDeps: () => getJson('/healthz/deps'),
  tokenUsage: () => getJson('/v1/dashboard/token-usage')
}
