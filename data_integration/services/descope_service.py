'''
Service handling all interactions with the Descope API.
Manages user authentication, data synchronization, and user profile updates.
'''

"""
Service for handling Descope integration and data synchronization
"""
from descope import DescopeClient
from datetime import datetime
import logging
import time
import re
import json
import unicodedata
from typing import Dict, Any, List, Optional, Union
from ..config.settings import DESCOPE_PROJECT_ID, DESCOPE_MANAGEMENT_KEY
from ..database.models import User
from ..database.database import get_db_session

logger = logging.getLogger(__name__)

class DescopeService:
    def __init__(self):
        self.client = DescopeClient(
            project_id=DESCOPE_PROJECT_ID,
            management_key=DESCOPE_MANAGEMENT_KEY
        )

    def fetch_all_users_batched(self):
        """
        Fetch all users using multiple search_all calls with small delays
        """
        all_users = set()  # Use a set to store unique user IDs
        user_data = {}     # Store full user data by ID
        attempt = 0
        max_attempts = 5   # Try up to 5 times to get different user sets
        
        while attempt < max_attempts:
            try:
                logger.info(f"Fetching batch attempt {attempt + 1}/{max_attempts}")
                response = self.client.mgmt.user.search_all()
                if not isinstance(response, dict) or 'users' not in response:
                    logger.error("Unexpected response format")
                    break
                
                batch_users = response['users']
                if not batch_users:
                    break
                
                new_users = 0
                for user in batch_users:
                    user_id = user['userId'] if isinstance(user, dict) else user
                    if user_id not in all_users:
                        all_users.add(user_id)
                        user_data[user_id] = user
                        new_users += 1
                
                logger.info(f"Batch {attempt + 1}: Found {new_users} new users. "
                          f"Total unique users: {len(all_users)}")
                
                # If we didn't get any new users, try one more time then stop
                if new_users == 0 and attempt > 0:
                    break
                
                # Add a delay between attempts
                time.sleep(5)
                attempt += 1
            except Exception as e:
                logger.error(f"Error in batch {attempt + 1}: {e}")
                break
        
        logger.info(f"Total unique users fetched: {len(all_users)}")
        return list(user_data.values())

    def is_valid_email(self, email: str) -> bool:
        """
        Validate email format with comprehensive checks including international domains
        """
        if not isinstance(email, str):
            return False
            
        # Comprehensive email regex pattern that supports international domains
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Additional checks
        if not email or len(email) > 254 or ' ' in email:
            return False
            
        if not re.match(pattern, email):
            return False
            
        # Check domain part
        try:
            local_part, domain = email.rsplit('@', 1)
            if not '.' in domain or domain.endswith('.') or domain.startswith('.'):
                return False
            if len(local_part) > 64:
                return False
            if any(c in local_part for c in '<>()[]\\,;:'):
                return False
        except ValueError:
            return False
            
        return True

    def extract_social_id(self, login_id: str) -> Optional[str]:
        """
        Extract potential identifier from social login ID
        """
        if not isinstance(login_id, str):
            return None
            
        # Extract provider and ID
        parts = login_id.split('-', 1)
        if len(parts) != 2:
            return None
            
        provider, social_id = parts
        
        # Handle known social providers
        if provider == 'facebook':
            return social_id
        elif provider == 'google':
            return social_id
        elif provider == 'github':
            return social_id
            
        return None

    def normalize_name(self, name: str) -> str:
        """
        Normalize name by converting international characters to ASCII
        and removing special characters
        """
        # Convert to NFKD form and remove non-ASCII characters
        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
        
        # Convert to lowercase and remove special characters
        name = name.lower().strip()
        name = re.sub(r'[^a-z0-9\s]', '', name)
        name = re.sub(r'\s+', '.', name)
        
        return name

    def generate_email_from_name(self, name: Union[str, Dict[str, Any]], domain: str = "example.com") -> Optional[str]:
        """
        Generate potential email from user's name with international character support
        """
        if isinstance(name, dict):
            # Try different name fields
            display_name = name.get('displayName', '')
            first_name = name.get('firstName', '')
            last_name = name.get('lastName', '')
            
            if display_name:
                name = display_name
            elif first_name or last_name:
                name = f"{first_name} {last_name}".strip()
            else:
                return None
        
        if not isinstance(name, str) or not name.strip():
            return None
            
        # Normalize name and generate email
        normalized_name = self.normalize_name(name)
        if not normalized_name:
            # If normalization removes all characters, use a hash of the original name
            import hashlib
            name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
            normalized_name = f"user{name_hash}"
            
        return f"{normalized_name}@{domain}"

    def clean_potential_email(self, text: str) -> str:
        """
        Clean and extract potential email from text with enhanced pattern recognition
        """
        if not isinstance(text, str):
            return ""
            
        # Remove common prefixes and suffixes
        text = re.sub(r'^(user:|email:|login:|id:|uid:|mail:|contact:|username:|account:)', '', text.lower().strip())
        text = re.sub(r'(\s+|^)(at|@|＠|﹫|［at］|\[at\]|\(at\)|<at>|\{at\})', '@', text)
        
        # Replace encoded characters and common substitutions
        replacements = {
            '%40': '@',
            ' at ': '@',
            '[at]': '@',
            '(at)': '@',
            '{at}': '@',
            '<at>': '@',
            'dot': '.',
            '[dot]': '.',
            '(dot)': '.',
            '{dot}': '.',
            '<dot>': '.',
            '．': '.',
            '。': '.',
            '［dot］': '.',
            '＠': '@'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Remove spaces and special characters
        text = re.sub(r'\s+', '', text)
        
        # Extract email pattern if exists
        email_patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Standard email
            r'[a-zA-Z0-9._%+-]+\s*[@＠]\s*[a-zA-Z0-9.-]+\s*\.\s*[a-zA-Z]{2,}',  # With spaces
            r'[a-zA-Z0-9._%+-]+\[at\][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # With [at]
        ]
        
        for pattern in email_patterns:
            match = re.search(pattern, text)
            if match:
                potential_email = match.group(0)
                # Clean up any remaining spaces or special characters
                potential_email = re.sub(r'\s+', '', potential_email)
                if self.is_valid_email(potential_email):
                    return potential_email
        
        return text

    def extract_email(self, user_data: Any) -> str:
        """
        Enhanced email extraction with support for various data formats and patterns
        """
        try:
            # Handle string input
            if isinstance(user_data, str):
                cleaned = self.clean_potential_email(user_data)
                if self.is_valid_email(cleaned):
                    return cleaned
                return ""

            # Handle dict input
            if not isinstance(user_data, dict):
                return ""

            # First try direct email fields
            email = user_data.get('email', '')
            if self.is_valid_email(email):
                return email

            # Check loginIds array with enhanced cleaning
            login_ids = user_data.get('loginIds', [])
            if isinstance(login_ids, list):
                for login_id in login_ids:
                    # First try direct email extraction
                    cleaned_email = self.clean_potential_email(login_id)
                    if self.is_valid_email(cleaned_email):
                        return cleaned_email
                    
                    # Try to extract social ID and combine with name
                    social_id = self.extract_social_id(login_id)
                    if social_id:
                        name = user_data.get('name', {})
                        if isinstance(name, (dict, str)) and (
                            isinstance(name, str) or name.get('displayName')
                        ):
                            # Try to generate email from name
                            email = self.generate_email_from_name(name)
                            if email:
                                return email

            # Check userId with cleaning
            user_id = user_data.get('userId', '')
            cleaned_user_id = self.clean_potential_email(user_id)
            if self.is_valid_email(cleaned_user_id):
                return cleaned_user_id

            # Check custom attributes
            custom_attrs = user_data.get('customAttributes', {})
            if isinstance(custom_attrs, dict):
                for key, value in custom_attrs.items():
                    if isinstance(value, str):
                        cleaned_value = self.clean_potential_email(value)
                        if self.is_valid_email(cleaned_value):
                            return cleaned_value

            # Try to generate email from name as last resort
            name = user_data.get('name', {})
            if name:
                email = self.generate_email_from_name(name)
                if email:
                    return email

            # If no valid email found, return empty string
            return ""
        except Exception as e:
            logger.error(f"Error extracting email: {e}")
            return ""

    def sync_users_to_db(self):
        """Synchronize Descope users to local database"""
        users = self.fetch_all_users_batched()
        synced_count = 0
        error_count = 0
        emails_from_login = 0
        
        with get_db_session() as session:
            for user_data in users:
                try:
                    # Handle string input
                    if isinstance(user_data, str):
                        login_id = user_data
                        email = self.extract_email(user_data)
                        country = ""
                        roles_str = ""
                        raw_data = {"userId": user_data}
                    else:
                        login_id = user_data.get('userId', '')
                        email = self.extract_email(user_data)
                        custom_attrs = user_data.get('customAttributes', {})
                        country = custom_attrs.get('country', '') if isinstance(custom_attrs, dict) else ''
                        roles = custom_attrs.get('userRoles', '') if isinstance(custom_attrs, dict) else ''
                        roles_str = roles if isinstance(roles, str) else ', '.join(roles) if isinstance(roles, list) else ''
                        raw_data = user_data

                    if not user_data.get('email') and '@' in email:
                        emails_from_login += 1
                    
                    existing_user = session.query(User).filter_by(
                        login_id=login_id
                    ).first()
                    
                    if existing_user:
                        existing_user.email = email
                        existing_user.country = country
                        existing_user.user_roles = roles_str
                        existing_user.last_sync = datetime.utcnow()
                        existing_user.raw_data = raw_data
                        action = "Updated"
                    else:
                        new_user = User(
                            login_id=login_id,
                            email=email,
                            country=country,
                            user_roles=roles_str,
                            raw_data=raw_data,
                            last_sync=datetime.utcnow()
                        )
                        session.add(new_user)
                        action = "Added"
                    
                    if synced_count % 1000 == 0:
                        session.commit()
                        logger.info(f"Progress: {synced_count} users processed. "
                                  f"Found {emails_from_login} emails in login IDs.")
                    
                    synced_count += 1
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error syncing user {user_data.get('userId', 'unknown')}: {e}")
                    session.rollback()
                    continue
            
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Error committing final transaction: {e}")
                session.rollback()
                error_count += 1
        
        return {
            'total_processed': len(users),
            'synced': synced_count,
            'errors': error_count,
            'emails_from_login': emails_from_login
        }