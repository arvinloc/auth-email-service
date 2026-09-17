from fastapi import Header, HTTPException, status
from typing import Annotated
from app.core.auth.auth import decode_jwt

# Получение айдишника юзера для дальнейшего резолва


def get_current_user_id(authorization: Annotated[str | None, Header()] = None) -> int:
    # Если заголовка нету то 401
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Authentication Credentials")

    payload = decode_jwt(authorization[7:])
    # если нету ни user_id, ни пейлоада то ошибка
    if not payload or not payload.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Authentication Credentials")

    return payload["user_id"]
