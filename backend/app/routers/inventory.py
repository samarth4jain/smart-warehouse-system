from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from ..database import get_db
from ..services.inventory_service import InventoryService

router = APIRouter()

class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    unit: str = "pcs"
    unit_price: float = 0.0
    reorder_level: int = 10
    location: Optional[str] = None

class StockUpdate(BaseModel):
    product_id: int
    quantity_change: int
    movement_type: str
    reason: Optional[str] = None

@router.get("/summary")
async def get_inventory_summary(db: Session = Depends(get_db)):
    """Get inventory summary with low stock alerts"""
    service = InventoryService(db)
    return service.get_inventory_summary()

@router.get("/products")
async def get_all_products(db: Session = Depends(get_db)):
    """Get all products"""
    service = InventoryService(db)
    return service.get_all_products()

@router.get("/products/{sku}")
async def get_product_by_sku(sku: str, db: Session = Depends(get_db)):
    """Get product by SKU"""
    service = InventoryService(db)
    product = service.get_product_by_sku(sku)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products")
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    service = InventoryService(db)
    try:
        return service.create_product(product.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stock/update")
async def update_stock(stock_update: StockUpdate, db: Session = Depends(get_db)):
    """Update stock levels"""
    service = InventoryService(db)
    success = service.update_stock(
        product_id=stock_update.product_id,
        quantity_change=stock_update.quantity_change,
        movement_type=stock_update.movement_type,
        reason=stock_update.reason
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update stock")
    
    return {"message": "Stock updated successfully"}

@router.get("/movements")
async def get_stock_movements(
    product_id: Optional[int] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get stock movement history"""
    service = InventoryService(db)
    return service.get_stock_movements(product_id=product_id, limit=limit)

@router.get("/low-stock")
async def get_low_stock_items(db: Session = Depends(get_db)):
    """Get items with low stock"""
    service = InventoryService(db)
    summary = service.get_inventory_summary()
    return summary["low_stock_alerts"]
