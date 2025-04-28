from typing import Union, List

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.user_models import User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        surname: str,
        hashed_password: str,
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            hashed_password=hashed_password,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = (
            delete(User)
            .where(User.id == user_id)
            .returning(User.id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_all_users(self) -> List[User]:
        query = select(User)
        result = await self.db_session.execute(query)
        users = result.scalars().all()
        return users

    async def update_user(self, user_id: int, **kwargs) -> Union[User, None]:
        query = (
            update(User)
            .where(User.id == user_id)
            .values(kwargs)
            .returning(User)
        )
        res = await self.db_session.execute(query)
        update_user = res.scalar()
        await self.db_session.commit()
        return update_user
