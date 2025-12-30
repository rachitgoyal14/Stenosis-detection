from fastapi import FastAPI
from api.upload import router as upload_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Atrio.AI",
)

app.include_router(upload_router)

