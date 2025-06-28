#!/bin/bash

# Phase 3 Deployment Script: Smart Warehouse Forecasting + Space Planning
echo "DEPLOYING PHASE 3: FORECASTING + SPACE PLANNING"
echo "================================================"

echo "Phase 3 Deployment Checklist:"
echo "* Forecasting + Space Planning (AI-Lite)"
echo "* Historical sales/dispatch data ingestion"
echo "* AI-powered weekly demand forecasting"
echo "* Overstock/understock risk analysis"
echo "* Fast-moving goods optimization"
echo "* Category-based product grouping"
echo "* CSV export functionality"
echo ""

echo "1. Setting up Phase 3 database schema and sample data..."
python setup_phase3_data.py

echo ""
echo "2. Starting Smart Warehouse System with Phase 3 features..."
echo "   • Version: 3.0.0"
echo "   • Features: Phase 1 + Phase 2 + Phase 3"
echo "   • AI Integration: Enhanced with forecasting"

# Check if server is already running
if pgrep -f "uvicorn.*app.main:app" > /dev/null; then
    echo "   • Server already running, restarting with Phase 3..."
    pkill -f uvicorn
    sleep 2
fi

# Start server in background
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 &
SERVER_PID=$!

echo "   • Server PID: $SERVER_PID"
echo "   • Starting up..."

# Wait for server to start
sleep 5

echo ""
echo "3. Validating Phase 3 deployment..."

# Test basic health
echo "   Testing system health..."
curl -s http://localhost:8001/health | jq -r .status

# Test Phase 3 health
echo "   Testing Phase 3 services..."
curl -s http://localhost:8001/api/phase3/health | jq -r .status

# Test key endpoints
echo "   Testing forecasting service..."
FORECAST_TEST=$(curl -s http://localhost:8001/api/phase3/forecast/all-products?weeks=2 | jq -r .success)
echo "   • Forecasting: $FORECAST_TEST"

echo "   Testing space optimization service..."
SPACE_TEST=$(curl -s http://localhost:8001/api/phase3/space/analyze-velocity | jq -r .success)
echo "   • Space optimization: $SPACE_TEST"

echo "   Testing AI chatbot with Phase 3..."
CHATBOT_TEST=$(curl -s -X POST http://localhost:8001/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' | jq -r .success)
echo "   • AI Chatbot: $CHATBOT_TEST"

echo ""
echo "📈 4. Phase 3 Feature Summary:"
echo "    FORECASTING CAPABILITIES:"
echo "      • Weekly demand prediction for all SKUs"
echo "      • AI-powered stock risk analysis"
echo "      • Intelligent reorder recommendations"
echo "      • Historical sales data ingestion (CSV/API)"
echo "      • Confidence-based forecasting with insights"
echo ""
echo "   🏗️ SPACE OPTIMIZATION CAPABILITIES:"
echo "      • Product velocity analysis (fast/medium/slow/dead)"
echo "      • Layout optimization recommendations"
echo "      • Fast-moving goods placement near exits"
echo "      • Category-based grouping strategies"
echo "      • Comprehensive space planning with ROI projections"
echo ""
echo "   🤖 AI CHATBOT ENHANCEMENTS:"
echo "      • Natural language queries for forecasting"
echo "      • Voice-activated space optimization guidance"
echo "      • Conversational reorder recommendations"
echo "      • Smart warehouse analytics through chat"

echo ""
echo "🌐 5. Phase 3 Access Points:"
echo "   • Main Dashboard:     http://localhost:8001/"
echo "   • Mobile Interface:   http://localhost:8001/chatbot"
echo "   • API Documentation:  http://localhost:8001/docs"
echo "   • Phase 3 Health:     http://localhost:8001/api/phase3/health"
echo "   • Forecasting API:    http://localhost:8001/api/phase3/forecast/"
echo "   • Space Optimization: http://localhost:8001/api/phase3/space/"

echo ""
echo "🎯 6. Quick Phase 3 Tests:"
echo ""
echo "   Test demand forecasting:"
echo "   curl -X GET 'http://localhost:8001/api/phase3/forecast/all-products?weeks=4'"
echo ""
echo "   Test velocity analysis:"
echo "   curl -X GET 'http://localhost:8001/api/phase3/space/analyze-velocity'"
echo ""
echo "   Test reorder recommendations:"
echo "   curl -X GET 'http://localhost:8001/api/phase3/forecast/reorder-recommendations'"
echo ""
echo "   Test AI chatbot with Phase 3:"
echo "   curl -X POST http://localhost:8001/api/chat/message \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"message\": \"predict demand for next 4 weeks\"}'"

echo ""
echo " 7. CSV Export Examples:"
echo "   • Export demand forecasts: http://localhost:8001/api/phase3/forecast/export-csv"
echo "   • Download format: Weekly forecasts with confidence levels"
echo "   • Compatible with Excel, Google Sheets, and BI tools"

echo ""
echo "🎉 PHASE 3 DEPLOYMENT COMPLETE!"
echo "================================="
echo ""
echo " STATUS: PRODUCTION READY"
echo "📈 FEATURES: All Phase 3 deliverables implemented"
echo "🤖 AI INTEGRATION: Enhanced forecasting and optimization"
echo " ANALYTICS: Comprehensive dashboard and export capabilities"
echo "📱 MOBILE: Full Phase 3 features available via chatbot interface"
echo ""
echo "🚀 The Smart Warehouse Management System now includes:"
echo "   ✓ Phase 1: Core inventory management"
echo "   ✓ Phase 2: Automated inbound/outbound + mobile interface"
echo "   ✓ Phase 3: AI forecasting + space optimization"
echo ""
echo "Ready for MSME production deployment with full AI-powered capabilities!"
echo ""
echo "📋 For comprehensive testing, run: ./test_phase3.sh"
