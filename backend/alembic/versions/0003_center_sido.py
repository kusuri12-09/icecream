"""add province field to center

Revision ID: 0003_center_sido
Revises: 0002_activity_video_metadata
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_center_sido"
down_revision = "0002_activity_video_metadata"
branch_labels = None
depends_on = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = {column["name"] for column in inspector.get_columns("center")}
    if "sido" not in columns:
        op.add_column("center", sa.Column("sido", sa.String(length=50), nullable=True))
        op.create_index("ix_center_sido", "center", ["sido"])

    center = sa.table(
        "center",
        sa.column("id", sa.Integer),
        sa.column("address", sa.String),
        sa.column("sido", sa.String),
        sa.column("sido_sigungu", sa.String),
    )
    connection = op.get_bind()
    for row in connection.execute(sa.select(center.c.id, center.c.address, center.c.sido_sigungu)):
        address = (row.address or "").strip()
        sido_sigungu = (row.sido_sigungu or "").strip()
        source = address or sido_sigungu
        if source:
            connection.execute(
                center.update().where(center.c.id == row.id).values(sido=source.split()[0])
            )


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = {column["name"] for column in inspector.get_columns("center")}
    if "sido" in columns:
        op.drop_index("ix_center_sido", table_name="center")
        op.drop_column("center", "sido")
