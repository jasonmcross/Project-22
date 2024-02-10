# scr/users/database_module.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://PhilopateerAz:CF3q1wNWbOle@ep-lively-hat-a5tacpqp-pooler.us-east-2.aws.neon.tech/Project22?sslmode=require&pgbouncer=true"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()