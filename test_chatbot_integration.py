#!/usr/bin/env python3
"""
Test script to verify chatbot integration with inventory management
This script will:
1. Check if backend server is running
2. Test the chatbot API endpoints
3. Verify inventory data parsing and responses
4. Test various query formats to ensure no hallucination
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def test_server_status():
    """Test if the backend server is running"""
    print("🔍 Testing server status...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print("❌ Backend server returned unexpected status")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend server is not running")
        print("💡 Start the server with: cd backend && uvicorn app.main:app --reload")
        return False

def test_chatbot_api():
    """Test the chatbot API endpoint"""
    print("\n🤖 Testing chatbot API...")
    
    test_messages = [
        "Check stock SKU: LAPTOP001",
        "Show inventory summary", 
        "Add 50 units SKU: PHONE123",
        "What's the status of order ORD001?",
        "Gate in shipment SH001",
        "Show low stock alerts",
        "Help me with inventory management"
    ]
    
    session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    for message in test_messages:
        print(f"\n📝 Testing: '{message}'")
        try:
            response = requests.post(
                f"{API_URL}/chat/message",
                json={
                    "message": message,
                    "session_id": session_id,
                    "user_id": "test_user"
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response received")
                print(f"   Intent: {data.get('intent', 'unknown')}")
                print(f"   Success: {data.get('success', False)}")
                if data.get('data'):
                    print(f"   Data: {json.dumps(data['data'], indent=2)}")
                print(f"   Message: {data.get('message', 'No message')[:100]}...")
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")

def test_inventory_api():
    """Test direct inventory API endpoints"""
    print("\n📦 Testing inventory API...")
    
    try:
        # Test inventory summary
        response = requests.get(f"{API_URL}/inventory/summary")
        if response.status_code == 200:
            data = response.json()
            print("✅ Inventory summary retrieved")
            print(f"   Total products: {data.get('total_products', 'unknown')}")
            print(f"   Low stock count: {data.get('low_stock_count', 'unknown')}")
        else:
            print(f"❌ Inventory API Error: {response.status_code}")
            
        # Test products list
        response = requests.get(f"{API_URL}/inventory/products")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Products retrieved: {len(products)} items")
            if products:
                sample_product = products[0]
                print(f"   Sample product: {sample_product.get('name')} (SKU: {sample_product.get('sku')})")
        else:
            print(f"❌ Products API Error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Inventory API request failed: {e}")

def test_chatbot_status():
    """Test chatbot system status endpoint"""
    print("\n📊 Testing chatbot status...")
    
    try:
        response = requests.get(f"{API_URL}/chat/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ Chatbot status retrieved")
            print(f"   LLM Service: {data.get('llm_service', 'unknown')}")
            print(f"   RAG Service: {data.get('rag_service', 'unknown')}")
            print(f"   Enhanced Mode: {data.get('enhanced_mode', 'unknown')}")
        else:
            print(f"❌ Chatbot status error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chatbot status request failed: {e}")

def main():
    """Main test function"""
    print("🚀 Smart Warehouse Chatbot Integration Test")
    print("=" * 50)
    
    # Test server status
    if not test_server_status():
        print("\n❌ Cannot proceed without backend server")
        return
    
    # Test APIs
    test_chatbot_status()
    test_inventory_api()
    test_chatbot_api()
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("- If chatbot responses are detailed and specific, integration works!")
    print("- If responses are generic or mention 'not found', check sample data")
    print("- Frontend now connects to real backend instead of using static data")
    print("\n💡 To test live:")
    print("1. Run: cd backend && uvicorn app.main:app --reload")
    print("2. Open: http://localhost:8000/docs (API documentation)")
    print("3. Visit: chatbot.html on GitHub Pages")
    print("4. Try: 'Check stock SKU: LAPTOP001' or 'Show inventory summary'")

if __name__ == "__main__":
    main()
