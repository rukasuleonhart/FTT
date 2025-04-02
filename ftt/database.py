from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ftt.settings import settings  # Usar a instância única de Settings

# Criar o motor do banco de dados
engine = create_engine(
    settings.DATABASE_URL,  # Usa a instância única de settings
    pool_size=10,
    max_overflow=20,
)

# Criar uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
