FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir fastapi uvicorn httpx sqlalchemy pymysql redis
COPY src /app/src
EXPOSE 18080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "18080"]
