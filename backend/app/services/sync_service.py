from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.external.kspo_client import ActivityRecord, CenterRecord, KspoClient
from app.models import ActivityVideo, Center


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
    return synced
