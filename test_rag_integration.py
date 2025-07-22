#!/usr/bin/env python3
"""
Test RAG Integration with ChatbotService
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.orm import sessionmaker
from backend.app.database import engine
from backend.app.services.chatbot_service import ChatbotService

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_rag_integration():
    """Test RAG integration in ChatbotService"""
    
    print("🧪 Testing RAG Integration with ChatbotService")
    print("=" * 60)
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Initialize the chatbot service
        print("\n1. Initializing ChatbotService...")
        chatbot = ChatbotService(db)
        
        # Check RAG status
        print(f"   RAG Service Available: {hasattr(chatbot, 'rag_service') and chatbot.rag_service is not None}")
        print(f"   RAG Enabled: {getattr(chatbot, 'rag_enabled', False)}")
        print(f"   Enhanced NLP Available: {hasattr(chatbot, 'enhanced_nlp_processor')}")
        
        # Test various queries
        test_queries = [
            "What's our current inventory status?",
            "How can I optimize storage space?",
            "What are the best practices for inventory management?",
            "Show me items with low stock levels",
            "Help me understand warehouse operations"
        ]
        
        print("\n2. Testing RAG-Enhanced Responses:")
        print("-" * 40)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Query {i}: {query}")
            
            try:
                response = chatbot.process_message(query)
                print(f"   Intent: {response.get('intent', 'unknown')}")
                print(f"   RAG Used: {response.get('rag_used', False)}")
                print(f"   Confidence: {response.get('confidence', 0):.2f}")
                print(f"   Response: {response.get('message', 'No response')[:100]}...")
                
            except Exception as e:
                print(f"   Error: {str(e)}")
        
        print("\n✅ RAG Integration Test Complete!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_rag_integration()
