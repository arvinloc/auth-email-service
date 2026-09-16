from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from decouple import config

SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL",default=None)

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("SQLALCHEMY_DATABASE_URL is empty or not set in env")

engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)


class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
