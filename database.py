from sqlmodel import (
    select,
    SQLModel, 
    text,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from data import (
    CARD_RARITY,
    ERAS
)
from models.models import (
    Era,
    Rarity
)

DB_USER = "postgres"
DB_PASSWORD = "%40Luminous9"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "toolsdb"

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# main engine for the actual app
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def ensure_database_exists():
    # Connect to DEFAULT postgres database, NOT the target DB
    default_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

    default_engine = create_async_engine(default_url, isolation_level="AUTOCOMMIT")

    async with default_engine.connect() as conn:

        result = await conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
        )
        exists = result.scalar()
        if not exists:
            print(f"Database '{DB_NAME}' does not exist. Creating...")
            await conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))

        else:
            print(f"Database '{DB_NAME}' already exists.")


async def init_db():
    await ensure_database_exists()

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    await initial_data()


async def initial_data():

    async with AsyncSessionLocal() as session:
        existing = await session.execute(select(Rarity))
        data = existing.scalars().first()
        if not data :
            for rarity in CARD_RARITY:
                entry = Rarity(**rarity)
                session.add(entry)

            for era in ERAS:
                entry = Era(**era)
                session.add(entry)

            await session.commit()
