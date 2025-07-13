from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from ..database import get_db
from ..models.database_models import (
    Product, Inventory, InboundShipment, OutboundOrder, 
    StockMovement, ChatMessage
)
from ..services.inventory_service import InventoryService

router = APIRouter()

@router.get("/overview")
async def get_dashboard_overview(db: Session = Depends(get_db)):
    """Get dashboard overview with key metrics"""
    
    # Inventory metrics
    inventory_service = InventoryService(db)
    inventory_summary = inventory_service.get_inventory_summary()
    
    # Total products
    total_products = inventory_summary["total_products"]
    low_stock_count = inventory_summary["low_stock_count"]
    
    # Total inventory value (approximate)
    total_value = db.query(func.sum(Inventory.quantity * Product.unit_price)).join(
        Product, Inventory.product_id == Product.id
    ).scalar() or 0
    
    # Inbound shipments
    pending_inbound = db.query(func.count(InboundShipment.id)).filter(
        InboundShipment.status.in_(["pending", "arrived"])
    ).scalar()
    
    # Outbound orders
    pending_outbound = db.query(func.count(OutboundOrder.id)).filter(
        OutboundOrder.status.in_(["pending", "picking", "packed"])
    ).scalar()
    
    # Recent activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_movements = db.query(func.count(StockMovement.id)).filter(
        StockMovement.created_at >= week_ago
    ).scalar()
    
    # Chat activity
    total_chat_messages = db.query(func.count(ChatMessage.id)).scalar()
    recent_chats = db.query(func.count(ChatMessage.id)).filter(
        ChatMessage.created_at >= week_ago
    ).scalar()
    
    return {
        "inventory": {
            "total_products": total_products,
            "low_stock_items": low_stock_count,
            "total_value": round(total_value, 2)
        },
        "operations": {
            "pending_inbound": pending_inbound,
            "pending_outbound": pending_outbound,
            "recent_movements": recent_movements
        },
        "chatbot": {
            "total_messages": total_chat_messages,
            "recent_messages": recent_chats
        }
    }

@router.get("/inventory-alerts")
async def get_inventory_alerts(db: Session = Depends(get_db)):
    """Get inventory alerts and notifications"""
    inventory_service = InventoryService(db)
    summary = inventory_service.get_inventory_summary()
    
    alerts = []
    
    # Low stock alerts
    for item in summary["low_stock_alerts"]:
        alerts.append({
            "type": "low_stock",
            "severity": "warning",
            "message": f"{item['name']} (SKU: {item['sku']}) is running low",
            "details": {
                "available": item["available_quantity"],
                "reorder_level": item["reorder_level"],
                "product_id": item["product_id"]
            }
        })
    
    # Zero stock alerts
    zero_stock_items = [item for item in summary["inventory"] if item["available_quantity"] == 0]
    for item in zero_stock_items:
        alerts.append({
            "type": "out_of_stock",
            "severity": "critical",
            "message": f"{item['name']} (SKU: {item['sku']}) is out of stock",
            "details": {
                "product_id": item["product_id"]
            }
        })
    
    return {"alerts": alerts, "count": len(alerts)}

@router.get("/recent-activity")
async def get_recent_activity(limit: int = 20, db: Session = Depends(get_db)):
    """Get recent warehouse activity"""
    
    # Recent stock movements
    movements = db.query(StockMovement).join(
        Product, StockMovement.product_id == Product.id
    ).order_by(StockMovement.created_at.desc()).limit(limit).all()
    
    activities = []
    
    for movement in movements:
        product = movement.product
        activities.append({
            "type": "stock_movement",
            "timestamp": movement.created_at,
            "description": f"{movement.movement_type.title()}: {abs(movement.quantity)} {product.unit} of {product.name}",
            "details": {
                "product": product.name,
                "sku": product.sku,
                "quantity": movement.quantity,
                "movement_type": movement.movement_type,
                "reason": movement.reason
            }
        })
    
    # Sort by timestamp
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {"activities": activities[:limit]}

@router.get("/performance-metrics")
async def get_performance_metrics(days: int = 30, db: Session = Depends(get_db)):
    """Get performance metrics for the specified period"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Inbound performance
    total_shipments = db.query(func.count(InboundShipment.id)).filter(
        InboundShipment.created_at >= start_date
    ).scalar()
    
    completed_shipments = db.query(func.count(InboundShipment.id)).filter(
        and_(
            InboundShipment.created_at >= start_date,
            InboundShipment.status == "completed"
        )
    ).scalar()
    
    # Outbound performance
    total_orders = db.query(func.count(OutboundOrder.id)).filter(
        OutboundOrder.created_at >= start_date
    ).scalar()
    
    dispatched_orders = db.query(func.count(OutboundOrder.id)).filter(
        and_(
            OutboundOrder.created_at >= start_date,
            OutboundOrder.status.in_(["dispatched", "delivered"])
        )
    ).scalar()
    
    # Stock movements
    inbound_movements = db.query(func.count(StockMovement.id)).filter(
        and_(
            StockMovement.created_at >= start_date,
            StockMovement.movement_type == "inbound"
        )
    ).scalar()
    
    outbound_movements = db.query(func.count(StockMovement.id)).filter(
        and_(
            StockMovement.created_at >= start_date,
            StockMovement.movement_type == "outbound"
        )
    ).scalar()
    
    return {
        "period_days": days,
        "inbound": {
            "total_shipments": total_shipments,
            "completed_shipments": completed_shipments,
            "completion_rate": round((completed_shipments / total_shipments * 100) if total_shipments > 0 else 0, 2)
        },
        "outbound": {
            "total_orders": total_orders,
            "dispatched_orders": dispatched_orders,
            "dispatch_rate": round((dispatched_orders / total_orders * 100) if total_orders > 0 else 0, 2)
        },
        "movements": {
            "inbound_movements": inbound_movements,
            "outbound_movements": outbound_movements,
            "total_movements": inbound_movements + outbound_movements
        }
    }

@router.get("/top-products")
async def get_top_products(limit: int = 10, metric: str = "movement", db: Session = Depends(get_db)):
    """Get top products by various metrics"""
    
    if metric == "movement":
        # Most active products by stock movement
        query = db.query(
            Product.id,
            Product.sku,
            Product.name,
            func.count(StockMovement.id).label('movement_count'),
            func.sum(func.abs(StockMovement.quantity)).label('total_quantity')
        ).join(
            StockMovement, Product.id == StockMovement.product_id
        ).group_by(Product.id).order_by(
            func.count(StockMovement.id).desc()
        ).limit(limit)
        
        results = query.all()
        
        return {
            "metric": "movement",
            "products": [
                {
                    "product_id": result.id,
                    "sku": result.sku,
                    "name": result.name,
                    "movement_count": result.movement_count,
                    "total_quantity": result.total_quantity
                } for result in results
            ]
        }
    
    elif metric == "stock":
        # Products with highest stock levels
        query = db.query(
            Product.id,
            Product.sku,
            Product.name,
            Inventory.quantity,
            Inventory.available_quantity
        ).join(
            Inventory, Product.id == Inventory.product_id
        ).order_by(Inventory.quantity.desc()).limit(limit)
        
        results = query.all()
        
        return {
            "metric": "stock",
            "products": [
                {
                    "product_id": result.id,
                    "sku": result.sku,
                    "name": result.name,
                    "quantity": result.quantity,
                    "available_quantity": result.available_quantity
                } for result in results
            ]
        }
    
    else:
        raise HTTPException(status_code=400, detail="Invalid metric. Use 'movement' or 'stock'")

@router.get("/system-health")
async def get_system_health(db: Session = Depends(get_db)):
    """Get system health status"""
    
    try:
        # Database connectivity test
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = "error"
    
    # Check for any critical issues
    inventory_service = InventoryService(db)
    summary = inventory_service.get_inventory_summary()
    
    critical_issues = []
    
    # Check for out of stock items
    out_of_stock = len([item for item in summary["inventory"] if item["available_quantity"] == 0])
    if out_of_stock > 0:
        critical_issues.append(f"{out_of_stock} products are out of stock")
    
    # Check for high low stock percentage
    low_stock_percentage = (summary["low_stock_count"] / summary["total_products"] * 100) if summary["total_products"] > 0 else 0
    if low_stock_percentage > 20:
        critical_issues.append(f"{low_stock_percentage:.1f}% of products are below reorder level")
    
    return {
        "database": db_status,
        "critical_issues": critical_issues,
        "status": "healthy" if db_status == "healthy" and len(critical_issues) == 0 else "warning",
        "timestamp": datetime.utcnow()
    }
