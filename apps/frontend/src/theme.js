import { theme } from 'antd'

export const defaultChartConfig = {
  timeframes: ['15m', '1h', '4h', '1d'],
  indicators: ['EMA20', 'EMA50', 'EMA200', 'BOLL', 'RSI14', 'MACD', 'VOLUME'],
}

export const appleLikeTheme = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorBgBase: '#F5F7FA',
    colorTextBase: '#1D1D1F',
    colorPrimary: '#3B82F6',
    borderRadius: 14,
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Inter, Roboto, Arial, sans-serif",
  },
  components: {
    Card: {
      borderRadiusLG: 14,
    },
    Tabs: {
      itemSelectedColor: '#1D1D1F',
      inkBarColor: '#3B82F6',
    },
  },
}
