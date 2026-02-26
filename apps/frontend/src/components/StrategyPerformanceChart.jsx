import React from 'react'
import ReactECharts from 'echarts-for-react'

function toNum(v) {
  const n = Number(v)
  return Number.isFinite(n) ? n : null
}

export default function StrategyPerformanceChart({ versions = [], optimizations = [] }) {
  const vSorted = [...versions].sort((a, b) => (a.strategy_version || 0) - (b.strategy_version || 0))
  const x = vSorted.map((v) => `v${v.strategy_version}`)

  const bestSharpeMap = {}
  for (const o of optimizations || []) {
    let s = o.summary_json
    if (typeof s === 'string') {
      try { s = JSON.parse(s) } catch (_) { s = {} }
    }
    const bs = toNum(s?.best_sharpe)
    if (bs != null) bestSharpeMap[o.strategy_version] = bs
  }

  const sharpe = vSorted.map((v) => bestSharpeMap[v.strategy_version] ?? null)
  const iterCount = vSorted.map((v) => (optimizations || []).filter((o) => o.strategy_version === v.strategy_version).length)

  const option = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['best_sharpe', 'optimization_count'] },
    xAxis: { type: 'category', data: x },
    yAxis: [{ type: 'value', name: 'sharpe' }, { type: 'value', name: 'count', splitLine: { show: false } }],
    series: [
      { name: 'best_sharpe', type: 'line', data: sharpe, smooth: true },
      { name: 'optimization_count', type: 'bar', yAxisIndex: 1, data: iterCount, itemStyle: { opacity: 0.55 } },
    ],
    grid: { left: 40, right: 40, top: 30, bottom: 40 },
  }

  return <ReactECharts option={option} style={{ height: 260 }} />
}
