import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ --- Correction du chemin pour importer `app` ---
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import Base
from app.core.config import settings

# ✅ Chargement de la configuration Alembic
config = context.config

# ✅ Configuration du logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Métadonnées utilisées pour l’autogénération
target_metadata = Base.metadata


def run_migrations_offline():
    """Exécute les migrations sans connexion directe à la base de données."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Exécute les migrations avec une connexion directe à la base de données."""
    connectable = engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
