from datetime import datetime, timezone
from threading import Lock
from typing import Literal
import logging

from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.external.kspo_client import ActivityRecord, CenterRecord, KspoClient
from app.models import ActivityVideo, Center


logger = logging.getLogger(__name__)
SYNC_LOCK_KEY = 8_391_071
_process_sync_lock = Lock()
SyncLock = Literal["postgresql", "process"]


def sync_centers(db: Session, records: list[CenterRecord]) -> int:
    for record in records:
        center = db.scalar(select(Center).where(Center.ext_center_id == record.ext_center_id))
        if center is None:
            center = Center(ext_center_id=record.ext_center_id, name=record.name, address=record.address)
            db.add(center)
        center.name = record.name
        center.address = record.address
        center.sido_sigungu = record.sido_sigungu
        center.latitude = record.latitude
        center.longitude = record.longitude
        center.measure_count = record.measure_count
        center.synced_at = datetime.now(timezone.utc)
    return len(records)


def sync_activities(db: Session, records: list[ActivityRecord]) -> int:
    for record in records:
        video = db.scalar(select(ActivityVideo).where(ActivityVideo.ext_video_id == record.ext_video_id))
        if video is None:
            video = ActivityVideo(ext_video_id=record.ext_video_id, title=record.title, url=record.url)
            db.add(video)
        video.title = record.title
        video.fitness_element = record.fitness_element
        video.fitness_elements = list(record.fitness_elements) or ([record.fitness_element] if record.fitness_element else None)
        video.age_group = record.age_group
        video.url = record.url
        video.description = record.description
        video.thumbnail_url = record.thumbnail_url
        video.fitness_level = record.fitness_level
        video.equipment = record.equipment
        video.training_place = record.training_place
        video.muscle_part = record.muscle_part
        video.duration_seconds = record.duration_seconds
        video.source_fitness_factor = record.source_fitness_factor
        video.source_age_group = record.source_age_group
        video.synced_at = datetime.now(timezone.utc)
    return len(records)


def sync_targets(db: Session, client: KspoClient, targets: list[str], center_url: str | None, activity_url: str | None) -> dict[str, int]:
    synced = {"centers": 0, "activities": 0}
    if "CENTERS" in targets and center_url:
        synced["centers"] = sync_centers(db, client.fetch_centers(center_url))
    if "ACTIVITIES" in targets and activity_url:
        synced["activities"] = sync_activities(db, client.fetch_activities(activity_url))
    db.commit()
    logger.info("공공 데이터 동기화 완료 targets=%s synced=%s", targets, synced)
    return synced


def acquire_sync_lock(db: Session) -> SyncLock | None:
    """PostgreSQL advisory lock으로 중복 배치를 막고 SQLite에서는 프로세스 락을 사용한다."""
    dialect = db.get_bind().dialect.name
    if dialect == "postgresql":
        acquired = db.execute(text("SELECT pg_try_advisory_lock(:lock_key)"), {"lock_key": SYNC_LOCK_KEY}).scalar()
        return "postgresql" if acquired else None
    return "process" if _process_sync_lock.acquire(blocking=False) else None


def release_sync_lock(db: Session, lock: SyncLock) -> None:
    if lock == "postgresql":
        try:
            db.execute(text("SELECT pg_advisory_unlock(:lock_key)"), {"lock_key": SYNC_LOCK_KEY})
        except SQLAlchemyError:
            logger.exception("PostgreSQL 동기화 잠금 해제 실패")
        return
    _process_sync_lock.release()
