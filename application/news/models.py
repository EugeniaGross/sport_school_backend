from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import validates

from database import Base

from types_sports.models import TypesSports


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    date: Mapped[date]
    address: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text())
    image: Mapped[str] = mapped_column(String(500))
    type_sport_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("types_sports.id", ondelete="CASCADE"), nullable=True
    )

    type_sport: Mapped["TypesSports"] = relationship(back_populates="news")

    photos: Mapped[list["PhotoNews"]] = relationship(back_populates="news")

    def __repr__(self):
        return f"{self.name}"


class PhotoNews(Base):
    __tablename__ = "photo_news"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(500))
    order: Mapped[int]
    news_id: Mapped[int] = mapped_column(
        ForeignKey("news.id", ondelete="CASCADE"), nullable=True
    )

    news: Mapped["News"] = relationship(back_populates="photos")

    @validates("order")
    def validate_order(self, key, value):
        if value <= 0:
            raise ValueError("Order must be greater than 0")
        return value

    def __repr__(self):
        return f"{self.image}"
