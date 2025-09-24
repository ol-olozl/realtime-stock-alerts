from fastapi import FastAPI

app = FastAPI(title="Realtime Stock Alerts - Ingest (skeleton)")

@app.get("/")
def root():
    return {"ok": True, "service": "fastapi_ingest"}

@app.get("/health")
def health():
    return {"status": "healthy"}
