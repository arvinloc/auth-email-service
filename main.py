from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectedRoute import get_current_user
from app.db.schema.user import UserOutput
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging.logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация базы данных при поднятии сервера
    logger.info("Starting up service")
    create_tables()
    logger.info("Database connected sucessfully")
    yield
    logger.info("Server shut down")

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "Running"}


@app.get("/protected")
def read_protected(payload: UserOutput = Depends(get_current_user)):
    return {"data": payload}
