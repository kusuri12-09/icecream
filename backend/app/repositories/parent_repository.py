from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Parent


def find_by_email(db: Session, email: str) -> Parent | None:
    return db.scalar(select(Parent).where(Parent.email == email))


def save(db: Session, parent: Parent) -> Parent:
    db.add(parent)
    db.commit()
    db.refresh(parent)
    return parent
