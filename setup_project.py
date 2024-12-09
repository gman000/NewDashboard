import os
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
def create_file(path, content):
    with open(path, 'w') as file:
        file.write(content)
    print(f"Created file: {path}")
# Project structure
PROJECT_ROOT = "data_integration"
DIRECTORIES = [
    "",
    "config",
    "database",
    "services",
    "api",
    "tasks",
    "templates",
    "static/css",
    "utils"
]
# File definitions with headers
FILES = {
    "config/settings.py": """'''
Configuration file containing all environment variables, constants, and settings
for the data integration system. Includes database connections, API keys,
and system-wide parameters.
'''\n\n""",
    "config/__init__.py": "",
    "database/models.py": """'''
SQLAlchemy models defining the database schema for the integrated data system.
Contains User, Sketch, Event, and AggregatedStats models with their relationships
and data structures.
'''\n\n""",
    "database/database.py": """'''
Database connection management and utilities.
Handles connection pooling, session management, and provides
utility functions for bulk operations and optimized queries.
'''\n\n""",
    "database/__init__.py": "",
    "services/descope_service.py": """'''
Service handling all interactions with the Descope API.
Manages user authentication, data synchronization, and user profile updates.
'''\n\n""",
    "services/elasticsearch_service.py": """'''
Service managing all Elasticsearch operations.
Handles querying sketch data, event tracking, and data synchronization
from Elasticsearch to the local database.
'''\n\n""",
    "services/data_sync_service.py": """'''
Orchestration service managing data synchronization between Descope,
Elasticsearch, and the local database. Handles incremental updates
and data consistency.
'''\n\n""",
    "services/__init__.py": "",
    "api/routes.py": """'''
API endpoints for the dashboard application.
Handles data requests, provides aggregated statistics,
and manages real-time data updates.
'''\n\n""",
    "api/__init__.py": "",
    "tasks/background_jobs.py": """'''
Background task definitions for data synchronization and report generation.
Manages periodic updates, cache invalidation, and data aggregation jobs.
'''\n\n""",
    "tasks/__init__.py": "",
    "utils/cache_manager.py": """'''
Utilities for managing cached data and pre-aggregated reports.
Handles cache invalidation, update strategies, and optimization.
'''\n\n""",
    "utils/performance.py": """'''
Performance optimization utilities and monitoring tools.
Includes query optimization, memory management, and performance metrics.
'''\n\n""",
    "utils/__init__.py": "",
    "templates/dashboard.html": """<!--
Main dashboard template providing the user interface for data visualization
and exploration. Includes drill-down capabilities and dynamic updates.
-->\n\n""",
    "static/css/styles.css": """/*
Stylesheet for the dashboard interface.
Contains all styling rules for the data visualization and UI components.
*/\n\n""",
    "app.py": """'''
Main application entry point.
Initializes the Flask application, sets up background tasks,
and configures all necessary services.
'''\n\n""",
    "requirements.txt": """# Project dependencies
# Run: pip install -r requirements.txt
Flask==2.0.1
SQLAlchemy==1.4.23
elasticsearch==7.17.0
descope==1.3.0
redis==4.0.2
celery==5.2.3
psycopg2-binary==2.9.3
python-dotenv==0.19.2
""",
    "README.md": """# Data Integration Dashboard
## Overview
Integration system combining Descope user data with Elasticsearch sketch events.
Provides fast access to user activity data with drill-down capabilities.
## Features
- Real-time data synchronization
- Pre-aggregated reports
- Performance-optimized queries
- Background processing
- Drill-down analytics
## Setup Instructions
[To be added]
## Architecture
[To be added]
## Performance Considerations
[To be added]
"""
}
def setup_project():
    # Create project root if it doesn't exist
    create_directory(PROJECT_ROOT)
    # Create all directories
    for dir_path in DIRECTORIES:
        full_path = os.path.join(PROJECT_ROOT, dir_path)
        create_directory(full_path)
    # Create all files with their headers
    for file_path, content in FILES.items():
        full_path = os.path.join(PROJECT_ROOT, file_path)
        create_file(full_path, content)
if __name__ == "__main__":
    setup_project()