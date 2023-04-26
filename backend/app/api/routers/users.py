import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.future import select

from app.models import Chat, ChatDetail
from db.database import get_async_session_context, get_user_db_context

from utils.exceptions import AuthorityDenyException, InvalidParamsException, DataBaseException
from app.models.userModel import User
from utils.response import response, get_http_message
from app.schemas.userSchema import UserRead, UserUpdate, UserCreate, LimitSchema, AccountSchema, KeySchema, \
    UserResetPassword
from app.controller.userController import auth_backend, fastapi_users, current_active_user, \
    get_user_manager_context, current_super_user

from fastapi import APIRouter, Depends

router = APIRouter()

# login auth user
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"]
)
# reset password
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
# register user
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@router.get("/user", tags=["user"])
async def get_all_users(_user: User = Depends(current_super_user)):
    """
    get all user

    :param _user:

    :return:
    """
    async with get_async_session_context() as session:
        r = await session.execute(select(User))
        results = r.scalars().all()
        return results


@router.get("/user/{user_id}/account", tags=["user"], response_model=AccountSchema)
async def get_user_account(user_id: int = None, _user: User = Depends(current_active_user), ):
    """
    get user account message

    :param user_id:

    :param _user:

    :return:
    """
    async with get_async_session_context() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        user = user.scalars().all()[0]
        if user is None:
            raise InvalidParamsException("errors.userNotFound")
        results = jsonable_encoder(user)
        return results


@router.patch("/user/{user_id}/set_api_key", tags=["user"])
async def update_api_key(keySchema: KeySchema, user_id: int = None, _user: User = Depends(current_active_user)):
    """
    set or update api_key

    :param keySchema:

    :param user_id:

    :param _user:

    :return:
    """
    async with get_async_session_context() as session:
        target_user: User = await session.get(User, user_id)
        if target_user is None:
            raise InvalidParamsException("errors.userNotExist")
        for attr, value in keySchema.dict(exclude_unset=True).items():
            if value is not None:
                setattr(target_user, attr, value)

        session.add(target_user)
        result = await session.commit()
        return result


@router.patch("/user/{user_id}/reset-password", tags=["user"], response_model=UserResetPassword)
async def reset_password(userResetPassword: UserResetPassword, _user: User = Depends(current_active_user)):
    """
    retset password

    :param userResetPassword:

    :param _user:

    :return:
    """
    if not userResetPassword.new_password:
        raise InvalidParamsException("errors.newPasswordRequired")
    if _user.id != userResetPassword.user_id and not _user.is_superuser:
        raise AuthorityDenyException("errors.noPermission")
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as db:
            async with get_user_manager_context(db) as user_manager:
                result = await session.get(User, userResetPassword.user_id)
                target_user = result
                if target_user is None:
                    raise InvalidParamsException("errors.userNotExist")
                target_user.hashed_password = user_manager.password_helper.hash(userResetPassword.new_password)
                session.add(target_user)
                await session.commit()
                return response(200, message=get_http_message(200), result={})


@router.post("/user/{user_id}/limit", tags=["user"])
async def update_limit(limit: LimitSchema, user_id: int = None, _user: User = Depends(current_super_user)):
    """
    set or update user limit

    :param limit:

    :param user_id:

    :param _user:

    :return:
    """
    async with get_async_session_context() as session:
        target_user: User = await session.get(User, user_id)
        if target_user is None:
            raise InvalidParamsException("errors.userNotExist")
        for attr, value in limit.dict(exclude_unset=True).items():
            if value is not None:
                setattr(target_user, attr, value)

        # 使用**kargs类似的写法，但是跳过None值
        session.add(target_user)
        await session.commit()
        return response(200, message=get_http_message(200), result={})

#get or update user message
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/user",
    tags=["user"],
)
