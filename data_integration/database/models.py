'''
SQLAlchemy models defining the database schema for the integrated data system.
Contains User, Sketch, Event, and AggregatedStats models with their relationships
and data structures.
'''

"""
Database models for the data integration system
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login_id = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, index=True)
    created_time = Column(DateTime)
    country = Column(String)
    user_roles = Column(String)  # Store roles as comma-separated string
    raw_data = Column(JSON)      # Store complete Descope data for reference
    last_sync = Column(DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {
            'id': self.id,
            'login_id': self.login_id,
            'email': self.email,
            'created_time': self.created_time.isoformat() if self.created_time else None,
            'country': self.country,
            'user_roles': self.user_roles,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None
        }
    @classmethod
    def from_descope_data(cls, user_data):
        """Create a User instance from Descope user data"""
        # Extract login ID
        login_id = user_data.get('loginId', '')
        # Extract created time and convert from timestamp if needed
        created_time = None
        if 'createdTime' in user_data:
            try:
                # Assuming createdTime is in milliseconds
                timestamp = int(user_data['createdTime'])
                created_time = datetime.fromtimestamp(timestamp / 1000)
            except (ValueError, TypeError):
                created_time = None
        # Extract roles and join them as a string
        roles = user_data.get('roleNames', [])
        roles_str = ','.join(roles) if roles else ''
        return cls(
            login_id=login_id,
            email=user_data.get('email', ''),
            created_time=created_time,
            country=user_data.get('country', ''),
            user_roles=roles_str,
            raw_data=user_data
        )
