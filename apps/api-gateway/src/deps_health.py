from sqlalchemy import create_engine, text
from redis import Redis


def check_mysql(mysql_dsn: str) -> bool:
    engine = create_engine(mysql_dsn, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True


def check_redis(redis_url: str) -> bool:
    client = Redis.from_url(redis_url)
    return bool(client.ping())
