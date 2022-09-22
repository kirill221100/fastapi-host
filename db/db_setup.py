from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import Config as cfg

engine = create_engine(cfg.SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
