from fastapi.exceptions import HTTPException
from fastapi import Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import decode_token

"""
We need to protect our API endpoints such that users require to provide access tokens to access them. This is where HTTP Bearer Authentication comes in. 
HTTP Bearer Authentication is an HTTP authentication scheme that involves security tokens called Bearer Tokens. This can be understood as 
"give access to the bearer of the token". Everytime a client is to make a request to a protected endpoint, 
they must send a string in form of Bearer <token> in the request's Authorization header.
"""


class AccessTokenBearer(HTTPBearer):

    def __init__(self, auto_error = True):  # to determine the behaviour of our class if an error occurs
        super().__init__(auto_error = auto_error)  # this is going to call the __init__ method of our parent class (HTTPBearer class)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)

        token = creds.credentials  # to give access to our token

        token_data = decode_token(token)

        if not self.token_valid:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token!"
            )

        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token."
            )
        return token_data

    def token_valid(self, token: str) -> bool:  # func to check whether our token is valid


        token_data = decode_token(token)

        return True if token_data else False