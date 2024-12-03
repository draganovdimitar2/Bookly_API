from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from .errors import register_all_errors
version = 'v1'  # This is the version of the API
app = FastAPI(  # our web server
    title='Bookly',  # title of the API
    description='A REST API for a book review web service',  # decr of the API
    version=version  # The version of the API
)

register_all_errors(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])  # include routers in our main app
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])
