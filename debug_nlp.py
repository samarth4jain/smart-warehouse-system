#!/usr/bin/env python3
"""
Quick debug test for NLP intent classification
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.enhanced_nlp_processor import EnhancedNLPProcessor

def test_intent_classification():
    """Test specific intent classification"""
    nlp = EnhancedNLPProcessor()
    
    test_queries = [
        "show low stock",
        "low stock alerts", 
        "what items are running low",
        "any low stock items",
        "show me monitors",
        "check bluetooth headphones",
        "Monitor 24-inch",
        "show all products",
        "inventory status"
    ]
    
    print("🔍 Testing Intent Classification")
    print("=" * 50)
    
    for query in test_queries:
        result = nlp.process_layman_query(query)
        print(f"Query: '{query}'")
        print(f"  Intent: {result.get('intent', 'None')} (confidence: {result.get('confidence', 0):.2f})")
        print(f"  Entities: {result.get('entities', {})}")
        print()

if __name__ == "__main__":
    test_intent_classification()
