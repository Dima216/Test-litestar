from typing import Union, List

from app.core.schemas.user_schemas import ShowUser, UserCreate
from app.core.dals import UserDAL
from app.core.models.user_models import User
from app.core.hashing import Hasher


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            hashed_password=Hasher.get_password_hash(body.password),
        )
        return ShowUser(
            id=user.id,
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


async def _delete_user(user_id, session) -> Union[int, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id,
        )
        return deleted_user_id


async def _update_user(
    updated_user_params: dict, user_id: int, session
) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user = await user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user


async def _get_user_by_id(user_id, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return user


async def _get_all_users(session) -> List[User]:
    async with session.begin():
        user_dal = UserDAL(session)
        users = await user_dal.get_all_users()
        return users
