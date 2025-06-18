from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

# URL de la base de datos Railway
DATABASE_URL = (
    "mysql+asyncmy://root:BuYGMrZkhEixlhvpehSraSzScbYJNNLY"
    "@maglev.proxy.rlwy.net:17631/railway"
)

# Crear el motor de base de datos asíncrono
engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)

# Sesión asíncrona
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base para modelos SQLAlchemy
Base = declarative_base()

# Dependency para FastAPI (maneja la conexión a la base de datos)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
