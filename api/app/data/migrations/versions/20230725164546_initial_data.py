"""initial_data

Revision ID: 20230725164546
Revises: 20230725162750
Create Date: 2023-07-25 16:45:47.152904

"""
from pathlib import Path

from alembic import op


# revision identifiers, used by Alembic
revision = "20230725164546"
down_revision = "20230725162750"
branch_labels = None
depends_on = None


def upgrade() -> None:
    file = Path(
        f"./app/data/migrations/versions/sqls/{revision}_initial_data/UP.sql"
    )
    op.execute(sqltext=file.read_text())


def downgrade() -> None:
    file = Path(
        f"./app/data/migrations/versions/sqls/{revision}_initial_data/DOWN.sql"
    )
    op.execute(sqltext=file.read_text())
