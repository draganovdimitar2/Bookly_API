from markdown_it.rules_block import table
from pygments.lexer import default
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

class User(SQLModel, table= True):
    __tablename__ = 'books'
    uid: uuid.UUID = Field(  # Field names define column names in our database in this case the name of the column is "uid"
        default_factory=uuid.uuid4,  # Automatically generate a random UUID for new rows
        sa_column=Column(
            pg.UUID,  # specifies that this column will store UUIDs in PostgreSQL’s native UUID format
            primary_key=True,  # cannot be duplicate values in this column across different rows
            unique=True,
            # ensuring each row has a unique identifier (Although primary_key=True already implies uniqueness,)
            nullable=False  # uid field cannot be NULL
        )
    )
    username: str
    email: str
    password:str
    roles: str
    firstName: str
    lastName: bool = Field(default = False)  # set a default value to false
    applications: list = Field(sa_column=Column(pg.JSON), default=[])  # store list as JSON
    isActive: bool = False

    def __repr__(self):
        return f'<User {self.username}>'
