#!/usr/bin/env python3
"""
Quick Inventory Setup for Chatbot Testing
Creates basic sample products and inventory for testing the chatbot integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime, timedelta
import random

try:
    from sqlalchemy.orm import sessionmaker
    from backend.app.database import engine
    from backend.app.models.database_models import Product, Inventory, Vendor, Customer
except ImportError as e:
    print(f"Database import error: {e}")
    print("Please ensure you're running this from the project root directory")
    print("Usage: python quick_inventory_setup.py")
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_quick_inventory():
    """Set up basic inventory data for chatbot testing"""
    print("📦 Setting up Quick Inventory Data for Chatbot Testing...")
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing inventory data...")
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.query(Vendor).delete()
        db.query(Customer).delete()
        
        # Create sample vendors
        vendors = [
            Vendor(name="TechSupply Corp", contact_info="tech@supply.com", address="123 Tech St"),
            Vendor(name="Electronics Direct", contact_info="sales@electronics.com", address="456 Circuit Ave"),
            Vendor(name="Office Solutions Inc", contact_info="orders@office.com", address="789 Business Blvd")
        ]
        
        for vendor in vendors:
            db.add(vendor)
        db.flush()  # Flush to get IDs
        
        # Create sample customers
        customers = [
            Customer(name="Acme Corporation", contact_info="procurement@acme.com", address="111 Corporate Way"),
            Customer(name="Tech Startup LLC", contact_info="ops@startup.com", address="222 Innovation Dr"),
            Customer(name="Retail Chain Co", contact_info="supply@retail.com", address="333 Store St")
        ]
        
        for customer in customers:
            db.add(customer)
        db.flush()
        
        # Create sample products with realistic SKUs
        products_data = [
            # Electronics
            {"sku": "LAPTOP001", "name": "Business Laptop Pro", "category": "Electronics", "unit": "units", "vendor_id": vendors[0].id},
            {"sku": "PHONE123", "name": "Smartphone X", "category": "Electronics", "unit": "units", "vendor_id": vendors[1].id},
            {"sku": "TABLET001", "name": "Tablet Device", "category": "Electronics", "unit": "units", "vendor_id": vendors[1].id},
            {"sku": "HEADSET001", "name": "Wireless Headset", "category": "Electronics", "unit": "units", "vendor_id": vendors[1].id},
            
            # Office Supplies
            {"sku": "PAPER001", "name": "A4 Copy Paper", "category": "Office", "unit": "reams", "vendor_id": vendors[2].id},
            {"sku": "PEN001", "name": "Blue Ink Pens", "category": "Office", "unit": "boxes", "vendor_id": vendors[2].id},
            {"sku": "PRINTER001", "name": "Laser Printer", "category": "Office", "unit": "units", "vendor_id": vendors[0].id},
            
            # Medical/Safety
            {"sku": "MASK001", "name": "Safety Masks", "category": "Medical", "unit": "boxes", "vendor_id": vendors[0].id},
            {"sku": "GLOVES001", "name": "Disposable Gloves", "category": "Medical", "unit": "boxes", "vendor_id": vendors[0].id},
            
            # Industrial
            {"sku": "TOOL001", "name": "Power Drill", "category": "Industrial", "unit": "units", "vendor_id": vendors[0].id},
            {"sku": "SAFETY001", "name": "Hard Hats", "category": "Industrial", "unit": "units", "vendor_id": vendors[0].id}
        ]
        
        products = []
        for product_data in products_data:
            product = Product(
                sku=product_data["sku"],
                name=product_data["name"],
                description=f"High quality {product_data['name'].lower()} for business use",
                category=product_data["category"],
                unit=product_data["unit"],
                unit_cost=round(random.uniform(10.0, 500.0), 2),
                vendor_id=product_data["vendor_id"],
                location=f"Zone-{random.choice(['A', 'B', 'C'])}-{random.randint(1, 20)}"
            )
            products.append(product)
            db.add(product)
        
        db.flush()  # Flush to get product IDs
        
        # Create inventory records with realistic stock levels
        for product in products:
            # Some products have good stock, some are low
            if product.sku in ["LAPTOP001", "PHONE123", "TABLET001"]:
                # High-value electronics - moderate stock
                total_qty = random.randint(50, 200)
                reserved_qty = random.randint(5, 20)
            elif product.sku in ["PAPER001", "PEN001", "MASK001", "GLOVES001"]:
                # High-volume supplies - high stock
                total_qty = random.randint(200, 1000)
                reserved_qty = random.randint(10, 50)
            elif product.sku in ["PRINTER001", "TOOL001", "SAFETY001"]:
                # Low-volume items - low stock (for testing alerts)
                total_qty = random.randint(5, 30)
                reserved_qty = random.randint(1, 5)
            else:
                total_qty = random.randint(20, 100)
                reserved_qty = random.randint(2, 10)
            
            inventory = Inventory(
                product_id=product.id,
                quantity=total_qty,
                reserved_quantity=min(reserved_qty, total_qty),
                reorder_point=max(10, total_qty // 10),
                last_updated=datetime.utcnow()
            )
            db.add(inventory)
        
        # Commit all changes
        db.commit()
        
        # Print summary
        print("\n✅ Sample inventory data created successfully!")
        print("\n📊 Summary:")
        product_count = db.query(Product).count()
        inventory_count = db.query(Inventory).count()
        print(f"   Products: {product_count}")
        print(f"   Inventory records: {inventory_count}")
        print(f"   Vendors: {len(vendors)}")
        print(f"   Customers: {len(customers)}")
        
        print("\n🧪 Test Commands:")
        print("   'Check stock SKU: LAPTOP001'")
        print("   'Show inventory summary'")
        print("   'Add 25 units SKU: PHONE123'")
        print("   'What items are low on stock?'")
        print("   'Check stock SKU: PRINTER001'")
        
        print("\n🔧 Start backend server:")
        print("   cd backend && uvicorn app.main:app --reload")
        print("\n🌐 Test frontend:")
        print("   Visit: https://samarth4jain.github.io/smart-warehouse-system/chatbot.html")
        
    except Exception as e:
        print(f"❌ Error setting up data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    setup_quick_inventory()
