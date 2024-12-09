"""
Test script for Descope data synchronization
"""
import os
import sys
import logging
from pprint import pformat
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from data_integration.database.database import init_db
from data_integration.services.descope_service import DescopeService
from data_integration.database.models import User

def analyze_user_without_email(user_data):
    """Analyze user data to understand why email extraction failed"""
    relevant_fields = {
        'userId': user_data.get('userId'),
        'loginIds': user_data.get('loginIds', []),
        'email': user_data.get('email'),
        'name': user_data.get('name', {}),
        'customAttributes': user_data.get('customAttributes', {})
    }
    return relevant_fields

def show_synced_users():
    """Display the users that have been synced to the database"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from data_integration.config.settings import DATABASE_URL
    
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    users = session.query(User).all()
    total_users = len(users)
    
    if total_users == 0:
        print("\nNo users found in database.")
        session.close()
        return

    print("\nSynced Users Summary:")
    print("-" * 100)
    print(f"{'Login ID':<30} {'Email':<30} {'Country':<15} {'Roles':<25}")
    print("-" * 100)
    
    empty_email_count = 0
    empty_country_count = 0
    empty_roles_count = 0
    users_without_email = []
    
    for user in users:
        if not user.email:
            empty_email_count += 1
            if len(users_without_email) < 5:  # Store first 5 users without email
                try:
                    raw_data = user.raw_data
                    if isinstance(raw_data, str):
                        raw_data = json.loads(raw_data)
                    users_without_email.append(analyze_user_without_email(raw_data))
                except Exception as e:
                    logger.error(f"Error analyzing user data: {e}")
        
        if not user.country:
            empty_country_count += 1
        if not user.user_roles:
            empty_roles_count += 1
            
        # Print first 10 users as sample
        if users.index(user) < 10:
            print(f"{user.login_id[:30]:<30} {user.email[:30]:<30} {user.country[:15]:<15} {user.user_roles[:25]:<25}")
    
    print("-" * 100)
    print("\nData Quality Summary:")
    print(f"Total Users: {total_users}")
    
    if total_users > 0:
        print(f"Users without email: {empty_email_count} ({empty_email_count/total_users*100:.1f}%)")
        print(f"Users without country: {empty_country_count} ({empty_country_count/total_users*100:.1f}%)")
        print(f"Users without roles: {empty_roles_count} ({empty_roles_count/total_users*100:.1f}%)")
        
        if users_without_email:
            print("\nSample of Users Without Email:")
            print(json.dumps(users_without_email, indent=2))
    
    session.close()

def main():
    try:
        # Initialize database
        logger.info("Initializing database...")
        init_db()
        
        # Initialize Descope service
        logger.info("Starting Descope synchronization...")
        descope_service = DescopeService()
        
        # Sync users
        result = descope_service.sync_users_to_db()
        
        # Log results
        logger.info("Synchronization completed:")
        logger.info(f"Total processed: {result['total_processed']}")
        logger.info(f"Successfully synced: {result['synced']}")
        logger.info(f"Errors: {result['errors']}")
        
        # Show synced users
        show_synced_users()
        
    except Exception as e:
        logger.error(f"Error during synchronization: {e}")
        raise

if __name__ == "__main__":
    main()