import pathlib
import sys
from datetime import datetime

import alembic
from sqlalchemy import engine_from_config, pool

from logging.config import fileConfig
import logging

# we're appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import DATABASE_URL  # noqa

# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config
config.set_main_option(
    "file_template",
    "%(year)d%(month)02d%(day)02d%(hour)02d%(minute)02d%(second)02d_%%(rev)s",
)


# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def configure_context():
    alembic.context.configure(
        literal_binds=True,
        # Define the naming scheme for Alembic .py and .pyc files
        transaction_per_migration=True,
        render_as_batch=True,
        template_args={
            "year": datetime.now().year,
            "month": datetime.now().month,
            "day": datetime.now().day,
            "hour": datetime.now().hour,
            "minute": datetime.now().minute,
            "second": datetime.now().second,
        },
    )


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """
    configure_context()
    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", str(DATABASE_URL))

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(connection=connection, target_metadata=None)

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    configure_context()

    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
