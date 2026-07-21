from app.core.errors import AppError
from app.core.ids import decode_id, encode_id
from app.core.utils import age_months
from app.models import Center, Measurement, MeasurementItem, Parent
from app.repositories import center_repository, child_repository, measurement_repository
from app.schemas import (
    Grade,
    GradeHistory,
    GrowthSeries,
    ItemKey,
    MeasurementCreate,
    MeasurementListItem,
    MeasurementType,
    SeriesPoint,
)
from app.services.diagnosis_engine import API_ITEMS, judge, load_criteria
from sqlalchemy.orm import Session


def get_owned(db: Session, parent: Parent, external_id: str) -> Measurement:
    measurement = measurement_repository.find_by_id(db, decode_id(external_id, "measurement"))
    if measurement is None:
        raise AppError("MEASUREMENT_NOT_FOUND", "측정 기록을 찾을 수 없습니다.", 404)
    if measurement.child.parent_id != parent.id:
        raise AppError("MEASUREMENT_ACCESS_DENIED", "해당 측정 기록에 접근할 수 없습니다.", 403)
    return measurement


def create(db: Session, parent: Parent, child_external_id: str, payload: MeasurementCreate) -> Measurement:
    child = child_repository.find_by_id(db, decode_id(child_external_id, "child"))
    if child is None:
        raise AppError("CHILD_NOT_FOUND", "자녀 정보를 찾을 수 없습니다.", 404)
    if child.parent_id != parent.id:
        raise AppError("CHILD_ACCESS_DENIED", "해당 자녀에 접근할 수 없습니다.", 403)
    months = age_months(child.birth_year_month, payload.measured_at)
    if not 48 <= months <= 83:
        raise AppError("INVALID_REQUEST_BODY", "진단 대상 연령은 48~83개월입니다.", 422)
    center: Center | None = None
    if payload.center_id:
        center = center_repository.find_by_id(db, decode_id(payload.center_id, "center"))
        if center is None:
            raise AppError("CENTER_NOT_FOUND", "센터를 찾을 수 없습니다.", 404)
    values = {item.item_key.value: item.value for item in payload.items}
    result = judge(child.gender, months, values)
    measurement = measurement_repository.create(
        db,
        Measurement(
            child_id=child.id,
            center_id=center.id if payload.type is MeasurementType.OFFICIAL and center else None,
            type=payload.type,
            grade=result.grade,
            age_months_at_measure=months,
            measured_at=payload.measured_at,
        ),
    )
    for item in payload.items:
        db.add(
            MeasurementItem(
                measurement_id=measurement.id,
                item_key=item.item_key,
                value=item.value,
                item_grade=result.item_grades.get(item.item_key),
            )
        )
    if center and payload.type is MeasurementType.OFFICIAL:
        center.measure_count += 1
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    return get_owned(db, parent, encode_id("measurement", measurement.id))


def list_page(
    db: Session,
    parent: Parent,
    child_external_id: str,
    measurement_type: MeasurementType | None,
    page: int,
    size: int,
    sort: str,
) -> tuple[list[MeasurementListItem], int]:
    child = child_repository.find_by_id(db, decode_id(child_external_id, "child"))
    if child is None:
        raise AppError("CHILD_NOT_FOUND", "자녀 정보를 찾을 수 없습니다.", 404)
    if child.parent_id != parent.id:
        raise AppError("CHILD_ACCESS_DENIED", "해당 자녀에 접근할 수 없습니다.", 403)
    rows = measurement_repository.list_by_child(db, child.id, measurement_type, not sort.endswith(",asc"))
    selected = rows[(page - 1) * size : (page - 1) * size + size]
    return (
        [
            MeasurementListItem(
                id=encode_id("measurement", row.id),
                type=MeasurementType(row.type),
                measured_at=row.measured_at,
                grade=Grade(row.grade or "SEED"),
            )
            for row in selected
        ],
        len(rows),
    )


def delete(db: Session, parent: Parent, external_id: str) -> None:
    measurement_repository.delete(db, get_owned(db, parent, external_id))


def growth(db: Session, parent: Parent, child_external_id: str, item_key: ItemKey | None) -> dict:
    child = child_repository.find_by_id(db, decode_id(child_external_id, "child"))
    if child is None:
        raise AppError("CHILD_NOT_FOUND", "자녀 정보를 찾을 수 없습니다.", 404)
    if child.parent_id != parent.id:
        raise AppError("CHILD_ACCESS_DENIED", "해당 자녀에 접근할 수 없습니다.", 403)
    rows = measurement_repository.list_with_items_by_child(db, child.id)
    criteria = load_criteria()
    selected = [item_key.value] if item_key else list(API_ITEMS)
    series = []
    for api_key in selected:
        key = API_ITEMS[api_key]
        points = [
            SeriesPoint(measured_at=row.measured_at, value=float(item.value), type=MeasurementType(row.type))
            for row in rows
            for item in row.items
            if item.item_key == api_key
        ]
        if points:
            series.append(GrowthSeries(item_key=ItemKey(api_key), label=criteria["items"][key]["label"], unit=criteria["items"][key]["unit"], points=points))
    grades = [GradeHistory(measured_at=row.measured_at, grade=Grade(row.grade or "SEED")) for row in rows]
    return {"childId": child_external_id, "series": series, "gradeHistory": grades}
