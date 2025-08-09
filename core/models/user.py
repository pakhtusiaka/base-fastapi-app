from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)

        # Для SQLAlchemy 2.0 рекомендуется добавить repr
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"