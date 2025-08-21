from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from types_sports.models import TypesSports


class Coach(Base):
    __tablename__ = "coaches"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text())
    image: Mapped[str] = mapped_column(String(500))
    type_sport_id: Mapped[int] = mapped_column(
        ForeignKey("types_sports.id", ondelete="CASCADE")
    )

    type_sport: Mapped["TypesSports"] = relationship(back_populates="coaches")
