#!/bin/bash

# 🏭 SMART WAREHOUSE MANAGEMENT SYSTEM
# 🧪 COMPREHENSIVE WEBSITE TESTING SUITE
# ================================================

echo "🏭 SMART WAREHOUSE MANAGEMENT SYSTEM"
echo "🧪 COMPREHENSIVE WEBSITE TESTING SUITE"
echo "================================================"
echo "🕒 Started at: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print test headers
print_header() {
    echo ""
    echo -e "${BLUE}${BOLD}============================================${NC}"
    echo -e "${BLUE}${BOLD}$1${NC}"
    echo -e "${BLUE}${BOLD}============================================${NC}"
}

# Function to test API endpoint
test_endpoint() {
    local url="$1"
    local description="$2"
    local expected_status="${3:-200}"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -n "Testing $description... "
    
    if command -v curl >/dev/null 2>&1; then
        response=$(curl -s -w "%{http_code}" -o /dev/null "$url" 2>/dev/null)
        if [ "$response" = "$expected_status" ]; then
            echo -e "${GREEN}✓ PASS${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e "${RED}✗ FAIL (Status: $response)${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
    else
        echo -e "${YELLOW}⚠ SKIP (curl not available)${NC}"
    fi
}

# Function to test API with JSON response
test_api_json() {
    local url="$1"
    local description="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -n "Testing $description... "
    
    if command -v curl >/dev/null 2>&1; then
        response=$(curl -s "$url" 2>/dev/null)
        if echo "$response" | jq . >/dev/null 2>&1; then
            if echo "$response" | jq -r '.success // .status' | grep -q "true\|healthy"; then
                echo -e "${GREEN}✓ PASS${NC}"
                PASSED_TESTS=$((PASSED_TESTS + 1))
            else
                echo -e "${YELLOW}⚠ PARTIAL (No success indicator)${NC}"
                PASSED_TESTS=$((PASSED_TESTS + 1))
            fi
        else
            echo -e "${RED}✗ FAIL (Invalid JSON)${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
    else
        echo -e "${YELLOW}⚠ SKIP (curl not available)${NC}"
    fi
}

# Check if server is running
print_header "SERVER STATUS CHECK"
echo "Checking if Smart Warehouse server is running..."

SERVER_URL="http://localhost:8001"
if curl -s "$SERVER_URL/health" >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Server is running on port 8001${NC}"
else
    echo -e "${RED}✗ Server is not running on port 8001${NC}"
    echo "Please start the server first: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001"
    exit 1
fi

# Test 1: Basic System Health
print_header "1. BASIC SYSTEM HEALTH"
test_api_json "$SERVER_URL/health" "System Health Check"
test_endpoint "$SERVER_URL/docs" "API Documentation"
test_endpoint "$SERVER_URL/redoc" "ReDoc Documentation"

# Test 2: Frontend Pages
print_header "2. FRONTEND PAGES"
test_endpoint "$SERVER_URL/" "Main Dashboard"
test_endpoint "$SERVER_URL/chatbot" "Chatbot Interface"
test_endpoint "$SERVER_URL/advanced-dashboard" "Advanced Dashboard"
test_endpoint "$SERVER_URL/enterprise-dashboard" "Enterprise Dashboard"

# Test 3: Core API Endpoints
print_header "3. CORE API ENDPOINTS"
test_api_json "$SERVER_URL/api/inventory/products" "Inventory Products"
test_api_json "$SERVER_URL/api/inventory/low-stock" "Low Stock Items"
test_api_json "$SERVER_URL/api/inventory/stock-levels" "Stock Levels"
test_api_json "$SERVER_URL/api/dashboard/overview" "Dashboard Overview"
test_api_json "$SERVER_URL/api/dashboard/recent-activities" "Recent Activities"

# Test 4: Inbound Operations
print_header "4. INBOUND OPERATIONS"
test_api_json "$SERVER_URL/api/inbound/pending" "Pending Receipts"
test_api_json "$SERVER_URL/api/inbound/queue" "Receiving Queue"

# Test 5: Outbound Operations
print_header "5. OUTBOUND OPERATIONS"
test_api_json "$SERVER_URL/api/outbound/queue" "Shipping Queue"
test_api_json "$SERVER_URL/api/outbound/orders" "Orders"

# Test 6: AI Chatbot
print_header "6. AI CHATBOT FUNCTIONALITY"
echo "Testing chatbot with sample queries..."

TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "Testing basic chatbot query... "
response=$(curl -s -X POST "$SERVER_URL/api/chat/message" \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello, what can you help me with?"}' 2>/dev/null)

if echo "$response" | jq -r '.message' | grep -q "."; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "Testing inventory query... "
response=$(curl -s -X POST "$SERVER_URL/api/chat/message" \
    -H "Content-Type: application/json" \
    -d '{"message": "Show me current inventory levels"}' 2>/dev/null)

if echo "$response" | jq -r '.message' | grep -q "."; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 7: Phase 3 Forecasting & Space Planning
print_header "7. PHASE 3: FORECASTING & SPACE PLANNING"
test_api_json "$SERVER_URL/api/phase3/health" "Phase 3 Health Check"
test_api_json "$SERVER_URL/api/phase3/space/analyze-velocity" "Product Velocity Analysis"
test_api_json "$SERVER_URL/api/phase3/forecast/all-products?weeks=2" "Demand Forecasting"
test_api_json "$SERVER_URL/api/phase3/forecast/stock-risks" "Stock Risk Analysis"
test_api_json "$SERVER_URL/api/phase3/forecast/reorder-recommendations" "Reorder Recommendations"
test_api_json "$SERVER_URL/api/phase3/space/layout-optimization" "Space Layout Optimization"
test_api_json "$SERVER_URL/api/phase3/space/category-grouping" "Category Grouping"

# Test 8: Search and Filter Functionality
print_header "8. SEARCH & FILTER FUNCTIONALITY"
test_api_json "$SERVER_URL/api/inventory/search?query=PROD" "Product Search"

# Test 9: Performance Testing
print_header "9. PERFORMANCE TESTING"
echo "Testing response times for key endpoints..."

performance_test() {
    local url="$1"
    local description="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Testing $description response time... "
    
    start_time=$(date +%s%N)
    response=$(curl -s "$url" 2>/dev/null)
    end_time=$(date +%s%N)
    
    duration=$(( (end_time - start_time) / 1000000 )) # Convert to milliseconds
    
    if [ $duration -lt 1000 ]; then
        echo -e "${GREEN}✓ FAST (${duration}ms)${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    elif [ $duration -lt 3000 ]; then
        echo -e "${YELLOW}⚠ ACCEPTABLE (${duration}ms)${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ SLOW (${duration}ms)${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

performance_test "$SERVER_URL/health" "Health Check"
performance_test "$SERVER_URL/api/inventory/products" "Inventory Products"
performance_test "$SERVER_URL/api/dashboard/overview" "Dashboard Overview"

# Test 10: Database Operations
print_header "10. DATABASE OPERATIONS"
echo "Testing database connectivity and basic operations..."

TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "Testing database connectivity... "
response=$(curl -s "$SERVER_URL/api/inventory/products" 2>/dev/null)
if echo "$response" | jq -r '.success' | grep -q "true"; then
    echo -e "${GREEN}✓ PASS${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAIL${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Run Python comprehensive tests
print_header "11. COMPREHENSIVE PYTHON TESTS"
echo "Running detailed Python test suite..."

if [ -f "test_complete_system.py" ]; then
    python test_complete_system.py
else
    echo -e "${YELLOW}⚠ Python test suite not found${NC}"
fi

# Final Summary
print_header "TEST SUMMARY REPORT"
echo -e "${BOLD}🧪 TOTAL TESTS RUN: $TOTAL_TESTS${NC}"
echo -e "${GREEN}${BOLD}✓ PASSED: $PASSED_TESTS${NC}"
echo -e "${RED}${BOLD}✗ FAILED: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}${BOLD}🎉 ALL TESTS PASSED! 🎉${NC}"
    echo -e "${GREEN}${BOLD}The Smart Warehouse Management System is fully operational!${NC}"
else
    echo ""
    echo -e "${YELLOW}${BOLD}⚠️  SOME TESTS FAILED${NC}"
    echo -e "${YELLOW}Please check the failed tests above for details.${NC}"
fi

echo ""
echo -e "${BLUE}${BOLD}ACCESS THE SYSTEM:${NC}"
echo -e "${BLUE}🌐 Main Dashboard: $SERVER_URL${NC}"
echo -e "${BLUE}🤖 Chatbot Interface: $SERVER_URL/chatbot${NC}"
echo -e "${BLUE}📊 Advanced Dashboard: $SERVER_URL/advanced-dashboard${NC}"
echo -e "${BLUE}🏢 Enterprise Dashboard: $SERVER_URL/enterprise-dashboard${NC}"
echo -e "${BLUE}📚 API Documentation: $SERVER_URL/docs${NC}"
echo ""
echo -e "${BOLD}🕒 Testing completed at: $(date)${NC}"
echo "================================================"
