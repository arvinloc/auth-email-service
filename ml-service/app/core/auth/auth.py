import jwt
from decouple import config

JWT_SECRET = config("JWT_SECRET")       
JWT_ALGORITHM = config("JWT_ALGORITHM")

def decode_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None