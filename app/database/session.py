"""Database session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool 
from app.core.config import settings
from app.database.base import Base
from app.database.models import user, bank_account, loan, investment, market_loan, swith_request
from app.core.logger import logger
# Create database engine 
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    # echo=settings.DEBUG, # Log SQL queries in debug mode
)

# Create session factory 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    Dependency to get database session. 

    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def create_tables():
    """
    Create all tables in the database. 
    """
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """
    Drop all the tables in the database.
    """
    Base.metadata.drop_all(bind=engine)