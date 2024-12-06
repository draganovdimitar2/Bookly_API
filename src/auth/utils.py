from datetime import timedelta, datetime
from passlib.context import CryptContext
from src.config import Config
import jwt
import uuid
import logging
from itsdangerous import URLSafeTimedSerializer

passwd_context = CryptContext(
    schemes=['bcrypt']  # list of the algorithm used to hash the password
)

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(
        password: str) -> str:  # to generate unreadable string of the password which will be stored in our database
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:  # used for log in to verify the password
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {
        'user': user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:  # to decode the token and check whether it is valid
    try:  # try to decode the token and return it's data
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]  # algorithm to decode the token
        )

        return token_data

    except jwt.PyJWTError as e:  # in case we failed to decode the token
        logging.exception(e)  # to log the error
        return None  # return None if the token is not decoded


serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET,
    salt='email-configuration'
)


def create_url_safe_token(data: dict):
    """Serialize a dict into a URLSafe token"""
    token = serializer.dumps(data)

    return token


def decode_url_safe_token(token: str):
    """Deserialize a URLSafe token to get data"""
    try:
        token_data = serializer.loads(token)  # return the data that is decoded within our token

        return token_data

    except Exception as e:
        logging.error(str(e))
