from logging.config import fileConfig

from alembic import context

from src.core import get_settings
from src.database import Base, engine


config = context.config
fileConfig(config.config_file_name)

config.set_main_option('sqlalchemy.url', get_settings().DB_URL)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    async def do_migrations(connection):
        context.configure(
            connection = connection,
            target_metadata = target_metadata
        )
        
        async with context.begin_transaction():
            await context.run_migrations()
            
    async with engine.connect() as connection:
        await connection.run_sync(do_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
