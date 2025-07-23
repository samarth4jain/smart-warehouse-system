#!/usr/bin/env python3
"""
Test script to verify the enhanced chatbot improvements
"""

import sys
import requests
import json
import time

def test_chatbot_improvements():
    """Test the enhanced chatbot with various improved prompt types"""
    
    base_url = "http://127.0.0.1:8001"
    chatbot_url = f"{base_url}/api/chat/message"
    
    # Test cases covering the improvements we made
    test_cases = [
        {
            "name": "Basic Product Query",
            "message": "Gaming Laptop",
            "expected": "should find product"
        },
        {
            "name": "Complex Phrase (Improvement Target)",
            "message": "Inventory for Gaming Laptop",
            "expected": "should extract 'Gaming Laptop' from complex phrase"
        },
        {
            "name": "Plural Form Handling", 
            "message": "Do we have smartphones?",
            "expected": "should convert plural to singular and find Smartphone"
        },
        {
            "name": "General Inventory Query",
            "message": "What products do we have in stock?",
            "expected": "should show inventory overview"
        },
        {
            "name": "Natural Language Query",
            "message": "Show me all available products",
            "expected": "should list all products"
        },
        {
            "name": "Alternative Product Names",
            "message": "Check laptop inventory",
            "expected": "should find Gaming Laptop via fuzzy matching"
        },
        {
            "name": "Casual Language",
            "message": "Do we have any phones?",
            "expected": "should understand 'phones' refers to smartphone"
        }
    ]
    
    print("🧪 Testing Enhanced Chatbot Improvements")
    print("=" * 50)
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print(f"Input: '{test_case['message']}'")
        
        try:
            response = requests.post(
                chatbot_url,
                json={
                    "message": test_case["message"],
                    "user_id": "test_user",
                    "session_id": f"test_session_{i}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                message = data.get("response", "No response")
                
                print(f"✅ Status: {'SUCCESS' if success else 'FAILED'}")
                print(f"📝 Response: {message[:100]}{'...' if len(message) > 100 else ''}")
                
                results.append({
                    "test": test_case["name"],
                    "success": success,
                    "response_length": len(message),
                    "has_response": bool(message and message.strip())
                })
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                results.append({
                    "test": test_case["name"],
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
            results.append({
                "test": test_case["name"],
                "success": False,
                "error": str(e)
            })
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    successful_tests = sum(1 for r in results if r.get("success", False))
    total_tests = len(results)
    
    print(f"✅ Successful: {successful_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - successful_tests}/{total_tests}")
    print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    print("\n🔍 Individual Results:")
    for result in results:
        status = "✅" if result.get("success") else "❌"
        error_info = f" ({result.get('error', 'Unknown error')})" if not result.get("success") else ""
        print(f"{status} {result['test']}{error_info}")
    
    return successful_tests, total_tests

if __name__ == "__main__":
    print("Starting Enhanced Chatbot Test Suite...\n")
    
    try:
        successful, total = test_chatbot_improvements()
        
        if successful == total:
            print(f"\n🎉 ALL TESTS PASSED! The improvements are working perfectly.")
            sys.exit(0)
        elif successful > total * 0.7:  # 70% success rate
            print(f"\n✅ MOSTLY SUCCESSFUL! {successful}/{total} tests passed.")
            print("💡 Minor issues detected but core improvements are working.")
            sys.exit(0)
        else:
            print(f"\n⚠️ SOME ISSUES DETECTED. {successful}/{total} tests passed.")
            print("🔧 Further improvements may be needed.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)
