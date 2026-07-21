from sqlalchemy.orm import Session

from app.models import Center
from app.repositories import center_repository
from app.schemas import RegionMapItem, RegionalInsight


def _group_by_region(rows: list[Center]) -> dict[str, int]:
    grouped: dict[str, int] = {}
    for center in rows:
        if center.sido_sigungu:
            grouped[center.sido_sigungu] = grouped.get(center.sido_sigungu, 0) + center.measure_count
    return grouped


def regional(db: Session, region: str | None) -> RegionalInsight:
    grouped = _group_by_region(center_repository.list_all(db))
    selected_region = region or (max(grouped, key=lambda key: grouped[key]) if grouped else "전국")
    region_count = grouped.get(selected_region, 0)
    national_avg = sum(grouped.values()) / len(grouped) if grouped else 0
    if not grouped:
        level, percentile = "INSUFFICIENT", 0
    elif region_count > national_avg * 1.1:
        level, percentile = "ABOVE_AVG", 75
    elif region_count < national_avg * 0.9:
        level, percentile = "BELOW_AVG", 28
    else:
        level, percentile = "AROUND_AVG", 50
    message = f"{selected_region}의 유아 체력측정 참여 현황을 확인해보세요."
    if level == "BELOW_AVG":
        message = f"{selected_region}의 유아 체력측정 참여는 전국 평균보다 낮은 편이에요. 가까운 센터에서 측정해보세요."
    return RegionalInsight(
        region=selected_region,
        region_measure_count=region_count,
        national_avg=round(national_avg, 2),
        relative_level=level,
        percentile=percentile,
        message=message,
        cta={"type": "CENTER_CONNECT", "label": "근처 센터 찾기"},
    )


def regional_map(db: Session) -> tuple[list[RegionMapItem], bool]:
    grouped = _group_by_region(center_repository.list_all(db))
    maximum = max(grouped.values(), default=0)
    items = [
        RegionMapItem(
            sido_sigungu=region,
            measure_count=count,
            participation_rate=round(count / maximum, 4) if maximum else 0,
        )
        for region, count in sorted(grouped.items(), key=lambda pair: pair[1], reverse=True)
    ]
    return items, not bool(items)
