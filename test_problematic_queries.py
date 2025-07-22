#!/usr/bin/env python3
"""
Test specific problematic queries
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import get_db
from backend.app.services.enhanced_rag_service import EnhancedWarehouseRAGService

def test_problematic_queries():
    """Test the specific queries that were failing"""
    
    db = next(get_db())
    rag_service = EnhancedWarehouseRAGService(db)
    
    test_queries = [
        "Add new product with SKU TEST001",
        "Delete product COMP005",
        "How many wireless headphones do we have?"
    ]
    
    print("🔍 Testing Problematic Queries")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        intent, entities = rag_service._classify_intent(query)
        print(f"🎯 Intent: {intent}")
        print(f"📊 Entities: {entities}")

if __name__ == "__main__":
    test_problematic_queries()
