#!/usr/bin/env python3
"""
Simple test script for enhanced layman language chatbot without database operations
"""
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.enhanced_nlp_processor import EnhancedNLPProcessor

def test_nlp_processor():
    """Test the enhanced NLP processor with various layman language queries"""
    
    # Initialize NLP processor
    nlp = EnhancedNLPProcessor()
    
    # Test queries demonstrating layman language understanding
    test_cases = [
        {
            "query": "Do we have any laptops?",
            "expected_intent": "inventory_check",
            "description": "Casual inventory check"
        },
        {
            "query": "Got any blue widgets left?",
            "expected_intent": "inventory_check", 
            "description": "Very casual stock inquiry"
        },
        {
            "query": "We just got 50 more keyboards",
            "expected_intent": "stock_update",
            "description": "Casual stock update notification"
        },
        {
            "query": "Truck arrived with delivery!",
            "expected_intent": "inbound_operations",
            "description": "Casual delivery notification"
        },
        {
            "query": "Customer wants their order shipped ASAP",
            "expected_intent": "outbound_operations",
            "description": "Urgent shipping request"
        },
        {
            "query": "Hi! Can you help me check stock?",
            "expected_intent": "inventory_check",
            "description": "Polite greeting with request"
        },
        {
            "query": "What needs attention around here?",
            "expected_intent": "alerts_monitoring",
            "description": "Casual alert inquiry"
        },
        {
            "query": "Thanks for your help!",
            "expected_intent": "help_general",
            "description": "Gratitude expression"
        }
    ]
    
    print("🤖 Enhanced Layman Language NLP Test")
    print("=" * 60)
    print("Testing natural language understanding with casual queries...")
    print()
    
    success_count = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        expected_intent = test_case["expected_intent"]
        description = test_case["description"]
        
        print(f"Test {i}: {description}")
        print(f"Query: \"{query}\"")
        print("-" * 40)
        
        try:
            # Process the query
            result = nlp.process_layman_query(query)
            
            intent = result["intent"]
            confidence = result["confidence"]
            entities = result["entities"]
            context = result["context"]
            response_style = result["response_style"]
            
            # Check if intent matches expected
            intent_match = intent == expected_intent
            if intent_match:
                success_count += 1
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
            
            print(f"Status: {status}")
            print(f"Intent: {intent} (expected: {expected_intent})")
            print(f"Confidence: {confidence:.2f}")
            print(f"Response Style: {response_style}")
            
            if entities:
                print(f"Entities: {entities}")
            
            # Show context understanding
            context_features = []
            if context.get("is_greeting"):
                context_features.append("greeting")
            if context.get("is_polite"):
                context_features.append("polite")
            if context.get("is_urgent"):
                context_features.append("urgent")
            if context.get("is_uncertain"):
                context_features.append("uncertain")
            
            if context_features:
                print(f"Context: {', '.join(context_features)}")
            
            # Demonstrate response generation
            if intent == "inventory_check" and entities.get("product_name"):
                sample_response = nlp.generate_response(
                    "inventory_found", 
                    response_style,
                    product=entities["product_name"],
                    quantity=25,
                    status_message="Stock levels look good!"
                )
                print(f"Sample Response: {sample_response}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()
    
    # Summary
    print("📊 Test Summary")
    print("=" * 30)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {success_count}")
    print(f"Failed: {total_tests - success_count}")
    print(f"Success Rate: {(success_count/total_tests)*100:.1f}%")
    
    print("\n🎯 Enhanced Features Demonstrated:")
    print("• Natural language intent classification")
    print("• Entity extraction from casual language")
    print("• Context awareness (greeting, politeness, urgency)")
    print("• Response style adaptation")
    print("• Fuzzy product name matching")
    print("• Conversation flow understanding")
    
    print("\n💬 Example Supported Queries:")
    example_queries = [
        "Do we have any blue widgets?",
        "Got 25 more keyboards today",
        "Truck just arrived!",
        "Customer needs their order ASAP",
        "What's running low?",
        "Thanks! You're very helpful",
        "Can you check inventory for me?",
        "We're out of red chairs"
    ]
    
    for query in example_queries:
        print(f"  • \"{query}\"")

if __name__ == "__main__":
    test_nlp_processor()
