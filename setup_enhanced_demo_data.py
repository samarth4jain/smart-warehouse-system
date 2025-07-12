#!/usr/bin/env python3
"""
Enhanced Demo Data Setup for Smart Warehouse Analytics
Creates comprehensive sample data to showcase all enhanced analytics features
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime, timedelta
import random

try:
    from faker import Faker
    fake = Faker()
except ImportError:
    print("Installing faker package...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
    from faker import Faker
    fake = Faker()

try:
    from sqlalchemy.orm import sessionmaker
    from backend.app.database import engine
    from backend.app.models.database_models import (
        Product, Inventory, InboundShipment, OutboundOrder, 
        StockMovement, ChatMessage, DemandForecast, ProductVelocity, StockAlert
    )
except ImportError as e:
    print(f"Database import error: {e}")
    print("Please ensure the backend is properly set up")
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_enhanced_demo_data():
    """Set up comprehensive demo data for enhanced analytics"""
    print("🚀 Setting up Enhanced Demo Data for Smart Warehouse Analytics...")
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        for model in [StockAlert, DemandForecast, ProductVelocity, ChatMessage, 
                      StockMovement, OutboundOrder, InboundShipment, Inventory, Product]:
            try:
                db.query(model).delete()
            except:
                pass
        db.commit()
        
        # Create diverse product categories
        product_categories = [
            ("Electronics", ["Laptops", "Smartphones", "Tablets", "Headphones", "Monitors"]),
            ("Clothing", ["Shirts", "Jeans", "Jackets", "Shoes", "Accessories"]),
            ("Home & Garden", ["Furniture", "Appliances", "Decor", "Tools", "Plants"]),
            ("Sports", ["Equipment", "Apparel", "Footwear", "Supplements", "Gear"]),
            ("Books", ["Fiction", "Non-fiction", "Textbooks", "Magazines", "eBooks"])
        ]
        
        products = []
        print("Creating diverse product catalog...")
        
        for category, subcategories in product_categories:
            for subcategory in subcategories:
                for i in range(random.randint(8, 15)):
                    product = Product(
                        sku=f"{category[:3].upper()}-{subcategory[:3].upper()}-{i+1:03d}",
                        name=f"{subcategory} {fake.word().title()} {fake.word().title()}",
                        description=f"High-quality {subcategory.lower()} with advanced features. Premium product line.",
                        category=category,
                        unit_price=round(random.uniform(10, 2000), 2),
                        weight=round(random.uniform(0.1, 50), 2),
                        dimensions=f"{random.randint(10,100)}x{random.randint(10,100)}x{random.randint(5,50)}cm",
                        supplier=fake.company(),
                        reorder_level=random.randint(10, 100),
                        max_stock_level=random.randint(200, 1000)
                    )
                    products.append(product)
                    db.add(product)
        
        db.commit()
        print(f"✅ Created {len(products)} diverse products")
        
        # Create realistic inventory with varying levels
        print("Setting up realistic inventory levels...")
        for product in products:
            # Create varied inventory levels based on product velocity
            velocity = random.choice(['fast', 'medium', 'slow'])
            
            if velocity == 'fast':
                quantity = random.randint(50, 500)
                location_count = random.randint(3, 8)
            elif velocity == 'medium':
                quantity = random.randint(20, 200)
                location_count = random.randint(2, 5)
            else:  # slow
                quantity = random.randint(5, 100)
                location_count = random.randint(1, 3)
            
            # Create inventory entries across multiple locations
            for i in range(location_count):
                location_qty = quantity // location_count + random.randint(-10, 10)
                location_qty = max(0, location_qty)
                
                inventory = Inventory(
                    product_id=product.id,
                    location=f"Zone-{random.choice(['A', 'B', 'C', 'D'])}-{i+1:02d}",
                    quantity=location_qty,
                    available_quantity=location_qty - random.randint(0, min(5, location_qty)),
                    reserved_quantity=random.randint(0, min(10, location_qty))
                )
                db.add(inventory)
        
        db.commit()
        print("✅ Created realistic inventory distribution")
        
        # Generate historical stock movements
        print("Generating comprehensive movement history...")
        for _ in range(1000):  # Large dataset for analytics
            product = random.choice(products)
            movement_type = random.choice(['inbound', 'outbound', 'adjustment', 'transfer'])
            
            # Create realistic quantities based on movement type
            if movement_type == 'inbound':
                quantity = random.randint(20, 200)
            elif movement_type == 'outbound':
                quantity = -random.randint(1, 50)
            elif movement_type == 'adjustment':
                quantity = random.randint(-20, 20)
            else:  # transfer
                quantity = random.randint(-30, 30)
            
            movement = StockMovement(
                product_id=product.id,
                movement_type=movement_type,
                quantity=quantity,
                location=f"Zone-{random.choice(['A', 'B', 'C', 'D'])}-{random.randint(1, 10):02d}",
                reference_number=f"MOV-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                notes=f"Automated {movement_type} - System processed",
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 90))
            )
            db.add(movement)
        
        db.commit()
        print("✅ Generated comprehensive movement history")
        
        # Create diverse inbound shipments
        print("Creating inbound shipment records...")
        for _ in range(100):
            shipment = InboundShipment(
                shipment_number=f"IB-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(100, 999)}",
                supplier=fake.company(),
                expected_date=datetime.utcnow() + timedelta(days=random.randint(1, 30)),
                received_date=datetime.utcnow() - timedelta(days=random.randint(1, 60)) if random.choice([True, False]) else None,
                status=random.choice(['pending', 'in_transit', 'received', 'processing']),
                total_items=random.randint(10, 500),
                notes=f"Shipment from supplier - Standard delivery"
            )
            db.add(shipment)
        
        db.commit()
        print("✅ Created inbound shipment records")
        
        # Create diverse outbound orders
        print("Creating outbound order records...")
        for _ in range(200):
            order = OutboundOrder(
                order_number=f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                customer_name=fake.name(),
                customer_address=f"{fake.street_address()}, {fake.city()}, {fake.state()}",
                order_date=datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                required_date=datetime.utcnow() + timedelta(days=random.randint(1, 14)),
                status=random.choice(['pending', 'picking', 'packed', 'shipped', 'delivered']),
                priority=random.choice(['low', 'medium', 'high', 'urgent']),
                total_items=random.randint(1, 20),
                total_value=round(random.uniform(50, 5000), 2),
                shipping_method=random.choice(['standard', 'express', 'overnight', 'ground']),
                notes=f"Customer order - Priority processing"
            )
            db.add(order)
        
        db.commit()
        print("✅ Created outbound order records")
        
        # Generate intelligent chatbot conversations
        print("Creating AI chatbot interaction history...")
        chat_topics = [
            ("inventory", ["Check stock levels", "Where is product located", "Low stock alerts"]),
            ("orders", ["Order status inquiry", "Shipping tracking", "Order modification"]),
            ("analytics", ["Performance metrics", "Demand forecasting", "Efficiency reports"]),
            ("operations", ["Process optimization", "Workflow assistance", "System guidance"])
        ]
        
        for _ in range(300):
            topic, questions = random.choice(chat_topics)
            question = random.choice(questions)
            session_id = f"session_{random.randint(1000, 9999)}"
            
            # User message
            user_msg = ChatMessage(
                message=f"{question} for warehouse operations",
                sender="user",
                message_type="question",
                session_id=session_id,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(user_msg)
            
            # AI response
            ai_responses = {
                "inventory": "Based on current stock levels and analytics, here's the information you requested...",
                "orders": "I've checked the order status and shipping details for you...",
                "analytics": "Here are the latest performance metrics and insights...",
                "operations": "I can help optimize this process. Here's my recommendation..."
            }
            
            ai_msg = ChatMessage(
                message=f"{ai_responses[topic]} System analysis shows optimal performance levels.",
                sender="assistant",
                message_type="response",
                session_id=session_id,
                created_at=user_msg.created_at + timedelta(seconds=random.randint(5, 30))
            )
            db.add(ai_msg)
        
        db.commit()
        print("✅ Created AI chatbot interaction history")
        
        # Summary statistics
        total_products = db.query(Product).count()
        total_movements = db.query(StockMovement).count()
        total_orders = db.query(OutboundOrder).count()
        total_chats = db.query(ChatMessage).count()
        
        print("\n🎉 Enhanced Demo Data Setup Complete!")
        print("=" * 50)
        print(f"📦 Products Created: {total_products}")
        print(f"📊 Stock Movements: {total_movements}")
        print(f"📋 Orders Created: {total_orders}")
        print(f"🤖 Chat Messages: {total_chats}")
        print("=" * 50)
        print("\n🚀 Enhanced Analytics Features Available:")
        print("   • Executive Summary Dashboard")
        print("   • Advanced ROI Analysis")
        print("   • Risk Assessment & Mitigation")
        print("   • AI-Powered Forecasting")
        print("   • Optimization Recommendations")
        print("   • Smart Alerts & Monitoring")
        print("   • Performance Insights")
        print("\n✨ Ready for enterprise-grade demonstrations!")
        
    except Exception as e:
        print(f"❌ Error setting up demo data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    setup_enhanced_demo_data()"
