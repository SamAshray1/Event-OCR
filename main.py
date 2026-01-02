from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="EventOCR",
    description="Extract events from invitation images",
    version="0.1.0"
)

app.include_router(router)
