import React from 'react'
import { Alert, Empty, Spin } from 'antd'

export function LoadingBlock({ tip = 'Loading...' }) {
  return <Spin tip={tip} />
}

export function ErrorBlock({ error }) {
  return <Alert type="error" message={String(error)} showIcon />
}

export function EmptyBlock({ desc = 'No data' }) {
  return <Empty description={desc} />
}
