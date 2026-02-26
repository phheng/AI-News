import React from 'react'
import ReactECharts from 'echarts-for-react'

export default function StrategyTimelineChart({ groups = [] }) {
  const all = []
  for (const g of groups) {
    for (const v of g.versions || []) {
      all.push({
        strategy_id: g.strategy_id,
        x: v.created_at || v.effective_window_start || '',
        y: v.strategy_version || 0,
      })
    }
  }

  const sorted = all.sort((a, b) => String(a.x).localeCompare(String(b.x)))
  const xAxis = [...new Set(sorted.map((x) => x.x || 'unknown'))]

  const series = groups.map((g) => {
    const map = {}
    for (const v of g.versions || []) {
      const x = v.created_at || v.effective_window_start || 'unknown'
      map[x] = v.strategy_version || 0
    }
    return {
      name: g.strategy_id,
      type: 'line',
      data: xAxis.map((x) => (map[x] == null ? null : map[x])),
      connectNulls: true,
      smooth: true,
    }
  })

  const option = {
    tooltip: { trigger: 'axis' },
    legend: { type: 'scroll' },
    xAxis: { type: 'category', data: xAxis },
    yAxis: { type: 'value', name: 'strategy_version', minInterval: 1 },
    series,
    grid: { left: 50, right: 30, bottom: 80, top: 40 },
  }

  return <ReactECharts option={option} style={{ height: 340 }} />
}
