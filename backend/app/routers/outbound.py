from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ..services.outbound_service import OutboundService

router = APIRouter()

class OutboundOrderCreate(BaseModel):
    order_number: str
    customer_id: int
    expected_dispatch_date: Optional[datetime] = None
    priority: str = "normal"
    delivery_address: Optional[str] = None
    notes: Optional[str] = None

class OutboundItemCreate(BaseModel):
    order_id: int
    product_id: int
    ordered_quantity: int
    unit_price: float = 0.0
    notes: Optional[str] = None

class PickItemRequest(BaseModel):
    picked_quantity: int

class PackItemRequest(BaseModel):
    packed_quantity: int

@router.get("/orders")
async def get_all_orders(status: Optional[str] = None, db: Session = Depends(get_db)):
    """Get all outbound orders"""
    service = OutboundService(db)
    return service.get_all_orders(status=status)

@router.get("/orders/pending")
async def get_pending_orders(db: Session = Depends(get_db)):
    """Get pending orders"""
    service = OutboundService(db)
    return service.get_pending_orders()

@router.get("/orders/picking")
async def get_orders_for_picking(db: Session = Depends(get_db)):
    """Get orders ready for picking"""
    service = OutboundService(db)
    return service.get_orders_for_picking()

@router.get("/orders/dispatch")
async def get_orders_for_dispatch(db: Session = Depends(get_db)):
    """Get orders ready for dispatch"""
    service = OutboundService(db)
    return service.get_orders_for_dispatch()

@router.get("/orders/{order_number}")
async def get_order_by_number(order_number: str, db: Session = Depends(get_db)):
    """Get order by number"""
    service = OutboundService(db)
    order = service.get_order_by_number(order_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders/details/{order_id}")
async def get_order_details(order_id: int, db: Session = Depends(get_db)):
    """Get detailed order information"""
    service = OutboundService(db)
    details = service.get_order_details(order_id)
    if not details:
        raise HTTPException(status_code=404, detail="Order not found")
    return details

@router.post("/orders")
async def create_order(order: OutboundOrderCreate, db: Session = Depends(get_db)):
    """Create a new outbound order"""
    service = OutboundService(db)
    try:
        return service.create_order(order.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/orders/{order_id}/items")
async def add_order_item(
    order_id: int, 
    item: OutboundItemCreate, 
    db: Session = Depends(get_db)
):
    """Add item to order"""
    service = OutboundService(db)
    try:
        item_data = item.dict()
        item_data['order_id'] = order_id
        return service.add_order_item(order_id, item_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/orders/{order_id}/status/{status}")
async def update_order_status(
    order_id: int, 
    status: str, 
    db: Session = Depends(get_db)
):
    """Update order status"""
    service = OutboundService(db)
    success = service.update_order_status(order_id, status)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update order status")
    return {"message": f"Order status updated to {status}"}

@router.post("/items/{item_id}/pick")
async def pick_item(
    item_id: int,
    pick_data: PickItemRequest,
    db: Session = Depends(get_db)
):
    """Update picked quantity for order item"""
    service = OutboundService(db)
    success = service.pick_order_item(item_id, pick_data.picked_quantity)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update picked quantity")
    
    return {"message": "Item picked quantity updated"}

@router.post("/items/{item_id}/pack")
async def pack_item(
    item_id: int,
    pack_data: PackItemRequest,
    db: Session = Depends(get_db)
):
    """Update packed quantity for order item"""
    service = OutboundService(db)
    success = service.pack_order_item(item_id, pack_data.packed_quantity)
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update packed quantity")
    
    return {"message": "Item packed quantity updated"}

@router.get("/orders/{order_id}/stock-check")
async def check_stock_availability(order_id: int, db: Session = Depends(get_db)):
    """Check stock availability for order"""
    service = OutboundService(db)
    return service.check_stock_availability(order_id)
