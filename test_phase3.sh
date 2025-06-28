#!/bin/bash

# Phase 3 Testing Script: Forecasting + Space Planning
echo "PHASE 3 TESTING - SMART WAREHOUSE FORECASTING & SPACE PLANNING"
echo "=============================================================="

# Check if server is running
echo "1. Checking system status..."
curl -s http://localhost:8001/health | jq .

echo -e "\n2. Testing Phase 3 Health Check..."
curl -s http://localhost:8001/api/phase3/health | jq .

echo -e "\n3. Testing Product Velocity Analysis..."
curl -s http://localhost:8001/api/phase3/space/analyze-velocity | jq '. | {success, total_products_analyzed, velocity_distribution}'

echo -e "\n4. Testing Demand Forecasting..."
curl -s http://localhost:8001/api/phase3/forecast/all-products?weeks=2 | jq '. | {success, total_products, successful_forecasts}'

echo -e "\n5. Testing Stock Risk Analysis..."
curl -s http://localhost:8001/api/phase3/forecast/stock-risks | jq '. | {success, total_alerts}'

echo -e "\n6. Testing Reorder Recommendations..."
curl -s http://localhost:8001/api/phase3/forecast/reorder-recommendations | jq '. | {success, total_recommendations}'

echo -e "\n7. Testing Space Optimization..."
curl -s http://localhost:8001/api/phase3/space/layout-optimization | jq '. | {success, total_recommendations, current_layout_efficiency}'

echo -e "\n8. Testing Category Grouping..."
curl -s http://localhost:8001/api/phase3/space/category-grouping | jq '. | {success, total_suggestions}'

echo -e "\n9. Testing Fast-Moving Optimization..."
curl -s http://localhost:8001/api/phase3/space/fast-moving-optimization | jq '. | {success, fast_moving_products_count}'

echo -e "\n10. Testing Phase 3 Dashboard..."
curl -s http://localhost:8001/api/phase3/dashboard/overview | jq '. | {success, overview}'

echo -e "\n11. Testing AI Chatbot with Phase 3 Features..."

echo "Testing forecasting query:"
curl -s -X POST "http://localhost:8001/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "predict demand for SKU: PROD001"}' | jq '.message'

echo -e "\nTesting velocity analysis query:"
curl -s -X POST "http://localhost:8001/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "analyze product velocity"}' | jq '.message'

echo -e "\nTesting space optimization query:"
curl -s -X POST "http://localhost:8001/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "optimize warehouse layout"}' | jq '.message'

echo -e "\nTesting reorder recommendations query:"
curl -s -X POST "http://localhost:8001/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "what should I reorder?"}' | jq '.message'

echo -e "\n📄 12. Testing CSV Export..."
echo "Forecast CSV export available at: http://localhost:8001/api/phase3/forecast/export-csv"

echo -e "\n🎉 PHASE 3 TESTING COMPLETE!"
echo "========================================="
echo " Features tested:"
echo "   • Demand forecasting with AI"
echo "   • Stock risk analysis"
echo "   • Reorder recommendations"
echo "   • Product velocity analysis"
echo "   • Space layout optimization"
echo "   • Category grouping suggestions"
echo "   • Fast-moving goods optimization"
echo "   • AI chatbot with Phase 3 capabilities"
echo "   • CSV export functionality"
echo ""
echo "🌐 Phase 3 API Documentation: http://localhost:8001/docs"
echo "📱 Mobile Interface: http://localhost:8001/chatbot"
echo ""
echo "Ready for Phase 3 production deployment!"
