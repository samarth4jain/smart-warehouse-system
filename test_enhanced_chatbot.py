#!/usr/bin/env python3
"""
Test script for enhanced layman language chatbot
"""
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import get_db
from backend.app.services.conversational_chatbot_service import ConversationalChatbotService

def test_layman_queries():
    """Test various layman language queries"""
    
    # Get database session
    db = next(get_db())
    
    # Initialize chatbot service
    chatbot = ConversationalChatbotService(db)
    
    # Test queries with different levels of formality and context
    test_queries = [
        # Casual inventory checks
        "Do we have any laptops?",
        "Got any blue widgets left?",
        "How much stuff do we have in stock?",
        "Is there any inventory for chairs?",
        "Can you check if we have keyboards?",
        
        # Casual stock updates
        "We just got 50 more mice",
        "Add 25 widgets to the system",
        "Actually we have 100 keyboards not 75",
        
        # Casual operations
        "Truck just arrived!",
        "Customer wants their order ASAP",
        "Delivery is here for receiving",
        
        # General help and conversation
        "Hi! Can you help me?",
        "What can you do?",
        "I'm confused about how this works",
        "Thanks for your help!",
        
        # Urgent scenarios
        "URGENT: Check stock for emergency order",
        "ASAP - need to ship order ORD001",
        
        # Mixed formality
        "Please check inventory status for SKU: PROD001",
        "Could you tell me about stock levels?",
    ]
    
    print("🤖 Enhanced Layman Language Chatbot Test")
    print("=" * 60)
    print("Testing conversational warehouse assistant with natural language queries...")
    print()
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: \"{query}\"")
        print("-" * 40)
        
        try:
            # Process the message
            response = chatbot.process_message(query)
            
            print(f"Intent: {response['intent']} (confidence: {response.get('confidence', 0):.2f})")
            print(f"Response Style: {response.get('context', {}).get('formality', 'casual')}")
            print(f"Success: {response['success']}")
            
            if response.get('entities'):
                print(f"Entities: {response['entities']}")
            
            print(f"Response:")
            print(response['message'])
            
            if response.get('suggestions'):
                print(f"Suggestions: {', '.join(response['suggestions'][:3])}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()
    
    print("✅ Test completed!")
    print("\n🎯 Key Improvements:")
    print("• Natural language understanding")
    print("• Context-aware responses")
    print("• Multiple response styles (casual, formal, urgent)")
    print("• Better entity extraction")
    print("• Fuzzy product matching")
    print("• Conversational personality")

if __name__ == "__main__":
    test_layman_queries()
