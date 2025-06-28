from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.database_models import InboundShipment, InboundItem, Vendor, Product
from .inventory_service import InventoryService
from datetime import datetime

class InboundService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_service = InventoryService(db)

    def create_shipment(self, shipment_data: dict) -> InboundShipment:
        """Create a new inbound shipment"""
        shipment = InboundShipment(**shipment_data)
        self.db.add(shipment)
        self.db.commit()
        self.db.refresh(shipment)
        return shipment

    def get_shipment_by_number(self, shipment_number: str) -> Optional[InboundShipment]:
        """Get shipment by shipment number"""
        return self.db.query(InboundShipment).filter(
            InboundShipment.shipment_number == shipment_number
        ).first()

    def get_all_shipments(self, status: str = None) -> List[InboundShipment]:
        """Get all shipments, optionally filtered by status"""
        query = self.db.query(InboundShipment)
        if status:
            query = query.filter(InboundShipment.status == status)
        return query.order_by(InboundShipment.created_at.desc()).all()

    def update_shipment_status(self, shipment_id: int, status: str) -> bool:
        """Update shipment status"""
        try:
            shipment = self.db.query(InboundShipment).filter(
                InboundShipment.id == shipment_id
            ).first()
            
            if not shipment:
                return False
            
            shipment.status = status
            shipment.updated_at = datetime.utcnow()
            
            if status == "arrived":
                shipment.actual_arrival_date = datetime.utcnow()
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def add_shipment_item(self, shipment_id: int, item_data: dict) -> InboundItem:
        """Add item to shipment"""
        item_data['shipment_id'] = shipment_id
        item = InboundItem(**item_data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def receive_shipment_item(self, item_id: int, received_quantity: int, 
                            damaged_quantity: int = 0) -> bool:
        """Process received shipment item and update inventory"""
        try:
            item = self.db.query(InboundItem).filter(InboundItem.id == item_id).first()
            if not item:
                return False
            
            # Update item quantities
            item.received_quantity = received_quantity
            item.damaged_quantity = damaged_quantity
            
            # Update inventory
            usable_quantity = received_quantity - damaged_quantity
            if usable_quantity > 0:
                self.inventory_service.update_stock(
                    product_id=item.product_id,
                    quantity_change=usable_quantity,
                    movement_type="inbound",
                    reference_type="inbound_shipment",
                    reference_id=item.shipment_id,
                    reason=f"Received from shipment {item.shipment.shipment_number}"
                )
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            return False

    def complete_shipment(self, shipment_id: int) -> bool:
        """Mark shipment as completed"""
        return self.update_shipment_status(shipment_id, "completed")

    def get_pending_shipments(self) -> List[InboundShipment]:
        """Get all pending shipments"""
        return self.get_all_shipments(status="pending")

    def get_shipment_details(self, shipment_id: int) -> Optional[dict]:
        """Get detailed shipment information including items"""
        shipment = self.db.query(InboundShipment).filter(
            InboundShipment.id == shipment_id
        ).first()
        
        if not shipment:
            return None
        
        return {
            "shipment": shipment,
            "vendor": shipment.vendor,
            "items": [
                {
                    "item": item,
                    "product": item.product
                } for item in shipment.items
            ]
        }
