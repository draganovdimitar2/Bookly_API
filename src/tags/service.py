from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.db.models import Tag
from .schemas import TagAddModel, TagCreateModel
from src.errors import BookNotFound, TagNotFound, TagAlreadyExists

book_service = BookService()

server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
)


class TagService:

    async def get_tags(self, session: AsyncSession):
        """Get all tags"""

        statement = select(Tag).order_by(desc(Tag.created_at))  # retrieves all tags ordered by their creation date

        result = await session.exec(statement)

        return result.all()

    async def add_tags_to_book(
            self, book_uid: str, tag_data: TagAddModel, session: AsyncSession
    ):
        """Add tags to a book"""

        book = await book_service.get_book(book_uid=book_uid, session=session)  # to verify the existence of the book

        if not book:  # if the book is not found -> raise an exception
            raise BookNotFound()

        for tag_item in tag_data.tags:  # to check if the tag already exists in the database
            result = await session.exec(
                select(Tag).where(Tag.name == tag_item.name)
            )

            tag = result.one_or_none()
            if not tag:  # creates a new tag if not
                tag = Tag(name=tag_item.name)

            book.tags.append(tag)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def get_tag_by_uid(self, tag_uid: str, session: AsyncSession):
        """Get tag by uid"""

        statement = select(Tag).where(Tag.uid == tag_uid)  # retrieves a tag by it's unique identifier

        result = await session.exec(statement)

        return result.first()

    async def add_tag(self, tag_data: TagCreateModel, session: AsyncSession):
        """Create a tag"""

        statement = select(Tag).where(
            Tag.name == tag_data.name)  # checks if a tag with the same name already exists in the database

        result = await session.exec(statement)

        tag = result.first()

        if tag:
            raise TagAlreadyExists()

        new_tag = Tag(
            name=tag_data.name)  # if the tag doesn't exist, a new Tag instance is created and added to the database

        session.add(new_tag)

        await session.commit()

        return new_tag

    async def update_tag(
            self, tag_uid, tag_update_data: TagCreateModel, session: AsyncSession
    ):
        """Update a tag"""

        tag = await self.get_tag_by_uid(tag_uid, session)

        update_data_dict = tag_update_data.model_dump()

        for k, v in update_data_dict.items():
            setattr(tag, k, v)

            await session.commit()

            await session.refresh(tag)

        return tag

    async def delete_tag(self, tag_uid: str, session: AsyncSession):
        """Delete a tag"""

        tag = await self.get_tag_by_uid(tag_uid, session)

        if not tag:  # if not found raise an exception
            raise TagNotFound()

        await session.delete(tag)  # deletes a tag identified by tag_uid from the database

        await session.commit()
