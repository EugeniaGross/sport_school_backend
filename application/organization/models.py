from datetime import time
import enum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text

from database import Base


class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(String(500))
    email: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(500))
    telegram_link: Mapped[Optional[str]] = mapped_column(String(100))
    vk_link: Mapped[Optional[str]] = mapped_column(String(100))
    whats_app_link: Mapped[Optional[str]] = mapped_column(String(100))
    rutube_link: Mapped[Optional[str]] = mapped_column(String(100))

    phones: Mapped[list["OrganizationPhone"]] = relationship(
        back_populates="organization"
    )
    sport_objects: Mapped[list["OrganizationSportObject"]] = relationship(
        back_populates="organization"
    )

    def __repr__(self):
        return f"{self.name}"


class OrganizationSportObject(Base):
    __tablename__ = "organization_sport_objects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    description: Mapped[Optional[str]] = mapped_column(Text())
    image: Mapped[str] = mapped_column(String(500))
    start_works: Mapped[time]
    end_works: Mapped[time]
    phone: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(500))
    address: Mapped[str] = mapped_column(String(500))

    organization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE")
    )

    organization: Mapped[Optional["Organization"]] = relationship(
        back_populates="sport_objects"
    )

    def __repr__(self):
        return f"{self.name}"


class OrganizationPhone(Base):
    __tablename__ = "organization_phones"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(100))

    organization_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE")
    )

    organization: Mapped[Optional["Organization"]] = relationship(
        back_populates="phones"
    )

    def __repr__(self):
        return f"{self.phone}"


class OrganizationInfo(Base):
    __tablename__ = "organization_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(1000))
    description: Mapped[Optional[str]] = mapped_column(Text())

    documents: Mapped[list["OrganizationDocument"]] = relationship(
        back_populates="organization_info"
    )

    def __repr__(self):
        return f"{self.category}"


class DocumentCategory(Base):
    __tablename__ = "document_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))

    documents: Mapped[list["OrganizationDocument"]] = relationship(
        back_populates="category"
    )

    def __repr__(self):
        return f"{self.name}"


class OrganizationDocument(Base):
    __tablename__ = "organization_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(1000))
    file: Mapped[str] = mapped_column(String(500))
    organization_info_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("organization_info.id", ondelete="CASCADE"), nullable=True
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("document_category.id", ondelete="CASCADE"), nullable=True
    )

    organization_info: Mapped[Optional["OrganizationInfo"]] = relationship(
        back_populates="documents"
    )
    category: Mapped[Optional["DocumentCategory"]] = relationship(
        back_populates="documents"
    )

    def __repr__(self):
        return f"{self.name}"
