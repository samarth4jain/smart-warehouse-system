#!/usr/bin/env python3
"""
Database initialization script for Smart Warehouse System
This script creates all necessary tables and populates them with sample data
"""

import sys
import os
from datetime import datetime

# Add the backend app to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import engine
from backend.app.models.database_models import (
    Base, Product, Inventory, StockMovement, InboundShipment, OutboundOrder,
    Vendor, Customer, User, ChatSession
)

def create_all_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def populate_sample_data():
    """Populate database with sample data"""
    from backend.app.database import SessionLocal
    
    db = SessionLocal()
    try:
        print("Adding sample data...")
        
        # Create sample vendors (suppliers)
        vendors = [
            Vendor(name="TechCorp Electronics", contact_person="John Smith", 
                    email="john@techcorp.com", phone="555-1234", 
                    address="123 Tech Street, Silicon Valley, CA"),
            Vendor(name="Fashion World Inc", contact_person="Sarah Johnson", 
                    email="sarah@fashionworld.com", phone="555-5678", 
                    address="456 Fashion Ave, New York, NY"),
            Vendor(name="BookMart Publishing", contact_person="Mike Brown", 
                    email="mike@bookmart.com", phone="555-9012", 
                    address="789 Book Lane, Boston, MA"),
        ]
        
        for vendor in vendors:
            db.add(vendor)
        db.commit()
        
        # Create sample customers
        customers = [
            Customer(name="ABC Retail", contact_person="Lisa Davis", 
                    email="lisa@abcretail.com", phone="555-2468", 
                    address="321 Retail Blvd, Chicago, IL"),
            Customer(name="XYZ Electronics", contact_person="Tom Wilson", 
                    email="tom@xyzelectronics.com", phone="555-1357", 
                    address="654 Electronics Way, Austin, TX"),
            Customer(name="Local Bookstore", contact_person="Emma Green", 
                    email="emma@localbookstore.com", phone="555-8642", 
                    address="987 Book Street, Portland, OR"),
        ]
        
        for customer in customers:
            db.add(customer)
        db.commit()
        
        # Create sample products
        products = [
            Product(sku="LAPTOP001", name="Gaming Laptop", category="Electronics", 
                   reorder_level=10, location="A-1-01-001"),
            Product(sku="PHONE001", name="Smartphone", category="Electronics", 
                   reorder_level=25, location="A-1-02-001"),
            Product(sku="TSHIRT001", name="Cotton T-Shirt", category="Clothing", 
                   reorder_level=50, location="B-1-01-001"),
            Product(sku="JEANS001", name="Denim Jeans", category="Clothing", 
                   reorder_level=30, location="B-1-01-001"),
            Product(sku="SNEAKERS001", name="Running Sneakers", category="Footwear", 
                   reorder_level=20, location="B-2-01-001"),
            Product(sku="BOOK001", name="Python Programming Guide", category="Books", 
                   reorder_level=15, location="C-1-01-001"),
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        
        # Create sample inventory
        inventories = [
            Inventory(product_id=1, quantity=45, reserved_quantity=5, available_quantity=40),
            Inventory(product_id=2, quantity=120, reserved_quantity=10, available_quantity=110),
            Inventory(product_id=3, quantity=200, reserved_quantity=25, available_quantity=175),
            Inventory(product_id=4, quantity=85, reserved_quantity=15, available_quantity=70),
            Inventory(product_id=5, quantity=60, reserved_quantity=8, available_quantity=52),
            Inventory(product_id=6, quantity=75, reserved_quantity=5, available_quantity=70),
        ]
        
        for inventory in inventories:
            db.add(inventory)
        db.commit()
        
        # Create sample stock movements
        movements = [
            StockMovement(product_id=1, movement_type="inbound", quantity=50, 
                         reference_type="purchase", reference_id="PO001", 
                         reason="Initial stock", notes="First delivery"),
            StockMovement(product_id=1, movement_type="outbound", quantity=5, 
                         reference_type="sale", reference_id="SO001", 
                         reason="Customer order", notes="Sold to ABC Retail"),
            StockMovement(product_id=2, movement_type="inbound", quantity=150, 
                         reference_type="purchase", reference_id="PO002", 
                         reason="Restock", notes="Regular restock"),
            StockMovement(product_id=2, movement_type="outbound", quantity=30, 
                         reference_type="sale", reference_id="SO002", 
                         reason="Bulk order", notes="XYZ Electronics order"),
        ]
        
        for movement in movements:
            db.add(movement)
        db.commit()
        
        # Create sample users
        users = [
            User(username="admin", email="admin@warehouse.com", 
                 role="admin", full_name="System Administrator"),
            User(username="manager", email="manager@warehouse.com", 
                 role="supervisor", full_name="Warehouse Manager"),
            User(username="operator", email="operator@warehouse.com", 
                 role="operator", full_name="Warehouse Operator"),
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        print("Sample data added successfully!")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing Smart Warehouse Database...")
    create_all_tables()
    populate_sample_data()
    print("Database initialization complete!")
