import React from 'react'
import ReactECharts from 'echarts-for-react'

export default function StrategyEvolutionChart({ groups = [] }) {
  const categories = groups.map((g) => g.strategy_id)
  const latestVersion = groups.map((g) => g.latest_version || 0)
  const optimizeCount = groups.map((g) => g.optimize_count || 0)

  const option = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['latest_version', 'optimize_count'] },
    xAxis: { type: 'category', data: categories },
    yAxis: [{ type: 'value', name: 'version' }, { type: 'value', name: 'optimize', splitLine: { show: false } }],
    series: [
      { name: 'latest_version', type: 'bar', data: latestVersion, itemStyle: { borderRadius: [4, 4, 0, 0] } },
      { name: 'optimize_count', type: 'line', yAxisIndex: 1, data: optimizeCount, smooth: true },
    ],
    grid: { left: 40, right: 40, bottom: 60, top: 30 },
  }

  return <ReactECharts option={option} style={{ height: 320 }} />
}
