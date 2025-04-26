from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

from database import Base

if TYPE_CHECKING:
    from athletes.models import Athlet
    from coaches.models import Coach
    from upcoming_events.models import UpcommingEvents


class TypesSports(Base):
    __tablename__ = "types_sports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())

    uncoming_events: Mapped[list["UpcommingEvents"]] = relationship(
        back_populates="type_sport"
    )
    coaches: Mapped[list["Coach"]] = relationship(back_populates="type_sport")
    athletes: Mapped[list["Athlet"]] = relationship(
        back_populates="type_sport"
    )

    def __repr__(self):
        return f"{self.name}"
