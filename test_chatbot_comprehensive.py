#!/usr/bin/env python3
"""
Comprehensive Chatbot Testing Script
Tests all types of sample queries and saves results to file
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
SESSION_ID = f"test_session_{int(time.time())}"
OUTPUT_FILE = "chatbot_test_results.json"
OUTPUT_MD_FILE = "chatbot_test_results.md"

def test_chatbot_query(query, description="", expected_intent=None):
    """Test a single chatbot query and return results"""
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json={
                "message": query,
                "session_id": SESSION_ID,
                "user_id": "test_user"
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  # in milliseconds
        
        if response.status_code == 200:
            data = response.json()
            
            result = {
                "query": query,
                "description": description,
                "success": True,
                "response_time_ms": response_time,
                "intent": data.get("intent", "unknown"),
                "confidence": data.get("confidence", 0),
                "success_status": data.get("success", False),
                "enhanced_mode": data.get("enhanced_mode", False),
                "message": data.get("message", ""),
                "entities": data.get("entities", {}),
                "data": data.get("data", {}),
                "suggestions": data.get("suggestions", []),
                "actions": data.get("actions", {}),
                "timestamp": data.get("timestamp", ""),
                "expected_intent": expected_intent,
                "intent_match": expected_intent is None or data.get("intent") == expected_intent
            }
            
            print(f"✅ Query: '{query[:50]}...' - Intent: {result['intent']} - Time: {response_time}ms")
            return result
            
        else:
            result = {
                "query": query,
                "description": description,
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "response_time_ms": response_time
            }
            print(f"❌ Query: '{query[:50]}...' - Error: {response.status_code}")
            return result
            
    except Exception as e:
        result = {
            "query": query,
            "description": description,
            "success": False,
            "error": str(e),
            "response_time_ms": 0
        }
        print(f"❌ Query: '{query[:50]}...' - Exception: {str(e)}")
        return result

def run_comprehensive_tests():
    """Run comprehensive chatbot tests"""
    print("🧪 Starting Comprehensive Chatbot Testing")
    print("=" * 60)
    
    # Define test categories and queries
    test_categories = [
        {
            "category": "Basic Greetings & Conversation",
            "queries": [
                ("hello", "Basic greeting"),
                ("hi there", "Casual greeting"),
                ("good morning", "Time-specific greeting"),
                ("hey", "Very casual greeting"),
                ("hi", "Simple greeting"),
                ("good afternoon", "Afternoon greeting"),
                ("what's up?", "Slang greeting"),
                ("how are you?", "Personal inquiry"),
                ("thanks", "Gratitude expression"),
                ("thank you", "Formal thanks"),
                ("bye", "Farewell"),
                ("goodbye", "Formal farewell"),
                ("see you later", "Casual farewell")
            ]
        },
        {
            "category": "Inventory Management Queries",
            "queries": [
                ("show low stock", "Direct low stock query", "alerts_monitoring"),
                ("check inventory", "General inventory check", "inventory_check"),
                ("what's in stock?", "Casual stock inquiry", "inventory_check"),
                ("show me all products", "Product listing request", "inventory_check"),
                ("check stock levels", "Stock level inquiry", "inventory_check"),
                ("what products do we have?", "Product catalog request", "inventory_check"),
                ("show inventory summary", "Inventory overview", "inventory_check"),
                ("check warehouse inventory", "Warehouse inventory check", "inventory_check"),
                ("what items are available?", "Availability inquiry", "inventory_check"),
                ("display current stock", "Stock display request", "inventory_check")
            ]
        },
        {
            "category": "Product Search Queries",
            "queries": [
                ("check bluetooth headphones", "Specific product search", "inventory_check"),
                ("find wireless mouse", "Product search with 'find'", "inventory_check"),
                ("look for laptop", "Product search with 'look for'", "inventory_check"),
                ("search for keyboard", "Product search with 'search'", "inventory_check"),
                ("do we have monitors?", "Casual product inquiry", "inventory_check"),
                ("check office chair", "Office furniture search", "inventory_check"),
                ("where is the laptop?", "Product location inquiry", "inventory_check"),
                ("show me wireless mouse details", "Detailed product info", "inventory_check"),
                ("what about bluetooth devices?", "Category search", "inventory_check"),
                ("check electronic items", "Category-based search", "inventory_check")
            ]
        },
        {
            "category": "Natural Language Alert Queries",
            "queries": [
                ("what items are running low?", "Natural language low stock", "alerts_monitoring"),
                ("what needs attention?", "General attention query", "alerts_monitoring"),
                ("any items need reordering?", "Reorder inquiry", "alerts_monitoring"),
                ("show me problem areas", "Problem identification", "alerts_monitoring"),
                ("what's critically low?", "Critical stock inquiry", "alerts_monitoring"),
                ("are we running out of anything?", "Stock depletion check", "alerts_monitoring"),
                ("what should I be worried about?", "Concern-based query", "alerts_monitoring"),
                ("which products need attention?", "Product attention query", "alerts_monitoring"),
                ("any red flags in inventory?", "Alert metaphor query", "alerts_monitoring"),
                ("what items are in trouble?", "Trouble identification", "alerts_monitoring")
            ]
        },
        {
            "category": "Casual & Conversational Queries",
            "queries": [
                ("do we have any laptops?", "Casual availability check", "inventory_check"),
                ("got any wireless mice?", "Slang availability check", "inventory_check"),
                ("how many keyboards are there?", "Quantity inquiry", "inventory_check"),
                ("are there enough office chairs?", "Sufficiency inquiry", "inventory_check"),
                ("do we still have bluetooth headphones?", "Continuing availability", "inventory_check"),
                ("is there any laptop left?", "Remaining stock inquiry", "inventory_check"),
                ("how much stuff do we have?", "General quantity inquiry", "inventory_check"),
                ("what's the deal with monitors?", "Casual status inquiry", "inventory_check"),
                ("tell me about our mouse inventory", "Narrative inquiry", "inventory_check"),
                ("give me the lowdown on headphones", "Informal information request", "inventory_check")
            ]
        },
        {
            "category": "SKU & Code-based Queries",
            "queries": [
                ("check SKU LAPTOP001", "Direct SKU query", "inventory_check"),
                ("show me MOUSE001", "SKU display request", "inventory_check"),
                ("what's the status of HEAD001?", "SKU status inquiry", "inventory_check"),
                ("look up product CHAIR001", "SKU lookup", "inventory_check"),
                ("check stock for LAPTOP001", "SKU stock check", "inventory_check"),
                ("show details for MOUSE001", "SKU details request", "inventory_check"),
                ("find product with code HEAD001", "Code-based search", "inventory_check"),
                ("check item CHAIR001", "Item code check", "inventory_check"),
                ("what about SKU LAPTOP001?", "Casual SKU inquiry", "inventory_check"),
                ("tell me about product MOUSE001", "Narrative SKU request", "inventory_check")
            ]
        },
        {
            "category": "Analytics & Reporting Queries",
            "queries": [
                ("show me warehouse status", "Warehouse overview", "reporting_analytics"),
                ("generate inventory report", "Report generation", "reporting_analytics"),
                ("what's our warehouse performance?", "Performance inquiry", "reporting_analytics"),
                ("show me the analytics", "Analytics request", "reporting_analytics"),
                ("give me a summary", "Summary request", "reporting_analytics"),
                ("how are we doing today?", "Performance check", "reporting_analytics"),
                ("show dashboard", "Dashboard request", "reporting_analytics"),
                ("what are the metrics?", "Metrics inquiry", "reporting_analytics"),
                ("display warehouse overview", "Overview request", "reporting_analytics"),
                ("show me key statistics", "Statistics request", "reporting_analytics")
            ]
        },
        {
            "category": "Operations & Status Queries",
            "queries": [
                ("how are operations today?", "Daily operations check", "reporting_analytics"),
                ("what's happening in the warehouse?", "Activity inquiry", "reporting_analytics"),
                ("show me today's activities", "Daily activity request", "reporting_analytics"),
                ("any deliveries today?", "Delivery inquiry", "operations_check"),
                ("what's the warehouse status?", "Status inquiry", "reporting_analytics"),
                ("how is everything running?", "General operations check", "reporting_analytics"),
                ("show me current operations", "Operations overview", "reporting_analytics"),
                ("what's going on today?", "Activity summary", "reporting_analytics"),
                ("any issues with operations?", "Issue identification", "reporting_analytics"),
                ("how smooth are operations?", "Operations quality check", "reporting_analytics")
            ]
        },
        {
            "category": "Help & Support Queries",
            "queries": [
                ("help", "Basic help request"),
                ("what can you do?", "Capability inquiry"),
                ("how do I use this?", "Usage inquiry"),
                ("what features are available?", "Feature inquiry"),
                ("can you help me?", "Help request"),
                ("what commands work?", "Command inquiry"),
                ("show me examples", "Example request"),
                ("how does this work?", "Functionality inquiry"),
                ("what are your capabilities?", "Capability question"),
                ("guide me", "Guidance request"),
                ("I need assistance", "Assistance request"),
                ("what can I ask you?", "Query scope inquiry"),
                ("show me what you can do", "Demonstration request")
            ]
        },
        {
            "category": "Edge Cases & Error Handling",
            "queries": [
                ("", "Empty query"),
                ("check nonexistent product", "Non-existent product"),
                ("find product XYZ123", "Invalid product code"),
                ("show me unicorns", "Nonsense product"),
                ("asdfghjkl", "Random characters"),
                ("check product with very long name that doesn't exist", "Long non-existent product"),
                ("find something", "Vague request"),
                ("show me everything about nothing", "Contradictory request"),
                ("check inventory for mars rovers", "Impossible product"),
                ("123456789", "Numbers only"),
                ("!@#$%^&*()", "Special characters only"),
                ("find . . . .", "Dots only")
            ]
        },
        {
            "category": "Complex & Multi-intent Queries",
            "queries": [
                ("show me low stock items and generate a report", "Multi-intent query"),
                ("check bluetooth headphones and tell me if we need more", "Complex inquiry"),
                ("what items are low and how can I fix it?", "Problem + solution query"),
                ("show warehouse status and highlight problems", "Status + analysis"),
                ("find all electronics and check their stock levels", "Category + analysis"),
                ("tell me about inventory and suggest improvements", "Info + recommendation"),
                ("check all products that need attention today", "Time-bound complex query"),
                ("show me everything that's wrong with our inventory", "Comprehensive problem query"),
                ("analyze our stock and tell me what to do", "Analysis + action request"),
                ("give me a complete picture of warehouse operations", "Comprehensive overview")
            ]
        }
    ]
    
    all_results = []
    category_stats = {}
    
    for category_info in test_categories:
        category = category_info["category"]
        queries = category_info["queries"]
        
        print(f"\n📂 Testing Category: {category}")
        print("-" * 50)
        
        category_results = []
        category_stats[category] = {
            "total": len(queries),
            "successful": 0,
            "failed": 0,
            "avg_response_time": 0
        }
        
        for query_info in queries:
            if len(query_info) == 3:
                query, description, expected_intent = query_info
            else:
                query, description = query_info
                expected_intent = None
            
            result = test_chatbot_query(query, description, expected_intent)
            result["category"] = category
            
            category_results.append(result)
            all_results.append(result)
            
            if result["success"]:
                category_stats[category]["successful"] += 1
            else:
                category_stats[category]["failed"] += 1
            
            # Small delay between requests
            time.sleep(0.1)
        
        # Calculate average response time for category
        successful_times = [r["response_time_ms"] for r in category_results if r["success"]]
        if successful_times:
            category_stats[category]["avg_response_time"] = round(sum(successful_times) / len(successful_times), 2)
    
    return all_results, category_stats

def save_results_json(results, filename):
    """Save results to JSON file"""
    output_data = {
        "test_metadata": {
            "timestamp": datetime.now().isoformat(),
            "session_id": SESSION_ID,
            "base_url": BASE_URL,
            "total_queries": len(results)
        },
        "results": results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Results saved to {filename}")

def save_results_markdown(results, stats, filename):
    """Save results to Markdown file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Comprehensive Chatbot Testing Results\n\n")
        f.write(f"**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Session ID:** {SESSION_ID}\n")
        f.write(f"**Base URL:** {BASE_URL}\n")
        f.write(f"**Total Queries Tested:** {len(results)}\n\n")
        
        # Overall statistics
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful
        avg_time = round(sum(r.get("response_time_ms", 0) for r in results if r["success"]) / max(successful, 1), 2)
        
        f.write("## 📊 Overall Statistics\n\n")
        f.write(f"- **Total Queries:** {len(results)}\n")
        f.write(f"- **Successful:** {successful} ({round(successful/len(results)*100, 1)}%)\n")
        f.write(f"- **Failed:** {failed} ({round(failed/len(results)*100, 1)}%)\n")
        f.write(f"- **Average Response Time:** {avg_time} ms\n\n")
        
        # Category statistics
        f.write("## 📂 Category Statistics\n\n")
        for category, stat in stats.items():
            success_rate = round(stat["successful"] / stat["total"] * 100, 1)
            f.write(f"### {category}\n")
            f.write(f"- **Total:** {stat['total']}\n")
            f.write(f"- **Successful:** {stat['successful']} ({success_rate}%)\n")
            f.write(f"- **Failed:** {stat['failed']}\n")
            f.write(f"- **Avg Response Time:** {stat['avg_response_time']} ms\n\n")
        
        # Detailed results by category
        f.write("## 📝 Detailed Test Results\n\n")
        
        current_category = None
        for result in results:
            if result.get("category") != current_category:
                current_category = result.get("category")
                f.write(f"### {current_category}\n\n")
            
            # Query header
            status_emoji = "✅" if result["success"] else "❌"
            f.write(f"{status_emoji} **Query:** `{result['query']}`\n")
            
            if result.get("description"):
                f.write(f"**Description:** {result['description']}\n")
            
            if result["success"]:
                f.write(f"**Intent:** {result.get('intent', 'unknown')}\n")
                f.write(f"**Confidence:** {result.get('confidence', 0)}\n")
                f.write(f"**Response Time:** {result.get('response_time_ms', 0)} ms\n")
                f.write(f"**Enhanced Mode:** {result.get('enhanced_mode', False)}\n")
                f.write(f"**Success Status:** {result.get('success_status', False)}\n")
                
                if result.get("expected_intent"):
                    match = "✅" if result.get("intent_match") else "❌"
                    f.write(f"**Intent Match:** {match} (Expected: {result['expected_intent']})\n")
                
                # Response preview
                message = result.get("message", "")
                if message:
                    preview = message.replace('\n', ' ')[:200]
                    if len(message) > 200:
                        preview += "..."
                    f.write(f"**Response:** {preview}\n")
                
                # Data summary
                if result.get("data"):
                    f.write(f"**Data Available:** Yes\n")
                
                # Suggestions
                suggestions = result.get("suggestions", [])
                if suggestions:
                    f.write(f"**Suggestions:** {', '.join(suggestions[:3])}\n")
            else:
                f.write(f"**Error:** {result.get('error', 'Unknown error')}\n")
            
            f.write("\n---\n\n")
    
    print(f"✅ Markdown report saved to {filename}")

def main():
    """Main function to run comprehensive chatbot tests"""
    print("🚀 Starting Comprehensive Chatbot Testing Suite")
    print("This will test all types of queries and save results to files")
    print("=" * 70)
    
    try:
        # Run tests
        results, stats = run_comprehensive_tests()
        
        # Save results
        print(f"\n💾 Saving results...")
        save_results_json(results, OUTPUT_FILE)
        save_results_markdown(results, stats, OUTPUT_MD_FILE)
        
        # Print summary
        successful = sum(1 for r in results if r["success"])
        print(f"\n🎯 Test Summary:")
        print(f"Total queries tested: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {len(results) - successful}")
        print(f"Success rate: {round(successful/len(results)*100, 1)}%")
        
        print(f"\n📁 Files created:")
        print(f"- {OUTPUT_FILE} (JSON format)")
        print(f"- {OUTPUT_MD_FILE} (Markdown format)")
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")

if __name__ == "__main__":
    main()
