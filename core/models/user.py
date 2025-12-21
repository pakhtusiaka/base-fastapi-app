from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import UniqueConstraint

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)

    foo: Mapped[int]
    bar: Mapped[int]
    
#Пример составного уникального ограничения для записи из колонок foo и bar()
    __table_args__ = (
        UniqueConstraint("foo", "bar"),
    )

    # Для SQLAlchemy 2.0 рекомендуется добавить repr
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"
