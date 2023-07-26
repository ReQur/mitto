"""initial_tables

Revision ID: 20230725162750
Revises: 
Create Date: 2023-07-25 16:27:51.458536

"""
from pathlib import Path

from alembic import op


# revision identifiers, used by Alembic
revision = "20230725162750"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    file = Path(
        f"./app/data/migrations/versions/sqls/{revision}_initial_tables/UP.sql"
    )
    op.execute(sqltext=file.read_text())


def downgrade() -> None:
    file = Path(
        f"./app/data/migrations/versions/sqls/{revision}_initial_tables/DOWN.sql"
    )
    op.execute(sqltext=file.read_text())
