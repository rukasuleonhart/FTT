import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Alembic Config
config = context.config

# Atualiza sqlalchemy.url com variáveis de ambiente
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configuração de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importação correta do modelo Base
from ftt.models import Base  # Ajuste para o caminho correto dos modelos

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executa as migrações no modo offline."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executa as migrações no modo online."""
    engine = create_engine(DATABASE_URL, poolclass=pool.NullPool, echo=True)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
