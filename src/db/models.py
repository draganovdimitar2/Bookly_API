from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from typing import List, Optional
from datetime import datetime, date
import uuid

"""
The Relationship function establishes a two-way connection between the User and Book models, 
with back_populates="user" indicating that each Book instance is linked back to the User instance that added it.
The sa_relationship_kwargs={"lazy": "selectin"} parameter optimizes the query performance by loading related Book
objects in a single query when the User object is accessed, reducing the number of database queries and improving efficiency.
"""


class User(SQLModel, table=True):
    __tablename__ = 'users'
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,  # Automatically generate a new UUID for each user
        sa_column=Column(
            pg.UUID,  # PostgreSQL-specific data type for UUIDs
            primary_key=True,  # Set uid as the primary key (enforcing uniqueness automatically)
            unique=True,  # Explicitly enforces uniqueness, though redundant on primary keys
            nullable=False  # Prevents NULL values in the uid column, ensuring each user has a UUID
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(
        pg.VARCHAR, nullable=False, server_default='user'
    ))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)  # this field should be excluded from serialization
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List['Book'] = Relationship(  # This field serves not as database row but as means to access related objects
        back_populates='user', sa_relationship_kwargs={'lazy': 'selectin'}  # to retrieve all books added by a user
    )  # to access the books submitted by user
    reviews: List['Review'] = Relationship(
        back_populates='user', sa_relationship_kwargs={'lazy': 'selectin'}
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,  # Automatically generate a new UUID for each book
        sa_column=Column(
            pg.UUID,  # PostgreSQL-specific data type for UUID
            primary_key=True,  # Set uid as the primary key (enforcing uniqueness automatically)
            unique=True,  # Explicitly enforces uniqueness, though redundant on primary keys
            nullable=False  # Prevents NULL values in the uid column, ensuring each Book has a UUID
        )
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None,
                                          foreign_key='users.uid')  # linking each book entry to the user who submitted it
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates='books')
    reviews: List['Review'] = Relationship(  # this relationship allow us to access the reviews left on a book
        back_populates='book', sa_relationship_kwargs={'lazy': 'selectin'}  # maps to our book
    )

    def __repr__(self) -> str:
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False
        )
    )
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None,
                                          foreign_key='users.uid')  # linking each review to the user who submitted it
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key='books.uid')
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates='reviews')
    book: Optional[Book] = Relationship(back_populates='reviews')

    def __repr__(self) -> str:
        return f"<Review for book -> {self.book_uid} by user -> {self.user_uid}>"
