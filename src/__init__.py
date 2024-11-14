from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print('server is starting . . . .')
    await init_db()  # db function should be called with await
    yield  # the code from the top is going to run at the start of the server, the bottom one will run when server stops
    print('server has been stopped')


version = 'v1'  # This is the version of the API
app = FastAPI(  # our web server
    title='Books',  # title of the API
    description='A job finder FAST API for books and organizations',  # decr of the API
    version=version  # The version of the API
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])  # to include routers in our main app
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
"""
Prefix --> This is the path through which all related endpoints can be accessed.
This implies that all book-related endpoints can be accessed using http://localhost:8000/api/v1/users.
Tags --> The list of tags associated with the endpoints that fall within a given router.
"""
