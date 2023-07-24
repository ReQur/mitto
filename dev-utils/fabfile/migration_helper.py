import os

import subprocess
from datetime import datetime
from pathlib import Path

from fabric import task


@task(
    autoprint=True,
    help=dict(message="migration version name"),
)
def generate_version(c, message: str = ""):
    api_dir = Path("../api/")
    sqls_dir = Path(api_dir / "app/data/migrations/versions/sqls")
    os.chdir(api_dir)
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    command = f'alembic revision --rev-id={current_date} -m "{message}"'
    subprocess.run(command, shell=True)

    migration_dir = Path(sqls_dir / f"{current_date}_{message}")
    migration_dir.mkdir()
    Path.touch(migration_dir / "UP.sql")
    Path.touch(migration_dir / "DOWN.sql")

    return message
