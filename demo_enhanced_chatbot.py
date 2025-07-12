#!/usr/bin/env python3
"""
Demo script showing enhanced layman language chatbot capabilities
"""

def demo_enhanced_chatbot():
    """
    Interactive demo of the enhanced chatbot features
    """
    print("🤖 Smart Warehouse Assistant - Enhanced Layman Language Demo")
    print("=" * 60)
    print("The chatbot now understands natural, casual language!")
    print("Try these example queries or type your own:\n")
    
    # Example queries to demonstrate
    examples = [
        {
            "category": "📦 Inventory Checks",
            "queries": [
                "Do we have any laptops?",
                "Got any blue widgets left?",
                "Is there inventory for chairs?",
                "Can you check if we have keyboards?",
                "Where are the red widgets?"
            ]
        },
        {
            "category": "📝 Stock Updates", 
            "queries": [
                "We just got 50 more mice",
                "Add 25 widgets to the system",
                "Actually we have 100 keyboards not 75",
                "Put 30 units in the system",
                "Fix the count for laptops"
            ]
        },
        {
            "category": "🚚 Operations",
            "queries": [
                "Truck just arrived!",
                "Customer wants their order ASAP",
                "Delivery is here for receiving",
                "Ship order ORD001 today",
                "Process the delivery"
            ]
        },
        {
            "category": "⚠️ Alerts & Monitoring",
            "queries": [
                "What needs attention?",
                "Any problems today?",
                "Is everything running smooth?",
                "Show me what's wrong",
                "What's running low?"
            ]
        },
        {
            "category": "💬 Conversation",
            "queries": [
                "Hi! Can you help me?",
                "What can you do?",
                "I'm confused about this",
                "Thanks for your help!",
                "How does this work?"
            ]
        }
    ]
    
    # Display examples
    for example in examples:
        print(f"\n{example['category']}:")
        for i, query in enumerate(example['queries'], 1):
            print(f"  {i}. \"{query}\"")
    
    print("\n" + "=" * 60)
    print("🎯 Key Features Demonstrated:")
    print("• Natural language understanding")
    print("• Casual conversation support")
    print("• Context-aware responses")
    print("• Multiple response styles (casual, formal, urgent)")
    print("• Smart entity extraction")
    print("• Fuzzy product matching")
    print("• No technical knowledge required!")
    
    print("\n💡 Usage Tips:")
    print("• Just talk naturally - no special commands needed")
    print("• The system understands casual language")
    print("• You can be specific or general")
    print("• Context matters - greetings, urgency, politeness")
    print("• Product names can be partial or fuzzy")
    
    print("\n🌐 Access the chatbot at: http://127.0.0.1:8000/chatbot")
    print("(Make sure the backend server is running)")
    
    return True

if __name__ == "__main__":
    demo_enhanced_chatbot()
