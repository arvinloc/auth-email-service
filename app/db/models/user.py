from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    email = Column(String(70), unique=True)
    password = Column(String(250))
    # для проверки в логине будет юзаться
    is_verified = Column(Boolean, default=False)
