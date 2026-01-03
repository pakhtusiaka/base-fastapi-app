from fastapi import (
    APIRouter,
    Depends,
)

from core.schemas.user import CreateUserData, ReadUserData
from crud.users import (
    get_all_users, 
    create_user_data
    )
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    tags=["Users"],
)

@router.get(path="", response_model=list[ReadUserData])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_getter),
    # session: Annotated [
    #     AsyncSession, 
    #     Depends(db_helper.session_getter),
    #     ],
 ):
    users = await get_all_users(session=session)
    return users

@router.post(path="", response_model=ReadUserData)
async def create_user(
    user_create: CreateUserData,
    session: AsyncSession = Depends(db_helper.session_getter),

):
    user = await create_user_data(
        session=session,
        user_create=user_create
        )
    return user