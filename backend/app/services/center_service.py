"""체력인증센터 DB 캐시 조회 서비스.

공공데이터 API 호출과 캐시 갱신은 ``sync_service``의 관리자·Cron 동기화 경로에서만 수행한다.
"""

from math import asin, cos, radians, sin, sqrt

from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models import Center
from app.repositories import center_repository


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    earth = 6371.0
    d_lat, d_lng = radians(lat2 - lat1), radians(lng2 - lng1)
    value = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return 2 * earth * asin(sqrt(value))


def search(
    db: Session,
    lat: float | None,
    lng: float | None,
    radius_km: float,
    name: str | None,
    sido: str | None,
    sido_sigungu: str | None,
) -> list[tuple[Center, float | None]]:
    if (lat is None) != (lng is None):
        raise AppError("INVALID_REQUEST_BODY", "lat과 lng은 함께 입력해야 합니다.", 422)
    rows = center_repository.list_all(db)
    if not rows:
        raise AppError("CENTER_NOT_FOUND", "체력인증센터를 찾을 수 없습니다.", 404)
    result: list[tuple[Center, float | None]] = []
    for center in rows:
        if name and name.casefold() not in center.name.casefold():
            continue
        if sido and (center.sido or "") != sido:
            continue
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
    return result
