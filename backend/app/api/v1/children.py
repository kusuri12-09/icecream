from fastapi import APIRouter

from app.api.common import DbDep, ParentDep, child_out, dump, success
from app.schemas import ChildCreate, ChildUpdate
from app.services import child_service


router = APIRouter(prefix="/api/v1/children", tags=["children"])


@router.post("", status_code=201)
def create_child(payload: ChildCreate, parent: ParentDep, db: DbDep) -> dict:
    return success(dump(child_out(child_service.create(db, parent, payload))))


@router.get("")
def list_children(parent: ParentDep, db: DbDep) -> dict:
    items = [dump(child_out(child, include_created=False)) for child in child_service.list_all(db, parent)]
    return success({"items": items, "page": 1, "size": 20, "totalElements": len(items), "totalPages": 1 if items else 0})


@router.get("/{child_id}")
def get_child(child_id: str, parent: ParentDep, db: DbDep) -> dict:
    return success(dump(child_out(child_service.get_owned(db, parent, child_id))))


@router.patch("/{child_id}")
def update_child(child_id: str, payload: ChildUpdate, parent: ParentDep, db: DbDep) -> dict:
    return success(dump(child_out(child_service.update(db, parent, child_id, payload))))


@router.delete("/{child_id}")
def delete_child(child_id: str, parent: ParentDep, db: DbDep) -> dict:
    child_service.delete(db, parent, child_id)
    return success({"id": child_id, "deleted": True})
