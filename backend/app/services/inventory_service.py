from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from ..models.database_models import Product, Inventory, StockMovement
from ..database import get_db
from datetime import datetime

class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self) -> List[Product]:
        """Get all products with their inventory information"""
        return self.db.query(Product).all()

    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU"""
        return self.db.query(Product).filter(Product.sku == sku).first()

    def create_product(self, product_data: dict) -> Product:
        """Create a new product"""
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        # Create initial inventory record
        inventory = Inventory(
            product_id=product.id,
            quantity=0,
            reserved_quantity=0,
            available_quantity=0
        )
        self.db.add(inventory)
        self.db.commit()
        
        return product

    def get_inventory_summary(self):
        """Get inventory summary with low stock alerts"""
        query = self.db.query(
            Product.id,
            Product.sku,
            Product.name,
            Product.category,
            Product.reorder_level,
            Product.location,
            Inventory.quantity,
            Inventory.reserved_quantity,
            Inventory.available_quantity,
            Inventory.last_updated
        ).join(Inventory, Product.id == Inventory.product_id)
        
        results = query.all()
        
        inventory_data = []
        low_stock_items = []
        
        for item in results:
            inventory_item = {
                "product_id": item.id,
                "sku": item.sku,
                "name": item.name,
                "category": item.category,
                "location": item.location,
                "quantity": item.quantity,
                "reserved_quantity": item.reserved_quantity,
                "available_quantity": item.available_quantity,
                "reorder_level": item.reorder_level,
                "last_updated": item.last_updated,
                "needs_reorder": item.available_quantity <= item.reorder_level
            }
            
            inventory_data.append(inventory_item)
            
            if item.available_quantity <= item.reorder_level:
                low_stock_items.append(inventory_item)
        
        return {
            "inventory": inventory_data,
            "low_stock_alerts": low_stock_items,
            "total_products": len(inventory_data),
            "low_stock_count": len(low_stock_items)
        }

    def update_stock(self, product_id: int, quantity_change: int, movement_type: str, 
                     reference_type: str = None, reference_id: int = None, 
                     reason: str = None, created_by: str = "system") -> bool:
        """Update stock levels and create stock movement record"""
        try:
            # Get current inventory
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product_id).first()
            if not inventory:
                return False
            
            # Update inventory
            inventory.quantity += quantity_change
            inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
            inventory.last_updated = datetime.utcnow()
            
            # Create stock movement record
            movement = StockMovement(
                product_id=product_id,
                movement_type=movement_type,
                quantity=quantity_change,
                reference_type=reference_type,
                reference_id=reference_id,
                reason=reason,
                created_by=created_by
            )
            
            self.db.add(movement)
            self.db.commit()
            
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def reserve_stock(self, product_id: int, quantity: int) -> bool:
        """Reserve stock for outbound orders"""
        try:
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product_id).first()
            if not inventory or inventory.available_quantity < quantity:
                return False
            
            inventory.reserved_quantity += quantity
            inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
            inventory.last_updated = datetime.utcnow()
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def release_stock(self, product_id: int, quantity: int) -> bool:
        """Release reserved stock"""
        try:
            inventory = self.db.query(Inventory).filter(Inventory.product_id == product_id).first()
            if not inventory:
                return False
            
            inventory.reserved_quantity = max(0, inventory.reserved_quantity - quantity)
            inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
            inventory.last_updated = datetime.utcnow()
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def get_stock_movements(self, product_id: int = None, limit: int = 100):
        """Get stock movement history"""
        query = self.db.query(StockMovement)
        
        if product_id:
            query = query.filter(StockMovement.product_id == product_id)
        
        movements = query.order_by(StockMovement.created_at.desc()).limit(limit).all()
        
        # Join with product information
        result = []
        for movement in movements:
            product = self.db.query(Product).filter(Product.id == movement.product_id).first()
            result.append({
                "id": movement.id,
                "product_sku": product.sku if product else "Unknown",
                "product_name": product.name if product else "Unknown",
                "movement_type": movement.movement_type,
                "quantity": movement.quantity,
                "reference_type": movement.reference_type,
                "reference_id": movement.reference_id,
                "reason": movement.reason,
                "created_at": movement.created_at,
                "created_by": movement.created_by
            })
        
        return result
