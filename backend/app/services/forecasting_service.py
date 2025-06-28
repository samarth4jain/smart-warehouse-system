import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import logging
import json
from ..models.database_models import (
    Product, SalesHistory, DemandForecast, StockAlert, 
    ProductVelocity, Inventory
)
from .openai_compatible_service import OpenAICompatibleService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ForecastingService:
    """
    Phase 3: AI-powered forecasting and demand prediction service
    Uses historical sales data and OpenAI to predict demand and flag stock risks
    """
    
    def __init__(self):
        self.llm_service = OpenAICompatibleService()
        
    def ingest_sales_data(self, db: Session, sales_data: List[Dict]) -> Dict:
        """
        Ingest historical sales/dispatch data from Excel/API
        """
        try:
            ingested_count = 0
            errors = []
            
            for record in sales_data:
                try:
                    # Find product by SKU
                    product = db.query(Product).filter(
                        Product.sku == record.get('sku')
                    ).first()
                    
                    if not product:
                        errors.append(f"Product not found for SKU: {record.get('sku')}")
                        continue
                    
                    # Create sales history record
                    sales_record = SalesHistory(
                        product_id=product.id,
                        quantity_sold=record.get('quantity_sold', 0),
                        sale_date=pd.to_datetime(record.get('sale_date')),
                        unit_price=record.get('unit_price', 0.0),
                        total_value=record.get('total_value', 0.0),
                        customer_type=record.get('customer_type', 'retail'),
                        season=self._get_season(pd.to_datetime(record.get('sale_date'))),
                        channel=record.get('channel', 'store')
                    )
                    
                    db.add(sales_record)
                    ingested_count += 1
                    
                except Exception as e:
                    errors.append(f"Error processing record {record}: {str(e)}")
                    
            db.commit()
            
            return {
                "success": True,
                "ingested_count": ingested_count,
                "errors": errors,
                "message": f"Successfully ingested {ingested_count} sales records"
            }
            
        except Exception as e:
            logger.error(f"Error ingesting sales data: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to ingest sales data"
            }
    
    def generate_demand_forecast(self, db: Session, product_id: int, weeks: int = 4) -> Dict:
        """
        Generate weekly demand forecast for a product using AI
        """
        try:
            # Get product info
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"success": False, "error": "Product not found"}
            
            # Get historical sales data
            historical_data = self._get_historical_sales(db, product_id)
            
            if not historical_data:
                return self._generate_simple_forecast(db, product, weeks)
            
            # Prepare data for AI analysis
            sales_summary = self._prepare_sales_summary(historical_data)
            
            # Use AI to predict demand
            ai_forecast = self._get_ai_forecast(product, sales_summary, weeks)
            
            # Save forecasts to database
            forecasts = []
            for week in range(1, weeks + 1):
                forecast_date = datetime.now() + timedelta(weeks=week)
                predicted_demand = ai_forecast.get(f'week_{week}', 0)
                confidence = ai_forecast.get('confidence', 0.7)
                
                forecast = DemandForecast(
                    product_id=product_id,
                    forecast_date=forecast_date,
                    predicted_demand=predicted_demand,
                    confidence_level=confidence,
                    forecast_type="weekly",
                    ai_generated=True,
                    model_version="gpt-4-turbo"
                )
                
                db.add(forecast)
                forecasts.append({
                    "week": week,
                    "date": forecast_date.strftime("%Y-%m-%d"),
                    "predicted_demand": predicted_demand,
                    "confidence": confidence
                })
            
            db.commit()
            
            return {
                "success": True,
                "product": {
                    "id": product.id,
                    "sku": product.sku,
                    "name": product.name
                },
                "forecasts": forecasts,
                "ai_insights": ai_forecast.get('insights', [])
            }
            
        except Exception as e:
            logger.error(f"Error generating forecast: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def analyze_stock_risks(self, db: Session) -> Dict:
        """
        Analyze all products for overstock/understock risks using AI
        """
        try:
            products = db.query(Product).all()
            alerts = []
            
            for product in products:
                # Get current inventory
                inventory = db.query(Inventory).filter(
                    Inventory.product_id == product.id
                ).first()
                
                if not inventory:
                    continue
                
                # Get recent forecasts
                recent_forecast = db.query(DemandForecast).filter(
                    DemandForecast.product_id == product.id,
                    DemandForecast.forecast_date >= datetime.now()
                ).order_by(DemandForecast.forecast_date).first()
                
                # Analyze risk using AI
                risk_analysis = self._analyze_product_risk(
                    product, inventory, recent_forecast
                )
                
                if risk_analysis.get('alert_needed'):
                    alert = StockAlert(
                        product_id=product.id,
                        alert_type=risk_analysis['alert_type'],
                        severity=risk_analysis['severity'],
                        current_stock=inventory.available_quantity,
                        recommended_stock=risk_analysis.get('recommended_stock'),
                        predicted_stockout_date=risk_analysis.get('stockout_date'),
                        reorder_quantity=risk_analysis.get('reorder_quantity'),
                        reorder_urgency=risk_analysis.get('urgency', 'normal'),
                        ai_generated=True,
                        message=risk_analysis.get('message')
                    )
                    
                    db.add(alert)
                    alerts.append({
                        "product": {
                            "id": product.id,
                            "sku": product.sku,
                            "name": product.name
                        },
                        "alert_type": risk_analysis['alert_type'],
                        "severity": risk_analysis['severity'],
                        "message": risk_analysis.get('message'),
                        "recommended_action": risk_analysis.get('recommended_action')
                    })
            
            db.commit()
            
            return {
                "success": True,
                "total_alerts": len(alerts),
                "alerts": alerts,
                "analysis_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing stock risks: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_reorder_recommendations(self, db: Session) -> Dict:
        """
        Generate AI-powered reorder recommendations
        """
        try:
            # Get products with low stock or upcoming stockouts
            low_stock_products = self._get_low_stock_products(db)
            
            recommendations = []
            for product_data in low_stock_products:
                product = product_data['product']
                inventory = product_data['inventory']
                
                # Get forecast data
                forecast = db.query(DemandForecast).filter(
                    DemandForecast.product_id == product.id,
                    DemandForecast.forecast_date >= datetime.now()
                ).order_by(DemandForecast.forecast_date).first()
                
                # Generate AI recommendation
                ai_recommendation = self._get_ai_reorder_recommendation(
                    product, inventory, forecast
                )
                
                recommendations.append({
                    "product": {
                        "id": product.id,
                        "sku": product.sku,
                        "name": product.name,
                        "category": product.category
                    },
                    "current_stock": inventory.available_quantity,
                    "reorder_level": product.reorder_level,
                    "recommended_quantity": ai_recommendation.get('quantity', 0),
                    "urgency": ai_recommendation.get('urgency', 'normal'),
                    "reasoning": ai_recommendation.get('reasoning'),
                    "estimated_cost": ai_recommendation.get('estimated_cost'),
                    "supplier_lead_time": ai_recommendation.get('lead_time', '7-14 days')
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
    
    def export_forecast_csv(self, db: Session, weeks: int = 4) -> str:
        """
        Export weekly demand forecasts to CSV format
        """
        try:
            # Get all recent forecasts
            forecasts = db.query(DemandForecast, Product).join(Product).filter(
                DemandForecast.forecast_date >= datetime.now(),
                DemandForecast.forecast_date <= datetime.now() + timedelta(weeks=weeks)
            ).all()
            
            # Convert to DataFrame
            data = []
            for forecast, product in forecasts:
                data.append({
                    'SKU': product.sku,
                    'Product_Name': product.name,
                    'Category': product.category,
                    'Forecast_Date': forecast.forecast_date.strftime('%Y-%m-%d'),
                    'Predicted_Demand': forecast.predicted_demand,
                    'Confidence_Level': forecast.confidence_level,
                    'Current_Stock': self._get_current_stock(db, product.id),
                    'Reorder_Level': product.reorder_level
                })
            
            df = pd.DataFrame(data)
            
            # Generate CSV filename
            filename = f"demand_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = f"/tmp/{filename}"
            
            # Save to CSV
            df.to_csv(filepath, index=False)
            
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting forecast CSV: {str(e)}")
            return None
    
    # Helper methods
    def _get_historical_sales(self, db: Session, product_id: int) -> List[Dict]:
        """Get historical sales data for a product"""
        sales = db.query(SalesHistory).filter(
            SalesHistory.product_id == product_id
        ).order_by(desc(SalesHistory.sale_date)).limit(100).all()
        
        return [
            {
                "date": sale.sale_date,
                "quantity": sale.quantity_sold,
                "value": sale.total_value,
                "season": sale.season,
                "channel": sale.channel
            }
            for sale in sales
        ]
    
    def _prepare_sales_summary(self, historical_data: List[Dict]) -> str:
        """Prepare sales data summary for AI analysis"""
        if not historical_data:
            return "No historical sales data available"
        
        df = pd.DataFrame(historical_data)
        
        summary = f"""
        Sales Analysis Summary:
        - Total sales records: {len(df)}
        - Date range: {df['date'].min()} to {df['date'].max()}
        - Average weekly sales: {df['quantity'].mean():.1f} units
        - Peak sales: {df['quantity'].max()} units
        - Minimum sales: {df['quantity'].min()} units
        - Total quantity sold: {df['quantity'].sum()} units
        - Average unit value: ${df['value'].mean():.2f}
        - Seasonal patterns: {df.groupby('season')['quantity'].mean().to_dict()}
        - Channel performance: {df.groupby('channel')['quantity'].mean().to_dict()}
        """
        
        return summary
    
    def _get_ai_forecast(self, product: Product, sales_summary: str, weeks: int) -> Dict:
        """Use AI to generate demand forecast"""
        try:
            prompt = f"""
            As an inventory management expert, analyze the following product and sales data to predict weekly demand:
            
            Product Information:
            - SKU: {product.sku}
            - Name: {product.name}
            - Category: {product.category}
            - Current Reorder Level: {product.reorder_level}
            
            Historical Sales Data:
            {sales_summary}
            
            Please provide a {weeks}-week demand forecast with:
            1. Predicted weekly demand for each week
            2. Confidence level (0-1)
            3. Key insights and factors influencing the forecast
            4. Seasonal or trend considerations
            
            Return your response as JSON with this structure:
            {{
                "week_1": <predicted_demand>,
                "week_2": <predicted_demand>,
                "week_3": <predicted_demand>,
                "week_4": <predicted_demand>,
                "confidence": <0-1>,
                "insights": ["insight1", "insight2", "insight3"],
                "trend": "increasing/decreasing/stable",
                "seasonality_factor": <factor>
            }}
            """
            
            response = self.llm_service.get_completion(prompt)
            
            # Parse JSON response
            try:
                forecast_data = json.loads(response)
                return forecast_data
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return self._parse_text_forecast(response, weeks)
                
        except Exception as e:
            logger.error(f"Error getting AI forecast: {str(e)}")
            return self._generate_simple_forecast_data(weeks)
    
    def _analyze_product_risk(self, product: Product, inventory: Inventory, forecast) -> Dict:
        """Analyze stock risk for a product using AI"""
        try:
            current_stock = inventory.available_quantity
            reorder_level = product.reorder_level
            
            forecast_demand = forecast.predicted_demand if forecast else product.reorder_level
            
            prompt = f"""
            Analyze stock risk for this product:
            
            Product: {product.name} (SKU: {product.sku})
            Current Stock: {current_stock} units
            Reorder Level: {reorder_level} units
            Predicted Weekly Demand: {forecast_demand} units
            Category: {product.category}
            
            Determine:
            1. Risk level (low/medium/high/critical)
            2. Alert type (overstock/understock/reorder)
            3. Recommended stock level
            4. Urgency (low/normal/urgent)
            5. Specific recommendation message
            
            Return JSON:
            {{
                "alert_needed": true/false,
                "alert_type": "overstock/understock/reorder",
                "severity": "low/medium/high/critical",
                "recommended_stock": <number>,
                "reorder_quantity": <number>,
                "urgency": "low/normal/urgent",
                "message": "detailed message",
                "recommended_action": "specific action to take"
            }}
            """
            
            response = self.llm_service.get_completion(prompt)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._generate_basic_risk_analysis(current_stock, reorder_level, forecast_demand)
                
        except Exception as e:
            logger.error(f"Error analyzing product risk: {str(e)}")
            return {"alert_needed": False}
    
    def _get_ai_reorder_recommendation(self, product: Product, inventory: Inventory, forecast) -> Dict:
        """Get AI-powered reorder recommendation"""
        try:
            prompt = f"""
            Generate a reorder recommendation for:
            
            Product: {product.name} (SKU: {product.sku})
            Category: {product.category}
            Current Stock: {inventory.available_quantity} units
            Reorder Level: {product.reorder_level} units
            Unit Price: ${product.unit_price}
            Predicted Demand: {forecast.predicted_demand if forecast else 'Unknown'} units/week
            
            Provide recommendation with:
            1. Optimal reorder quantity
            2. Urgency level
            3. Cost estimate
            4. Reasoning
            
            Return JSON:
            {{
                "quantity": <number>,
                "urgency": "low/normal/urgent",
                "reasoning": "explanation",
                "estimated_cost": <number>,
                "lead_time": "estimated delivery time"
            }}
            """
            
            response = self.llm_service.get_completion(prompt)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._generate_basic_reorder_recommendation(product, inventory)
                
        except Exception as e:
            logger.error(f"Error getting reorder recommendation: {str(e)}")
            return self._generate_basic_reorder_recommendation(product, inventory)
    
    def _generate_simple_forecast(self, db: Session, product: Product, weeks: int) -> Dict:
        """Generate simple forecast when no historical data is available"""
        base_demand = product.reorder_level // 2  # Simple heuristic
        
        forecasts = []
        for week in range(1, weeks + 1):
            forecast_date = datetime.now() + timedelta(weeks=week)
            
            forecast = DemandForecast(
                product_id=product.id,
                forecast_date=forecast_date,
                predicted_demand=base_demand,
                confidence_level=0.5,
                forecast_type="weekly",
                ai_generated=False,
                model_version="simple_heuristic"
            )
            
            db.add(forecast)
            forecasts.append({
                "week": week,
                "date": forecast_date.strftime("%Y-%m-%d"),
                "predicted_demand": base_demand,
                "confidence": 0.5
            })
        
        db.commit()
        
        return {
            "success": True,
            "product": {"id": product.id, "sku": product.sku, "name": product.name},
            "forecasts": forecasts,
            "ai_insights": ["Forecast based on reorder level due to limited historical data"]
        }
    
    def _get_season(self, date: datetime) -> str:
        """Determine season from date"""
        month = date.month
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"
    
    def _get_low_stock_products(self, db: Session) -> List[Dict]:
        """Get products with low stock levels"""
        products = db.query(Product, Inventory).join(Inventory).filter(
            Inventory.available_quantity <= Product.reorder_level
        ).all()
        
        return [
            {
                "product": product,
                "inventory": inventory
            }
            for product, inventory in products
        ]
    
    def _get_current_stock(self, db: Session, product_id: int) -> int:
        """Get current stock for a product"""
        inventory = db.query(Inventory).filter(
            Inventory.product_id == product_id
        ).first()
        
        return inventory.available_quantity if inventory else 0
    
    def _generate_simple_forecast_data(self, weeks: int) -> Dict:
        """Generate fallback forecast data"""
        return {
            f"week_{i}": 10 for i in range(1, weeks + 1)
        } | {
            "confidence": 0.5,
            "insights": ["Basic forecast due to AI service unavailability"],
            "trend": "stable"
        }
    
    def _parse_text_forecast(self, response: str, weeks: int) -> Dict:
        """Parse text response when JSON parsing fails"""
        # Simple parsing logic for text responses
        return self._generate_simple_forecast_data(weeks)
    
    def _generate_basic_risk_analysis(self, current_stock: int, reorder_level: int, forecast_demand: int) -> Dict:
        """Generate basic risk analysis when AI is unavailable"""
        if current_stock <= reorder_level:
            return {
                "alert_needed": True,
                "alert_type": "understock",
                "severity": "medium",
                "recommended_stock": reorder_level * 2,
                "reorder_quantity": reorder_level,
                "urgency": "normal",
                "message": f"Stock level ({current_stock}) below reorder point ({reorder_level})",
                "recommended_action": "Place reorder immediately"
            }
        return {"alert_needed": False}
    
    def _generate_basic_reorder_recommendation(self, product: Product, inventory: Inventory) -> Dict:
        """Generate basic reorder recommendation when AI is unavailable"""
        quantity = max(product.reorder_level, 20)
        return {
            "quantity": quantity,
            "urgency": "normal",
            "reasoning": "Based on reorder level and safety stock calculations",
            "estimated_cost": quantity * product.unit_price,
            "lead_time": "7-14 days"
        }
