#!/usr/bin/env python3
"""
Smart Warehouse RAG Demo - Natural Language Database Operations
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.orm import sessionmaker
from backend.app.database import engine
from backend.app.services.enhanced_chatbot_service import EnhancedChatbotService

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def interactive_demo():
    """Interactive demo of natural language database operations"""
    
    print("🏭 Smart Warehouse Management System")
    print("💬 Natural Language Database Interface")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Initialize chatbot
        print("🚀 Initializing AI Assistant...")
        chatbot = EnhancedChatbotService(db)
        print("✅ Ready! You can now use natural language to interact with the warehouse database.\n")
        
        # Show sample commands
        print("💡 **Sample Commands:**")
        print("   📊 'What is the stock level of ELEC001?'")
        print("   ➕ 'Add 50 units to COMP001'")
        print("   ➖ 'Remove 10 units from TOOL001'")
        print("   📋 'Show me low stock alerts'")
        print("   🏷️ 'List all electronics products'")
        print("   📈 'Generate demand forecast'")
        print("   🗑️ 'Delete product TEST001'")
        print("   🔍 'Show me all stock alerts'")
        print("   📦 'What products are in Tools category?'")
        print("   🎯 'Set ELEC002 stock to 100'")
        print()
        print("Type 'quit' or 'exit' to end the session.")
        print("-" * 60)
        
        session_id = "demo_session"
        
        while True:
            try:
                # Get user input
                user_input = input("\n🗣️  You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("👋 Thank you for using Smart Warehouse System!")
                    break
                
                if not user_input:
                    continue
                
                # Process the query
                print("🤔 Processing...")
                response = chatbot.process_message(user_input, session_id=session_id, user_id="demo_user")
                
                # Display response
                print(f"\n🤖 Assistant: {response.get('message', 'No response generated')}")
                
                # Show additional info if available
                if response.get('intent'):
                    print(f"🎯 Intent: {response['intent']}")
                
                if response.get('action_taken'):
                    print(f"⚡ Action: {response['action_taken']}")
                
                if not response.get('success', True):
                    print(f"⚠️  Status: Operation encountered issues")
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                continue
        
    except Exception as e:
        print(f"❌ Failed to initialize system: {str(e)}")
        return False
    
    finally:
        db.close()
    
    return True

def quick_demo():
    """Quick demonstration with pre-defined queries"""
    
    print("🏭 Smart Warehouse System - Quick Demo")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Initialize chatbot
        print("🚀 Initializing system...")
        chatbot = EnhancedChatbotService(db)
        print("✅ System ready!\n")
        
        # Demo queries
        demo_queries = [
            "What is the stock level of ELEC001?",
            "Show me low stock alerts",
            "Add 25 units to COMP001", 
            "List electronics products",
            "Generate demand forecast",
            "What stock alerts do we have?"
        ]
        
        print("🎬 Running Quick Demo with Sample Queries...")
        print("-" * 50)
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n📝 Query {i}: {query}")
            print("-" * 30)
            
            try:
                response = chatbot.process_message(query, session_id="quick_demo", user_id="demo")
                
                # Clean response for display
                message = response.get('message', 'No response')
                if len(message) > 200:
                    message = message[:200] + "..."
                
                print(f"🤖 Response: {message}")
                print(f"🎯 Intent: {response.get('intent', 'unknown')}")
                print(f"✅ Success: {response.get('success', False)}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print(f"\n🎉 Quick demo completed!")
        print(f"💡 The system can handle natural language queries for:")
        print(f"   - Stock checking and inventory queries")
        print(f"   - Adding, removing, and updating stock levels")
        print(f"   - Product management (create/delete)")
        print(f"   - Low stock alerts and notifications")
        print(f"   - Demand forecasting and analytics")
        print(f"   - Category-based product searches")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    print("🏭 Smart Warehouse Natural Language Database Interface")
    print("Choose demo mode:")
    print("1. Interactive Demo (type your own queries)")
    print("2. Quick Demo (pre-defined queries)")
    print("3. Exit")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            interactive_demo()
        elif choice == "2":
            quick_demo()
        elif choice == "3":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice. Running quick demo...")
            quick_demo()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
