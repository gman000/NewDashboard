'''
API endpoints for the dashboard application.
Handles data requests, provides aggregated statistics,
and manages real-time data updates.
'''

from flask import Blueprint, jsonify, request
from data_integration.database.database import Session
from data_integration.database.models import User
from sqlalchemy import desc

api = Blueprint('api', __name__)

@api.route('/api/users', methods=['GET'])
def get_users():
    """Get users from the database with pagination"""
    session = Session()
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get total count
        total_count = session.query(User).count()
        
        # Get paginated users
        users = session.query(User)\
            .order_by(desc(User.created_time))\
            .offset(offset)\
            .limit(per_page)\
            .all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()