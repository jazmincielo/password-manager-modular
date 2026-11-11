from sqlmodel import SQLModel, create_engine, Session
from config.settings import settings

# Motor de base de datos usando la URI de Supabase PostgreSQL (Session Pooler IPv4 - puerto 6543)
engine = create_engine(settings.DATABASE_URL, echo=True)

def init_db():
    """Inicializa las tablas de la base de datos."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Retorna una sesión de base de datos."""
    return Session(engine)
