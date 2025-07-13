#!/bin/bash

# Commercial Deployment Script for Smart Warehouse Management System
# This script deploys the commercial-grade features and ensures all components are ready

echo "🚀 Starting Commercial Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

print_success "Python 3 is installed"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

print_success "pip3 is installed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing commercial dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "All dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Initialize database
print_status "Initializing database..."
cd backend
python -c "
from app.database import engine, Base
Base.metadata.create_all(bind=engine)
print('Database tables created successfully')
"

if [ $? -eq 0 ]; then
    print_success "Database initialized"
else
    print_warning "Database initialization had issues, but continuing..."
fi

cd ..

# Create sample data
print_status "Creating sample data for commercial features..."
python setup_sample_data.py

# Verify commercial features
print_status "Verifying commercial features..."

# Check if commercial dashboard exists
if [ -f "frontend/commercial_intelligence_dashboard.html" ]; then
    print_success "Commercial Intelligence Dashboard is ready"
else
    print_warning "Commercial Intelligence Dashboard not found"
fi

# Check if commercial router exists
if [ -f "backend/app/routers/commercial_features.py" ]; then
    print_success "Commercial Features Router is ready"
else
    print_error "Commercial Features Router not found"
    exit 1
fi

# Start the application
print_status "Starting Smart Warehouse Management System..."

# Kill any existing processes on port 8000
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    print_warning "Port 8000 is in use. Killing existing process..."
    kill -9 $(lsof -Pi :8000 -sTCP:LISTEN -t)
    sleep 2
fi

# Start the FastAPI server
print_status "Launching FastAPI server with commercial features..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

# Wait for server to start
sleep 5

# Check if server is running
if curl -s http://localhost:8000/health > /dev/null; then
    print_success "Server is running successfully!"
    echo ""
    echo "🎉 Commercial Deployment Complete!"
    echo ""
    echo "Access your Smart Warehouse System:"
    echo "📊 Main Dashboard: http://localhost:8000"
    echo "🤖 AI Assistant: http://localhost:8000/chatbot"
    echo "📈 Advanced Dashboard: http://localhost:8000/advanced-dashboard"
    echo "🏢 Enterprise Dashboard: http://localhost:8000/enterprise-dashboard"
    echo "🧠 Commercial Intelligence: http://localhost:8000/commercial-intelligence"
    echo "📋 API Documentation: http://localhost:8000/docs"
    echo ""
    echo "🔥 Commercial Features Available:"
    echo "   • Executive Dashboard with KPIs"
    echo "   • Advanced Analytics & ROI Calculator"
    echo "   • QR Code Management System"
    echo "   • Automated Inventory Optimization"
    echo "   • Smart Alerts & Notifications"
    echo "   • Computer Vision Quality Control"
    echo "   • IoT Sensor Integration"
    echo "   • Compliance Reporting"
    echo "   • AMR Fleet Management"
    echo ""
    echo "Press Ctrl+C to stop the server"
    
    # Keep script running to show server output
    wait
else
    print_error "Server failed to start. Check the logs above for errors."
    exit 1
fi
