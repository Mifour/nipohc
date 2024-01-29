import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# default values for tests
pg_pwd = os.environ.get("POSTGRES_PASSWORD", "password")
pg_user = os.environ.get("POSTGRES_USER", "nipohc_test_user")
pg_db = os.environ.get("POSTGRES_DB", "nipohc_test")
pg_host = os.environ.get("POSTGRES_HOST", "127.0.0.1")
SQLALCHEMY_DATABASE_URL = f"postgresql://{pg_user}:{pg_pwd}@{pg_host}:5432/{pg_db}"


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
