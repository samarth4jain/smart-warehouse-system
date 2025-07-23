#!/bin/bash

# Enhanced Warehouse System Startup Script
echo "🚀 Starting Enhanced Smart Warehouse System..."

# Change to project directory
cd /Users/SAM/Downloads/smart-warehouse-system

# Set Python path
export PYTHONPATH=$PYTHONPATH:/Users/SAM/Downloads/smart-warehouse-system

# Start the backend server
echo "📡 Starting FastAPI Backend Server on port 8001..."
cd backend
/Users/SAM/Downloads/smart-warehouse-system/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload &

# Wait for server to start
sleep 5

# Check if server is running
echo "🔍 Checking server status..."
if curl -s http://localhost:8001/docs > /dev/null; then
    echo "✅ Backend server is running successfully!"
    echo "📊 API Documentation: http://localhost:8001/docs"
    echo "💬 Chatbot API: http://localhost:8001/api/chat/message"
    echo "📈 Dashboard: http://localhost:8001/"
    echo ""
    echo "🌐 Frontend URLs:"
    echo "📋 Main Dashboard: file:///Users/SAM/Downloads/smart-warehouse-system/frontend/dashboard.html"
    echo "💬 Chatbot Interface: file:///Users/SAM/Downloads/smart-warehouse-system/frontend/chatbot.html"
    echo "🏢 Enterprise Dashboard: file:///Users/SAM/Downloads/smart-warehouse-system/frontend/enterprise_dashboard.html"
    echo ""
    echo "🧪 Test the enhanced chatbot improvements:"
    echo "cd /Users/SAM/Downloads/smart-warehouse-system && /Users/SAM/Downloads/smart-warehouse-system/.venv/bin/python test_enhanced_chatbot.py"
else
    echo "❌ Server failed to start. Check the logs above."
fi

echo ""
echo "📚 Press Ctrl+C to stop the server"
wait
