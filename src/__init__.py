from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from .errors import register_all_errors
import asyncio
from src.reviews.service import ReviewService
from src.notifications.consumer import NotificationConsumer
from src.config import Config
from src.middleware import register_middleware

review_service = ReviewService()
notification_consumer = NotificationConsumer()

version = 'v1'  # This is the version of the API
version_prefix = f"/api/{version}"
app = FastAPI(  # our web server
    title='Bookly',  # title of the API
    description='A REST API for a book review web service',  # decr of the API
    version=version,  # The version of the API
    contact={
        'name': 'Dimitar Draganov',
        'url': 'https://github.com/draganovdimitar2',
        'email': 'dragnovdimitar2@gmail.com'
    },
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc"
)


@app.on_event("startup")
async def startup_event():
    """
    Start the Azure Service Bus listener in the background when the application starts.
    """
    asyncio.create_task(notification_consumer.process_messages())


register_all_errors(app)

register_middleware(app)

app.include_router(book_router, prefix=f"{version_prefix}/books", tags=['books'])  # include routers in our main app
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"{version_prefix}/reviews", tags=['reviews'])
app.include_router(tags_router, prefix=f"{version_prefix}/tags", tags=["tags"])
