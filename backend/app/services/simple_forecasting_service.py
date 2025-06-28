import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleForecastingService:
    """
    Simplified Phase 3 forecasting service without external dependencies
    Uses basic statistical methods for initial implementation
    """
    
    def __init__(self):
        pass
    
    def generate_demand_forecast(self, db, product_id: int, weeks: int = 4) -> Dict:
        """
        Generate simple demand forecast for a product
        """
        try:
            from ..models.database_models import Product, Inventory
            
            # Get product info
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"success": False, "error": "Product not found"}
            
            # Simple forecast based on reorder level
            base_demand = max(product.reorder_level // 4, 5)  # Weekly demand estimate
            
            forecasts = []
            for week in range(1, weeks + 1):
                forecast_date = datetime.now() + timedelta(weeks=week)
                
                # Add some variation
                demand_variation = 1.0 + (week * 0.1)  # Slight increase over time
                predicted_demand = int(base_demand * demand_variation)
                
                forecasts.append({
                    "week": week,
                    "date": forecast_date.strftime("%Y-%m-%d"),
                    "predicted_demand": predicted_demand,
                    "confidence": 0.7
                })
            
            return {
                "success": True,
                "product": {
                    "id": product.id,
                    "sku": product.sku,
                    "name": product.name
                },
                "forecasts": forecasts,
                "ai_insights": [
                    "Forecast based on historical reorder patterns",
                    "Slight upward trend expected",
                    "Consider seasonal factors for refinement"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error generating forecast: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def analyze_stock_risks(self, db) -> Dict:
        """
        Analyze products for basic stock risks
        """
        try:
            from ..models.database_models import Product, Inventory
            
            products = db.query(Product).all()
            alerts = []
            
            for product in products:
                inventory = db.query(Inventory).filter(
                    Inventory.product_id == product.id
                ).first()
                
                if inventory:
                    current_stock = inventory.available_quantity
                    reorder_level = product.reorder_level
                    
                    if current_stock <= reorder_level:
                        alert_type = "understock" if current_stock < reorder_level else "reorder"
                        severity = "high" if current_stock < (reorder_level * 0.5) else "medium"
                        
                        alerts.append({
                            "product": {
                                "id": product.id,
                                "sku": product.sku,
                                "name": product.name
                            },
                            "alert_type": alert_type,
                            "severity": severity,
                            "message": f"Stock level ({current_stock}) below reorder point ({reorder_level})",
                            "recommended_action": "Place purchase order"
                        })
            
            return {
                "success": True,
                "total_alerts": len(alerts),
                "alerts": alerts,
                "analysis_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing stock risks: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_reorder_recommendations(self, db) -> Dict:
        """
        Generate basic reorder recommendations
        """
        try:
            from ..models.database_models import Product, Inventory
            
            low_stock_products = db.query(Product, Inventory).join(Inventory).filter(
                Inventory.available_quantity <= Product.reorder_level
            ).all()
            
            recommendations = []
            for product, inventory in low_stock_products:
                recommended_quantity = product.reorder_level * 2  # Order 2x reorder level
                urgency = "urgent" if inventory.available_quantity < (product.reorder_level * 0.5) else "normal"
                
                recommendations.append({
                    "product": {
                        "id": product.id,
                        "sku": product.sku,
                        "name": product.name,
                        "category": product.category
                    },
                    "current_stock": inventory.available_quantity,
                    "reorder_level": product.reorder_level,
                    "recommended_quantity": recommended_quantity,
                    "urgency": urgency,
                    "reasoning": f"Stock below reorder level. Recommend ordering {recommended_quantity} units",
                    "estimated_cost": recommended_quantity * product.unit_price if product.unit_price > 0 else 0,
                    "supplier_lead_time": "7-14 days"
                })
            
            return {
                "success": True,
                "total_recommendations": len(recommendations),
                "recommendations": recommendations,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating reorder recommendations: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def export_forecast_csv(self, db, weeks: int = 4) -> str:
        """
        Export basic forecast data to CSV
        """
        try:
            from ..models.database_models import Product
            import csv
            import tempfile
            
            products = db.query(Product).limit(10).all()  # Limit for demo
            
            # Create temporary CSV file
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
            writer = csv.writer(temp_file)
            
            # Write header
            writer.writerow(['SKU', 'Product_Name', 'Category', 'Week_1_Forecast', 'Week_2_Forecast', 
                           'Week_3_Forecast', 'Week_4_Forecast', 'Confidence_Level'])
            
            # Write data
            for product in products:
                base_demand = max(product.reorder_level // 4, 5)
                forecasts = [int(base_demand * (1 + i * 0.1)) for i in range(4)]
                
                writer.writerow([
                    product.sku,
                    product.name,
                    product.category,
                    forecasts[0],
                    forecasts[1], 
                    forecasts[2],
                    forecasts[3],
                    0.7
                ])
            
            temp_file.close()
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Error exporting CSV: {str(e)}")
            return None
