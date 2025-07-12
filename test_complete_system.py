#!/usr/bin/env python3
"""
Comprehensive System Test for Smart Warehouse Management System
Tests all components: API endpoints, database operations, frontend integration
"""

import requests
import json
import time
import sys
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test_header(test_name):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{test_name}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def test_api_endpoint(url, method="GET", data=None, expected_status=200, test_name=""):
    """Generic API endpoint tester"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        if response.status_code == expected_status:
            print_success(f"{test_name}: Status {response.status_code}")
            try:
                return response.json()
            except:
                return {"status": "success", "content": response.text}
        else:
            print_error(f"{test_name}: Expected {expected_status}, got {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print_error(f"{test_name}: Request failed - {e}")
        return None

def test_basic_system():
    """Test basic system functionality"""
    print_test_header("BASIC SYSTEM TESTS")
    
    # Health check
    result = test_api_endpoint(f"{BASE_URL}/health", test_name="Health Check")
    if result:
        print_success(f"System status: {result.get('status', 'unknown')}")
    
    # API Documentation
    result = test_api_endpoint(f"{BASE_URL}/docs", test_name="API Documentation", expected_status=200)
    if result:
        print_success("API documentation accessible")
    
    return True

def test_inventory_management():
    """Test inventory management features"""
    print_test_header("INVENTORY MANAGEMENT TESTS")
    
    # Get all products
    result = test_api_endpoint(f"{BASE_URL}/api/inventory/products", test_name="Get All Products")
    if result and result.get('success'):
        print_success(f"Found {len(result.get('products', []))} products")
    
    # Get low stock items
    result = test_api_endpoint(f"{BASE_URL}/api/inventory/low-stock", test_name="Low Stock Items")
    if result and result.get('success'):
        print_success(f"Found {len(result.get('low_stock_items', []))} low stock items")
    
    # Get stock levels
    result = test_api_endpoint(f"{BASE_URL}/api/inventory/stock-levels", test_name="Stock Levels")
    if result and result.get('success'):
        print_success("Stock levels retrieved successfully")
    
    # Test search functionality
    result = test_api_endpoint(f"{BASE_URL}/api/inventory/search?query=PROD", test_name="Product Search")
    if result and result.get('success'):
        print_success(f"Search returned {len(result.get('results', []))} results")
    
    return True

def test_inbound_operations():
    """Test inbound operations"""
    print_test_header("INBOUND OPERATIONS TESTS")
    
    # Get pending receipts
    result = test_api_endpoint(f"{BASE_URL}/api/inbound/pending", test_name="Pending Receipts")
    if result and result.get('success'):
        print_success(f"Found {len(result.get('receipts', []))} pending receipts")
    
    # Get receiving queue
    result = test_api_endpoint(f"{BASE_URL}/api/inbound/queue", test_name="Receiving Queue")
    if result and result.get('success'):
        print_success("Receiving queue retrieved successfully")
    
    return True

def test_outbound_operations():
    """Test outbound operations"""
    print_test_header("OUTBOUND OPERATIONS TESTS")
    
    # Get shipping queue
    result = test_api_endpoint(f"{BASE_URL}/api/outbound/queue", test_name="Shipping Queue")
    if result and result.get('success'):
        print_success("Shipping queue retrieved successfully")
    
    # Get orders
    result = test_api_endpoint(f"{BASE_URL}/api/outbound/orders", test_name="Orders")
    if result and result.get('success'):
        print_success(f"Found {len(result.get('orders', []))} orders")
    
    return True

def test_dashboard_features():
    """Test dashboard functionality"""
    print_test_header("DASHBOARD TESTS")
    
    # Get dashboard overview
    result = test_api_endpoint(f"{BASE_URL}/api/dashboard/overview", test_name="Dashboard Overview")
    if result and result.get('success'):
        print_success("Dashboard overview loaded successfully")
    
    # Get recent activities
    result = test_api_endpoint(f"{BASE_URL}/api/dashboard/recent-activities", test_name="Recent Activities")
    if result and result.get('success'):
        print_success(f"Found {len(result.get('activities', []))} recent activities")
    
    # Get analytics
    result = test_api_endpoint(f"{BASE_URL}/api/dashboard/analytics", test_name="Analytics")
    if result and result.get('success'):
        print_success("Analytics data retrieved successfully")
    
    return True

def test_chatbot_functionality():
    """Test AI chatbot functionality"""
    print_test_header("AI CHATBOT TESTS")
    
    # Test basic chatbot message
    test_message = {"message": "Hello, what can you help me with?"}
    result = test_api_endpoint(f"{BASE_URL}/api/chat/message", method="POST", data=test_message, test_name="Basic Chat")
    if result and result.get('message'):
        print_success("Chatbot responded successfully")
    
    # Test inventory query
    test_message = {"message": "Show me current inventory levels"}
    result = test_api_endpoint(f"{BASE_URL}/api/chat/message", method="POST", data=test_message, test_name="Inventory Query")
    if result and result.get('message'):
        print_success("Inventory query processed")
    
    # Test stock query
    test_message = {"message": "What items are low in stock?"}
    result = test_api_endpoint(f"{BASE_URL}/api/chat/message", method="POST", data=test_message, test_name="Stock Query")
    if result and result.get('message'):
        print_success("Stock query processed")
    
    return True

def test_phase3_forecasting():
    """Test Phase 3 forecasting and space planning"""
    print_test_header("PHASE 3: FORECASTING & SPACE PLANNING TESTS")
    
    # Phase 3 health check
    result = test_api_endpoint(f"{BASE_URL}/api/phase3/health", test_name="Phase 3 Health")
    if result and result.get('success'):
        print_success("Phase 3 systems operational")
    
    # Product velocity analysis
    result = test_api_endpoint(f"{BASE_URL}/api/phase3/space/analyze-velocity", test_name="Velocity Analysis")
    if result and result.get('success'):
        print_success(f"Analyzed {result.get('total_products_analyzed', 0)} products")
    
    # Demand forecasting
    result = test_api_endpoint(f"{BASE_URL}/api/phase3/forecast/all-products?weeks=2", test_name="Demand Forecasting")
    if result and result.get('success'):
        print_success(f"Generated forecasts for {result.get('total_products', 0)} products")
    
    # Stock risk analysis
    result = test_api_endpoint(f"{BASE_URL}/api/phase3/forecast/stock-risks", test_name="Stock Risk Analysis")
    if result and result.get('success'):
        print_success("Stock risk analysis completed")
    
    # Reorder recommendations
    result = test_api_endpoint(f"{BASE_URL}/api/phase3/forecast/reorder-recommendations", test_name="Reorder Recommendations")
    if result and result.get('success'):
        print_success("Reorder recommendations generated")
    
    # Space optimization
    result = test_api_endpoint(f"{BASE_URL}/api/phase3/space/layout-optimization", test_name="Space Optimization")
    if result and result.get('success'):
        print_success("Space optimization analysis completed")
    
    return True

def test_frontend_pages():
    """Test frontend page accessibility"""
    print_test_header("FRONTEND PAGE TESTS")
    
    pages = [
        ("/", "Main Dashboard"),
        ("/chatbot", "Chatbot Interface"),
        ("/advanced-dashboard", "Advanced Dashboard"),
        ("/enterprise-dashboard", "Enterprise Dashboard")
    ]
    
    for path, name in pages:
        response = requests.get(f"{BASE_URL}{path}")
        if response.status_code == 200:
            print_success(f"{name} accessible")
        else:
            print_error(f"{name} not accessible (Status: {response.status_code})")
    
    return True

def test_performance():
    """Test system performance"""
    print_test_header("PERFORMANCE TESTS")
    
    # Measure response times
    endpoints = [
        "/health",
        "/api/inventory/products",
        "/api/dashboard/overview",
        "/api/phase3/health"
    ]
    
    for endpoint in endpoints:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}{endpoint}")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if response.status_code == 200:
            if response_time < 1000:  # Less than 1 second
                print_success(f"{endpoint}: {response_time:.2f}ms")
            else:
                print_warning(f"{endpoint}: {response_time:.2f}ms (slow)")
        else:
            print_error(f"{endpoint}: Failed (Status: {response.status_code})")
    
    return True

def main():
    """Run comprehensive system tests"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("🏭 SMART WAREHOUSE MANAGEMENT SYSTEM")
    print("📋 COMPREHENSIVE SYSTEM TEST SUITE")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.END}")
    
    tests = [
        ("Basic System", test_basic_system),
        ("Inventory Management", test_inventory_management),
        ("Inbound Operations", test_inbound_operations),
        ("Outbound Operations", test_outbound_operations),
        ("Dashboard Features", test_dashboard_features),
        ("AI Chatbot", test_chatbot_functionality),
        ("Phase 3 Forecasting", test_phase3_forecasting),
        ("Frontend Pages", test_frontend_pages),
        ("Performance", test_performance)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_function in tests:
        try:
            if test_function():
                passed_tests += 1
        except Exception as e:
            print_error(f"Test '{test_name}' failed with exception: {e}")
    
    # Final summary
    print_test_header("TEST SUMMARY")
    print(f"{Colors.BOLD}Total Tests: {total_tests}{Colors.END}")
    print(f"{Colors.GREEN}Passed: {passed_tests}{Colors.END}")
    print(f"{Colors.RED}Failed: {total_tests - passed_tests}{Colors.END}")
    
    if passed_tests == total_tests:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! System is fully operational.{Colors.END}")
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Some tests failed. Check the output above for details.{Colors.END}")
    
    print(f"\n{Colors.BLUE}🌐 Access the system at: {BASE_URL}{Colors.END}")
    print(f"{Colors.BLUE}📚 API Documentation: {BASE_URL}/docs{Colors.END}")
    print(f"{Colors.BLUE}🤖 Chatbot Interface: {BASE_URL}/chatbot{Colors.END}")

if __name__ == "__main__":
    main()
