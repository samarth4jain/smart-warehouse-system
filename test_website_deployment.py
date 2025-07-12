#!/usr/bin/env python3
"""
Test the deployed website integration with enhanced chatbot
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_website_endpoints():
    """Test all main website endpoints"""
    print("🌐 Testing Website Integration")
    print("=" * 50)
    
    endpoints = [
        ("/", "Main Dashboard"),
        ("/chatbot", "Enhanced Chatbot Interface"),
        ("/api/chat/message", "Chatbot API (POST)"),
        ("/api/inventory/products", "Inventory API"),
        ("/api/dashboard/overview", "Dashboard API"),
        ("/health", "Health Check")
    ]
    
    for endpoint, name in endpoints:
        try:
            if endpoint == "/api/chat/message":
                # Test POST request for chatbot
                response = requests.post(
                    f"{BASE_URL}{endpoint}",
                    json={"message": "show low stock"},
                    headers={"Content-Type": "application/json"}
                )
            else:
                response = requests.get(f"{BASE_URL}{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ {name}: Working (Status {response.status_code})")
                
                # For chatbot API, show response preview
                if endpoint == "/api/chat/message":
                    data = response.json()
                    intent = data.get('intent', 'unknown')
                    message_preview = data.get('message', '')[:50] + "..."
                    print(f"   🤖 Intent: {intent}")
                    print(f"   💬 Response: {message_preview}")
            else:
                print(f"❌ {name}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {name}: Failed - {e}")

def test_enhanced_chatbot_features():
    """Test specific enhanced chatbot features"""
    print("\n🤖 Testing Enhanced Chatbot Features")
    print("=" * 50)
    
    test_queries = [
        ("show low stock", "Low Stock Alert System"),
        ("check bluetooth headphones", "Fuzzy Product Search"),
        ("what items are running low?", "Natural Language Alerts"),
        ("check monitor", "Smart Product Matching"),
        ("help", "Help System")
    ]
    
    for query, description in test_queries:
        print(f"\n🧪 Testing: {description}")
        print(f"Query: '{query}'")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/chat/message",
                json={"message": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                intent = data.get('intent', 'unknown')
                confidence = data.get('confidence', 0)
                success = data.get('success', False)
                
                print(f"   ✅ Intent: {intent} (confidence: {confidence:.2f})")
                print(f"   ✅ Success: {success}")
                
                # Show brief response preview
                message = data.get('message', '')
                preview = message.split('\n')[0][:80] + "..." if len(message) > 80 else message.split('\n')[0]
                print(f"   💬 Response: {preview}")
                
                # Show data if available
                if data.get('data'):
                    print(f"   📊 Has structured data: Yes")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.2)  # Small delay between requests

def main():
    print("🚀 WEBSITE INTEGRATION TEST")
    print("Testing Enhanced Natural Language Chatbot Deployment")
    print("=" * 80)
    
    # Test basic website functionality
    test_website_endpoints()
    
    # Test enhanced chatbot features
    test_enhanced_chatbot_features()
    
    print("\n" + "=" * 80)
    print("🎯 INTEGRATION TEST COMPLETE!")
    print("=" * 80)
    
    print("\n🌐 **Access Your Enhanced Chatbot:**")
    print(f"• Chatbot Interface: {BASE_URL}/chatbot")
    print(f"• Main Dashboard: {BASE_URL}")
    print(f"• API Documentation: {BASE_URL}/docs")
    
    print("\n✨ **Enhanced Features Available:**")
    print("• Natural language understanding")
    print("• Smart low stock alerts")
    print("• Fuzzy product search")
    print("• Conversational responses")
    print("• Context-aware assistance")
    
    print("\n🎮 **Try These Commands:**")
    print("• 'show low stock' - See items needing reorder")
    print("• 'check bluetooth headphones' - Smart product search")
    print("• 'what items are running low?' - Natural language alerts")

if __name__ == "__main__":
    main()
