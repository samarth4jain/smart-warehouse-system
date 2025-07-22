#!/usr/bin/env python3
"""
Debug script to test individual queries and their intent classification
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import get_db
from backend.app.services.enhanced_rag_service import EnhancedWarehouseRAGService

def test_individual_queries():
    """Test specific queries for debugging"""
    
    db = next(get_db())
    rag_service = EnhancedWarehouseRAGService(db)
    
    test_queries = [
        "Set TOOL001 stock to 100",
        "Show me stock levels for all electronics",
        "What products are low on stock?",
        "Show me stock alerts",
        "How many wireless headphones do we have?",
        "Show me all products in Electronics category",
        "How do I check inventory?"
    ]
    
    print("🔍 Individual Query Intent Classification Debug")
    print("=" * 70)
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        intent, entities = rag_service._classify_intent(query)
        print(f"🎯 Intent: {intent}")
        print(f"📊 Entities: {entities}")
        
        # Test the actual processing
        result = rag_service.process_natural_language_query(query)
        print(f"✅ Success: {result.get('success', False)}")
        print(f"🔄 Action: {result.get('action', 'unknown')}")
        if not result.get('success'):
            print(f"❌ Error: {result.get('error', 'No error message')}")

if __name__ == "__main__":
    test_individual_queries()
