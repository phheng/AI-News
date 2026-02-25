from fastapi import FastAPI

from .deps_health import check_mysql, check_redis
from .settings import settings

app = FastAPI(title="crypto-intel-api-gateway", version="0.1.0")


def _mysql_dsn() -> str:
    return (
        f"mysql+pymysql://{settings.mysql_user}:{settings.mysql_password}"
        f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}?charset=utf8mb4"
    )


@app.get('/healthz')
def healthz():
    return {"ok": True, "service": "crypto-intel-api-gateway"}


@app.get('/healthz/deps')
def healthz_deps():
    mysql_ok = False
    redis_ok = False
    errors = []
    try:
        mysql_ok = check_mysql(_mysql_dsn())
    except Exception as e:
        errors.append(f"mysql: {e}")

    try:
        redis_ok = check_redis(settings.redis_url)
    except Exception as e:
        errors.append(f"redis: {e}")

    return {
        "ok": mysql_ok and redis_ok,
        "mysql": mysql_ok,
        "redis": redis_ok,
        "errors": errors,
    }


@app.get('/readyz')
def readyz():
    return {"ok": True}


@app.get('/version')
def version():
    return {"version": "0.1.0", "env": settings.app_env}


@app.get('/v1/dashboard/overview')
def dashboard_overview():
    return {"ok": True, "data": {"agents": 4, "status": "bootstrap"}}


@app.get('/v1/dashboard/news')
def dashboard_news():
    return {"ok": True, "data": {"urgent": [], "latest": []}}


@app.get('/v1/dashboard/market')
def dashboard_market():
    return {
        "ok": True,
        "data": {
            "default_timeframes": ["15m", "1h", "4h", "1d"],
            "default_indicators": ["EMA20", "EMA50", "EMA200", "BOLL", "RSI14", "MACD", "VOLUME"],
        },
    }


@app.get('/v1/dashboard/strategy')
def dashboard_strategy():
    return {"ok": True, "data": {"candidates": [], "optimized": []}}


@app.get('/v1/dashboard/backtest')
def dashboard_backtest():
    return {"ok": True, "data": {"backtests": [], "paper": []}}
