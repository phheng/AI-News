from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from redis import Redis

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


def _fetch_json(url: str, params: dict | None = None) -> dict:
    try:
        with httpx.Client(timeout=settings.gateway_timeout_sec) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            return {"ok": True, "data": resp.json()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


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
    news = _fetch_json(f"{settings.news_agent_base}/healthz")
    market = _fetch_json(f"{settings.market_agent_base}/healthz")
    strategy = _fetch_json(f"{settings.strategy_agent_base}/healthz")
    backtest = _fetch_json(f"{settings.backtest_agent_base}/healthz")

    return {
        "ok": True,
        "data": {
            "agents": {
                "news": news["ok"],
                "market": market["ok"],
                "strategy": strategy["ok"],
                "backtest": backtest["ok"],
            }
        },
    }


@app.get('/v1/dashboard/news')
def dashboard_news(limit: int = 20):
    urgent = _fetch_json(f"{settings.news_agent_base}/v1/news/urgent", {"limit": limit})
    latest = _fetch_json(f"{settings.news_agent_base}/v1/news/events", {"limit": limit})
    analysis = _fetch_json(f"{settings.news_agent_base}/v1/news/analysis")
    return {"ok": True, "data": {"urgent": urgent, "latest": latest, "analysis": analysis}}


@app.get('/v1/dashboard/market')
def dashboard_market(symbol: str = "BTCUSDT", timeframe: str = "1h"):
    candles = _fetch_json(
        f"{settings.market_agent_base}/v1/market/ohlcv",
        {"symbol": symbol, "timeframe": timeframe, "limit": 200},
    )
    indicators = _fetch_json(
        f"{settings.market_agent_base}/v1/market/indicators",
        {"symbol": symbol, "timeframe": timeframe},
    )
    return {
        "ok": True,
        "data": {
            "symbol": symbol,
            "timeframe": timeframe,
            "default_timeframes": ["15m", "1h", "4h", "1d"],
            "default_indicators": ["EMA20", "EMA50", "EMA200", "BOLL", "RSI14", "MACD", "VOLUME"],
            "candles": candles,
            "indicators": indicators,
        },
    }


@app.get('/v1/dashboard/strategy')
def dashboard_strategy(strategy_id: str | None = None):
    payload = {"strategy_id": strategy_id} if strategy_id else None
    # placeholder: strategy agent currently has specs endpoint by path, keep simple structure now
    return {"ok": True, "data": {"query": payload, "candidates": [], "optimized": []}}


@app.get('/v1/dashboard/backtest')
def dashboard_backtest(run_id: str | None = None):
    if not run_id:
        return {"ok": True, "data": {"backtests": [], "paper": []}}

    run = _fetch_json(f"{settings.backtest_agent_base}/v1/backtest/runs/{run_id}")
    metrics = _fetch_json(f"{settings.backtest_agent_base}/v1/backtest/runs/{run_id}/metrics")
    artifacts = _fetch_json(f"{settings.backtest_agent_base}/v1/backtest/runs/{run_id}/artifacts")
    return {"ok": True, "data": {"run": run, "metrics": metrics, "artifacts": artifacts}}


@app.post('/v1/notify/telegram/strategy-cycle')
def notify_strategy_cycle(req: TelegramCycleNotifyRequest):
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    stream = "crypto-intel:stream:notification.telegram"
    event_id = redis_client.xadd(
        stream,
        {
            "template": "strategy_cycle_summary_v1",
            "to": req.to,
            "strategy_id": req.strategy_id,
            "strategy_version": str(req.strategy_version),
            "backtest_summary": req.backtest_summary,
            "paper_summary": req.paper_summary,
            "optimization_action": req.optimization_action,
            "next_window": req.next_window,
            "risk_notice": req.risk_notice,
        },
    )

    return {
        "ok": True,
        "data": {
            "template": "strategy_cycle_summary_v1",
            "to": req.to,
            "strategy_id": req.strategy_id,
            "strategy_version": req.strategy_version,
            "queued": True,
            "event_id": event_id,
        },
    }
