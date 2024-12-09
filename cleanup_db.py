"""
Script to clean up and reinitialize the database
"""
import os
import sys
# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from data_integration.database.database import engine
from data_integration.database.models import Base
def cleanup_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(engine)
    print("Creating all tables...")
    Base.metadata.create_all(engine)
    print("Database reinitialized successfully!")
if __name__ == "__main__":
    cleanup_database()