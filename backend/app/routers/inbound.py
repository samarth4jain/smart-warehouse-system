from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ..services.inbound_service import InboundService

router = APIRouter()

class InboundShipmentCreate(BaseModel):
    shipment_number: str
    vendor_id: int
    expected_date: Optional[datetime] = None
    driver_name: Optional[str] = None
    vehicle_number: Optional[str] = None
    notes: Optional[str] = None

class InboundItemCreate(BaseModel):
    shipment_id: int
    product_id: int
    expected_quantity: int
    unit_cost: float = 0.0
    batch_number: Optional[str] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None

class ReceiveItemRequest(BaseModel):
    received_quantity: int
    damaged_quantity: int = 0

@router.get("/shipments")
async def get_all_shipments(status: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all inbound shipments"""
    service = InboundService(db)
    return service.get_all_shipments(status=status)

@router.get("/shipments/pending")
async def get_pending_shipments(db: Session = Depends(get_db)):
    """Get pending shipments"""
    service = InboundService(db)
    return service.get_pending_shipments()

@router.get("/shipments/{shipment_number}")
async def get_shipment_by_number(shipment_number: str, db: Session = Depends(get_db)):
    """Get shipment by number"""
    service = InboundService(db)
    shipment = service.get_shipment_by_number(shipment_number)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

@router.get("/shipments/details/{shipment_id}")
async def get_shipment_details(shipment_id: int, db: Session = Depends(get_db)):
    """Get detailed shipment information"""
    service = InboundService(db)
    details = service.get_shipment_details(shipment_id)
    if not details:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return details

@router.post("/shipments")
async def create_shipment(shipment: InboundShipmentCreate, db: Session = Depends(get_db)):
    """Create a new inbound shipment"""
    service = InboundService(db)
    try:
        return service.create_shipment(shipment.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/shipments/{shipment_id}/items")
async def add_shipment_item(
    shipment_id: int, 
    item: InboundItemCreate, 
    db: Session = Depends(get_db)
):
    """Add item to shipment"""
    service = InboundService(db)
    try:
        item_data = item.dict()
        item_data['shipment_id'] = shipment_id
        return service.add_shipment_item(shipment_id, item_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/shipments/{shipment_id}/status/{status}")
async def update_shipment_status(
    shipment_id: int, 
    status: str, 
    db: Session = Depends(get_db)
):
    """Update shipment status"""
    service = InboundService(db)
    success = service.update_shipment_status(shipment_id, status)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update shipment status")
    return {"message": f"Shipment status updated to {status}"}

@router.post("/items/{item_id}/receive")
async def receive_item(
    item_id: int,
    receive_data: ReceiveItemRequest,
    db: Session = Depends(get_db)
):
    """Process received item and update inventory"""
    service = InboundService(db)
    success = service.receive_shipment_item(
        item_id=item_id,
        received_quantity=receive_data.received_quantity,
        damaged_quantity=receive_data.damaged_quantity
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to process received item")
    
    return {"message": "Item received and inventory updated"}

@router.put("/shipments/{shipment_id}/complete")
async def complete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    """Mark shipment as completed"""
    service = InboundService(db)
    success = service.complete_shipment(shipment_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to complete shipment")
    return {"message": "Shipment completed successfully"}
