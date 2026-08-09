from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
#This is the database connection string.
engine = create_engine(SQLALCHEMY_URL)
# engine is sql alchemy connection maneger, Hey SQLAlchemy, here's my database. Figure out how to talk to it.
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
#sessionmaker is like a machine that creates database sessions.
#A session is temporary workspace for talking to the database.
Base = declarative_base()
#creates a base class that all of database models will inherit from. The child classes become tables

#when it is called
def get_db():
    db = SessionLocal() #creates session
    try:
        yield db 
        #doc line 5

    finally:
        db.close() #delets the session

#This means:
# Open file.
# Give file to user.
# When user is done, close file.