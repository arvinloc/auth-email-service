import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from decouple import config
import datetime

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")


class AuthHandler(object):
    @staticmethod
    def sign_jwt(user_id:int):

        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
        }

        return jwt.encode(payload=payload,key= JWT_SECRET,algorithm=JWT_ALGORITHM)


    @staticmethod
    def decode_jwt(token:str) -> dict:
        try:
            decoded_token = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
            return decoded_token
        except ExpiredSignatureError:
            print('Token has expired')
            return None
        except InvalidTokenError:
            print('Invalid token')
            return None