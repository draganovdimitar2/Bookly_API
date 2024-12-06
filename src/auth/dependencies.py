from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import decode_token
from src.db.blocklist import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import List
from src.db.models import User
from src.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission
)

user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):  # to determine the behaviour of our class if an error occurs
        super().__init__(
            auto_error=auto_error)  # this is going to call the __init__ method of our parent class (HTTPBearer class)

    async def __call__(self,
                       request: Request) -> HTTPAuthorizationCredentials:  # __call__ method makes the class callable (like a func)
        creds = await super().__call__(request)

        token = creds.credentials  # to give access to our token

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise InvalidToken()

        if await token_in_blocklist(token_data['jti']):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:  # func to check whether our token is valid

        token_data = decode_token(token)

        return token_data is not None  # return True if it's not None else it will return False

    def verify_token_data(self, token_data):
        raise NotImplementedError(
            "Please Override this method in child classes")  # throwing an error if this method is not override


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self,
                          token_data: dict) -> None:  # throw an error if we provide refresh token instead of access token
        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):  # func to create dependency

    def verify_token_data(self,
                          token_data: dict) -> None:
        if token_data and not token_data[
            "refresh"]:  # like the above func but here the refresh claim should be false
            raise RefreshTokenRequired()


async def get_current_user(token_details: dict = Depends(AccessTokenBearer()),  # identify the user from the token
                           session: AsyncSession = Depends(get_session)
                           ):
    user_email = token_details['user']['email']  # extracts the user's email from the token_details

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:

    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles  # These will be the roles that are authorized to perform a certain action

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:  # check if the user’s role is valid
            return True  # indicating the user has permission

        raise InsufficientPermission()
