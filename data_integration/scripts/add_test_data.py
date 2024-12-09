'''
Script to add test data to the database.
Creates sample users for testing the API and frontend.
'''

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_integration.database.models import User
from data_integration.config.settings import DATABASE_URL

# Create database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Test data
test_users = [
    {
        'login_id': 'user1',
        'email': 'user1@example.com',
        'created_time': datetime.utcnow(),
        'country': 'USA',
        'user_roles': 'admin,user',
        'raw_data': {'test': 'data1'}
    },
    {
        'login_id': 'user2',
        'email': 'user2@example.com',
        'created_time': datetime.utcnow(),
        'country': 'Canada',
        'user_roles': 'user',
        'raw_data': {'test': 'data2'}
    },
    {
        'login_id': 'user3',
        'email': 'user3@example.com',
        'created_time': datetime.utcnow(),
        'country': 'UK',
        'user_roles': 'user,editor',
        'raw_data': {'test': 'data3'}
    }
]

def add_test_data():
    """Add test users to the database"""
    try:
        # Add each test user
        for user_data in test_users:
            user = User(**user_data)
            session.add(user)
        
        # Commit the changes
        session.commit()
        print("Successfully added test users to the database")
    except Exception as e:
        session.rollback()
        print(f"Error adding test data: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    add_test_data()