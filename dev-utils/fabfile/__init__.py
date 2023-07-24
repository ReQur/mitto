from invoke import Collection
from .migration_helper import generate_version

namespace = Collection(
    generate_version
)
