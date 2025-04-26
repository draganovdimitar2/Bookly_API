from src.db.models import Review
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from .schemas import ReviewCreateModel
from ..auth.routes import user_service
from ..books.routes import book_service
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage

from src.config import Config


class ReviewService:
    def __init__(self):
        self.connection_string = Config.AZURE_SERVICE_BUS_CONNECTION_STRING
        self.queue_name = Config.AZURE_SERVICE_BUS_QUEUE_NAME

    async def add_review_to_book(self, user_email: str, book_uid: str, review_data: ReviewCreateModel, session: AsyncSession):
        try:
            book = await book_service.get_book(
                book_uid=book_uid,
                session=session
            )
            user = await user_service.get_user_by_email(
                email=user_email,
                session=session
            )

            if not book:  # If book is not found
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Book not found'
                )

            if not user:  # If user is not found
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='User not found'
                )
            review_data_dict = review_data.dict()
            new_review = Review(  # create a new Review instance
                **review_data_dict
            )
            new_review.user = user  # associate review with the user
            new_review.book = book  # associate review with the book
            session.add(new_review)
            await session.commit()

            # Step 5: Notify the book uploader via Azure Service Bus
            await self.send_service_bus_message(book.title, review_data.review_text)

            return new_review
        except Exception as e:
            print(f"Error adding review to book: {e}")
            raise

    async def send_service_bus_message(self, book_name: str, review_content: str):
        try:
            print("Attempt to connect to Azure Service Bus.")
            async with ServiceBusClient.from_connection_string(self.connection_string) as client:
                print("Attempt to get the queue name")
                sender = client.get_queue_sender(queue_name=self.queue_name)
                async with sender:
                    print("Making the message")
                    message = ServiceBusMessage(f"{book_name}|{review_content}")
                    print("Trying to send to message")
                    await sender.send_messages(message)
                    print("Message sent to Azure Service Bus.")
        except Exception as e:
            print(f"Error sending message to Azure Service Bus: {e}")
            raise
