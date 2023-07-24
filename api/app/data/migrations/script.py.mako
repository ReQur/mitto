"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from pathlib import Path

from alembic import op
${imports if imports else ""}

# revision identifiers, used by Alembic
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    file = Path(f"./sqls/{revision}_${message}/UP.sql")
    op.execute(sqltext=file.read_text())



def downgrade() -> None:
    file = Path(f"./sqls/{revision}_${message}/DOWN.sql")
    op.execute(sqltext=file.read_text())
