import os


class Settings:
    app_env: str = os.getenv("CRYPTO_INTEL_APP_ENV", "dev")
    mysql_host: str = os.getenv("CRYPTO_INTEL_MYSQL_HOST", "127.0.0.1")
    mysql_port: int = int(os.getenv("CRYPTO_INTEL_MYSQL_PORT", "3306"))
    mysql_user: str = os.getenv("CRYPTO_INTEL_MYSQL_USER", "root")
    mysql_password: str = os.getenv("CRYPTO_INTEL_MYSQL_PASSWORD", "")
    mysql_database: str = os.getenv("CRYPTO_INTEL_MYSQL_DATABASE", "crypto_intel")
    redis_url: str = os.getenv("CRYPTO_INTEL_REDIS_URL", "redis://127.0.0.1:6379/0")

    news_agent_base: str = os.getenv("CRYPTO_INTEL_NEWS_AGENT_BASE", "http://127.0.0.1:18101")
    market_agent_base: str = os.getenv("CRYPTO_INTEL_MARKET_AGENT_BASE", "http://127.0.0.1:18102")
    strategy_agent_base: str = os.getenv("CRYPTO_INTEL_STRATEGY_AGENT_BASE", "http://127.0.0.1:18103")
    backtest_agent_base: str = os.getenv("CRYPTO_INTEL_BACKTEST_AGENT_BASE", "http://127.0.0.1:18104")
    gateway_timeout_sec: float = float(os.getenv("CRYPTO_INTEL_GATEWAY_TIMEOUT_SEC", "3.0"))


settings = Settings()
