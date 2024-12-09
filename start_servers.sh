#!/bin/bash

# Colors for better visibility
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting NewDashboard Development Environment${NC}"
echo "This script will start both backend and frontend servers"

# Function to check if a port is in use
check_port() {
    lsof -i :$1 >/dev/null 2>&1
    return $?
}

# Kill any existing processes on ports 5002 and 5174
echo "Cleaning up any existing processes..."
if check_port 5002; then
    echo "Cleaning up port 5002..."
    lsof -ti:5002 | xargs kill -9 2>/dev/null
fi

if check_port 5174; then
    echo "Cleaning up port 5174..."
    lsof -ti:5174 | xargs kill -9 2>/dev/null
fi

# Start the backend server
echo -e "${GREEN}Starting backend server...${NC}"
PYTHONPATH=/Users/gnir/NewDashboard python data_integration/app.py &

# Wait for backend to be ready
echo "Waiting for backend to start..."
while ! nc -z localhost 5002; do   
  sleep 1
done
echo -e "${GREEN}Backend is ready at http://localhost:5002${NC}"

# Start the frontend server
echo -e "${GREEN}Starting frontend server...${NC}"
cd frontend && npm run dev

# Note: The script will stay running with the frontend server
# To stop both servers, press Ctrl+C and both servers will be terminated