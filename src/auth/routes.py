from fastapi.exceptions import HTTPException
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
from src.db.blocklist import add_jti_to_blocklist
from src.config import Config
from src.db.main import get_session
from fastapi import (
    APIRouter,
    Depends,
    status,
    BackgroundTasks
)
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker
)
from .schemas import (
    UserCreateModel,
    UserLoginModel,
    UserBooksModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel
)
from .utils import (
    create_access_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
    generate_password_hash
)
from src.errors import (
    UserAlreadyExists,
    UserNotFound,
    InvalidCredentials,
    InvalidToken
)
from datetime import (
    timedelta,
    datetime
)
from src.mail import (
    mail,
    create_message
)

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRY = True


@auth_router.post('/send_mail')
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = '<h1>Welcome to the app</h1>'

    message = create_message(
        recipients=emails,
        subject="Welcome",
        body=html
    )

    await mail.send_message(message)

    return {'message': 'Email send successfully'}


@auth_router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED

)
async def create_user_Account(
        user_data: UserCreateModel,
        bg_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)  # return a bool based on if user exists or not

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this link <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[email],
        subject="Verify your email",
        body=html_message
    )

    bg_tasks.add_task(mail.send_message, message)  # using background task when sending emails so that it will take less time (to offload the task)

    return {
        "message": "Account Created! Check email to verify your account!",
        "user": new_user
    }


@auth_router.get('/verify/{token}')
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)  # decode the token

    user_email = token_data.get('email')  # get the email from the token

    if user_email:  # if the email is not None
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True},
                                       session)  # update is_verified to True in our database

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        content={'message': 'An error occurred during verification'},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


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

    raise InvalidCredentials()


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
    raise InvalidToken()


@auth_router.get('/me', response_model=UserBooksModel)  # return the current user with a list of his books
async def get_current_user(user=Depends(get_current_user), _: bool = Depends(role_checker)):
    return user


@auth_router.get('/logout')
async def revoke_token(token_data: dict = Depends(AccessTokenBearer())):
    jti = token_data['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            'message': 'Logged Out Successfully'
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.post("/password-reset-request")
async def password_rest_request(email_data: PasswordResetRequestModel):
    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
        <h1>Reset Your Password</h1>
        <p>Please click this link <a href="{link}">link</a> to Reset Your Password</p>
        """

    message = create_message(
        recipients=[email],
        subject="Reset Your Password",
        body=html_message
    )

    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "Please check your email for instruction on how to reset your password"
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.post('/password-reset-confirm/{token}')
async def reset_account_password(
        token: str,
        passwords: PasswordResetConfirmModel,
        session: AsyncSession = Depends(get_session)
):
    new_password = passwords.new_password  # make a variable for the new password
    confirm_password = passwords.confirm_new_password  # make a variable for the confirm password

    if new_password != confirm_password:  # if passwords do not match
        raise HTTPException(
            detail="Passwords do not match!",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_url_safe_token(token)  # decode the token

    user_email = token_data.get('email')  # get the email from the token

    if user_email:  # if the email is not None
        user = await user_service.get_user_by_email(user_email, session)  # get the user

        if not user:  # if the user is not found raise an error
            raise UserNotFound()

        password_hash = generate_password_hash(new_password)  # to generate unreadable string of the new password
        await user_service.update_user(user, {"password_hash": password_hash},
                                       session)  # update the user with the new password

        return JSONResponse(
            content={"message": "Password reset Successfully!"},
            status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        content={'message': 'An error occurred during password reset.'},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
