#!/usr/bin/env python3
"""
Create minimal database for testing dashboard
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app.database import engine, Base, SessionLocal
from backend.app.models.database_models import Product, Inventory
from datetime import datetime

def create_minimal_data():
    """Create minimal data for testing"""
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Product).count() > 0:
            print("Database already has data. Skipping initialization.")
            return
        
        print("Creating minimal sample data...")
        
        # Create sample products
        products = [
            Product(
                sku="PROD001",
                name="Test Product 1",
                description="A test product",
                category="Electronics",
                unit_price=99.99,
                reorder_level=10
            ),
            Product(
                sku="PROD002",
                name="Test Product 2",
                description="Another test product",
                category="Hardware",
                unit_price=149.99,
                reorder_level=5
            ),
        ]
        
        for product in products:
            db.add(product)
        
        db.commit()
        
        # Create inventory for products
        for product in products:
            inventory = Inventory(
                product_id=product.id,
                quantity=50,
                reserved_quantity=5,
                available_quantity=45
            )
            db.add(inventory)
        
        db.commit()
        print("Minimal database setup completed successfully!")
        
    except Exception as e:
        print(f"Error creating minimal data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Setting up minimal database for Smart Warehouse System...")
    create_minimal_data()
