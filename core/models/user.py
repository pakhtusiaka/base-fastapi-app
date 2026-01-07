from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import UniqueConstraint, ForeignKey
from datetime import datetime
from .base import Base


# class User(Base):
#     username: Mapped[str] = mapped_column(unique=True)

#     foo: Mapped[int]
#     bar: Mapped[int]

#Пример составного уникального ограничения для записи из колонок foo и bar()
    # __table_args__ = (
    #     UniqueConstraint("foo", "bar"),
    # )

    # Для SQLAlchemy 2.0 рекомендуется добавить repr
    # def __repr__(self):
    #     return f"User(id={self.id!r}, username={self.username!r})"

class UserData(Base):
    first_name: Mapped[str] = mapped_column()
    second_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    telephone: Mapped[str] = mapped_column()

class AccessToken(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.id"))
    expires_access_token: Mapped[datetime] = mapped_column
    refresh_token: Mapped[datetime] = mapped_column

    