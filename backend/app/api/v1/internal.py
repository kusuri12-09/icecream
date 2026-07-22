from datetime import datetime, timezone
import hmac

from fastapi import APIRouter, Request

from app.api.common import DbDep, ParentDep, success
from app.core.config import get_settings
from app.external.kspo_client import ExternalApiUnavailable, KspoClient
from app.schemas import SyncRequest
from app.services.sync_service import acquire_sync_lock, release_sync_lock, sync_targets


router = APIRouter(prefix="/api/v1/internal", tags=["internal"])


def _validate_cron_request(request: Request, secret: str | None) -> None:
    from app.core.errors import AppError

    if not secret:
        raise AppError("CRON_NOT_CONFIGURED", "Cron 인증이 설정되지 않았습니다.", 503)
    authorization = request.headers.get("authorization", "")
    expected = f"Bearer {secret}"
    if not hmac.compare_digest(authorization, expected):
        raise AppError("AUTH_UNAUTHORIZED", "Cron 인증이 필요합니다.", 401)


def _run_cron_sync(request: Request, db: DbDep, targets: list[str]) -> dict:
    settings = get_settings()
    _validate_cron_request(request, settings.cron_secret)
    if not settings.kspo_api_key or any(
        target == "CENTERS" and not settings.kspo_center_url or target == "ACTIVITIES" and not settings.kspo_activity_url
        for target in targets
    ):
        raise ExternalApiUnavailable()
    lock = acquire_sync_lock(db)
    if lock is None:
        from app.core.errors import AppError

        raise AppError("SYNC_IN_PROGRESS", "동기화가 이미 실행 중입니다.", 409)
    try:
        synced = sync_targets(
            db,
            KspoClient(settings.kspo_api_key),
            targets,
            settings.kspo_center_url,
            settings.kspo_activity_url,
        )
        return success({"targets": targets, "synced": synced, "syncedAt": datetime.now(timezone.utc).isoformat()})
    except ExternalApiUnavailable:
        db.rollback()
        raise
    finally:
        release_sync_lock(db, lock)


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


@router.get("/cron-sync/centers")
def cron_sync_centers(request: Request, db: DbDep) -> dict:
    return _run_cron_sync(request, db, ["CENTERS"])


@router.get("/cron-sync/activities")
def cron_sync_activities(request: Request, db: DbDep) -> dict:
    return _run_cron_sync(request, db, ["ACTIVITIES"])
