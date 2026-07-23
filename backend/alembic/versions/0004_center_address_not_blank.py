"""prevent blank center addresses

Revision ID: 0004_center_address_not_blank
Revises: 0003_center_sido
"""

from alembic import op
import sqlalchemy as sa


revision = "0004_center_address_not_blank"
down_revision = "0003_center_sido"
branch_labels = None
depends_on = None

CONSTRAINT_NAME = "ck_center_address_not_blank"


def _has_constraint(connection: sa.Connection) -> bool:
    return any(
        constraint.get("name") == CONSTRAINT_NAME
        for constraint in sa.inspect(connection).get_check_constraints("center")
    )


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(sa.text("DELETE FROM center WHERE address IS NULL OR trim(address) = ''"))
    if _has_constraint(connection):
        return

    if connection.dialect.name == "sqlite":
        with op.batch_alter_table("center", recreate="always") as batch_op:
            batch_op.create_check_constraint(CONSTRAINT_NAME, "length(trim(address)) > 0")
    else:
        op.create_check_constraint(CONSTRAINT_NAME, "center", "length(trim(address)) > 0")


def downgrade() -> None:
    connection = op.get_bind()
    if not _has_constraint(connection):
        return

    if connection.dialect.name == "sqlite":
        with op.batch_alter_table("center", recreate="always") as batch_op:
            batch_op.drop_constraint(CONSTRAINT_NAME, type_="check")
    else:
        op.drop_constraint(CONSTRAINT_NAME, "center", type_="check")
