#!/usr/bin/env python3
"""
Final Demo: Enhanced Natural Language Chatbot for Warehouse Management
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_query(query, description=""):
    """Test a single query and show results"""
    print(f"\n💬 {description}")
    print(f"Query: '{query}'")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json={"message": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"🎯 Intent: {data.get('intent', 'unknown')} (confidence: {data.get('confidence', 0):.2f})")
            print(f"📝 Response:\n{data.get('message', 'No response')}")
            
            if data.get('data'):
                print(f"📊 Data: {json.dumps(data['data'], indent=2)}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def main():
    print("🎉 ENHANCED NATURAL LANGUAGE CHATBOT DEMO")
    print("=" * 80)
    print("Testing the warehouse management chatbot with natural, casual language!")
    print("=" * 80)
    
    # Test categories that work well
    demo_tests = [
        # Low stock and alerts (Working perfectly!)
        ("show low stock", "🔔 Alert Monitoring - Show low stock items"),
        ("what items are running low?", "🔔 Alert Monitoring - Casual language low stock check"),
        ("any low stock items", "🔔 Alert Monitoring - Simple low stock query"),
        
        # Specific product searches (Working well with exact names)
        ("check bluetooth headphones", "📦 Product Search - Bluetooth headphones"),
        ("office chair location", "📦 Product Search - Office chair with location"),
        ("check monitor", "📦 Product Search - Monitor stock"),
        ("wireless mouse inventory", "📦 Product Search - Wireless mouse"),
        
        # General help and guidance (Working perfectly)
        ("help", "❓ Help System - General help"),
        ("what can you do?", "❓ Help System - Capabilities inquiry"),
        
        # Dashboard and reporting (Some working)
        ("inventory status", "📊 Reporting - Inventory status"),
        ("warehouse summary", "📊 Reporting - Warehouse overview"),
        
        # Conversational responses (Working well)
        ("hi there", "👋 Conversation - Greeting"),
        ("thank you", "👋 Conversation - Gratitude"),
        
        # Advanced natural language (Testing boundaries)
        ("hey, do we have any notebooks?", "🗣️  Casual Language - Notebook inquiry"),
        ("where can I find the power banks?", "🗣️  Casual Language - Location query"),
    ]
    
    for query, description in demo_tests:
        test_query(query, description)
        time.sleep(0.5)
    
    print("\n" + "=" * 80)
    print("🎯 DEMO COMPLETE!")
    print("=" * 80)
    print("\n✅ **What's Working Great:**")
    print("• Low stock monitoring with natural language")
    print("• Specific product searches with fuzzy matching")
    print("• Conversational responses and personality")
    print("• Help system with context-aware responses")
    print("• Location and inventory details")
    
    print("\n🔄 **Areas for Future Enhancement:**")
    print("• More complex entity extraction (e.g., 'how many X do we have?')")
    print("• Better handling of ambiguous product names")
    print("• Advanced analytics and reporting queries")
    print("• Multi-step conversation flows")
    
    print("\n🚀 **Try these working examples:**")
    print("• 'show low stock' - See items that need reordering")
    print("• 'check bluetooth headphones' - Get detailed product info")
    print("• 'office chair location' - Find where products are stored")
    print("• 'what items are running low?' - Natural language alerts")
    print("• 'help' - See all available commands")

if __name__ == "__main__":
    main()
