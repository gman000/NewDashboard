'''
Main application entry point.
Initializes the Flask application, sets up background tasks,
and configures all necessary services.
'''

from flask import Flask, make_response, request
from data_integration.api.routes import api
from data_integration.database.database import init_db

app = Flask(__name__)

@app.after_request
def after_request(response):
    # Allow any origin for development
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True, port=5002)