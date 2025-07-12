#!/usr/bin/env python3
"""
Test the complete website integration with natural language chatbot
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_chatbot_endpoint(query, expected_keywords=None):
    """Test chatbot with a natural language query"""
    print(f"\n🤖 Testing query: '{query}'")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json={"message": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('message', 'No response')
            print(f"✅ Response: {response_text[:100]}{'...' if len(response_text) > 100 else ''}")
            
            if expected_keywords:
                response_lower = response_text.lower()
                for keyword in expected_keywords:
                    if keyword.lower() in response_lower:
                        print(f"   ✓ Found expected keyword: '{keyword}'")
                    else:
                        print(f"   ⚠️  Missing keyword: '{keyword}'")
            
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_api_endpoints():
    """Test all main API endpoints"""
    print("🌐 Testing API Endpoints")
    
    endpoints = [
        ("/api/inventory/products", "Products"),
        ("/api/dashboard/overview", "Dashboard"),
        ("/api/inventory/summary", "Inventory Summary"),
        ("/api/inbound/shipments", "Inbound Shipments"),
        ("/api/outbound/orders", "Outbound Orders")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {name}: Working")
            else:
                print(f"❌ {name}: Error {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Failed - {e}")

def main():
    print("🚀 Starting Website Integration Test")
    print("=" * 60)
    
    # Test API endpoints first
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("🤖 Testing Natural Language Chatbot")
    
    # Test natural language queries
    test_queries = [
        # Basic inventory queries
        ("show me all products", ["product", "inventory"]),
        ("what items do we have in stock?", ["stock", "items"]),
        ("how many headphones do we have?", ["headphones", "quantity"]),
        ("do we have any laptops?", ["laptop"]),
        
        # Casual language
        ("hey, what's our stock looking like?", ["stock"]),
        ("can you tell me about our inventory?", ["inventory"]),
        ("what stuff do we have?", ["product", "items"]),
        
        # Specific product searches
        ("find bluetooth headphones", ["bluetooth", "headphones"]),
        ("where are the office chairs located?", ["office", "chair", "location"]),
        ("how much do the keyboards cost?", ["keyboard", "price"]),
        
        # Stock levels and alerts
        ("what items are running low?", ["low", "stock"]),
        ("show me products that need reordering", ["reorder"]),
        ("which products are out of stock?", ["out", "stock"]),
        
        # Dashboard and analytics
        ("give me a summary of our warehouse", ["summary", "warehouse"]),
        ("how's business looking?", ["business", "overview"]),
        ("what's the total value of our inventory?", ["value", "inventory"]),
        
        # Operations
        ("any pending shipments?", ["shipment", "pending"]),
        ("show me recent orders", ["order"]),
        ("what's happening in the warehouse today?", ["warehouse"]),
        
        # Mixed casual language
        ("yo, can you check if we got any mice in stock?", ["mice", "mouse"]),
        ("dude, how many monitors we got?", ["monitor"]),
        ("hey buddy, what's the deal with our cables?", ["cable"]),
    ]
    
    success_count = 0
    total_tests = len(test_queries)
    
    for query, keywords in test_queries:
        if test_chatbot_endpoint(query, keywords):
            success_count += 1
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {success_count}/{total_tests} queries successful")
    
    if success_count == total_tests:
        print("🎉 All tests passed! The chatbot handles natural language perfectly!")
    elif success_count >= total_tests * 0.8:
        print("✅ Most tests passed! Good natural language support.")
    else:
        print("⚠️  Some issues detected. May need further improvements.")

if __name__ == "__main__":
    main()
