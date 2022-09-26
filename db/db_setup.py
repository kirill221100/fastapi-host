from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData as metadata
from core.config import Config as cfg

# engine = create_engine(cfg.SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)
# session = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
#
# Base = declarative_base()
#
#
# def get_db():
#     db = session()
#     try:
#         yield db
#     finally:
#         db.close()

engine = create_async_engine(cfg.SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

