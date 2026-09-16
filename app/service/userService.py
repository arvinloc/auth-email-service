from app.db.repository.userRepo import UserRepository
from app.db.schema.user import UserOutput,UserInCreate,UserInLogin,UserWithToken
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException


class UserService:
    def __init__(self,session:Session):
        self.__userRepository = UserRepository(session=session)

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