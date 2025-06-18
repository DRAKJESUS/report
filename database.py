from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

DATABASE_URL = (
    "mysql+asyncmy://root:BuYGMrZkhEixlhvpehSraSzScbYJNNLY"
    "@maglev.proxy.rlwy.net:17631/railway"
)

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()