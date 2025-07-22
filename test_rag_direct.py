#!/usr/bin/env python3
"""
Simple RAG Service Test
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.orm import sessionmaker
from backend.app.database import engine
from backend.app.services.enhanced_rag_service import EnhancedWarehouseRAGService

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_rag_directly():
    """Test RAG service directly"""
    
    print("🧪 Testing RAG Service Directly")
    print("=" * 40)
    
    db = SessionLocal()
    
    try:
        print("\n1. Initializing RAG Service...")
        rag_service = EnhancedWarehouseRAGService(db)
        print("   ✅ RAG Service initialized")
        
        print("\n2. Testing simple query...")
        try:
            result = rag_service.process_natural_language_query("What's our current inventory status?")
            print(f"   Result type: {type(result)}")
            print(f"   Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
            
            if isinstance(result, dict):
                print(f"   Message: {result.get('message', 'No message')[:100]}...")
                print(f"   Success: {result.get('success', 'Unknown')}")
                print(f"   Intent: {result.get('intent', 'Unknown')}")
            else:
                print(f"   Raw result: {str(result)[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n✅ Direct RAG test complete!")
        
    except Exception as e:
        print(f"❌ Error initializing RAG: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_rag_directly()
