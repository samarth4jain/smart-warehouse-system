#!/bin/bash

# Cloud Startup Script for Smart Warehouse System
# This script runs when the app starts in production

echo "🏭 Starting Smart Warehouse System..."

# Set production environment
export ENVIRONMENT=production

# Create database if it doesn't exist
python3 -c "
from backend.app.database import engine, Base
from backend.app.models.database_models import *
import os

print('📦 Setting up database...')
Base.metadata.create_all(bind=engine)

# Add sample data if database is empty
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

from backend.app.models.database_models import Product
if session.query(Product).count() == 0:
    print('📊 Adding sample data...')
    
    # Add sample products
    product1 = Product(
        sku='PROD001',
        name='Laptop Computer',
        description='High-performance laptop for business use',
        category='Electronics',
        unit_price=999.99,
        supplier='TechCorp Inc',
        reorder_level=10,
        max_stock_level=100
    )
    
    product2 = Product(
        sku='PROD002',
        name='Office Chair',
        description='Ergonomic office chair with lumbar support',
        category='Furniture', 
        unit_price=299.99,
        supplier='OfficeMax Ltd',
        reorder_level=5,
        max_stock_level=50
    )
    
    session.add_all([product1, product2])
    
    # Add inventory
    from backend.app.models.database_models import Inventory
    inv1 = Inventory(product_id=1, quantity=25, location='A1-B2-C3')
    inv2 = Inventory(product_id=2, quantity=15, location='B1-C2-D3')
    
    session.add_all([inv1, inv2])
    
    session.commit()
    print('✅ Sample data added successfully!')

session.close()
print('🎯 Database ready!')
"

echo "🌐 Starting web server..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
