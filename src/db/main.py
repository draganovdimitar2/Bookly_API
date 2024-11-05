from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.books.models import Book

engine = create_async_engine(
    url = Config.DATABASE_URL,
    echo = True
)

async def init_db():  # this makes the connection to db
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)  # conn is our connection object. we want to access the metadata object on top of this SQLModel


#function to return our session
async def get_session()->AsyncSession:

    async_session = async_sessionmaker(  # we have to bond it with our AsyncEngine to carry out our CRUD
        bind = engine,
        class_ = AsyncSession,
        expire_on_commit=False  # every session can be used after commiting
    )

    async with async_session() as session:
        yield session