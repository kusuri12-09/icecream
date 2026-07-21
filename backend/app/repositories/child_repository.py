from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Child


def find_by_id(db: Session, child_id: int) -> Child | None:
    return db.get(Child, child_id)


def list_by_parent(db: Session, parent_id: int) -> list[Child]:
    return list(db.scalars(select(Child).where(Child.parent_id == parent_id).order_by(Child.id)).all())


def save(db: Session, child: Child) -> Child:
    db.add(child)
    db.commit()
    db.refresh(child)
    return child


def delete(db: Session, child: Child) -> None:
    db.delete(child)
    db.commit()
