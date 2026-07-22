from dataclasses import dataclass
import hashlib
from math import ceil
import re
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
    measure_count: int = 0


@dataclass(frozen=True)
class ActivityRecord:
    ext_video_id: str
    title: str
    fitness_element: str | None
    age_group: str | None
    url: str
    description: str | None = None
    thumbnail_url: str | None = None
    fitness_level: str | None = None
    equipment: str | None = None
    training_place: str | None = None
    muscle_part: str | None = None
    duration_seconds: int | None = None
    source_fitness_factor: str | None = None
    source_age_group: str | None = None
    fitness_elements: tuple[str, ...] = ()


FITNESS_FACTOR_MAP: dict[str, tuple[str, ...]] = {
    "심폐지구력": ("CARDIO",),
    "근력": ("GRIP",),
    "근지구력": ("MUSCULAR_END",),
    "근력/근지구력": ("GRIP", "MUSCULAR_END"),
    "유연성": ("FLEXIBILITY",),
    "민첩성": ("AGILITY",),
    "순발력": ("POWER",),
    "협응력": ("COORDINATION",),
}


AGE_GROUP_MAP = {
    "유소년": "PRESCHOOL",
    "유아": "PRESCHOOL",
    "PRESCHOOL": "PRESCHOOL",
}


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
    for key in ("response", "body", "items", "data", "item"):
        value = body.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = _items(value)
            if nested:
                return nested
    return []


def _number(value: Any) -> float | None:
    try:
        return float(str(value).replace(",", "")) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _integer(value: Any) -> int | None:
    if value in (None, ""):
        return None
    match = re.search(r"\d+", str(value))
    return int(match.group()) if match else None


def _resource_url(base_url: Any, file_name: Any = None) -> str | None:
    if base_url in (None, ""):
        return None
    base = str(base_url)
    if file_name in (None, "") or base.endswith(str(file_name)):
        return base
    return f"{base.rstrip('/')}/{str(file_name).lstrip('/')}"


def normalize_fitness_elements(value: Any) -> tuple[str, ...]:
    raw = str(value or "").strip()
    if not raw:
        return ()
    if raw in FITNESS_FACTOR_MAP:
        return FITNESS_FACTOR_MAP[raw]
    elements: list[str] = []
    for part in re.split(r"[/,·]+", raw):
        mapped = FITNESS_FACTOR_MAP.get(part.strip(), ())
        for element in mapped:
            if element not in elements:
                elements.append(element)
    return tuple(elements)


def normalize_age_group(value: Any) -> str | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    return AGE_GROUP_MAP.get(raw.upper(), AGE_GROUP_MAP.get(raw, raw))


def parse_sido_sigungu(address: str) -> str | None:
    parts = address.split()
    return " ".join(parts[:2]) if len(parts) >= 2 else None


def _total_count(payload: Any) -> int | None:
    if not isinstance(payload, dict):
        return None
    response = payload.get("response")
    body = response.get("body") if isinstance(response, dict) else None
    return _integer(_first(body, "totalCount", "total_count")) if isinstance(body, dict) else None


def _stable_center_id(name: str, address: str) -> str:
    source = f"{name.strip()}|{address.strip()}".encode("utf-8")
    return f"kspo_center_{hashlib.sha256(source).hexdigest()[:32]}"


class KspoClient:
    def __init__(self, api_key: str, timeout: float = 10.0) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def _get(self, url: str, page_no: int = 1, num_of_rows: int = 1000) -> Any:
        try:
            response = httpx.get(
                url,
                params={"serviceKey": self.api_key, "pageNo": page_no, "numOfRows": num_of_rows, "resultType": "json"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ExternalApiUnavailable() from exc

    def fetch_centers(self, url: str) -> list[CenterRecord]:
        page_size = 1000
        first_page = self._get(url, page_no=1, num_of_rows=page_size)
        payloads = [first_page]
        total_count = _total_count(first_page)
        total_pages = ceil(total_count / page_size) if total_count else 1
        for page_no in range(2, total_pages + 1):
            payloads.append(self._get(url, page_no=page_no, num_of_rows=page_size))

        records: dict[str, CenterRecord] = {}
        for payload in payloads:
            for item in _items(payload):
                name = str(_first(item, "center_nm", "name", "centerName", "fcltyNm") or "이름 없는 센터")
                base_address = str(_first(item, "center_addr1", "address", "addr", "roadAddr", "refineRoadnmAddr") or "")
                detail_address = str(_first(item, "center_addr2", "detailAddress") or "")
                address = " ".join(part for part in (base_address, detail_address) if part).strip()
                ext_id = _first(item, "extCenterId", "centerId", "fcltyNo", "id")
                ext_id = str(ext_id or _stable_center_id(name, base_address))
                measure_count = _integer(_first(item, "test_cnt", "measureCount", "measure_count")) or 0
                current = records.get(ext_id)
                if current is None:
                    records[ext_id] = CenterRecord(
                        ext_center_id=ext_id,
                        name=name,
                        address=address,
                        sido_sigungu=str(_first(item, "sidoSigungu", "sidoNm") or parse_sido_sigungu(base_address) or "") or None,
                        latitude=_number(_first(item, "latitude", "lat", "la")),
                        longitude=_number(_first(item, "longitude", "lng", "lo")),
                        measure_count=measure_count,
                    )
                    continue
                records[ext_id] = CenterRecord(
                    ext_center_id=current.ext_center_id,
                    name=current.name,
                    address=current.address,
                    sido_sigungu=current.sido_sigungu,
                    latitude=current.latitude,
                    longitude=current.longitude,
                    measure_count=current.measure_count + measure_count,
                )
        return list(records.values())

    def fetch_activities(self, url: str) -> list[ActivityRecord]:
        page_size = 1000
        first_page = self._get(url, page_no=1, num_of_rows=page_size)
        payloads = [first_page]
        total_count = _total_count(first_page)
        total_pages = ceil(total_count / page_size) if total_count else 1
        for page_no in range(2, total_pages + 1):
            payloads.append(self._get(url, page_no=page_no, num_of_rows=page_size))

        records: dict[str, ActivityRecord] = {}
        for payload in payloads:
            for item in _items(payload):
                source_file_name = _first(item, "file_nm", "extVideoId", "videoId", "contentId", "id")
                if not source_file_name:
                    continue
                video_url = _resource_url(_first(item, "file_url"), source_file_name) or _resource_url(
                    _first(item, "url", "videoUrl", "link")
                )
                if not video_url:
                    continue
                source_factor = _first(item, "ftns_fctr_nm", "fitnessElement", "element")
                fitness_elements = normalize_fitness_elements(source_factor)
                source_age_group = _first(item, "aggrp_nm", "ageGroup", "targetAge")
                record = ActivityRecord(
                    ext_video_id=str(source_file_name),
                    title=str(_first(item, "vdo_ttl_nm", "trng_nm", "title", "videoTitle", "contentTitle") or "운동 활동"),
                    fitness_element=fitness_elements[0] if fitness_elements else None,
                    fitness_elements=fitness_elements,
                    age_group=normalize_age_group(source_age_group),
                    source_age_group=str(source_age_group) if source_age_group else None,
                    source_fitness_factor=str(source_factor) if source_factor else None,
                    url=video_url,
                    description=str(_first(item, "vdo_desc", "description") or "") or None,
                    thumbnail_url=_resource_url(_first(item, "img_file_url", "thumbnailUrl"), _first(item, "img_file_nm")),
                    fitness_level=str(_first(item, "ftns_lvl_nm", "fitnessLevel") or "") or None,
                    equipment=str(_first(item, "tool_nm", "equipment") or "") or None,
                    training_place=str(_first(item, "trng_plc_nm", "trainingPlace") or "") or None,
                    muscle_part=str(_first(item, "trng_mscl_part", "musclePart") or "") or None,
                    duration_seconds=_integer(_first(item, "vdo_len", "durationSeconds")),
                )
                records.setdefault(str(source_file_name), record)
        return list(records.values())
