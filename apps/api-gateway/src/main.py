from fastapi import FastAPI
from pydantic import BaseModel

from .deps_health import check_mysql, check_redis
from .settings import settings

app = FastAPI(title="crypto-intel-api-gateway", version="0.1.0")


class TelegramCycleNotifyRequest(BaseModel):
    to: str
    strategy_id: str
    strategy_version: int
    backtest_summary: str
    paper_summary: str
    optimization_action: str
    next_window: str
    risk_notice: str


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


@app.post('/v1/notify/telegram/strategy-cycle')
def notify_strategy_cycle(req: TelegramCycleNotifyRequest):
    # Dispatch wiring to message tool/service bus will be added in next step.
    # This endpoint defines the contract and idempotent envelope first.
    return {
        "ok": True,
        "data": {
            "template": "strategy_cycle_summary_v1",
            "to": req.to,
            "strategy_id": req.strategy_id,
            "strategy_version": req.strategy_version,
            "queued": True,
        },
    }
