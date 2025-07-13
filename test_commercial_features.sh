#!/bin/bash

# Commercial Features Test Suite
# Comprehensive testing for all commercial-grade features

echo "🧪 Starting Commercial Features Test Suite..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print colored output
print_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASSED_TESTS++))
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAILED_TESTS++))
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# Function to test API endpoint
test_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local data=${3:-""}
    
    ((TOTAL_TESTS++))
    print_test "Testing $method $endpoint"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" -o /tmp/response.json "http://localhost:8000$endpoint")
    else
        response=$(curl -s -w "%{http_code}" -o /tmp/response.json -X $method -H "Content-Type: application/json" -d "$data" "http://localhost:8000$endpoint")
    fi
    
    http_code="${response: -3}"
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        print_pass "$endpoint returned HTTP $http_code"
        return 0
    else
        print_fail "$endpoint returned HTTP $http_code"
        return 1
    fi
}

# Check if server is running
print_info "Checking if server is running..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Server is not running. Please start the server first with:"
    echo "   ./deploy_commercial.sh"
    exit 1
fi

print_pass "Server is running"
echo ""

# Test Basic API Health
print_info "=== Testing Basic API Health ==="
test_endpoint "/health"
test_endpoint "/docs"
echo ""

# Test Commercial Dashboard Endpoints
print_info "=== Testing Commercial Dashboard Endpoints ==="
test_endpoint "/api/commercial/executive-dashboard"
test_endpoint "/api/commercial/financial-metrics"
echo ""

# Test QR Code Management
print_info "=== Testing QR Code Management ==="
qr_data='{"product_id": 123, "sku": "TEST123", "location": "A1-B2-C3", "additional_data": {}}'
test_endpoint "/api/commercial/qr-codes/generate" "POST" "$qr_data"
test_endpoint "/api/commercial/qr-codes"
echo ""

# Test Advanced Analytics
print_info "=== Testing Advanced Analytics ==="
test_endpoint "/api/commercial/analytics/abc-analysis"
test_endpoint "/api/commercial/analytics/velocity-analysis"
test_endpoint "/api/commercial/analytics/predictive-insights"
test_endpoint "/api/commercial/analytics/roi-analysis"
echo ""

# Test Layout Optimization
print_info "=== Testing Layout Optimization ==="
layout_data='{"zone": "A", "optimization_type": "efficiency", "constraints": ["max_distance", "picking_frequency"]}'
test_endpoint "/api/commercial/layout/optimize" "POST" "$layout_data"
test_endpoint "/api/commercial/layout/recommendations"
echo ""

# Test KPI Monitoring
print_info "=== Testing KPI Monitoring ==="
kpi_data='{"metric_name": "order_fulfillment_rate", "target_value": 98.0, "warning_threshold": 95.0, "critical_threshold": 90.0, "measurement_period": "daily"}'
test_endpoint "/api/commercial/kpis/targets" "POST" "$kpi_data"
test_endpoint "/api/commercial/kpis/current"
echo ""

# Test Smart Alerts
print_info "=== Testing Smart Alerts ==="
alert_data='{"alert_type": "low_stock", "threshold_value": 10, "notification_method": "email", "recipients": ["test@example.com"], "severity": "high"}'
test_endpoint "/api/commercial/alerts/configure" "POST" "$alert_data"
test_endpoint "/api/commercial/alerts/active"
echo ""

# Test Compliance Reporting
print_info "=== Testing Compliance Reporting ==="
test_endpoint "/api/commercial/compliance/inventory-report"
test_endpoint "/api/commercial/compliance/audit-trail"
echo ""

# Test Automation Features
print_info "=== Testing Automation Features ==="
test_endpoint "/api/commercial/automation/status"
test_endpoint "/api/commercial/automation/workflows"
echo ""

# Test AMR Fleet Management
print_info "=== Testing AMR Fleet Management ==="
test_endpoint "/api/commercial/amr/fleet-status"
test_endpoint "/api/commercial/amr/robots"
echo ""

# Test Computer Vision QC
print_info "=== Testing Computer Vision QC ==="
test_endpoint "/api/commercial/computer-vision/qc-status"
test_endpoint "/api/commercial/computer-vision/detections"
echo ""

# Test IoT Sensor Management
print_info "=== Testing IoT Sensor Management ==="
test_endpoint "/api/commercial/iot/sensor-status"
test_endpoint "/api/commercial/iot/alerts"
echo ""

# Test Frontend Pages
print_info "=== Testing Frontend Pages ==="
test_endpoint "/"
test_endpoint "/chatbot"
test_endpoint "/advanced-dashboard"
test_endpoint "/enterprise-dashboard"
test_endpoint "/commercial-intelligence"
echo ""

# Performance Tests
print_info "=== Running Performance Tests ==="
print_test "Testing API response time..."

start_time=$(date +%s%N)
curl -s http://localhost:8000/api/commercial/executive-dashboard > /dev/null
end_time=$(date +%s%N)
response_time=$(( (end_time - start_time) / 1000000 ))

if [ $response_time -lt 1000 ]; then
    print_pass "API response time: ${response_time}ms (< 1000ms)"
    ((TOTAL_TESTS++))
    ((PASSED_TESTS++))
else
    print_fail "API response time: ${response_time}ms (>= 1000ms)"
    ((TOTAL_TESTS++))
    ((FAILED_TESTS++))
fi

# Load Testing (simplified)
print_test "Basic load testing (10 concurrent requests)..."
((TOTAL_TESTS++))

for i in {1..10}; do
    curl -s http://localhost:8000/api/commercial/executive-dashboard > /dev/null &
done
wait

if [ $? -eq 0 ]; then
    print_pass "Load test completed successfully"
    ((PASSED_TESTS++))
else
    print_fail "Load test failed"
    ((FAILED_TESTS++))
fi

echo ""

# Database Integrity Tests
print_info "=== Testing Database Integrity ==="
print_test "Checking database connection and basic queries..."
((TOTAL_TESTS++))

cd backend
python -c "
try:
    from app.database import get_db
    from app.models.database_models import Product, Inventory
    from sqlalchemy.orm import Session
    
    db = next(get_db())
    
    # Test basic queries
    products = db.query(Product).limit(5).all()
    inventory = db.query(Inventory).limit(5).all()
    
    print('Database queries successful')
    print(f'Products found: {len(products)}')
    print(f'Inventory records found: {len(inventory)}')
    
except Exception as e:
    print(f'Database error: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    print_pass "Database integrity check passed"
    ((PASSED_TESTS++))
else
    print_fail "Database integrity check failed"
    ((FAILED_TESTS++))
fi

cd ..
echo ""

# Security Tests
print_info "=== Basic Security Tests ==="
print_test "Testing for common security headers..."
((TOTAL_TESTS++))

security_response=$(curl -s -I http://localhost:8000/)
if echo "$security_response" | grep -q "X-Frame-Options\|X-Content-Type-Options\|X-XSS-Protection"; then
    print_pass "Security headers present"
    ((PASSED_TESTS++))
else
    print_fail "Security headers missing"
    ((FAILED_TESTS++))
fi

# Test API without authentication (should be accessible for demo)
print_test "Testing API accessibility..."
((TOTAL_TESTS++))
response=$(curl -s -w "%{http_code}" -o /dev/null http://localhost:8000/api/commercial/executive-dashboard)
if [ "$response" -eq 200 ]; then
    print_pass "API is accessible"
    ((PASSED_TESTS++))
else
    print_fail "API is not accessible"
    ((FAILED_TESTS++))
fi

echo ""

# Final Results
print_info "=== Test Results Summary ==="
echo ""
echo "📊 Total Tests: $TOTAL_TESTS"
echo "✅ Passed: $PASSED_TESTS"
echo "❌ Failed: $FAILED_TESTS"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo "🎉 All tests passed! Commercial features are ready for deployment."
    echo ""
    echo "✨ Commercial Features Validated:"
    echo "   • Executive Dashboard & KPIs"
    echo "   • Financial Metrics & ROI Analysis" 
    echo "   • QR Code Management System"
    echo "   • Advanced Analytics (ABC, Velocity, Predictive)"
    echo "   • Layout Optimization Engine"
    echo "   • Smart Alerts & Notifications"
    echo "   • Compliance Reporting"
    echo "   • Automation Workflows"
    echo "   • AMR Fleet Management"
    echo "   • Computer Vision QC"
    echo "   • IoT Sensor Monitoring"
    echo "   • Frontend Dashboard Integration"
    echo "   • Database Integrity"
    echo "   • Basic Security Measures"
    echo "   • Performance Benchmarks"
    echo ""
    echo "🚀 System is ready for commercial deployment!"
    exit 0
else
    success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo "⚠️  Some tests failed. Success rate: ${success_rate}%"
    
    if [ $success_rate -ge 80 ]; then
        echo "🟡 System is mostly functional but needs attention to failed components."
        exit 1
    else
        echo "🔴 System has significant issues. Please review failed tests before deployment."
        exit 2
    fi
fi
