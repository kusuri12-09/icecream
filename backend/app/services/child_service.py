from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.ids import decode_id
from app.models import Child, Parent
from app.repositories import child_repository
from app.schemas import ChildCreate, ChildUpdate


def get_owned(db: Session, parent: Parent, external_id: str) -> Child:
    child = child_repository.find_by_id(db, decode_id(external_id, "child"))
    if child is None:
        raise AppError("CHILD_NOT_FOUND", "자녀 정보를 찾을 수 없습니다.", 404)
    if child.parent_id != parent.id:
        raise AppError("CHILD_ACCESS_DENIED", "해당 자녀에 접근할 수 없습니다.", 403)
    return child


def create(db: Session, parent: Parent, payload: ChildCreate) -> Child:
    return child_repository.save(
        db,
        Child(parent_id=parent.id, nickname=payload.nickname, gender=payload.gender, birth_year_month=payload.birth_year_month),
    )


def list_all(db: Session, parent: Parent) -> list[Child]:
    return child_repository.list_by_parent(db, parent.id)


def update(db: Session, parent: Parent, external_id: str, payload: ChildUpdate) -> Child:
    child = get_owned(db, parent, external_id)
    for field in ("nickname", "gender", "birth_year_month"):
        value = getattr(payload, field)
        if value is not None:
            setattr(child, field, value)
    return child_repository.save(db, child)


def delete(db: Session, parent: Parent, external_id: str) -> None:
    child_repository.delete(db, get_owned(db, parent, external_id))
