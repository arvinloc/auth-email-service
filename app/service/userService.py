from app.db.repository.userRepo import UserRepository
from app.db.repository.magicLinkRepo import MagicLinkRepository
from app.db.schema.user import UserOutput,UserInCreate,UserInLogin,UserWithToken
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from app.core.mail.mailer import send_magic_link
from sqlalchemy.orm import Session
from fastapi import HTTPException
import secrets
import hashlib
from datetime import timezone,timedelta,datetime


MAGIC_LINK_TTL_MINUTES = 15
FRONT_MAGIC_LINK = "http://localhost:8000/auth/magic-link/verify"

class UserService:
    def __init__(self,session:Session):
        self.__userRepository = UserRepository(session=session)
        self.__magicLinkRepository = MagicLinkRepository(session=session)

    def signup(self,user_details:UserInCreate) -> UserOutput:
        if self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400,detail="Unable to register with these credentials")

        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password

        return self.__userRepository.create_user(user_data=user_details)

    def login(self,login_data:UserInLogin) -> UserWithToken:

        user = self.__userRepository.get_user_by_email(email=login_data.email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not HashHelper.verify_password(
            plain_password=login_data.password,
            hashed_password=user.password):

            raise HTTPException(status_code=401,detail="Invalid email or password")
        token = AuthHandler.sign_jwt(user_id=user.id)
        if not token:
            raise HTTPException(status_code=500,detail="Unable to process request")

        return UserWithToken(token=token)

    def get_user_by_id(self,user_id:int):
        user = self.__userRepository.get_user_by_id(user_id=user_id)

        if user:
            return user
        raise HTTPException(status_code=401,detail="Invalid authentication credentials")


    def issue_magic_link(self, user:UserOutput) -> None:
        raw_token = secrets.token_urlsafe(32)

        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=MAGIC_LINK_TTL_MINUTES)


        self.__magicLinkRepository.create(
            user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        link = f"{FRONT_MAGIC_LINK}?token={raw_token}"

        send_magic_link(to_email=user.email,link=link)


    def consume_magic_link(self,raw_token:str):
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        token_record = self.__magicLinkRepository.mark_used_if_unused(token_hash=token_hash)

        if not token_record:
            raise HTTPException(status_code=400, detail="Invalid or expired link")

        expires_at = token_record.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Invalid or expired link")

        user = self.__userRepository.get_user_by_id(token_record.user_id)

        if not user:
            raise HTTPException(status_code=400, detail="Invalid or expired link")

        return user


