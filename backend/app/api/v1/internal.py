from datetime import datetime, timezone

from fastapi import APIRouter

from app.api.common import DbDep, ParentDep, success
from app.core.config import get_settings
from app.external.kspo_client import ExternalApiUnavailable, KspoClient
from app.schemas import SyncRequest
from app.services.sync_service import sync_targets


router = APIRouter(prefix="/api/v1/internal", tags=["internal"])


@router.post("/sync")
def sync(payload: SyncRequest, parent: ParentDep, db: DbDep) -> dict:
    from app.core.errors import AppError

    if not parent.is_admin:
        raise AppError("AUTH_UNAUTHORIZED", "관리자 인증이 필요합니다.", 401)
    settings = get_settings()
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
