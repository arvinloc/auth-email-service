from app.core.database import Base,engine
from app.db.models.user import User
from app.db.models.magicLinkToken import MagicLinkToken

def create_tables():
    Base.metadata.create_all(bind=engine)