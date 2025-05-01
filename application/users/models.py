from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hash_password: Mapped[str] = mapped_column(String(255))
