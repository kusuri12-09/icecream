"""add KSPO activity guide metadata

Revision ID: 0002_activity_video_metadata
Revises: 0001_initial
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_activity_video_metadata"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    existing_columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("activity_video")}
    columns = (
        ("fitness_elements", sa.JSON()),
        ("description", sa.Text()),
        ("thumbnail_url", sa.String(length=500)),
        ("fitness_level", sa.String(length=20)),
        ("equipment", sa.String(length=100)),
        ("training_place", sa.String(length=50)),
        ("muscle_part", sa.String(length=255)),
        ("duration_seconds", sa.Integer()),
        ("source_fitness_factor", sa.String(length=50)),
        ("source_age_group", sa.String(length=20)),
    )
    for name, column_type in columns:
        if name not in existing_columns:
            op.add_column("activity_video", sa.Column(name, column_type, nullable=True))


def downgrade() -> None:
    existing_columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("activity_video")}
    for name in (
        "source_age_group",
        "source_fitness_factor",
        "duration_seconds",
        "muscle_part",
        "training_place",
        "equipment",
        "fitness_level",
        "thumbnail_url",
        "description",
        "fitness_elements",
    ):
        if name in existing_columns:
            op.drop_column("activity_video", name)
