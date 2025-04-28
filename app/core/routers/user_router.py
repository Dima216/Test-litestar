from logging import getLogger
from typing import Annotated, List

from litestar.params import Body, Parameter
from litestar import Router, get, post, delete, put
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_200_OK
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions.user_actions import (
    _create_new_user,
    _delete_user,
    _get_user_by_id,
    _get_all_users,
    _update_user,
)
from app.core.schemas.user_schemas import (
    ShowUser,
    UpdateUserRequest,
    UserCreate,
    DeleteUserResponse,
)
from app.core.session import get_db

logger = getLogger(__name__)


@post("/", response_model=ShowUser)
async def create_user(
    data: Annotated[UserCreate, Body()],
    db: AsyncSession,
) -> ShowUser:
    try:
        return await _create_new_user(data, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    except Exception as e:
        logger.exception(e)


@delete("/", response_model=DeleteUserResponse, status_code=HTTP_200_OK)
async def delete_user(
    db: AsyncSession,
    user_id: int = Parameter(..., description="ID пользователя"),
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return deleted_user_id


@get("/", response_model=ShowUser)
async def get_user_by_id(
    db: AsyncSession,
    user_id: int = Parameter(..., description="ID пользователя"),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return ShowUser.model_validate(user)


@get("/all", response_model=List[ShowUser])
async def get_all_users(
    db: AsyncSession,
) -> List[ShowUser]:
    try:
        users = await _get_all_users(db)
        return [ShowUser.model_validate(user) for user in users]
    except Exception as e:
        logger.error(e)
        raise e


@put("/", response_model=ShowUser)
async def update_user_by_id(
    data: Annotated[UpdateUserRequest, Body()],
    db: AsyncSession,
    user_id: int = Parameter(..., description="ID пользователя"),
) -> ShowUser:
    updated_user_params = data.dict(exclude_none=True)
    if not updated_user_params:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    try:
        updated_user = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return ShowUser.model_validate(updated_user)


user_router = Router(
    path="/user",
    route_handlers=[create_user, delete_user, get_user_by_id, get_all_users, update_user_by_id],
    dependencies={"db": Provide(get_db)},
)
