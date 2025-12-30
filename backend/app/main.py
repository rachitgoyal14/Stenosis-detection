from fastapi import FastAPI
from api.upload import router as upload_router

app = FastAPI(
    title="Atrio.AI",
)

app.include_router(upload_router)
