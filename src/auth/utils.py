from passlib.context import CryptContext

passwd_context = CryptContext(
    schemes=['bcrypt']  # list of the algorithm used to hash the password
)


def generate_password_hash(
        password: str) -> str:  # to generate unreadable string of the password which will be stored in our database
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:  # used for log in to verify the password
    return passwd_context.verify(password, hash)
