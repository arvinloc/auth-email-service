from fastapi import FastAPI
from app.routers.predict import router
from app.core.load.model import get_pipeline
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # инициализация пайплайна обученной модели
    get_pipeline()
    print('pipeline loaded successfully')
    yield

app = FastAPI(title='text sentiment analyzer', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, tags=['predict'])


@app.get("/health")
def health():
    return {"status": "Running"}
