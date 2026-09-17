from .base import BaseRepository
from app.db.models.user import User
from app.db.schema.user import UserInCreate
from app.db.models.magicLinkToken import MagicLinkToken
import datetime

# Репозиторий для создания магической ссылки


class MagicLinkRepository(BaseRepository):
    def create(self, user_id: int, token_hash: str, expires_at: datetime) -> MagicLinkToken:
        token = MagicLinkToken(
            user_id=user_id, token_hash=token_hash, expires_at=expires_at)

        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)

        return token

    def mark_used_if_unused(self, token_hash: str) -> MagicLinkToken | None:
        updated = self.session.query(
            MagicLinkToken
        ).filter(
            MagicLinkToken.token_hash == token_hash,
            MagicLinkToken.used == False,
        ).update({"used": True}, synchronize_session=False)

        self.session.commit()

        if updated == 0:
            return None

        return self.session.query(MagicLinkToken).filter_by(token_hash=token_hash).first()
