#!/usr/bin/env python3
"""
Enhanced Database Setup with Natural Language RAG Integration
Creates comprehensive sample data and configures RAG for natural language operations
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime, timedelta
import random
from sqlalchemy.orm import sessionmaker
from backend.app.database import engine
from backend.app.models.database_models import (
    Product, Inventory, Vendor, Customer, InboundShipment, OutboundOrder,
    InboundItem, OutboundItem, StockMovement, User, ChatSession, ChatMessage,
    DemandForecast, ProductVelocity, StockAlert, WarehouseLayout, SpaceOptimization,
    SalesHistory, ConversationContext
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_comprehensive_warehouse_data():
    """Set up comprehensive warehouse data for natural language processing"""
    
    print("🏭 Setting up Smart Warehouse Database with Enhanced RAG Support...")
    
    db = SessionLocal()
    
    try:
        # Ensure tables exist first
        print("🏗️ Creating database tables...")
        from backend.app.models.database_models import Base
        from backend.app.database import engine
        Base.metadata.create_all(bind=engine)
        
        # Clear existing data (if any)
        print("🧹 Clearing existing data...")
        try:
            for table in [ChatMessage, ConversationContext, ChatSession, StockMovement, 
                         OutboundItem, InboundItem, OutboundOrder, InboundShipment, 
                         Inventory, Product, Customer, Vendor, User, DemandForecast, 
                         ProductVelocity, StockAlert, WarehouseLayout, SpaceOptimization, SalesHistory]:
                db.query(table).delete()
        except Exception as e:
            print(f"⚠️ Note: Some tables may not exist yet: {e}")
            pass
        
        # 1. Create Users
        print("👤 Creating users...")
        users = [
            User(
                username="warehouse_manager",
                email="manager@warehouse.com",
                full_name="John Manager",
                role="admin",
                department="management",
                phone="+1-555-0101",
                preferences={"language": "en", "dashboard_layout": "advanced", "notifications": True}
            ),
            User(
                username="inventory_operator",
                email="operator@warehouse.com", 
                full_name="Sarah Operator",
                role="operator",
                department="inventory",
                phone="+1-555-0102",
                preferences={"quick_actions": ["stock_check", "add_inventory"], "show_low_stock": True}
            ),
            User(
                username="inbound_supervisor",
                email="inbound@warehouse.com",
                full_name="Mike Inbound",
                role="supervisor", 
                department="inbound",
                phone="+1-555-0103"
            ),
            User(
                username="outbound_coordinator",
                email="outbound@warehouse.com",
                full_name="Lisa Outbound",
                role="operator",
                department="outbound", 
                phone="+1-555-0104"
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        # 2. Create Vendors
        print("🏢 Creating vendors...")
        vendors = [
            Vendor(
                name="TechSupply Corp",
                contact_person="Robert Tech",
                phone="+1-555-2001",
                email="orders@techsupply.com",
                address="123 Technology Drive, San Francisco, CA 94105"
            ),
            Vendor(
                name="Global Electronics Ltd", 
                contact_person="Anna Global",
                phone="+1-555-2002",
                email="sales@globalelec.com",
                address="456 Electronics Blvd, Austin, TX 78701"
            ),
            Vendor(
                name="Industrial Materials Inc",
                contact_person="David Industrial",
                phone="+1-555-2003", 
                email="contact@indmaterials.com",
                address="789 Industrial Way, Chicago, IL 60601"
            ),
            Vendor(
                name="Premium Office Solutions",
                contact_person="Emma Premium",
                phone="+1-555-2004",
                email="orders@premiumoffice.com", 
                address="321 Office Park, Seattle, WA 98101"
            )
        ]
        
        for vendor in vendors:
            db.add(vendor)
        db.commit()
        
        # 3. Create Customers
        print("🛒 Creating customers...")
        customers = [
            Customer(
                name="Retail Chain Plus",
                contact_person="Jennifer Retail",
                phone="+1-555-3001",
                email="orders@retailplus.com",
                address="111 Retail Street, New York, NY 10001"
            ),
            Customer(
                name="Manufacturing Corp",
                contact_person="Steve Manufacturing", 
                phone="+1-555-3002",
                email="procurement@manufacorp.com",
                address="222 Factory Lane, Detroit, MI 48201"
            ),
            Customer(
                name="Small Business Solutions",
                contact_person="Maria Business",
                phone="+1-555-3003",
                email="orders@smallbizsol.com",
                address="333 Business Ave, Denver, CO 80201"
            ),
            Customer(
                name="Enterprise Systems Ltd",
                contact_person="Alex Enterprise",
                phone="+1-555-3004", 
                email="purchasing@enterprisesys.com",
                address="444 Enterprise Blvd, Miami, FL 33101"
            )
        ]
        
        for customer in customers:
            db.add(customer)
        db.commit()
        
        # 4. Create Products with diverse categories
        print("📦 Creating products...")
        products_data = [
            # Electronics
            {"sku": "ELEC001", "name": "Wireless Bluetooth Headphones", "description": "High-quality noise-canceling wireless headphones with 30-hour battery life", "category": "Electronics", "unit": "pcs", "unit_price": 149.99, "reorder_level": 20, "location": "A1-01"},
            {"sku": "ELEC002", "name": "USB-C Fast Charger", "description": "65W USB-C fast charger compatible with laptops and smartphones", "category": "Electronics", "unit": "pcs", "unit_price": 39.99, "reorder_level": 50, "location": "A1-02"},
            {"sku": "ELEC003", "name": "Portable SSD 1TB", "description": "High-speed portable SSD with USB 3.2 interface", "category": "Electronics", "unit": "pcs", "unit_price": 129.99, "reorder_level": 15, "location": "A1-03"},
            {"sku": "ELEC004", "name": "Wireless Gaming Mouse", "description": "Precision wireless gaming mouse with RGB lighting", "category": "Electronics", "unit": "pcs", "unit_price": 79.99, "reorder_level": 25, "location": "A1-04"},
            {"sku": "ELEC005", "name": "4K Webcam", "description": "Ultra HD 4K webcam with auto-focus for streaming and video calls", "category": "Electronics", "unit": "pcs", "unit_price": 199.99, "reorder_level": 10, "location": "A1-05"},
            
            # Office Supplies
            {"sku": "OFFC001", "name": "Ergonomic Office Chair", "description": "Adjustable ergonomic office chair with lumbar support", "category": "Office Supplies", "unit": "pcs", "unit_price": 299.99, "reorder_level": 5, "location": "B2-01"},
            {"sku": "OFFC002", "name": "Standing Desk Converter", "description": "Adjustable standing desk converter for healthier work habits", "category": "Office Supplies", "unit": "pcs", "unit_price": 189.99, "reorder_level": 8, "location": "B2-02"},
            {"sku": "OFFC003", "name": "Premium Paper Shredder", "description": "Cross-cut paper shredder for sensitive documents", "category": "Office Supplies", "unit": "pcs", "unit_price": 159.99, "reorder_level": 3, "location": "B2-03"},
            {"sku": "OFFC004", "name": "Wireless Presenter Remote", "description": "Laser pointer presenter remote with USB receiver", "category": "Office Supplies", "unit": "pcs", "unit_price": 49.99, "reorder_level": 15, "location": "B2-04"},
            {"sku": "OFFC005", "name": "Multi-Function Printer", "description": "All-in-one wireless printer with scanning and copying", "category": "Office Supplies", "unit": "pcs", "unit_price": 249.99, "reorder_level": 6, "location": "B2-05"},
            
            # Industrial Tools
            {"sku": "TOOL001", "name": "Cordless Impact Drill", "description": "Professional 18V cordless impact drill with battery pack", "category": "Tools", "unit": "pcs", "unit_price": 179.99, "reorder_level": 12, "location": "C3-01"},
            {"sku": "TOOL002", "name": "Digital Multimeter", "description": "Professional digital multimeter for electrical testing", "category": "Tools", "unit": "pcs", "unit_price": 89.99, "reorder_level": 20, "location": "C3-02"},
            {"sku": "TOOL003", "name": "Laser Level", "description": "Self-leveling laser level for construction and installation", "category": "Tools", "unit": "pcs", "unit_price": 129.99, "reorder_level": 8, "location": "C3-03"},
            {"sku": "TOOL004", "name": "Socket Wrench Set", "description": "Complete 108-piece socket wrench set with ratchets", "category": "Tools", "unit": "set", "unit_price": 99.99, "reorder_level": 10, "location": "C3-04"},
            {"sku": "TOOL005", "name": "Pneumatic Air Compressor", "description": "Portable air compressor for pneumatic tools", "category": "Tools", "unit": "pcs", "unit_price": 399.99, "reorder_level": 4, "location": "C3-05"},
            
            # Components
            {"sku": "COMP001", "name": "Circuit Boards", "description": "PCB circuit boards for electronic device assembly", "category": "Components", "unit": "pcs", "unit_price": 24.99, "reorder_level": 100, "location": "D4-01"},
            {"sku": "COMP002", "name": "LED Light Strips", "description": "Flexible LED light strips with adhesive backing", "category": "Components", "unit": "meters", "unit_price": 12.99, "reorder_level": 200, "location": "D4-02"},
            {"sku": "COMP003", "name": "Capacitor Kit", "description": "Assorted capacitor kit for electronic repairs", "category": "Components", "unit": "kit", "unit_price": 34.99, "reorder_level": 30, "location": "D4-03"},
            {"sku": "COMP004", "name": "Connector Cables", "description": "Various connector cables for data transmission", "category": "Components", "unit": "pcs", "unit_price": 15.99, "reorder_level": 75, "location": "D4-04"},
            {"sku": "COMP005", "name": "Heat Sinks", "description": "Aluminum heat sinks for thermal management", "category": "Components", "unit": "pcs", "unit_price": 8.99, "reorder_level": 150, "location": "D4-05"}
        ]
        
        products = []
        for product_data in products_data:
            product = Product(**product_data)
            products.append(product)
            db.add(product)
        
        db.commit()
        
        # 5. Create Inventory for all products
        print("📊 Creating inventory records...")
        for product in products:
            # Create realistic stock levels - some low, some high
            stock_multiplier = random.choice([0.5, 0.8, 1.2, 1.5, 2.0, 3.0])
            total_quantity = int(product.reorder_level * stock_multiplier)
            reserved = random.randint(0, min(5, total_quantity // 4))
            
            inventory = Inventory(
                product_id=product.id,
                quantity=total_quantity,
                reserved_quantity=reserved,
                available_quantity=total_quantity - reserved,
                last_updated=datetime.utcnow()
            )
            db.add(inventory)
        
        db.commit()
        
        # 6. Create Warehouse Layout
        print("🏗️ Creating warehouse layout...")
        layout_zones = [
            {"zone_code": "A1", "zone_name": "Electronics Zone", "zone_type": "storage", "capacity": 1000, "current_utilization": 650, "distance_from_entrance": 10.0, "distance_from_exit": 25.0, "preferred_categories": ["Electronics"]},
            {"zone_code": "A2", "zone_name": "Electronics Overflow", "zone_type": "storage", "capacity": 500, "current_utilization": 200, "distance_from_entrance": 15.0, "distance_from_exit": 30.0, "preferred_categories": ["Electronics"]},
            {"zone_code": "B1", "zone_name": "Office Supplies Zone", "zone_type": "storage", "capacity": 800, "current_utilization": 450, "distance_from_entrance": 20.0, "distance_from_exit": 15.0, "preferred_categories": ["Office Supplies"]},
            {"zone_code": "B2", "zone_name": "Bulk Office Storage", "zone_type": "storage", "capacity": 600, "current_utilization": 280, "distance_from_entrance": 25.0, "distance_from_exit": 20.0, "preferred_categories": ["Office Supplies"]},
            {"zone_code": "C1", "zone_name": "Tools and Equipment", "zone_type": "storage", "capacity": 700, "current_utilization": 520, "distance_from_entrance": 30.0, "distance_from_exit": 10.0, "preferred_categories": ["Tools"]},
            {"zone_code": "C2", "zone_name": "Heavy Tools Storage", "zone_type": "storage", "capacity": 400, "current_utilization": 180, "distance_from_entrance": 35.0, "distance_from_exit": 5.0, "preferred_categories": ["Tools"]},
            {"zone_code": "D1", "zone_name": "Components Zone", "zone_type": "storage", "capacity": 1200, "current_utilization": 800, "distance_from_entrance": 8.0, "distance_from_exit": 35.0, "preferred_categories": ["Components"]},
            {"zone_code": "R1", "zone_name": "Receiving Area", "zone_type": "receiving", "capacity": 200, "current_utilization": 50, "distance_from_entrance": 0.0, "distance_from_exit": 50.0, "preferred_categories": []},
            {"zone_code": "S1", "zone_name": "Shipping Dock", "zone_type": "dispatch", "capacity": 150, "current_utilization": 30, "distance_from_entrance": 50.0, "distance_from_exit": 0.0, "preferred_categories": []},
            {"zone_code": "P1", "zone_name": "Pick and Pack Area", "zone_type": "picking", "capacity": 100, "current_utilization": 40, "distance_from_entrance": 25.0, "distance_from_exit": 25.0, "preferred_categories": []}
        ]
        
        for zone_data in layout_zones:
            zone_data["utilization_percentage"] = (zone_data["current_utilization"] / zone_data["capacity"]) * 100
            layout = WarehouseLayout(**zone_data)
            db.add(layout)
        
        db.commit()
        
        # 7. Create Sample Stock Movements
        print("📈 Creating stock movement history...")
        movement_types = ["inbound", "outbound", "adjustment", "transfer"]
        for i in range(50):
            product = random.choice(products)
            movement_type = random.choice(movement_types)
            
            if movement_type == "inbound":
                quantity = random.randint(10, 100)
            elif movement_type == "outbound":
                quantity = -random.randint(1, 20)
            else:
                quantity = random.randint(-10, 10)
            
            movement = StockMovement(
                product_id=product.id,
                movement_type=movement_type,
                quantity=quantity,
                reference_type=movement_type,
                reference_id=random.randint(1, 10),
                reason=f"Sample {movement_type} movement",
                notes=f"Automated test data for {product.sku}",
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                created_by="system_setup"
            )
            db.add(movement)
        
        db.commit()
        
        # 8. Create Sample Chat Sessions and Messages
        print("💬 Creating sample chat sessions...")
        sample_queries = [
            ("What is the current stock level of ELEC001?", "The current stock level for ELEC001 (Wireless Bluetooth Headphones) is 30 units with 25 available and 5 reserved."),
            ("Show me all products with low stock", "Here are the products with low stock levels: ELEC005 (8 units), OFFC001 (4 units), TOOL005 (3 units)."),
            ("Add 50 units to COMP001 inventory", "Successfully added 50 units to COMP001 (Circuit Boards). New total: 150 units."),
            ("What products are in the Electronics category?", "Electronics category contains: ELEC001 (Headphones), ELEC002 (Charger), ELEC003 (SSD), ELEC004 (Mouse), ELEC005 (Webcam)."),
            ("Generate demand forecast for next month", "Based on historical data, predicted demand for next month: ELEC001 (45 units), COMP001 (120 units), TOOL001 (18 units)."),
            ("Optimize warehouse layout for fast-moving items", "Recommendation: Move ELEC001 and COMP001 closer to shipping area. These items have high turnover rates."),
            ("Delete product COMP005 from inventory", "Product COMP005 (Heat Sinks) has been marked for deletion. Current stock will be depleted first before removal."),
            ("Create new inbound shipment from TechSupply Corp", "Created inbound shipment INB-2024-001 from TechSupply Corp. Expected arrival: tomorrow. Please specify products and quantities."),
            ("What's the utilization rate of zone A1?", "Zone A1 (Electronics Zone) utilization: 65% (650/1000 units). Operating at optimal capacity."),
            ("Show me overstock alerts", "Overstock detected: COMP002 (300% above reorder level), TOOL004 (250% above reorder level). Consider redistribution.")
        ]
        
        manager_user = db.query(User).filter(User.username == "warehouse_manager").first()
        operator_user = db.query(User).filter(User.username == "inventory_operator").first()
        
        for i, (query, response) in enumerate(sample_queries):
            user = manager_user if i % 2 == 0 else operator_user
            
            # Create session
            session = ChatSession(
                session_id=f"session_{i+1:03d}",
                user_id=user.id,
                title=f"Query about {query.split()[0:3]}",
                context_summary=f"Discussion about {query[:50]}...",
                total_messages=1,
                last_activity=datetime.utcnow() - timedelta(hours=random.randint(1, 72))
            )
            db.add(session)
            db.commit()
            
            # Create message
            message = ChatMessage(
                session_id=session.id,
                user_id=user.id,
                user_message=query,
                bot_response=response,
                intent="inventory_check" if "stock" in query.lower() else "general_query",
                confidence_score=0.95,
                action_taken="data_retrieval" if "show" in query.lower() or "what" in query.lower() else "data_modification",
                processing_time=random.uniform(0.1, 2.0),
                enhanced_mode=True,
                success=True
            )
            db.add(message)
        
        db.commit()
        
        # 9. Create Product Velocity Analysis
        print("🚀 Creating product velocity analysis...")
        velocity_categories = ["fast", "medium", "slow", "dead"]
        for product in products:
            # Simulate velocity based on category and reorder level
            if product.category == "Electronics":
                velocity = random.choice(["fast", "fast", "medium"])
            elif product.category == "Components":
                velocity = random.choice(["fast", "medium", "medium"])
            elif product.category == "Tools":
                velocity = random.choice(["medium", "slow"])
            else:
                velocity = random.choice(["medium", "slow", "dead"])
            
            velocity_record = ProductVelocity(
                product_id=product.id,
                velocity_category=velocity,
                weekly_turnover=random.uniform(2.0, 15.0) if velocity == "fast" else random.uniform(0.1, 5.0),
                monthly_turnover=random.uniform(8.0, 60.0) if velocity == "fast" else random.uniform(0.5, 20.0),
                days_of_supply=random.randint(7, 30) if velocity == "fast" else random.randint(30, 90),
                pick_frequency=random.randint(10, 50) if velocity == "fast" else random.randint(1, 10),
                last_movement_date=datetime.utcnow() - timedelta(days=random.randint(1, 7)),
                movement_trend=random.choice(["increasing", "stable", "decreasing"]),
                seasonality_pattern={"Q1": 1.2, "Q2": 0.8, "Q3": 1.0, "Q4": 1.4} if velocity == "fast" else {"Q1": 0.9, "Q2": 1.0, "Q3": 1.1, "Q4": 1.0}
            )
            db.add(velocity_record)
        
        db.commit()
        
        # 10. Create Stock Alerts
        print("⚠️ Creating stock alerts...")
        alert_types = ["overstock", "understock", "reorder"]
        for product in products[:10]:  # Create alerts for first 10 products
            inventory = db.query(Inventory).filter(Inventory.product_id == product.id).first()
            
            if inventory.available_quantity < product.reorder_level:
                alert_type = "understock"
                severity = "high" if inventory.available_quantity < (product.reorder_level * 0.5) else "medium"
                message = f"Stock level for {product.sku} ({product.name}) is below reorder level. Current: {inventory.available_quantity}, Reorder at: {product.reorder_level}"
            elif inventory.available_quantity > (product.reorder_level * 3):
                alert_type = "overstock"
                severity = "medium"
                message = f"Overstock detected for {product.sku} ({product.name}). Current: {inventory.available_quantity}, Normal level: {product.reorder_level * 2}"
            else:
                alert_type = "reorder"
                severity = "low"
                message = f"Consider reordering {product.sku} ({product.name}) soon. Current: {inventory.available_quantity}"
            
            alert = StockAlert(
                product_id=product.id,
                alert_type=alert_type,
                severity=severity,
                current_stock=inventory.available_quantity,
                recommended_stock=product.reorder_level * 2,
                predicted_stockout_date=datetime.utcnow() + timedelta(days=random.randint(7, 30)),
                reorder_quantity=product.reorder_level * 2,
                reorder_urgency="urgent" if severity == "high" else "normal",
                message=message,
                resolved=False
            )
            db.add(alert)
        
        db.commit()
        
        print("✅ Database setup completed successfully!")
        print(f"📊 Created:")
        print(f"   - {len(users)} Users")
        print(f"   - {len(vendors)} Vendors") 
        print(f"   - {len(customers)} Customers")
        print(f"   - {len(products)} Products with inventory")
        print(f"   - {len(layout_zones)} Warehouse zones")
        print(f"   - 50 Stock movements")
        print(f"   - {len(sample_queries)} Chat sessions with messages")
        print(f"   - Product velocity analysis")
        print(f"   - Stock alerts and forecasting data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        db.rollback()
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    success = setup_comprehensive_warehouse_data()
    if success:
        print("\n🎉 Smart Warehouse Database is ready for natural language operations!")
        print("📝 You can now use queries like:")
        print("   - 'Show me current stock levels'")
        print("   - 'Add 100 units to ELEC001'")
        print("   - 'Delete product COMP005'")
        print("   - 'What products are low on stock?'")
        print("   - 'Generate demand forecast'")
        print("   - 'Optimize warehouse layout'")
    else:
        print("\n❌ Database setup failed. Please check the error messages above.")
        sys.exit(1)
