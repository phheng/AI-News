from fastapi import FastAPI

app = FastAPI(title="crypto-intel-api-gateway", version="0.1.0")

@app.get('/healthz')
def healthz():
    return {"ok": True, "service": "crypto-intel-api-gateway"}

@app.get('/readyz')
def readyz():
    return {"ok": True}

@app.get('/version')
def version():
    return {"version": "0.1.0"}
