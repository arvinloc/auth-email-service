from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectedRoute import get_current_user
from app.db.schema.user import UserOutput 

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Инициализация базы данных при поднятии сервера
    print("Created!")
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter,tags=["auth"],prefix="/auth")


@app.get("/health")
def health():
    return {"status": "Running"}



@app.get("/protected")
def read_protected(payload: UserOutput = Depends(get_current_user)):
    return {"data": payload}