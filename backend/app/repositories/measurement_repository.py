from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Measurement


def find_by_id(db: Session, measurement_id: int) -> Measurement | None:
    return db.scalar(
        select(Measurement)
        .options(joinedload(Measurement.items), joinedload(Measurement.center), joinedload(Measurement.child))
        .where(Measurement.id == measurement_id)
    )


def list_by_child(
    db: Session,
    child_id: int,
    measurement_type: str | None = None,
    descending: bool = True,
) -> list[Measurement]:
    query = select(Measurement).where(Measurement.child_id == child_id)
    if measurement_type:
        query = query.where(Measurement.type == measurement_type)
    order = Measurement.measured_at.desc() if descending else Measurement.measured_at.asc()
    return list(db.scalars(query.order_by(order)).all())


def list_with_items_by_child(db: Session, child_id: int) -> list[Measurement]:
    return list(
        db.scalars(
            select(Measurement)
            .options(joinedload(Measurement.items))
            .where(Measurement.child_id == child_id)
            .order_by(Measurement.measured_at)
        ).unique().all()
    )


def create(db: Session, measurement: Measurement) -> Measurement:
    db.add(measurement)
    db.flush()
    return measurement


def delete(db: Session, measurement: Measurement) -> None:
    db.delete(measurement)
    db.commit()
