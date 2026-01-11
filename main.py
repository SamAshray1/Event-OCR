from fastapi import FastAPI
# from api.routes import router
# from api.routes import router2
from api.vlm_routes import router as vrouter

app = FastAPI(
    title="EventOCR",
    description="Extract events from invitation images",
    version="0.1.0"
)

# app.include_router(router)
# app.include_router(router2)
app.include_router(vrouter)