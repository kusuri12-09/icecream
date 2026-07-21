from datetime import datetime, timezone
from contextlib import asynccontextmanager
from math import asin, cos, radians, sin, sqrt
from typing import Annotated

from fastapi import Depends, FastAPI, Query
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.core.config import get_settings
from app.core.errors import AppError, app_error_handler, validation_error_handler
from app.core.ids import decode_id, encode_id
from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.core.utils import age_months, pages, to_float
from app.db import Base, engine, get_db
from app.external.kspo_client import ExternalApiUnavailable, KspoClient
from app.models import ActivityVideo, Center, Child, Measurement, MeasurementItem, Parent
from app.schemas import (
    ActivityOut, AuthData, CenterBrief, CenterOut, ChildCreate, ChildOut, ChildUpdate,
    FitnessElement, Gender, Grade, GradeHistory, GrowthSeries, ItemKey, LoginRequest, MeasurementCreate,
    MeasurementItemOut, MeasurementListItem, MeasurementOut, MeasurementType,
    ParentBrief, ParentOut, ProfileOut, RegionalInsight, RegionMapItem, SeriesPoint,
    SignupRequest, SyncRequest,
)
from app.services.diagnosis_engine import API_ITEMS, judge, load_criteria
from app.services.sync_service import sync_targets

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="아이쑥크림 API", version="0.1.0", lifespan=lifespan)
app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_error_handler)  # type: ignore[arg-type]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
bearer = HTTPBearer(auto_error=False)


def success(data: object) -> dict:
    return {"success": True, "data": data}


def dump(value: object) -> dict:
    return value.model_dump(by_alias=True, mode="json", exclude_none=True)  # type: ignore[attr-defined]


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
    items = []
    for item in measurement.items:
        key = API_ITEMS.get(item.item_key, item.item_key)
        items.append(MeasurementItemOut(
            item_key=ItemKey(item.item_key),
            label=criteria["items"][key]["label"],
            value=float(item.value),
            item_grade=Grade(item.item_grade) if item.item_grade else None,
            is_weak=item.item_grade == "SEED" and item.item_key != "BMI",
        ))
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


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/v1/auth/signup", status_code=201)
def signup(payload: SignupRequest, db: DbDep) -> dict:
    email = str(payload.email).lower()
    if db.scalar(select(Parent).where(Parent.email == email)):
        raise AppError("PARENT_ALREADY_EXISTS", "이미 가입된 이메일입니다.", 409)
    parent = Parent(
        email=email,
        password_hash=hash_password(payload.password),
        is_admin=email in settings.admin_email_set,
    )
    db.add(parent)
    db.commit()
    db.refresh(parent)
    auth = AuthData(parent=parent_brief(parent), access_token=create_access_token(parent.id, parent.is_admin))
    return success(dump(auth))


@app.post("/api/v1/auth/login")
def login(payload: LoginRequest, db: DbDep) -> dict:
    parent = db.scalar(select(Parent).where(Parent.email == str(payload.email).lower()))
    if parent is None or not verify_password(payload.password, parent.password_hash):
        raise AppError("AUTH_INVALID_CREDENTIALS", "이메일 또는 비밀번호가 올바르지 않습니다.", 401)
    auth = AuthData(parent=parent_brief(parent), access_token=create_access_token(parent.id, parent.is_admin))
    return success(dump(auth))


@app.get("/api/v1/auth/me")
def me(parent: ParentDep) -> dict:
    result = ParentOut(id=encode_id("parent", parent.public_id), email=parent.email, created_at=parent.created_at)
    return success(dump(result))


@app.post("/api/v1/children", status_code=201)
def create_child(payload: ChildCreate, parent: ParentDep, db: DbDep) -> dict:
    child = Child(parent_id=parent.id, nickname=payload.nickname, gender=payload.gender, birth_year_month=payload.birth_year_month)
    db.add(child)
    db.commit()
    db.refresh(child)
    return success(dump(child_out(child)))


@app.get("/api/v1/children")
def list_children(parent: ParentDep, db: DbDep) -> dict:
    children = db.scalars(select(Child).where(Child.parent_id == parent.id).order_by(Child.id)).all()
    items = [dump(child_out(child, include_created=False)) for child in children]
    return success({"items": items, "page": 1, "size": 20, "totalElements": len(items), "totalPages": 1 if items else 0})


@app.get("/api/v1/children/{child_id}")
def get_child(child_id: str, parent: ParentDep, db: DbDep) -> dict:
    return success(dump(child_out(owned_child(db, parent, child_id))))


@app.patch("/api/v1/children/{child_id}")
def update_child(child_id: str, payload: ChildUpdate, parent: ParentDep, db: DbDep) -> dict:
    child = owned_child(db, parent, child_id)
    for field in ("nickname", "gender", "birth_year_month"):
        value = getattr(payload, field)
        if value is not None:
            setattr(child, field, value)
    db.commit()
    db.refresh(child)
    return success(dump(child_out(child)))


@app.delete("/api/v1/children/{child_id}")
def delete_child(child_id: str, parent: ParentDep, db: DbDep) -> dict:
    owned_child(db, parent, child_id)
    db.delete(db.get(Child, decode_id(child_id, "child")))
    db.commit()
    return success({"id": child_id, "deleted": True})


@app.post("/api/v1/children/{child_id}/measurements", status_code=201)
def create_measurement(child_id: str, payload: MeasurementCreate, parent: ParentDep, db: DbDep) -> dict:
    child = owned_child(db, parent, child_id)
    months = age_months(child.birth_year_month, payload.measured_at)
    if not 48 <= months <= 83:
        raise AppError("INVALID_REQUEST_BODY", "진단 대상 연령은 48~83개월입니다.", 422)
    center = None
    if payload.center_id:
        center = db.get(Center, decode_id(payload.center_id, "center"))
        if center is None:
            raise AppError("CENTER_NOT_FOUND", "센터를 찾을 수 없습니다.", 404)
    values = {item.item_key.value: item.value for item in payload.items}
    result = judge(child.gender, months, values)
    measurement = Measurement(
        child_id=child.id,
        center_id=center.id if payload.type is MeasurementType.OFFICIAL and center else None,
        type=payload.type,
        grade=result.grade,
        age_months_at_measure=months,
        measured_at=payload.measured_at,
    )
    db.add(measurement)
    db.flush()
    for item in payload.items:
        db.add(MeasurementItem(
            measurement_id=measurement.id,
            item_key=item.item_key,
            value=item.value,
            item_grade=result.item_grades.get(item.item_key),
        ))
    if center and payload.type is MeasurementType.OFFICIAL:
        center.measure_count += 1
    db.commit()
    saved = owned_measurement(db, parent, encode_id("measurement", measurement.id))
    return success(dump(measurement_out(saved)))


@app.get("/api/v1/children/{child_id}/measurements")
def list_measurements(
    child_id: str,
    parent: ParentDep,
    db: DbDep,
    type: MeasurementType | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort: str = Query("measuredAt,desc"),
) -> dict:
    child = owned_child(db, parent, child_id)
    query = select(Measurement).where(Measurement.child_id == child.id)
    if type:
        query = query.where(Measurement.type == type)
    query = query.order_by(Measurement.measured_at.desc() if sort.endswith(",desc") else Measurement.measured_at.asc())
    all_items = db.scalars(query).all()
    selected = all_items[(page - 1) * size : (page - 1) * size + size]
    data = {
        "items": [dump(MeasurementListItem(id=encode_id("measurement", item.id), type=MeasurementType(item.type), measured_at=item.measured_at, grade=Grade(item.grade or "SEED"))) for item in selected],
        "page": page,
        "size": size,
        "totalElements": len(all_items),
        "totalPages": pages(len(all_items), size),
    }
    return success(data)


@app.get("/api/v1/measurements/{measurement_id}")
def get_measurement(measurement_id: str, parent: ParentDep, db: DbDep) -> dict:
    return success(dump(measurement_out(owned_measurement(db, parent, measurement_id))))


@app.delete("/api/v1/measurements/{measurement_id}")
def delete_measurement(measurement_id: str, parent: ParentDep, db: DbDep) -> dict:
    owned_measurement(db, parent, measurement_id)
    db.delete(db.get(Measurement, decode_id(measurement_id, "measurement")))
    db.commit()
    return success({"id": measurement_id, "deleted": True})


@app.get("/api/v1/children/{child_id}/growth")
def growth(child_id: str, parent: ParentDep, db: DbDep, item_key: ItemKey | None = None) -> dict:
    child = owned_child(db, parent, child_id)
    rows = db.scalars(
        select(Measurement).options(joinedload(Measurement.items))
        .where(Measurement.child_id == child.id).order_by(Measurement.measured_at)
    ).unique().all()
    criteria = load_criteria()
    selected = [item_key.value] if item_key else list(API_ITEMS)
    series = []
    for api_key in selected:
        key = API_ITEMS[api_key]
        points = [
            SeriesPoint(measured_at=row.measured_at, value=float(item.value), type=MeasurementType(row.type))
            for row in rows for item in row.items if item.item_key == api_key
        ]
        if points:
            series.append(GrowthSeries(item_key=ItemKey(api_key), label=criteria["items"][key]["label"], unit=criteria["items"][key]["unit"], points=points))
    grades = [GradeHistory(measured_at=row.measured_at, grade=Grade(row.grade)) for row in rows if row.grade]
    return success({"childId": child_id, "series": [dump(item) for item in series], "gradeHistory": [dump(item) for item in grades]})


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    earth = 6371.0
    d_lat, d_lng = radians(lat2 - lat1), radians(lng2 - lng1)
    value = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return 2 * earth * asin(sqrt(value))


def parse_fitness_element(value: str | None) -> FitnessElement | None:
    if value is None:
        return None
    try:
        return FitnessElement(value)
    except ValueError:
        return None


@app.get("/api/v1/centers")
def centers(
    parent: ParentDep,
    db: DbDep,
    lat: float | None = Query(None, ge=-90, le=90),
    lng: float | None = Query(None, ge=-180, le=180),
    radius_km: float = Query(10, ge=0.1, le=500),
    sido_sigungu: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> dict:
    del parent
    if (lat is None) != (lng is None):
        raise AppError("INVALID_REQUEST_BODY", "lat과 lng은 함께 입력해야 합니다.", 422)
    rows = list(db.scalars(select(Center)).all())
    if not rows:
        raise AppError("EXTERNAL_API_UNAVAILABLE", "외부 데이터를 일시적으로 사용할 수 없습니다.", 503)
    result = []
    for center in rows:
        if sido_sigungu and (center.sido_sigungu or "") != sido_sigungu:
            continue
        distance = None
        if lat is not None and center.latitude is not None and center.longitude is not None:
            assert lng is not None
            distance = haversine(lat, lng, float(center.latitude), float(center.longitude))
            if distance > radius_km:
                continue
        result.append((center, distance))
    if lat is not None:
        result.sort(key=lambda pair: pair[1] if pair[1] is not None else float("inf"))
    total = len(result)
    selected = result[(page - 1) * size : (page - 1) * size + size]
    items = [
        dump(CenterOut(
            id=encode_id("center", center.id), name=center.name, address=center.address,
            sido_sigungu=center.sido_sigungu, latitude=to_float(center.latitude), longitude=to_float(center.longitude),
            distance_km=round(distance, 2) if distance is not None else None,
            reservation_url=f"https://nfa.kspo.or.kr/reserve/{center.ext_center_id}",
        ))
        for center, distance in selected
    ]
    return success({"items": items, "page": page, "size": size, "totalElements": total, "totalPages": pages(total, size)})


@app.get("/api/v1/activities")
def activities(
    parent: ParentDep,
    db: DbDep,
    fitness_element: str | None = None,
    measurement_id: str | None = None,
    age_group: str = "PRESCHOOL",
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> dict:
    requested: set[str] = set()
    if measurement_id:
        measurement = owned_measurement(db, parent, measurement_id)
        requested = {item.item_key for item in measurement.items if item.item_grade == "SEED" and item.item_key != "BMI"}
    elif fitness_element:
        requested = {item.strip().upper() for item in fitness_element.split(",")}
    rows = list(db.scalars(select(ActivityVideo).where(func.upper(ActivityVideo.age_group) == age_group.upper())).all())
    if not rows:
        raise AppError("EXTERNAL_API_UNAVAILABLE", "외부 데이터를 일시적으로 사용할 수 없습니다.", 503)
    if requested:
        rows = [row for row in rows if row.fitness_element in requested]
    total = len(rows)
    selected = rows[(page - 1) * size : (page - 1) * size + size]
    items = [dump(ActivityOut(id=encode_id("video", row.id), title=row.title, fitness_element=parse_fitness_element(row.fitness_element), age_group=row.age_group, url=row.url)) for row in selected]
    return success({"items": items, "page": page, "size": size, "totalElements": total, "totalPages": pages(total, size)})


@app.get("/api/v1/insights/regional")
def regional_insight(parent: ParentDep, db: DbDep, sido_sigungu: str | None = None) -> dict:
    del parent
    values = list(db.scalars(select(Center)).all())
    grouped: dict[str, int] = {}
    for center in values:
        if center.sido_sigungu:
            grouped[center.sido_sigungu] = grouped.get(center.sido_sigungu, 0) + center.measure_count
    region = sido_sigungu or (max(grouped, key=lambda key: grouped[key]) if grouped else "전국")
    region_count = grouped.get(region, 0)
    national_avg = sum(grouped.values()) / len(grouped) if grouped else 0
    if not grouped:
        level, percentile = "INSUFFICIENT", 0
    elif region_count > national_avg * 1.1:
        level, percentile = "ABOVE_AVG", 75
    elif region_count < national_avg * 0.9:
        level, percentile = "BELOW_AVG", 28
    else:
        level, percentile = "AROUND_AVG", 50
    message = f"{region}의 유아 체력측정 참여 현황을 확인해보세요."
    if level == "BELOW_AVG":
        message = f"{region}의 유아 체력측정 참여는 전국 평균보다 낮은 편이에요. 가까운 센터에서 측정해보세요."
    result = RegionalInsight(
        region=region, region_measure_count=region_count, national_avg=round(national_avg, 2),
        relative_level=level, percentile=percentile, message=message,
        cta={"type": "CENTER_CONNECT", "label": "근처 센터 찾기"},
    )
    return success(dump(result))


@app.get("/api/v1/insights/regional/map")
def regional_map(parent: ParentDep, db: DbDep) -> dict:
    del parent
    values = list(db.scalars(select(Center)).all())
    grouped: dict[str, int] = {}
    for center in values:
        if center.sido_sigungu:
            grouped[center.sido_sigungu] = grouped.get(center.sido_sigungu, 0) + center.measure_count
    maximum = max(grouped.values(), default=0)
    items = [
        dump(RegionMapItem(sido_sigungu=region, measure_count=count, participation_rate=round(count / maximum, 4) if maximum else 0))
        for region, count in sorted(grouped.items(), key=lambda pair: pair[1], reverse=True)
    ]
    return success({"regions": items, "fallback": not bool(items)})


@app.post("/api/v1/internal/sync")
def sync(payload: SyncRequest, parent: ParentDep, db: DbDep) -> dict:
    if not parent.is_admin:
        raise AppError("AUTH_UNAUTHORIZED", "관리자 인증이 필요합니다.", 401)
    if not settings.kspo_api_key:
        raise ExternalApiUnavailable()
    if "CENTERS" in payload.targets and not settings.kspo_center_url:
        raise ExternalApiUnavailable()
    if "ACTIVITIES" in payload.targets and not settings.kspo_activity_url:
        raise ExternalApiUnavailable()
    try:
        synced = sync_targets(
            db,
            KspoClient(settings.kspo_api_key),
            payload.targets,
            settings.kspo_center_url,
            settings.kspo_activity_url,
        )
    except ExternalApiUnavailable:
        db.rollback()
        raise
    return success({"synced": synced, "syncedAt": datetime.now(timezone.utc).isoformat()})
