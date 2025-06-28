from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.database_models import OutboundOrder, OutboundItem, Customer, Product, Inventory
from .inventory_service import InventoryService
from datetime import datetime

class OutboundService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_service = InventoryService(db)

    def create_order(self, order_data: dict) -> OutboundOrder:
        """Create a new outbound order"""
        order = OutboundOrder(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order_by_number(self, order_number: str) -> Optional[OutboundOrder]:
        """Get order by order number"""
        return self.db.query(OutboundOrder).filter(
            OutboundOrder.order_number == order_number
        ).first()

    def get_all_orders(self, status: str = None) -> List[OutboundOrder]:
        """Get all orders, optionally filtered by status"""
        query = self.db.query(OutboundOrder)
        if status:
            query = query.filter(OutboundOrder.status == status)
        return query.order_by(OutboundOrder.created_at.desc()).all()

    def update_order_status(self, order_id: int, status: str) -> bool:
        """Update order status"""
        try:
            order = self.db.query(OutboundOrder).filter(
                OutboundOrder.id == order_id
            ).first()
            
            if not order:
                return False
            
            order.status = status
            order.updated_at = datetime.utcnow()
            
            if status == "dispatched":
                order.actual_dispatch_date = datetime.utcnow()
                # Release reserved stock and update inventory
                for item in order.items:
                    # Update inventory - subtract from total stock
                    self.inventory_service.update_stock(
                        product_id=item.product_id,
                        quantity_change=-item.picked_quantity,
                        movement_type="outbound",
                        reference_type="outbound_order",
                        reference_id=order_id,
                        reason=f"Dispatched order {order.order_number}"
                    )
                    # Release reserved stock
                    self.inventory_service.release_stock(
                        product_id=item.product_id,
                        quantity=item.picked_quantity
                    )
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def add_order_item(self, order_id: int, item_data: dict) -> OutboundItem:
        """Add item to order"""
        item_data['order_id'] = order_id
        item = OutboundItem(**item_data)
        self.db.add(item)
        
        # Reserve stock for this item
        self.inventory_service.reserve_stock(
            product_id=item.product_id,
            quantity=item.ordered_quantity
        )
        
        self.db.commit()
        self.db.refresh(item)
        return item

    def pick_order_item(self, item_id: int, picked_quantity: int) -> bool:
        """Update picked quantity for order item"""
        try:
            item = self.db.query(OutboundItem).filter(OutboundItem.id == item_id).first()
            if not item:
                return False
            
            item.picked_quantity = picked_quantity
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def pack_order_item(self, item_id: int, packed_quantity: int) -> bool:
        """Update packed quantity for order item"""
        try:
            item = self.db.query(OutboundItem).filter(OutboundItem.id == item_id).first()
            if not item:
                return False
            
            item.packed_quantity = packed_quantity
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def get_pending_orders(self) -> List[OutboundOrder]:
        """Get all pending orders"""
        return self.get_all_orders(status="pending")

    def get_orders_for_picking(self) -> List[OutboundOrder]:
        """Get orders ready for picking"""
        return self.get_all_orders(status="pending")

    def get_orders_for_dispatch(self) -> List[OutboundOrder]:
        """Get orders ready for dispatch (packed orders)"""
        return self.get_all_orders(status="packed")

    def get_order_details(self, order_id: int) -> Optional[dict]:
        """Get detailed order information including items"""
        order = self.db.query(OutboundOrder).filter(
            OutboundOrder.id == order_id
        ).first()
        
        if not order:
            return None
        
        return {
            "order": order,
            "customer": order.customer,
            "items": [
                {
                    "item": item,
                    "product": item.product
                } for item in order.items
            ]
        }

    def check_stock_availability(self, order_id: int) -> dict:
        """Check if all items in order have sufficient stock"""
        order = self.db.query(OutboundOrder).filter(
            OutboundOrder.id == order_id
        ).first()
        
        if not order:
            return {"available": False, "message": "Order not found"}
        
        availability_issues = []
        
        for item in order.items:
            inventory = self.db.query(Inventory).filter(
                Inventory.product_id == item.product_id
            ).first()
            
            if not inventory or inventory.available_quantity < item.ordered_quantity:
                availability_issues.append({
                    "product": item.product.name,
                    "sku": item.product.sku,
                    "ordered": item.ordered_quantity,
                    "available": inventory.available_quantity if inventory else 0
                })
        
        return {
            "available": len(availability_issues) == 0,
            "issues": availability_issues,
            "message": "Stock available" if len(availability_issues) == 0 else "Insufficient stock for some items"
        }
