from app.core.database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime

class MagicLinkToken(Base):
    __tablename__ = "magic_link_tokens"
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey("Users.id"))
    token_hash = Column(String(64),unique=True)
    expires_at = Column(DateTime)
    used = Column(Boolean,default=False)
