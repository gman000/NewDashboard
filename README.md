# NewDashboard

A dashboard application with user management capabilities.

## Quick Start

To start both the backend and frontend servers, simply run:

```bash
./start_servers.sh
```

This script will:
1. Clean up any existing processes on ports 5002 (backend) and 5174 (frontend)
2. Start the Flask backend server on http://localhost:5002
3. Start the Vite frontend server on http://localhost:5174
4. Ensure proper database initialization

## Manual Setup (if needed)

If you prefer to start the servers manually:

### Backend
```bash
# From the project root
PYTHONPATH=/Users/gnir/NewDashboard python data_integration/app.py
```

### Frontend
```bash
# From the project root
cd frontend && npm run dev
```

## Development

- Backend API runs on port 5002
- Frontend development server runs on port 5174
- The application uses PostgreSQL for data storage
- CORS is configured to allow frontend-backend communication

## Database

The application uses PostgreSQL. Make sure you have PostgreSQL installed and running.
The database will be automatically initialized when you start the backend server.

## Stopping the Servers

To stop both servers:
1. Press Ctrl+C in the terminal where you ran start_servers.sh
2. The script will clean up both frontend and backend processes