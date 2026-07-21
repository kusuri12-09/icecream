from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Center


def find_by_id(db: Session, center_id: int) -> Center | None:
    return db.get(Center, center_id)


def list_all(db: Session) -> list[Center]:
    return list(db.scalars(select(Center)).all())
