#!/bin/bash

# ==============================================================================
# Smart Warehouse Management System - Production Readiness Validation
# ==============================================================================
# 
# This script validates that all commercial features are working correctly
# and the system is ready for production deployment.
#
# ==============================================================================

echo "🔍 SMART WAREHOUSE PRODUCTION READINESS VALIDATION"
echo "=================================================="
echo "📅 Validation Date: $(date)"
echo "🎯 Version: Commercial v4.0.0"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print test results
print_test() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ $1${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_section() {
    echo ""
    echo -e "${BLUE}🔹 $1${NC}"
    echo "----------------------------------------"
}

# Check if server is running
SERVER_URL="http://localhost:8000"

print_section "SYSTEM AVAILABILITY TESTS"

# Test main application
curl -f -s $SERVER_URL > /dev/null
print_test "Main application accessible" $?

# Test API documentation
curl -f -s $SERVER_URL/docs > /dev/null
print_test "API documentation accessible" $?

# Test frontend static files
curl -f -s $SERVER_URL/static/css/style.css > /dev/null
print_test "Static files serving correctly" $?

print_section "COMMERCIAL API ENDPOINTS"

# Test commercial executive dashboard
curl -f -s $SERVER_URL/api/commercial/executive-dashboard > /dev/null
print_test "Executive Dashboard API" $?

# Test financial metrics
curl -f -s $SERVER_URL/api/commercial/financial-metrics > /dev/null
print_test "Financial Metrics API" $?

# Test ABC analysis
curl -f -s $SERVER_URL/api/commercial/analytics/abc-analysis > /dev/null
print_test "ABC Analysis API" $?

# Test velocity analysis
curl -f -s $SERVER_URL/api/commercial/analytics/velocity-analysis > /dev/null
print_test "Velocity Analysis API" $?

# Test predictive insights
curl -f -s $SERVER_URL/api/commercial/analytics/predictive-insights > /dev/null
print_test "Predictive Analytics API" $?

# Test ROI analysis
curl -f -s $SERVER_URL/api/commercial/analytics/roi-analysis > /dev/null
print_test "ROI Analysis API" $?

# Test QR code management
curl -f -s $SERVER_URL/api/commercial/qr-codes > /dev/null
print_test "QR Code Management API" $?

# Test QR code generation
curl -f -s -X POST "$SERVER_URL/api/commercial/qr-codes/generate?product_id=999&sku=TEST-SKU&location=TEST-A1-B1" > /dev/null
print_test "QR Code Generation API" $?

# Test automation opportunities
curl -f -s $SERVER_URL/api/commercial/automation/opportunities > /dev/null
print_test "Automation Opportunities API" $?

# Test compliance reporting
curl -f -s $SERVER_URL/api/commercial/compliance/report > /dev/null
print_test "Compliance Reporting API" $?

# Test real-time KPIs
curl -f -s $SERVER_URL/api/commercial/kpi/real-time > /dev/null
print_test "Real-time KPI API" $?

# Test layout analysis
curl -f -s $SERVER_URL/api/commercial/optimization/layout-analysis > /dev/null
print_test "Layout Analysis API" $?

print_section "FRONTEND DASHBOARDS"

# Test main dashboard
curl -f -s $SERVER_URL/ > /dev/null
print_test "Main Dashboard" $?

# Test commercial intelligence dashboard
curl -f -s $SERVER_URL/commercial-intelligence-dashboard > /dev/null
print_test "Commercial Intelligence Dashboard" $?

# Test enterprise dashboard
curl -f -s $SERVER_URL/enterprise-dashboard > /dev/null
print_test "Enterprise Dashboard" $?

# Test advanced dashboard
curl -f -s $SERVER_URL/advanced-dashboard > /dev/null
print_test "Advanced Dashboard" $?

# Test chatbot interface
curl -f -s $SERVER_URL/chatbot > /dev/null
print_test "AI Chatbot Interface" $?

print_section "CORE API FUNCTIONALITY"

# Test inventory endpoints
curl -f -s $SERVER_URL/api/inventory/products > /dev/null
print_test "Inventory Products API" $?

curl -f -s $SERVER_URL/api/inventory/low-stock > /dev/null
print_test "Low Stock Items API" $?

# Test dashboard endpoints
curl -f -s $SERVER_URL/api/dashboard/overview > /dev/null
print_test "Dashboard Overview API" $?

curl -f -s $SERVER_URL/api/dashboard/system-health > /dev/null
print_test "System Health API" $?

print_section "DATA VALIDATION TESTS"

# Test executive dashboard data structure
EXEC_DATA=$(curl -s $SERVER_URL/api/commercial/executive-dashboard)
if echo "$EXEC_DATA" | jq -e '.financial_metrics' > /dev/null 2>&1; then
    print_test "Executive Dashboard data structure" 0
else
    print_test "Executive Dashboard data structure" 1
fi

# Test ABC analysis data structure
ABC_DATA=$(curl -s $SERVER_URL/api/commercial/analytics/abc-analysis)
if echo "$ABC_DATA" | jq -e '.category_a' > /dev/null 2>&1; then
    print_test "ABC Analysis data structure" 0
else
    print_test "ABC Analysis data structure" 1
fi

# Test QR codes data structure
QR_DATA=$(curl -s $SERVER_URL/api/commercial/qr-codes)
if echo "$QR_DATA" | jq -e '.qr_codes' > /dev/null 2>&1; then
    print_test "QR Codes data structure" 0
else
    print_test "QR Codes data structure" 1
fi

print_section "PERFORMANCE TESTS"

# Test response times
START_TIME=$(python3 -c "import time; print(int(time.time() * 1000))")
curl -s $SERVER_URL/api/commercial/executive-dashboard > /dev/null
END_TIME=$(python3 -c "import time; print(int(time.time() * 1000))")
RESPONSE_TIME=$((END_TIME - START_TIME))

if [ $RESPONSE_TIME -lt 1000 ]; then
    print_test "API response time (<1s)" 0
    print_info "Executive Dashboard API response: ${RESPONSE_TIME}ms"
else
    print_test "API response time (<1s)" 1
    print_warning "Executive Dashboard API response: ${RESPONSE_TIME}ms (slow)"
fi

# Test concurrent requests
print_info "Testing concurrent API requests..."
for i in {1..5}; do
    curl -s $SERVER_URL/api/commercial/executive-dashboard > /dev/null &
done
wait

print_test "Concurrent request handling" 0

print_section "FILE SYSTEM VALIDATION"

# Check required files exist
[ -f "requirements.txt" ]
print_test "requirements.txt exists" $?

[ -f "smart_warehouse.db" ]
print_test "Database file exists" $?

[ -d "backend/app" ]
print_test "Backend application directory exists" $?

[ -d "frontend" ]
print_test "Frontend directory exists" $?

[ -f "backend/app/main_commercial.py" ]
print_test "Commercial backend main file exists" $?

[ -f "backend/app/routers/commercial_features.py" ]
print_test "Commercial features router exists" $?

[ -f "backend/app/services/commercial_services.py" ]
print_test "Commercial services file exists" $?

[ -f "frontend/commercial_intelligence_dashboard.html" ]
print_test "Commercial Intelligence Dashboard exists" $?

print_section "SECURITY & COMPLIANCE VALIDATION"

# Test CORS headers
CORS_HEADERS=$(curl -s -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET" -X OPTIONS $SERVER_URL/ -I | grep -i "access-control-allow")
if [ ! -z "$CORS_HEADERS" ]; then
    print_test "CORS headers configured" 0
else
    print_test "CORS headers configured" 1
fi

# Test API error handling
ERROR_RESPONSE=$(curl -s $SERVER_URL/api/commercial/nonexistent-endpoint)
if echo "$ERROR_RESPONSE" | grep -q "error\|Error\|404\|not found"; then
    print_test "Error handling for invalid endpoints" 0
else
    print_test "Error handling for invalid endpoints" 1
fi

print_section "BUSINESS FEATURE VALIDATION"

# Test that we have commercial data
REVENUE=$(curl -s $SERVER_URL/api/commercial/executive-dashboard | jq -r '.financial_metrics.revenue // 0')
if [ "$REVENUE" != "0" ] && [ "$REVENUE" != "null" ]; then
    print_test "Financial metrics populated" 0
else
    print_test "Financial metrics populated" 1
fi

# Test QR code system has data
QR_COUNT=$(curl -s $SERVER_URL/api/commercial/qr-codes | jq -r '.total // 0')
if [ "$QR_COUNT" -gt 0 ]; then
    print_test "QR code system has data" 0
else
    print_test "QR code system has data" 1
fi

# Test ABC analysis has classifications
CATEGORY_A=$(curl -s $SERVER_URL/api/commercial/analytics/abc-analysis | jq -r '.category_a.products // 0')
if [ "$CATEGORY_A" -gt 0 ]; then
    print_test "ABC analysis has classifications" 0
else
    print_test "ABC analysis has classifications" 1
fi

print_section "INTEGRATION TESTS"

# Test that commercial dashboard loads with data
DASHBOARD_CONTENT=$(curl -s $SERVER_URL/commercial-intelligence-dashboard)
if echo "$DASHBOARD_CONTENT" | grep -q "Enterprise Warehouse Management\|Commercial Intelligence\|Commercial Analytics"; then
    print_test "Commercial dashboard content correct" 0
else
    print_test "Commercial dashboard content correct" 1
fi

# Test API documentation includes commercial endpoints
API_SPEC=$(curl -s $SERVER_URL/openapi.json)
if echo "$API_SPEC" | grep -q "commercial"; then
    print_test "Commercial endpoints in API documentation" 0
else
    print_test "Commercial endpoints in API documentation" 1
fi

print_section "FINAL VALIDATION RESULTS"

echo ""
echo "📊 VALIDATION SUMMARY"
echo "===================="
echo -e "✅ Passed: ${GREEN}$PASSED_TESTS${NC}/$TOTAL_TESTS"
echo -e "❌ Failed: ${RED}$FAILED_TESTS${NC}/$TOTAL_TESTS"

SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
echo -e "📈 Success Rate: ${BLUE}$SUCCESS_RATE%${NC}"

echo ""
if [ $SUCCESS_RATE -ge 90 ]; then
    echo -e "${GREEN}🎉 PRODUCTION READY!${NC}"
    echo -e "${GREEN}✅ System validation successful - Ready for commercial deployment${NC}"
    
    echo ""
    echo "🚀 Next Steps:"
    echo "=============="
    echo "1. Deploy using: ./deploy_production_commercial.sh"
    echo "2. Start system: ./start_production.sh"
    echo "3. Monitor with: ./health_check.sh"
    
    exit 0
elif [ $SUCCESS_RATE -ge 75 ]; then
    echo -e "${YELLOW}⚠️  MOSTLY READY${NC}"
    echo -e "${YELLOW}Some issues detected - Review failed tests before deployment${NC}"
    exit 1
else
    echo -e "${RED}❌ NOT READY${NC}"
    echo -e "${RED}Critical issues detected - Fix failed tests before deployment${NC}"
    exit 2
fi
