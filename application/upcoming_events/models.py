from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from types_sports.models import TypesSports


class UpcommingEvents(Base):
    __tablename__ = "upcoming_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime]
    address: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    image: Mapped[str] = mapped_column(String(500))
    type_sport_id: Mapped[int] = mapped_column(
        ForeignKey("types_sports.id", ondelete="CASCADE")
    )

    type_sport: Mapped["TypesSports"] = relationship(back_populates="uncoming_events")
