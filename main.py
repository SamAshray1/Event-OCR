from fastapi import FastAPI
from app.api.routes import router
from app.api.routes import router2
from app.api.vlm_routes import router as vrouter

app = FastAPI(
    title="EventOCR",
    description="Extract events from invitation images",
    version="0.1.0"
)

app.include_router(router)
app.include_router(router2)
app.include_router(vrouter)