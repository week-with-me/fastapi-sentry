from logging.config import fileConfig

from alembic import context

from src.core import get_settings
from src.model import User
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
    def do_migrations(connection):
        context.configure(
            connection = connection,
            target_metadata = target_metadata,
            include_schemas = True
        )
        
        with context.begin_transaction():
            context.run_migrations()
            
    async with engine.connect() as connection:
        await connection.run_sync(do_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
