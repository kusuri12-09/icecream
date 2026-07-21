from dataclasses import dataclass
from typing import Any

import httpx

from app.core.errors import AppError


class ExternalApiUnavailable(AppError):
    def __init__(self, detail: str = "외부 데이터를 일시적으로 사용할 수 없습니다.") -> None:
        super().__init__("EXTERNAL_API_UNAVAILABLE", detail, 503)


@dataclass(frozen=True)
class CenterRecord:
    ext_center_id: str
    name: str
    address: str
    sido_sigungu: str | None
    latitude: float | None
    longitude: float | None


@dataclass(frozen=True)
class ActivityRecord:
    ext_video_id: str
    title: str
    fitness_element: str | None
    age_group: str | None
    url: str


def _first(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value
    return None


def _items(body: Any) -> list[dict[str, Any]]:
    if isinstance(body, list):
        return [item for item in body if isinstance(item, dict)]
    if not isinstance(body, dict):
        return []
    for key in ("items", "data", "item"):
        value = body.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = _items(value)
            if nested:
                return nested
    response = body.get("response")
    if response:
        return _items(response)
    return []


def _number(value: Any) -> float | None:
    try:
        return float(str(value).replace(",", "")) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def parse_sido_sigungu(address: str) -> str | None:
    parts = address.split()
    return " ".join(parts[:2]) if len(parts) >= 2 else None


class KspoClient:
    def __init__(self, api_key: str, timeout: float = 10.0) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def _get(self, url: str) -> Any:
        try:
            response = httpx.get(url, params={"serviceKey": self.api_key, "pageNo": 1, "numOfRows": 1000}, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ExternalApiUnavailable() from exc

    def fetch_centers(self, url: str) -> list[CenterRecord]:
        result = []
        for item in _items(self._get(url)):
            address = str(_first(item, "address", "addr", "roadAddr", "refineRoadnmAddr") or "")
            ext_id = _first(item, "extCenterId", "centerId", "fcltyNo", "id")
            if not ext_id:
                continue
            result.append(CenterRecord(
                ext_center_id=str(ext_id),
                name=str(_first(item, "name", "centerName", "fcltyNm") or "이름 없는 센터"),
                address=address,
                sido_sigungu=str(_first(item, "sidoSigungu", "sidoNm") or parse_sido_sigungu(address) or "") or None,
                latitude=_number(_first(item, "latitude", "lat", "la")),
                longitude=_number(_first(item, "longitude", "lng", "lo")),
            ))
        return result

    def fetch_activities(self, url: str) -> list[ActivityRecord]:
        result = []
        for item in _items(self._get(url)):
            ext_id = _first(item, "extVideoId", "videoId", "contentId", "id")
            target_url = _first(item, "url", "videoUrl", "link")
            if not ext_id or not target_url:
                continue
            result.append(ActivityRecord(
                ext_video_id=str(ext_id),
                title=str(_first(item, "title", "videoTitle", "contentTitle") or "운동 활동"),
                fitness_element=str(_first(item, "fitnessElement", "element") or "") or None,
                age_group=str(_first(item, "ageGroup", "targetAge") or "") or None,
                url=str(target_url),
            ))
        return result
