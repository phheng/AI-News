import React, { useEffect, useRef } from 'react'

const TF_MAP = {
  '15m': '15',
  '1h': '60',
  '4h': '240',
  '1d': 'D',
}

export default function TradingViewChart({ symbol = 'BTCUSDT', timeframe = '1h' }) {
  const containerRef = useRef(null)

  useEffect(() => {
    const container = containerRef.current
    if (!container) return
    container.innerHTML = ''

    const script = document.createElement('script')
    script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js'
    script.type = 'text/javascript'
    script.async = true
    script.innerHTML = JSON.stringify({
      autosize: true,
      symbol: `BYBIT:${symbol}.P`,
      interval: TF_MAP[timeframe] || '60',
      timezone: 'Asia/Shanghai',
      theme: 'light',
      style: '1',
      locale: 'en',
      hide_top_toolbar: false,
      hide_legend: false,
      withdateranges: true,
      allow_symbol_change: true,
      studies: [
        'MASimple@tv-basicstudies',
        'BB@tv-basicstudies',
        'RSI@tv-basicstudies',
        'MACD@tv-basicstudies',
      ],
      support_host: 'https://www.tradingview.com',
    })
    container.appendChild(script)
  }, [symbol, timeframe])

  return (
    <div style={{ height: 460, width: '100%' }}>
      <div className="tradingview-widget-container" ref={containerRef} style={{ height: '100%', width: '100%' }} />
    </div>
  )
}
