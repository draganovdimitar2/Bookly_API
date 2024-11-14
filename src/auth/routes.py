from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])

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
                    'user_uid': str(user.uid),
                    'role': user.role
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


@auth_router.get('/refresh_token')  # func to generate new access token in case we provide a valid refresh token
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    # we need to convert our timestamp to a datetime object
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(  # create a new token if the old one is expired
            user_data=token_details['user']  # to get the same user data for the current user (uid and email)
        )
        # if we are able to do this, return a JSONResponse
        return JSONResponse(content={
            'access_token': new_access_token
        })
    # in case it doesn't return that, it will raise an exception
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid or expired token!')

@auth_router.get('/me', response_model=UserModel)  # return current user 
async def get_current_user(user = Depends(get_current_user), _: bool = Depends(role_checker)):
    return user

@auth_router.get('/logout')
async def revoke_token(token_data: dict = Depends(AccessTokenBearer())):

    jti = token_data['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            'message':'Logged Out Successfully'
        },
        status_code=status.HTTP_200_OK
    )
