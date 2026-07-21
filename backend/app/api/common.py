from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.errors import AppError
from app.core.ids import decode_id, encode_id
from app.core.security import decode_access_token
from app.core.utils import age_months
from app.db import get_db
from app.models import Child, Measurement, Parent
from app.schemas import (
    CenterBrief,
    ChildOut,
    Gender,
    Grade,
    ItemKey,
    MeasurementItemOut,
    MeasurementOut,
    MeasurementType,
    ParentBrief,
    ProfileOut,
)
from app.services.diagnosis_engine import API_ITEMS, judge, load_criteria


bearer = HTTPBearer(auto_error=False)


def success(data: object) -> dict:
    return {"success": True, "data": data}


def dump(value: object) -> dict:
    return value.model_dump(by_alias=True, mode="json", exclude_none=True)  # type: ignore[attr-defined]


def current_parent(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    db: Annotated[Session, Depends(get_db)],
) -> Parent:
    if credentials is None:
        raise AppError("AUTH_UNAUTHORIZED", "인증이 필요합니다.", 401)
    try:
        payload = decode_access_token(credentials.credentials)
        parent_id = int(payload["sub"])
    except (ValueError, KeyError, TypeError):
        raise AppError("AUTH_UNAUTHORIZED", "인증이 필요합니다.", 401)
    parent = db.get(Parent, parent_id)
    if parent is None:
        raise AppError("AUTH_UNAUTHORIZED", "인증이 필요합니다.", 401)
    return parent


ParentDep = Annotated[Parent, Depends(current_parent)]
DbDep = Annotated[Session, Depends(get_db)]


def parent_brief(parent: Parent) -> ParentBrief:
    return ParentBrief(id=encode_id("parent", parent.public_id), email=parent.email)


def child_out(child: Child, include_created: bool = True) -> ChildOut:
    months = age_months(child.birth_year_month)
    return ChildOut(
        id=encode_id("child", child.id),
        nickname=child.nickname,
        gender=Gender(child.gender),
        birth_year_month=child.birth_year_month.strftime("%Y-%m"),
        age_months=months,
        in_target_range=48 <= months <= 83,
        created_at=child.created_at if include_created else None,
    )


def owned_child(db: Session, parent: Parent, external_id: str) -> Child:
    child = db.get(Child, decode_id(external_id, "child"))
    if child is None:
        raise AppError("CHILD_NOT_FOUND", "자녀 정보를 찾을 수 없습니다.", 404)
    if child.parent_id != parent.id:
        raise AppError("CHILD_ACCESS_DENIED", "해당 자녀에 접근할 수 없습니다.", 403)
    return child


def owned_measurement(db: Session, parent: Parent, external_id: str) -> Measurement:
    measurement = db.scalar(
        select(Measurement)
        .options(joinedload(Measurement.items), joinedload(Measurement.center), joinedload(Measurement.child))
        .where(Measurement.id == decode_id(external_id, "measurement"))
    )
    if measurement is None:
        raise AppError("MEASUREMENT_NOT_FOUND", "측정 기록을 찾을 수 없습니다.", 404)
    if measurement.child.parent_id != parent.id:
        raise AppError("MEASUREMENT_ACCESS_DENIED", "해당 측정 기록에 접근할 수 없습니다.", 403)
    return measurement


def measurement_out(measurement: Measurement) -> MeasurementOut:
    criteria = load_criteria()
    values = {API_ITEMS.get(item.item_key, item.item_key): float(item.value) for item in measurement.items}
    result = judge(measurement.child.gender, measurement.age_months_at_measure, values)
    items = [
        MeasurementItemOut(
            item_key=ItemKey(item.item_key),
            label=criteria["items"][API_ITEMS.get(item.item_key, item.item_key)]["label"],
            value=float(item.value),
            item_grade=Grade(item.item_grade) if item.item_grade else None,
            is_weak=item.item_grade == "SEED" and item.item_key != "BMI",
        )
        for item in measurement.items
    ]
    center = None
    if measurement.center:
        center = CenterBrief(id=encode_id("center", measurement.center.id), name=measurement.center.name)
    return MeasurementOut(
        id=encode_id("measurement", measurement.id),
        child_id=encode_id("child", measurement.child_id),
        type=MeasurementType(measurement.type),
        measured_at=measurement.measured_at,
        age_months_at_measure=measurement.age_months_at_measure,
        grade=Grade(measurement.grade or result.grade),
        center=center,
        items=items,
        profile=ProfileOut(
            strengths=[ItemKey(item) for item in result.strengths],
            weaknesses=[ItemKey(item) for item in result.weaknesses],
            undecidable_grades=[Grade(item) for item in result.undecidable_grades],
        ),
        created_at=measurement.created_at,
    )


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
