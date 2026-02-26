from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from redis import Redis
from redis.exceptions import ResponseError
from sqlalchemy import create_engine, text

from .deps_health import check_mysql, check_redis
from .event_contracts import make_event
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


def _db_rows(sql: str, params: dict | None = None) -> list[dict]:
    engine = create_engine(_mysql_dsn(), pool_pre_ping=True)
    with engine.connect() as conn:
        rows = conn.execute(text(sql), params or {}).mappings().all()
    return [dict(r) for r in rows]


def _safe_db_rows(sql: str, params: dict | None = None) -> tuple[list[dict], str | None]:
    try:
        return _db_rows(sql, params), None
    except Exception as e:
        return [], str(e)


def _stream_stats(redis_client: Redis, stream: str, group: str) -> dict:
    length = redis_client.xlen(stream)
    pending = 0
    consumers = 0
    try:
        g = redis_client.xinfo_groups(stream)
        for item in g:
            if item.get("name") == group:
                pending = int(item.get("pending", 0))
                consumers = int(item.get("consumers", 0))
                break
    except ResponseError:
        pass
    return {"stream": stream, "length": length, "pending": pending, "consumers": consumers}


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
    urgent, err1 = _safe_db_rows(
        """
        SELECT a.event_uid, e.title, e.source, e.url, a.alert_level, a.alert_reason, a.created_at
        FROM news_alerts a
        JOIN news_events e ON e.event_uid = a.event_uid
        ORDER BY a.created_at DESC
        LIMIT :lim
        """,
        {"lim": limit},
    )
    latest, err2 = _safe_db_rows(
        """
        SELECT event_uid, source, published_at, title, summary, url, sentiment_score
        FROM news_events
        ORDER BY published_at DESC
        LIMIT :lim
        """,
        {"lim": limit},
    )
    analysis, err3 = _safe_db_rows(
        """
        SELECT event_uid, impact_direction, confidence, analysis_version, created_at
        FROM news_analysis_outputs
        ORDER BY created_at DESC
        LIMIT :lim
        """,
        {"lim": limit},
    )
    errors = [e for e in [err1, err2, err3] if e]
    return {
        "ok": True,
        "data": {
            "urgent": urgent,
            "latest": latest,
            "analysis": analysis,
            "meta": {
                "sentiment_method": "headline keyword rules on real RSS titles (v1): bullish=[surge,rally,breakout,approve,bull], bearish=[hack,ban,dump,lawsuit,bear]",
                "urgent_count": len(urgent),
            },
        },
        "warnings": errors,
    }


@app.get('/v1/dashboard/market')
def dashboard_market(symbol: str = "BTCUSDT", timeframe: str = "1h", limit: int = 200):
    candles, err1 = _safe_db_rows(
        """
        SELECT venue, symbol, timeframe, ts, open, high, low, close, volume, turnover
        FROM market_ohlcv
        WHERE symbol=:symbol AND timeframe=:timeframe
        ORDER BY ts DESC
        LIMIT :lim
        """,
        {"symbol": symbol, "timeframe": timeframe, "lim": limit},
    )
    indicators, err2 = _safe_db_rows(
        """
        SELECT venue, symbol, timeframe, ts, indicator_name, indicator_params, indicator_value
        FROM technical_indicator_values
        WHERE symbol=:symbol AND timeframe=:timeframe
        ORDER BY ts DESC
        LIMIT 200
        """,
        {"symbol": symbol, "timeframe": timeframe},
    )
    errors = [e for e in [err1, err2] if e]
    return {
        "ok": True,
        "data": {
            "symbol": symbol,
            "timeframe": timeframe,
            "default_timeframes": ["15m", "1h", "4h", "1d"],
            "default_indicators": ["EMA20", "EMA50", "EMA200", "BOLL", "RSI14", "MACD", "VOLUME"],
            "candles": list(reversed(candles)),
            "indicators": list(reversed(indicators)),
        },
        "warnings": errors,
    }


@app.get('/v1/dashboard/strategy')
def dashboard_strategy(strategy_id: str | None = None, limit: int = 20):
    where = "WHERE sv.strategy_id=:strategy_id" if strategy_id else ""
    params = {"lim": limit}
    if strategy_id:
        params["strategy_id"] = strategy_id

    candidates, err1 = _safe_db_rows(
        f"""
        SELECT sv.strategy_id, sv.version AS strategy_version, ss.name, ss.template_type,
               sv.spec_json, sv.risk_json, sv.anti_liquidation_json,
               sv.created_at, sv.effective_window_start, sv.effective_window_end
        FROM strategy_versions sv
        LEFT JOIN strategy_specs ss ON ss.strategy_id = sv.strategy_id
        {where}
        ORDER BY sv.created_at DESC
        LIMIT :lim
        """,
        params,
    )

    optimized, err2 = _safe_db_rows(
        f"""
        SELECT strategy_id, strategy_version, validation_type AS optimization_action,
               status, summary_json, created_at
        FROM strategy_validation_runs
        {'WHERE strategy_id=:strategy_id' if strategy_id else ''}
        ORDER BY created_at DESC
        LIMIT :lim
        """,
        params,
    )

    errors = [e for e in [err1, err2] if e]
    payload = {"strategy_id": strategy_id} if strategy_id else None
    return {
        "ok": True,
        "data": {"query": payload, "candidates": candidates, "optimized": optimized},
        "warnings": errors,
    }


@app.get('/v1/dashboard/backtest')
def dashboard_backtest(run_id: str | None = None, limit: int = 20):
    if run_id:
        run = _fetch_json(f"{settings.backtest_agent_base}/v1/backtest/runs/{run_id}")
        metrics = _fetch_json(f"{settings.backtest_agent_base}/v1/backtest/runs/{run_id}/metrics")
        artifacts = _fetch_json(f"{settings.backtest_agent_base}/v1/backtest/runs/{run_id}/artifacts")
        return {"ok": True, "data": {"run": run, "metrics": metrics, "artifacts": artifacts}}

    backtests, err1 = _safe_db_rows(
        """
        SELECT r.run_id, r.strategy_id, r.strategy_version, r.status, r.started_at, r.ended_at,
               m.total_return, m.annual_return, m.max_drawdown, m.sharpe, m.win_rate, m.trade_count
        FROM backtest_runs r
        LEFT JOIN backtest_metrics m ON m.run_id = r.run_id
        ORDER BY r.created_at DESC
        LIMIT :lim
        """,
        {"lim": limit},
    )

    paper, err2 = _safe_db_rows(
        """
        SELECT r.run_id, r.strategy_id, r.strategy_version, r.window_start, r.window_end, r.status,
               m.pnl, m.max_drawdown, m.win_rate, m.trade_count, m.slippage_impact
        FROM paper_trading_runs r
        LEFT JOIN paper_trading_metrics m ON m.run_id = r.run_id
        ORDER BY r.window_end DESC
        LIMIT :lim
        """,
        {"lim": limit},
    )

    errors = [e for e in [err1, err2] if e]
    return {"ok": True, "data": {"backtests": backtests, "paper": paper}, "warnings": errors}


@app.get('/v1/dashboard/token-usage')
def dashboard_token_usage():
    # Heuristic estimator until provider-level token metering is wired.
    # Counts recent records and estimates token usage by stage.
    news_cnt_rows, _ = _safe_db_rows("SELECT COUNT(*) AS c FROM news_analysis_outputs WHERE created_at >= NOW() - INTERVAL 1 DAY")
    strat_cnt_rows, _ = _safe_db_rows("SELECT COUNT(*) AS c FROM strategy_validation_runs WHERE created_at >= NOW() - INTERVAL 1 DAY")
    backtest_cnt_rows, _ = _safe_db_rows("SELECT COUNT(*) AS c FROM backtest_runs WHERE created_at >= NOW() - INTERVAL 1 DAY")

    news_cnt = int((news_cnt_rows[0].get("c") if news_cnt_rows else 0) or 0)
    strat_cnt = int((strat_cnt_rows[0].get("c") if strat_cnt_rows else 0) or 0)
    backtest_cnt = int((backtest_cnt_rows[0].get("c") if backtest_cnt_rows else 0) or 0)

    # tunable multipliers
    news_tokens = news_cnt * 900
    strat_tokens = strat_cnt * 2200
    backtest_tokens = backtest_cnt * 1200
    total = news_tokens + strat_tokens + backtest_tokens

    return {
        "ok": True,
        "data": {
            "window": "24h",
            "estimated": True,
            "items": [
                {"agent": "news-agent", "events": news_cnt, "tokens": news_tokens, "share": round(news_tokens / total, 4) if total else 0},
                {"agent": "strategy-agent", "events": strat_cnt, "tokens": strat_tokens, "share": round(strat_tokens / total, 4) if total else 0},
                {"agent": "backtest-agent", "events": backtest_cnt, "tokens": backtest_tokens, "share": round(backtest_tokens / total, 4) if total else 0},
            ],
            "total_tokens": total,
            "note": "Estimated from DB event volumes; not provider-billed exact usage",
        },
    }


@app.get('/v1/dashboard/portfolio-summary')
def dashboard_portfolio_summary(limit: int = 50):
    rows, err = _safe_db_rows(
        """
        SELECT r.strategy_id, r.strategy_version, r.created_at,
               m.total_return, m.max_drawdown, m.sharpe, m.win_rate
        FROM backtest_runs r
        LEFT JOIN backtest_metrics m ON m.run_id=r.run_id
        WHERE r.strategy_id LIKE 'strat_portfolio_%'
        ORDER BY r.created_at DESC
        LIMIT :lim
        """,
        {"lim": limit},
    )

    grouped: dict[str, list[dict]] = {}
    for r in rows:
        grouped.setdefault(r.get("strategy_id", "unknown"), []).append(r)

    items = []
    total_ret = 0.0
    total_mdd = 0.0
    total_sharpe = 0.0
    n = 0
    for sid, arr in grouped.items():
        latest = arr[0]
        tr = float(latest.get("total_return") or 0.0)
        mdd = float(latest.get("max_drawdown") or 0.0)
        sh = float(latest.get("sharpe") or 0.0)
        score = max(0.0, sh * 0.7 + tr * 0.3 - mdd * 0.5)
        items.append({
            "strategy_id": sid,
            "latest_version": int(latest.get("strategy_version") or 0),
            "total_return": tr,
            "max_drawdown": mdd,
            "sharpe": sh,
            "score": score,
        })
        total_ret += tr
        total_mdd += mdd
        total_sharpe += sh
        n += 1

    # normalize weights from score
    ssum = sum(x["score"] for x in items) or 1.0
    for x in items:
        x["weight_suggest"] = round(x["score"] / ssum, 4)

    # simple static correlation template by asset class
    labels = [x["strategy_id"] for x in items]
    matrix = []
    for i, a in enumerate(labels):
        row = []
        for j, b in enumerate(labels):
            if i == j:
                row.append(1.0)
            elif ("btc" in a and "eth" in b) or ("eth" in a and "btc" in b):
                row.append(0.78)
            elif ("xau" in a and "xag" in b) or ("xag" in a and "xau" in b):
                row.append(0.71)
            else:
                row.append(0.28)
        matrix.append(row)

    return {
        "ok": True,
        "data": {
            "portfolio_id": "core_multi_asset_v1",
            "portfolio_return": round(total_ret / n, 6) if n else 0,
            "portfolio_drawdown": round(total_mdd / n, 6) if n else 0,
            "portfolio_sharpe": round(total_sharpe / n, 6) if n else 0,
            "strategies": items,
            "correlation": {"labels": labels, "matrix": matrix},
            "warnings": [err] if err else [],
        },
    }


@app.get('/v1/system/streams')
def system_streams(group: str = "crypto-intel-group"):
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    streams = [
        "crypto-intel:stream:news.events",
        "crypto-intel:stream:news.urgent",
        "crypto-intel:stream:market.ohlcv",
        "crypto-intel:stream:market.indicators",
        "crypto-intel:stream:strategy.generated",
        "crypto-intel:stream:backtest.completed",
        "crypto-intel:stream:paper.window.closed",
        "crypto-intel:stream:strategy.optimized",
        "crypto-intel:stream:notification.telegram",
        "crypto-intel:stream:dlq:notification.telegram",
        "crypto-intel:stream:dlq:paper.window.closed",
    ]
    items = []
    for s in streams:
        try:
            items.append(_stream_stats(redis_client, s, group))
        except Exception as e:
            items.append({"stream": s, "error": str(e)})
    return {"ok": True, "data": {"group": group, "items": items}}


@app.post('/v1/notify/telegram/strategy-cycle')
def notify_strategy_cycle(req: TelegramCycleNotifyRequest):
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    stream = "crypto-intel:stream:notification.telegram"
    event = make_event(
        event_type="notification.telegram",
        producer="crypto-intel-api-gateway",
        payload={
            "template": "strategy_cycle_summary_v1",
            "to": req.to,
            "strategy_id": req.strategy_id,
            "strategy_version": req.strategy_version,
            "backtest_summary": req.backtest_summary,
            "paper_summary": req.paper_summary,
            "optimization_action": req.optimization_action,
            "next_window": req.next_window,
            "risk_notice": req.risk_notice,
        },
    )
    stream_id = redis_client.xadd(stream, event)

    return {
        "ok": True,
        "data": {
            "template": "strategy_cycle_summary_v1",
            "to": req.to,
            "strategy_id": req.strategy_id,
            "strategy_version": req.strategy_version,
            "queued": True,
            "event_id": event["event_id"],
            "stream_id": stream_id,
        },
    }
