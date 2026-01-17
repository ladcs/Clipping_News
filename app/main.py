from fastapi import FastAPI
from api.v1.router import api_router

app = FastAPI(
    title="Bot News API",
    version="1.0.0",
)

app.include_router(api_router)

@app.get("/health", tags=["health"])
def healthcheck():
    return {"status": "ok"}
