from fastapi import APIRouter, Depends
from app.db.schema.user import UserInCreate, UserInLogin, UserWithToken, UserOutput, MagicLinkVerify
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.service.userService import UserService
from app.core.security.authHandler import AuthHandler
authRouter = APIRouter()


@authRouter.post("/login", status_code=200, response_model=UserWithToken)
def login(payload: UserInLogin, session: Session = Depends(get_db)):
    try:
        return UserService(session=session).login(login_data=payload)
    except Exception as error:
        print(error)
        raise error


@authRouter.post("/signup", status_code=201)
def signup(payload: UserInCreate, session: Session = Depends(get_db)):
    user = UserService(session=session).signup(user_details=payload)

    UserService(session=session).issue_magic_link(user)

    return {
        "message": "Check your email to confirm registration"
    }


@authRouter.post("/magic-link/verify")
def verify_magic_link(payload: MagicLinkVerify, session: Session = Depends(get_db)):
    user = UserService(session=session).consume_magic_link(payload.token)

    jwt_token = AuthHandler.sign_jwt(user_id=user.id)

    return {
        "token": jwt_token
    }
