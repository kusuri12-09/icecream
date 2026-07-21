from fastapi import APIRouter, Query

from app.api.common import DbDep, ParentDep, dump, measurement_out, success
from app.core.utils import pages
from app.schemas import ItemKey, MeasurementCreate, MeasurementType
from app.services import measurement_service


router = APIRouter(tags=["measurements"])


@router.post("/api/v1/children/{child_id}/measurements", status_code=201)
def create_measurement(child_id: str, payload: MeasurementCreate, parent: ParentDep, db: DbDep) -> dict:
    return success(dump(measurement_out(measurement_service.create(db, parent, child_id, payload))))


@router.get("/api/v1/children/{child_id}/measurements")
def list_measurements(
    child_id: str,
    parent: ParentDep,
    db: DbDep,
    type: MeasurementType | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("measuredAt,desc"),
) -> dict:
    items, total = measurement_service.list_page(db, parent, child_id, type, page, size, sort)
    return success({"items": [dump(item) for item in items], "page": page, "size": size, "totalElements": total, "totalPages": pages(total, size)})


@router.get("/api/v1/measurements/{measurement_id}")
def get_measurement(measurement_id: str, parent: ParentDep, db: DbDep) -> dict:
    return success(dump(measurement_out(measurement_service.get_owned(db, parent, measurement_id))))


@router.delete("/api/v1/measurements/{measurement_id}")
def delete_measurement(measurement_id: str, parent: ParentDep, db: DbDep) -> dict:
    measurement_service.delete(db, parent, measurement_id)
    return success({"id": measurement_id, "deleted": True})


@router.get("/api/v1/children/{child_id}/growth")
def growth(child_id: str, parent: ParentDep, db: DbDep, item_key: ItemKey | None = Query(None, alias="itemKey")) -> dict:
    result = measurement_service.growth(db, parent, child_id, item_key)
    return success({"childId": result["childId"], "series": [dump(item) for item in result["series"]], "gradeHistory": [dump(item) for item in result["gradeHistory"]]})
