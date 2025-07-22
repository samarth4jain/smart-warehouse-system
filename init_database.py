#!/usr/bin/env python3
"""
Initialize the Smart Warehouse System database with sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app.database import engine, Base, SessionLocal
from backend.app.models.database_models import (
    Product, Inventory, Vendor, Customer, InboundShipment, InboundItem, 
    OutboundOrder, OutboundItem, StockMovement, User, ChatSession, ChatMessage
)
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for the warehouse system"""
    
    # Create all tables first
    print("Creating database tables...")
    Base.metadata.drop_all(bind=engine)  # Drop all tables first
    Base.metadata.create_all(bind=engine)  # Recreate all tables
    
    db = SessionLocal()
    
    try:
        print("Creating sample data...")
        
        # Create sample vendors
        vendors = [
            Vendor(name="Tech Supplies Co.", contact_person="John Smith", phone="555-0101", email="john@techsupplies.com"),
            Vendor(name="Global Electronics", contact_person="Sarah Johnson", phone="555-0102", email="sarah@globalelec.com"),
            Vendor(name="Hardware Direct", contact_person="Mike Wilson", phone="555-0103", email="mike@hardwaredirect.com"),
        ]
        
        for vendor in vendors:
            db.add(vendor)
        db.commit()
        
        # Create sample customers
        customers = [
            Customer(name="ABC Corp", contact_person="Alice Brown", phone="555-0201", email="alice@abccorp.com"),
            Customer(name="XYZ Industries", contact_person="Bob Davis", phone="555-0202", email="bob@xyzind.com"),
            Customer(name="Tech Solutions Ltd", contact_person="Carol White", phone="555-0203", email="carol@techsol.com"),
        ]
        
        for customer in customers:
            db.add(customer)
        db.commit()
        
        # Create sample products
        products = [
            Product(sku="LAPTOP001", name="Business Laptop", description="High-performance business laptop", 
                   category="Electronics", unit="pcs", unit_price=1200.00, reorder_level=10, location="A1-01"),
            Product(sku="MOUSE001", name="Wireless Mouse", description="Ergonomic wireless mouse", 
                   category="Electronics", unit="pcs", unit_price=25.00, reorder_level=50, location="A1-02"),
            Product(sku="KEYBOARD001", name="Mechanical Keyboard", description="RGB mechanical gaming keyboard", 
                   category="Electronics", unit="pcs", unit_price=120.00, reorder_level=20, location="A1-03"),
            Product(sku="MONITOR001", name="4K Monitor", description="27-inch 4K UHD monitor", 
                   category="Electronics", unit="pcs", unit_price=350.00, reorder_level=15, location="A2-01"),
            Product(sku="CABLE001", name="USB-C Cable", description="High-speed USB-C charging cable", 
                   category="Accessories", unit="pcs", unit_price=15.00, reorder_level=100, location="A2-02"),
            Product(sku="HEADSET001", name="Noise-Cancelling Headset", description="Professional noise-cancelling headset", 
                   category="Electronics", unit="pcs", unit_price=200.00, reorder_level=25, location="A2-03"),
            Product(sku="TABLET001", name="Business Tablet", description="10-inch business tablet", 
                   category="Electronics", unit="pcs", unit_price=450.00, reorder_level=12, location="B1-01"),
            Product(sku="PRINTER001", name="Laser Printer", description="High-speed laser printer", 
                   category="Office Equipment", unit="pcs", unit_price=300.00, reorder_level=8, location="B1-02"),
            Product(sku="PHONE001", name="Smartphone", description="Latest model smartphone", 
                   category="Electronics", unit="pcs", unit_price=800.00, reorder_level=20, location="B1-03"),
            Product(sku="CHARGER001", name="Fast Charger", description="65W fast charging adapter", 
                   category="Accessories", unit="pcs", unit_price=35.00, reorder_level=75, location="B2-01"),
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        
        # Create inventory records
        for product in products:
            # Random inventory quantities
            base_quantity = random.randint(50, 500)
            reserved = random.randint(0, min(20, base_quantity // 4))
            
            inventory = Inventory(
                product_id=product.id,
                quantity=base_quantity,
                reserved_quantity=reserved,
                available_quantity=base_quantity - reserved
            )
            db.add(inventory)
        
        db.commit()
        
        # Create some inbound shipments
        for i in range(5):
            shipment = InboundShipment(
                shipment_number=f"INB-{2024}-{str(i+1).zfill(4)}",
                vendor_id=random.choice(vendors).id,
                expected_date=datetime.now() + timedelta(days=random.randint(1, 10)),
                status=random.choice(["pending", "arrived", "checked_in", "completed"]),
                driver_name=f"Driver {i+1}",
                vehicle_number=f"TRK-{random.randint(1000, 9999)}",
                notes=f"Sample shipment {i+1}"
            )
            db.add(shipment)
        
        db.commit()
        
        # Create some outbound orders
        for i in range(7):
            order = OutboundOrder(
                order_number=f"OUT-{2024}-{str(i+1).zfill(4)}",
                customer_id=random.choice(customers).id,
                order_date=datetime.now() - timedelta(days=random.randint(0, 30)),
                status=random.choice(["pending", "picking", "packed", "dispatched", "delivered"]),
                priority=random.choice(["low", "medium", "high"]),
                delivery_address=f"123 Sample St, City {i+1}",
                notes=f"Sample order {i+1}"
            )
            db.add(order)
        
        db.commit()
        
        # Create some stock movements
        for i in range(20):
            product = random.choice(products)
            movement_type = random.choice(["inbound", "outbound", "adjustment"])
            quantity = random.randint(-50, 100) if movement_type == "adjustment" else random.randint(1, 50)
            if movement_type == "outbound":
                quantity = -quantity
            
            movement = StockMovement(
                product_id=product.id,
                movement_type=movement_type,
                quantity=quantity,
                reason=f"Sample {movement_type} movement",
                reference_id=None,
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.add(movement)
        
        db.commit()
        
        # Create some chat messages
        # First create a default user for chat sessions
        default_user = User(
            username="system_user",
            email="system@warehouse.com",
            full_name="System User",
            role="admin",
            department="management"
        )
        db.add(default_user)
        db.commit()
        
        # Create a chat session
        chat_session = ChatSession(
            session_id="default-session",
            user_id=default_user.id,
            title="Sample Chat Session",
            context_summary="Initial system testing"
        )
        db.add(chat_session)
        db.commit()
        
        sample_messages = [
            "What is the current stock level for laptops?",
            "Show me low stock items",
            "When is the next shipment arriving?",
            "Generate a report for electronics category",
            "What are the top selling products?",
            "Show me pending orders",
            "Help me find product LAPTOP001",
            "What is the status of shipment INB-2024-0001?"
        ]
        
        for i, message in enumerate(sample_messages):
            chat = ChatMessage(
                session_id=chat_session.id,
                user_id=default_user.id,
                user_message=message,
                bot_response=f"This is a sample response to: {message}",
                intent="sample_query",
                confidence_score=0.95,
                success=True,
                created_at=datetime.now() - timedelta(hours=random.randint(1, 72))
            )
            db.add(chat)
        
        db.commit()
        
        print("Sample data created successfully!")
        print(f"Created {len(products)} products")
        print(f"Created {len(vendors)} vendors")
        print(f"Created {len(customers)} customers")
        print("Database initialization complete!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing Smart Warehouse System database...")
    create_sample_data()
    print("Done!")
