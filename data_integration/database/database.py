'''
Database connection management and utilities.
Handles connection pooling, session management, and provides
utility functions for bulk operations and optimized queries.
'''

"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from ..config.settings import DATABASE_URL
from .models import Base

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

def init_db():
    """Initialize the database schema"""
    Base.metadata.create_all(engine)

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()