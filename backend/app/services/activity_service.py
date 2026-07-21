from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models import ActivityVideo, Parent
from app.repositories import activity_repository
from app.services import measurement_service


def list_recommendations(
    db: Session,
    parent: Parent,
    fitness_element: str | None,
    measurement_id: str | None,
    age_group: str,
) -> list[ActivityVideo]:
    requested: set[str] = set()
    if measurement_id:
        measurement = measurement_service.get_owned(db, parent, measurement_id)
        requested = {item.item_key for item in measurement.items if item.item_grade == "SEED" and item.item_key != "BMI"}
    elif fitness_element:
        requested = {item.strip().upper() for item in fitness_element.split(",")}
    rows = activity_repository.list_by_age_group(db, age_group)
    if not rows:
        raise AppError("EXTERNAL_API_UNAVAILABLE", "외부 데이터를 일시적으로 사용할 수 없습니다.", 503)
    if requested:
        rows = [row for row in rows if row.fitness_element in requested]
    return rows
