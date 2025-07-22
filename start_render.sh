#!/bin/bash
# Render.com startup script

echo "🚀 Starting Smart Warehouse System on Render..."

# Set up database
python3 -c "
from backend.app.database import engine, Base
from backend.app.models.database_models import *

print('📦 Initializing database...')
Base.metadata.create_all(bind=engine)

# Add sample data
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

from backend.app.models.database_models import Product
if session.query(Product).count() == 0:
    print('📊 Adding sample data...')
    
    product1 = Product(
        sku='PROD001',
        name='Laptop Computer',
        description='High-performance laptop',
        category='Electronics',
        unit_price=999.99,
        supplier='TechCorp Inc',
        reorder_level=10,
        max_stock_level=100
    )
    
    product2 = Product(
        sku='PROD002', 
        name='Office Chair',
        description='Ergonomic office chair',
        category='Furniture',
        unit_price=299.99,
        supplier='OfficeMax Ltd',
        reorder_level=5,
        max_stock_level=50
    )
    
    session.add_all([product1, product2])
    
    from backend.app.models.database_models import Inventory
    inv1 = Inventory(product_id=1, quantity=25, location='A1-B2-C3')
    inv2 = Inventory(product_id=2, quantity=15, location='B1-C2-D3')
    
    session.add_all([inv1, inv2])
    session.commit()
    print('✅ Database ready!')

session.close()
"

echo "🌐 Starting web server on port $PORT..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
