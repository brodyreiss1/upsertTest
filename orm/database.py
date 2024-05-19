from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_URL = "postgresql+psycopg2://postgres:password@localhost:5432/"

engine = create_engine(
    SQLALCHEMY_URL,
    pool_pre_ping=True
)

Base = declarative_base()
