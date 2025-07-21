#!/usr/bin/env python3
"""
Test Enhanced RAG Natural Language Database Operations
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.orm import sessionmaker
from backend.app.database import engine
from backend.app.services.enhanced_rag_service import EnhancedWarehouseRAGService
from backend.app.services.enhanced_chatbot_service import EnhancedChatbotService

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_natural_language_operations():
    """Test various natural language operations"""
    
    print("🧪 Testing Enhanced RAG Natural Language Database Operations")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # Initialize services
        print("🚀 Initializing Enhanced RAG Service...")
        rag_service = EnhancedWarehouseRAGService(db)
        chatbot_service = EnhancedChatbotService(db)
        
        # Test queries
        test_queries = [
            # Stock checking
            "What is the current stock level of ELEC001?",
            "Show me stock levels for all electronics",
            "How many wireless headphones do we have?",
            
            # Stock modifications
            "Add 50 units to ELEC001",
            "Remove 10 units from COMP001",
            "Set TOOL001 stock to 100",
            
            # Product searches
            "Show me all products in Electronics category",
            "What products are low on stock?",
            "List all tools in the warehouse",
            
            # Advanced operations
            "Generate demand forecast",
            "Show me stock alerts",
            "Optimize warehouse layout",
            
            # Product management
            "Add new product with SKU TEST001",
            "Delete product COMP005",
            
            # General queries
            "What's the warehouse layout like?",
            "How do I check inventory?"
        ]
        
        print(f"\n📝 Testing {len(test_queries)} Natural Language Queries...")
        print("-" * 70)
        
        results = []
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i:2d}: {query}")
            print("-" * 50)
            
            try:
                # Test with RAG service directly
                rag_result = rag_service.process_natural_language_query(query, user_id=1)
                
                # Test with chatbot service
                chat_result = chatbot_service.process_message(query, session_id="test_session", user_id="1")
                
                # Display results
                print(f"✅ Intent: {rag_result.get('intent', 'unknown')}")
                print(f"🎯 Action: {rag_result.get('action', 'none')}")
                print(f"✨ Success: {rag_result.get('success', False)}")
                
                if rag_result.get('success'):
                    print(f"📋 Message: {rag_result.get('message', 'No message')[:100]}...")
                    if rag_result.get('data'):
                        data = rag_result['data']
                        if isinstance(data, list):
                            print(f"📊 Data: {len(data)} items returned")
                        elif isinstance(data, dict):
                            print(f"📊 Data: {len(data)} fields returned")
                else:
                    print(f"❌ Error: {rag_result.get('error', 'Unknown error')}")
                
                # Chatbot formatted response
                print(f"🤖 Chatbot Response: {chat_result.get('message', 'No response')[:100]}...")
                
                results.append({
                    "query": query,
                    "intent": rag_result.get('intent'),
                    "success": rag_result.get('success', False),
                    "action": rag_result.get('action')
                })
                
            except Exception as e:
                print(f"❌ Error testing query: {str(e)}")
                results.append({
                    "query": query,
                    "intent": "error",
                    "success": False,
                    "error": str(e)
                })
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        success_rate = (successful / total) * 100 if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {total - successful}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Intent breakdown
        intents = {}
        for result in results:
            intent = result.get('intent', 'unknown')
            if intent not in intents:
                intents[intent] = {'total': 0, 'success': 0}
            intents[intent]['total'] += 1
            if result['success']:
                intents[intent]['success'] += 1
        
        print(f"\n📋 Intent Breakdown:")
        for intent, stats in intents.items():
            rate = (stats['success'] / stats['total']) * 100 if stats['total'] > 0 else 0
            print(f"  {intent}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
        
        # Test specific database operations
        print(f"\n🔬 Testing Database Operations...")
        print("-" * 50)
        
        # Test adding stock
        print("Testing: Add stock operation...")
        add_result = rag_service.process_natural_language_query("Add 25 units to ELEC002", user_id=1)
        print(f"Add Stock Result: {'✅ Success' if add_result.get('success') else '❌ Failed'}")
        
        # Test stock check
        print("Testing: Stock check after addition...")
        check_result = rag_service.process_natural_language_query("What is the stock level of ELEC002?", user_id=1)
        print(f"Stock Check Result: {'✅ Success' if check_result.get('success') else '❌ Failed'}")
        if check_result.get('success') and check_result.get('data'):
            data = check_result['data']
            print(f"Current Stock: {data.get('available', 'Unknown')} units")
        
        # Test removing stock
        print("Testing: Remove stock operation...")
        remove_result = rag_service.process_natural_language_query("Remove 5 units from ELEC002", user_id=1)
        print(f"Remove Stock Result: {'✅ Success' if remove_result.get('success') else '❌ Failed'}")
        
        print(f"\n🎉 Enhanced RAG System Test Complete!")
        print(f"📈 Overall Performance: {success_rate:.1f}% success rate")
        
        if success_rate >= 80:
            print("✅ EXCELLENT: System performing very well!")
        elif success_rate >= 60:
            print("✅ GOOD: System performing adequately")
        elif success_rate >= 40:
            print("⚠️ FAIR: System needs improvement") 
        else:
            print("❌ POOR: System requires significant fixes")
        
        return success_rate >= 60
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    success = test_natural_language_operations()
    if success:
        print("\n🎯 Enhanced RAG system is working correctly!")
        print("💬 You can now use natural language for:")
        print("   - Stock checking: 'What is the stock of ELEC001?'")
        print("   - Stock updates: 'Add 100 units to COMP001'")
        print("   - Data deletion: 'Delete product DISC001'")
        print("   - Analytics: 'Show low stock alerts'")
        print("   - Product search: 'List electronics products'")
    else:
        print("\n❌ Enhanced RAG system needs fixes")
        sys.exit(1)
