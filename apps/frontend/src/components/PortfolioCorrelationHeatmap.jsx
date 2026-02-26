import React from 'react'
import ReactECharts from 'echarts-for-react'

export default function PortfolioCorrelationHeatmap({ labels = [], matrix = [] }) {
  const data = []
  for (let i = 0; i < labels.length; i += 1) {
    for (let j = 0; j < labels.length; j += 1) {
      data.push([i, j, matrix?.[i]?.[j] ?? 0])
    }
  }

  const option = {
    tooltip: { position: 'top' },
    xAxis: { type: 'category', data: labels, splitArea: { show: true }, axisLabel: { rotate: 20 } },
    yAxis: { type: 'category', data: labels, splitArea: { show: true } },
    visualMap: { min: -1, max: 1, calculable: true, orient: 'horizontal', left: 'center', bottom: 0 },
    series: [{ name: 'corr', type: 'heatmap', data, label: { show: true, formatter: ({ value }) => Number(value[2]).toFixed(2) } }],
    grid: { top: 20, bottom: 60, left: 90, right: 20 },
  }
  return <ReactECharts option={option} style={{ height: 340 }} />
}
