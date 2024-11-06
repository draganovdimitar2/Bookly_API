from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = True


@auth_router.post(
    '/signup',
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED

)
async def create_user_Account(
        user_data: UserCreateModel,
        session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)  # return a bool based on if user exists or not

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="A user with this email already exists.")

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)  # to check if user exists

    if user:  # check if the password matches the password in our database
        password_valid = verify_password(password, user.password_hash)  # return bool if the pass matches

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                refresh=True,  # provide our refresh and expiry
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Login successful!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )

    raise HTTPException(  # in case our two if-statements don't pass we raise an exception
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid e-mail or password.'
    )


