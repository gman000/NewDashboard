'''
Configuration file containing all environment variables, constants, and settings
for the data integration system. Includes database connections, API keys,
and system-wide parameters.
'''

"""
Configuration settings for the data integration system
"""
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Descope Configuration
DESCOPE_PROJECT_ID = 'P2c5c3JHvZ8w5oiRpMMZnRKRtP2e'
DESCOPE_MANAGEMENT_KEY = 'K2pbvJMBEqRTs191SIrdXftJUcqPp8KmXshfhl55EL0KsuzlQ6TJyM4cbAy0Uh5hMaotciV'
# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/data_integration')
# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')