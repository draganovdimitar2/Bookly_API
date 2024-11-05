from attr.filters import exclude
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid

class User(SQLModel, table = True):
    __tablename__ = 'users'
    uid: uuid.UUID = Field(
        default_factory = uuid.uuid4,  # Automatically generate a new UUID for each user
        sa_column = Column(
            pg.UUID,  # PostgreSQL-specific data type for UUIDs
            primary_key = True,   # Set uid as the primary key (enforcing uniqueness automatically)
            unique = True,  # Explicitly enforces uniqueness, though redundant on primary keys
            nullable = False  # Prevents NULL values in the uid column, ensuring each user has a UUID
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default = False)
    password_hash: str = Field(exclude = True)  # this field should be excluded from serialization
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default = datetime.now))
    updated_at:datetime = Field(sa_column = Column(pg.TIMESTAMP, default = datetime.now))


    def __repr__(self):
        return f"<User {self.username}>"