from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query

from app.api.common import DbDep, ParentDep, dump, success
from app.core.ids import encode_id
from app.core.utils import pages, to_float
from app.schemas import CenterOut
from app.services import center_service


router = APIRouter(prefix="/api/v1/centers", tags=["centers"])


def cache_is_stale(synced_at: datetime) -> bool:
    timestamp = synced_at if synced_at.tzinfo else synced_at.replace(tzinfo=timezone.utc)
    return timestamp < datetime.now(timezone.utc) - timedelta(days=7)


@router.get("")
def centers(
    parent: ParentDep,
    db: DbDep,
    lat: float | None = Query(None, ge=-90, le=90),
    lng: float | None = Query(None, ge=-180, le=180),
    radius_km: float = Query(10, ge=0.1, le=500, alias="radiusKm"),
    sido: str | None = Query(None),
    sido_sigungu: str | None = Query(None, alias="sidoSigungu"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> dict:
    del parent
    result = center_service.search(db, lat, lng, radius_km, sido, sido_sigungu)
    total = len(result)
    selected = result[(page - 1) * size : (page - 1) * size + size]
    items = [
        dump(
            CenterOut(
                id=encode_id("center", center.id),
                name=center.name,
                address=center.address,
                sido=center.sido,
                sido_sigungu=center.sido_sigungu,
                latitude=to_float(center.latitude),
                longitude=to_float(center.longitude),
                distance_km=round(distance, 2) if distance is not None else None,
                reservation_url=f"https://nfa.kspo.or.kr/reserve/{center.ext_center_id}",
                stale=cache_is_stale(center.synced_at),
            )
        )
        for center, distance in selected
    ]
    return success({"items": items, "page": page, "size": size, "totalElements": total, "totalPages": pages(total, size)})
