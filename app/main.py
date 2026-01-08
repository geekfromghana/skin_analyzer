
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes.upload import router as upload_router
from .routes.analyze import router as analyze_router

app = FastAPI(title="Mobile Image Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler(
        os.path.join(LOG_DIR, 'app.log'))]
)


@app.on_event("startup")
def ensure_storage_dir():
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)


@app.get("/")
def root():
    return {
        "service": app.title,
        "version": app.version,
        "storage": settings.STORAGE_DIR,
        "auth": "enabled" if settings.API_KEY else "disabled"
    }


app.include_router(upload_router)
app.include_router(analyze_router)
