from datetime import datetime, date
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg  # we will access everything as pg
import uuid


"""
Mapping Objects to Tables --> Python classes represent tables in the database.
Each object of this classes corresponds to a row in the database table.
The metadata (the data about our database) is represented in the SQLModel.
So when we define the class with SQLModel we get access to metadata present on our SQLModel class.
And whatever class is defined there, it is going to be created by calling 'create all method'
So when we are able to do this, any tables present in the metadata but absent in the database will be created.
Then we will be able to run our CRUD successfully.
"""


class Book(SQLModel , table=True):
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
    language:str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self) -> str:
        return f"<Book {self.title}>"
