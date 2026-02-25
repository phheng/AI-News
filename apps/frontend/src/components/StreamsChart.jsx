import React from 'react'
import ReactECharts from 'echarts-for-react'

export default function StreamsChart({ items = [] }) {
  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: items.map((x) => x.stream.replace('crypto-intel:stream:', '')) },
    yAxis: { type: 'value' },
    series: [
      {
        name: 'length',
        type: 'bar',
        data: items.map((x) => x.length || 0),
        itemStyle: { borderRadius: [4, 4, 0, 0] },
      },
    ],
    grid: { left: 40, right: 20, bottom: 80, top: 30 },
  }
  return <ReactECharts option={option} style={{ height: 320 }} />
}
