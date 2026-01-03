from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from sqlalchemy import select
from core.models.user import UserData as UserDataORM      # явный импорт ORM-класса под другим именем
from core.schemas.user import CreateUserData         # Pydantic схема для создания

from core.schemas.user import ReadUserData
from core.schemas.user import CreateUserData

async def get_all_users(
    session: AsyncSession,
    ) -> Sequence[UserDataORM]:
    stmt = select(UserDataORM).order_by(UserDataORM.id)
    result = await session.scalars(stmt)
    return result.all()

async def create_user_data(session: AsyncSession,user_create: CreateUserData,) -> UserDataORM:
    user = UserDataORM(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

# async def get_all_users(
#     session: AsyncSession,
#     ) -> Sequence[User]:
#     stmt = select(User).order_by(User.id)
#     return await session.scalar ("SELECT * FROM users")