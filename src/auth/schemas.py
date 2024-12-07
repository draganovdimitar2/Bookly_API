from pydantic import BaseModel, Field
from src.books.schemas import Book
from src.reviews.schemas import ReviewModel
import uuid
from typing import List
from datetime import datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserModel(BaseModel):  # to return all of the info related to the specific user
    uid: uuid.UUID  # everything is copied from the models except the things related to the database
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)  # this field should stay only to prevent returning the user password
    created_at: datetime
    updated_at: datetime


class UserBooksModel(UserModel):  # inherit from the class above
    books: List[Book]  # return a list of the books associated with the current user
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    addresses: List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
