import os


class Settings:
    app_env: str = os.getenv("CRYPTO_INTEL_APP_ENV", "dev")
    mysql_host: str = os.getenv("CRYPTO_INTEL_MYSQL_HOST", "127.0.0.1")
    mysql_port: int = int(os.getenv("CRYPTO_INTEL_MYSQL_PORT", "3306"))
    mysql_user: str = os.getenv("CRYPTO_INTEL_MYSQL_USER", "root")
    mysql_password: str = os.getenv("CRYPTO_INTEL_MYSQL_PASSWORD", "")
    mysql_database: str = os.getenv("CRYPTO_INTEL_MYSQL_DATABASE", "crypto_intel")
    redis_url: str = os.getenv("CRYPTO_INTEL_REDIS_URL", "redis://127.0.0.1:6379/0")


settings = Settings()
