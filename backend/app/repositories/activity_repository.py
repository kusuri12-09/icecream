from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ActivityVideo


def list_by_age_group(db: Session, age_group: str) -> list[ActivityVideo]:
    return list(db.scalars(select(ActivityVideo).where(func.upper(ActivityVideo.age_group) == age_group.upper())).all())
