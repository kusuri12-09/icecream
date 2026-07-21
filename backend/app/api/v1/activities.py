from fastapi import APIRouter, Query

from app.api.common import DbDep, ParentDep, dump, success
from app.core.ids import encode_id
from app.core.utils import pages
from app.schemas import ActivityOut, FitnessElement
from app.services import activity_service


router = APIRouter(prefix="/api/v1/activities", tags=["activities"])


def parse_fitness_element(value: str | None) -> FitnessElement | None:
    if value is None:
        return None
    try:
        return FitnessElement(value)
    except ValueError:
        return None


@router.get("")
def activities(
    parent: ParentDep,
    db: DbDep,
    fitness_element: str | None = Query(None, alias="fitnessElement"),
    measurement_id: str | None = Query(None, alias="measurementId"),
    age_group: str = Query("PRESCHOOL", alias="ageGroup"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> dict:
    rows = activity_service.list_recommendations(db, parent, fitness_element, measurement_id, age_group)
    total = len(rows)
    selected = rows[(page - 1) * size : (page - 1) * size + size]
    items = [
        dump(
            ActivityOut(
                id=encode_id("video", row.id),
                title=row.title,
                fitness_element=parse_fitness_element(row.fitness_element),
                age_group=row.age_group,
                url=row.url,
            )
        )
        for row in selected
    ]
    return success({"items": items, "page": page, "size": size, "totalElements": total, "totalPages": pages(total, size)})
