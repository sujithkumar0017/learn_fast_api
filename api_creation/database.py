from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty123@localhost/fast_api_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


# Dependency       # this dependency is used create a session to the database and for each request it will go session and it will send sql to the database after the operation is completed the session will close.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()