from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from .schemas import ReviewCreateModel
from ..auth.routes import user_service
from ..books.routes import book_service
import logging

book_service = BookService()
user_service = UserService()


class ReviewService:  # this class performs our CRUD related to reviews

    async def add_review_to_book(self, user_email: str, book_uid: str, review_data: ReviewCreateModel,
                                 session: AsyncSession):
        try:
            book = await book_service.get_book(  # try to get the book
                book_uid=book_uid,
                session=session
            )
            user = await user_service.get_user_by_email(
                email=user_email,
                session=session
            )
            review_data_dict = review_data.model_dump()  # dict representation of the review data
            new_review = Review(
                **review_data_dict  # unpack the review data dict
            )

            if not book:  # in case book is not found
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Book not found'
                )

            if not user:  # in case user is not found
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='User not found'
                )

            new_review.user = user  # associate the review to the user who created it

            new_review.book = book  # associate the review to the current book

            session.add(new_review)  # add the new_review instance

            await session.commit()  # commit new_review to the database

            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops ... Something went wrong!"
            )
