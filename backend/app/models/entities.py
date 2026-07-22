from datetime import date, datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class Parent(TimestampMixin, Base):
    __tablename__ = "parent"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    public_id: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid4()), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    children: Mapped[list["Child"]] = relationship(back_populates="parent", cascade="all, delete-orphan")


class Child(TimestampMixin, Base):
    __tablename__ = "child"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id", ondelete="CASCADE"), index=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    birth_year_month: Mapped[date] = mapped_column(Date, nullable=False)
    parent: Mapped[Parent] = relationship(back_populates="children")
    measurements: Mapped[list["Measurement"]] = relationship(back_populates="child", cascade="all, delete-orphan")
    __table_args__ = (CheckConstraint("gender IN ('MALE', 'FEMALE')", name="ck_child_gender"),)


class Center(TimestampMixin, Base):
    __tablename__ = "center"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ext_center_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    sido: Mapped[str | None] = mapped_column(String(50), index=True)
    sido_sigungu: Mapped[str | None] = mapped_column(String(50))
    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6))
    measure_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    measurements: Mapped[list["Measurement"]] = relationship(back_populates="center")
    __table_args__ = (
        Index("ix_center_sido_sigungu", "sido_sigungu"),
        Index("ix_center_lat_lng", "latitude", "longitude"),
    )


class Measurement(TimestampMixin, Base):
    __tablename__ = "measurement"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("child.id", ondelete="CASCADE"), index=True, nullable=False)
    center_id: Mapped[int | None] = mapped_column(ForeignKey("center.id", ondelete="SET NULL"), index=True)
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    grade: Mapped[str | None] = mapped_column(String(10))
    age_months_at_measure: Mapped[int] = mapped_column(Integer, nullable=False)
    measured_at: Mapped[date] = mapped_column(Date, nullable=False)
    child: Mapped[Child] = relationship(back_populates="measurements")
    center: Mapped[Center | None] = relationship(back_populates="measurements")
    items: Mapped[list["MeasurementItem"]] = relationship(back_populates="measurement", cascade="all, delete-orphan")
    __table_args__ = (
        Index("ix_measurement_child_measured", "child_id", "measured_at"),
        CheckConstraint("type IN ('OFFICIAL', 'SELF')", name="ck_measurement_type"),
    )


class MeasurementItem(TimestampMixin, Base):
    __tablename__ = "measurement_item"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    measurement_id: Mapped[int] = mapped_column(ForeignKey("measurement.id", ondelete="CASCADE"), nullable=False)
    item_key: Mapped[str] = mapped_column(String(20), nullable=False)
    value: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)
    item_grade: Mapped[str | None] = mapped_column(String(10))
    measurement: Mapped[Measurement] = relationship(back_populates="items")
    __table_args__ = (
        UniqueConstraint("measurement_id", "item_key", name="uq_item_per_measurement"),
        Index("ix_item_key_measurement", "item_key", "measurement_id"),
        CheckConstraint("value >= 0", name="ck_measurement_item_value"),
    )


class ActivityVideo(TimestampMixin, Base):
    __tablename__ = "activity_video"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ext_video_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    fitness_element: Mapped[str | None] = mapped_column(String(20), index=True)
    fitness_elements: Mapped[list[str] | None] = mapped_column(JSON)
    age_group: Mapped[str | None] = mapped_column(String(20), index=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    thumbnail_url: Mapped[str | None] = mapped_column(String(500))
    fitness_level: Mapped[str | None] = mapped_column(String(20))
    equipment: Mapped[str | None] = mapped_column(String(100))
    training_place: Mapped[str | None] = mapped_column(String(50))
    muscle_part: Mapped[str | None] = mapped_column(String(255))
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    source_fitness_factor: Mapped[str | None] = mapped_column(String(50))
    source_age_group: Mapped[str | None] = mapped_column(String(20))
    synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    __table_args__ = (Index("ix_video_element_age", "fitness_element", "age_group"),)


__all__ = ["ActivityVideo", "Base", "Center", "Child", "Measurement", "MeasurementItem", "Parent"]
