#!/usr/bin/env python3
"""
Test regex patterns for set stock commands
"""
import re

def test_set_stock_patterns():
    query = "Set TOOL001 stock to 100"
    query_lower = query.lower()
    
    print(f"Testing query: '{query}'")
    print(f"Query lower: '{query_lower}'")
    
    # Test the current patterns
    set_stock_patterns = [
        r'set\s+(\w+\d+|\w+)\s+stock\s+to\s+(\d+)', 
        r'update\s+(\w+\d+|\w+)\s+stock\s+to\s+(\d+)', 
        r'change\s+(\w+\d+|\w+)\s+stock\s+to\s+(\d+)'
    ]
    
    for i, pattern in enumerate(set_stock_patterns):
        print(f"\nPattern {i+1}: {pattern}")
        match = re.search(pattern, query_lower)
        if match:
            print(f"✅ Match found: {match.groups()}")
        else:
            print("❌ No match")
    
    # Test current SKU extraction pattern
    sku_pattern = r'\b([A-Z]{2,4}\d{3,4})\b'
    print(f"\nSKU pattern: {sku_pattern}")
    sku_match = re.search(sku_pattern, query, re.IGNORECASE)
    if sku_match:
        print(f"✅ SKU match: {sku_match.group(1)}")
    else:
        print("❌ No SKU match")

if __name__ == "__main__":
    test_set_stock_patterns()
