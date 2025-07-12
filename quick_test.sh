#!/bin/bash

# 🚀 QUICK TEST SCRIPT FOR SMART WAREHOUSE SYSTEM
# ===============================================

echo "🚀 SMART WAREHOUSE - QUICK SYSTEM TEST"
echo "======================================"

SERVER_URL="http://localhost:8001"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔍 Testing core system functionality..."
echo ""

# Quick health check
echo -n "1. System Health: "
if curl -s "$SERVER_URL/health" | jq -r '.status' | grep -q "healthy"; then
    echo -e "${GREEN}✓ HEALTHY${NC}"
else
    echo -e "${RED}✗ UNHEALTHY${NC}"
    exit 1
fi

# Quick frontend test
echo -n "2. Main Dashboard: "
if curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL/" | grep -q "200"; then
    echo -e "${GREEN}✓ ACCESSIBLE${NC}"
else
    echo -e "${RED}✗ NOT ACCESSIBLE${NC}"
fi

# Quick API test
echo -n "3. Inventory API: "
if curl -s "$SERVER_URL/api/inventory/products" | jq -r '.success' | grep -q "true"; then
    echo -e "${GREEN}✓ WORKING${NC}"
else
    echo -e "${RED}✗ NOT WORKING${NC}"
fi

# Quick chatbot test
echo -n "4. AI Chatbot: "
response=$(curl -s -X POST "$SERVER_URL/api/chat/message" \
    -H "Content-Type: application/json" \
    -d '{"message": "test"}' 2>/dev/null)
if echo "$response" | jq -r '.message' | grep -q "."; then
    echo -e "${GREEN}✓ RESPONDING${NC}"
else
    echo -e "${RED}✗ NOT RESPONDING${NC}"
fi

# Quick Phase 3 test
echo -n "5. Phase 3 Features: "
if curl -s "$SERVER_URL/api/phase3/health" | jq -r '.success' | grep -q "true"; then
    echo -e "${GREEN}✓ OPERATIONAL${NC}"
else
    echo -e "${RED}✗ NOT OPERATIONAL${NC}"
fi

echo ""
echo "🌐 Access the system at: $SERVER_URL"
echo "🤖 Chatbot interface: $SERVER_URL/chatbot"
echo "📚 API docs: $SERVER_URL/docs"
echo ""
echo "For comprehensive testing, run: ./test_all_features.sh"
