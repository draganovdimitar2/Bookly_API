from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
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

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])  # include routers in our main app
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])
