from fastapi import APIRouter, Query

from app.api.common import DbDep, ParentDep, dump, success
from app.services import insight_service


router = APIRouter(prefix="/api/v1/insights", tags=["insights"])


@router.get("/regional")
def regional_insight(parent: ParentDep, db: DbDep, sido_sigungu: str | None = Query(None, alias="sidoSigungu")) -> dict:
    del parent
    return success(dump(insight_service.regional(db, sido_sigungu)))


@router.get("/regional/map")
def regional_map(parent: ParentDep, db: DbDep) -> dict:
    del parent
    items, fallback = insight_service.regional_map(db)
    return success({"regions": [dump(item) for item in items], "fallback": fallback})
