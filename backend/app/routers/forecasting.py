from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import json
from ..database import get_db
from ..services.forecasting_service import ForecastingService
from ..services.space_optimization_service import SpaceOptimizationService
from ..services.enhanced_analytics_service import EnhancedAnalyticsService

router = APIRouter()

# Pydantic models for Phase 3
class SalesDataInput(BaseModel):
    sku: str
    quantity_sold: int
    sale_date: str
    unit_price: Optional[float] = 0.0
    total_value: Optional[float] = 0.0
    customer_type: Optional[str] = "retail"
    channel: Optional[str] = "store"

class ForecastRequest(BaseModel):
    product_id: int
    weeks: int = 4

class ForecastResponse(BaseModel):
    success: bool
    product: dict
    forecasts: List[dict]
    ai_insights: List[str]

class StockAlertResponse(BaseModel):
    success: bool
    total_alerts: int
    alerts: List[dict]
    analysis_date: str

class ReorderRecommendationResponse(BaseModel):
    success: bool
    total_recommendations: int
    recommendations: List[dict]
    generated_at: str

class SpaceOptimizationResponse(BaseModel):
    success: bool
    total_recommendations: int
    recommendations: List[dict]
    current_layout_efficiency: str

# Ultra-Enhanced Analytics Response Models
class UltraAnalyticsResponse(BaseModel):
    success: bool
    analysis_type: str
    insights: dict
    recommendations: List[dict]
    confidence_score: float
    generated_at: str

class CognitiveInsightsResponse(BaseModel):
    success: bool
    cognitive_analysis: dict
    strategic_insights: List[dict]
    innovation_opportunities: List[dict]
    risk_assessment: dict

class PredictiveAnalyticsResponse(BaseModel):
    success: bool
    predictions: dict
    trends: List[dict]
    market_intelligence: dict
    business_impact: dict

# Initialize services
forecasting_service = ForecastingService()
space_service = SpaceOptimizationService()
ultra_analytics_service = EnhancedAnalyticsService()

# Forecasting endpoints
@router.post("/forecast/ingest-sales", summary="Ingest Sales Data")
async def ingest_sales_data(
    sales_data: List[SalesDataInput],
    db: Session = Depends(get_db)
):
    """
    Ingest historical sales/dispatch data for forecasting
    """
    try:
        # Convert Pydantic models to dict for service
        sales_data_dict = [data.dict() for data in sales_data]
        
        result = forecasting_service.ingest_sales_data(db, sales_data_dict)
        
        if result["success"]:
            return {
                "message": result["message"],
                "ingested_count": result["ingested_count"],
                "errors": result.get("errors", [])
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting sales data: {str(e)}")

@router.post("/forecast/upload-sales-csv", summary="Upload Sales Data CSV")
async def upload_sales_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and ingest sales data from CSV file
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read CSV file
        contents = await file.read()
        
        # Use pandas to parse CSV
        import io
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Convert to expected format
        sales_data = []
        for _, row in df.iterrows():
            sales_data.append({
                "sku": row.get("sku", ""),
                "quantity_sold": int(row.get("quantity_sold", 0)),
                "sale_date": row.get("sale_date", ""),
                "unit_price": float(row.get("unit_price", 0.0)),
                "total_value": float(row.get("total_value", 0.0)),
                "customer_type": row.get("customer_type", "retail"),
                "channel": row.get("channel", "store")
            })
        
        result = forecasting_service.ingest_sales_data(db, sales_data)
        
        return {
            "message": f"Successfully processed {file.filename}",
            "ingested_count": result["ingested_count"],
            "errors": result.get("errors", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")

@router.post("/forecast/generate", response_model=ForecastResponse, summary="Generate Demand Forecast")
async def generate_demand_forecast(
    request: ForecastRequest,
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered weekly demand forecast for a product
    """
    try:
        result = forecasting_service.generate_demand_forecast(
            db, request.product_id, request.weeks
        )
        
        if result["success"]:
            return ForecastResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")

@router.get("/forecast/all-products", summary="Generate Forecasts for All Products")
async def generate_all_forecasts(
    weeks: int = 4,
    db: Session = Depends(get_db)
):
    """
    Generate forecasts for all products in the system
    """
    try:
        from ..models.database_models import Product
        
        products = db.query(Product).all()
        forecasts = []
        errors = []
        
        for product in products:
            try:
                result = forecasting_service.generate_demand_forecast(db, product.id, weeks)
                if result["success"]:
                    forecasts.append(result)
                else:
                    errors.append(f"Product {product.sku}: {result['error']}")
            except Exception as e:
                errors.append(f"Product {product.sku}: {str(e)}")
        
        return {
            "success": True,
            "total_products": len(products),
            "successful_forecasts": len(forecasts),
            "forecasts": forecasts,
            "errors": errors
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating all forecasts: {str(e)}")

@router.get("/forecast/stock-risks", response_model=StockAlertResponse, summary="Analyze Stock Risks")
async def analyze_stock_risks(db: Session = Depends(get_db)):
    """
    Analyze all products for overstock/understock risks using AI
    """
    try:
        result = forecasting_service.analyze_stock_risks(db)
        
        if result["success"]:
            return StockAlertResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing stock risks: {str(e)}")

@router.get("/forecast/reorder-recommendations", response_model=ReorderRecommendationResponse, summary="Get Reorder Recommendations")
async def get_reorder_recommendations(db: Session = Depends(get_db)):
    """
    Generate AI-powered reorder recommendations
    """
    try:
        result = forecasting_service.generate_reorder_recommendations(db)
        
        if result["success"]:
            return ReorderRecommendationResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.get("/forecast/export-csv", summary="Export Forecasts to CSV")
async def export_forecast_csv(
    weeks: int = 4,
    db: Session = Depends(get_db)
):
    """
    Export weekly demand forecasts to CSV file
    """
    try:
        from fastapi.responses import FileResponse
        
        filepath = forecasting_service.export_forecast_csv(db, weeks)
        
        if filepath:
            return FileResponse(
                filepath,
                media_type='text/csv',
                filename=f"demand_forecast_{datetime.now().strftime('%Y%m%d')}.csv"
            )
        else:
            raise HTTPException(status_code=500, detail="Error generating CSV file")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting CSV: {str(e)}")

# Space Optimization endpoints
@router.get("/space/analyze-velocity", summary="Analyze Product Velocity")
async def analyze_product_velocity(db: Session = Depends(get_db)):
    """
    Analyze product movement velocity to categorize fast/slow moving items
    """
    try:
        result = space_service.analyze_product_velocity(db)
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing velocity: {str(e)}")

@router.get("/space/layout-optimization", response_model=SpaceOptimizationResponse, summary="Generate Layout Optimization")
async def generate_layout_optimization(db: Session = Depends(get_db)):
    """
    Generate AI-powered layout optimization recommendations
    """
    try:
        result = space_service.generate_layout_optimization(db)
        
        if result["success"]:
            return SpaceOptimizationResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating layout optimization: {str(e)}")

@router.get("/space/category-grouping", summary="Suggest Category Grouping")
async def suggest_category_grouping(db: Session = Depends(get_db)):
    """
    Suggest logical product grouping by category and volume
    """
    try:
        result = space_service.suggest_category_grouping(db)
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error suggesting category grouping: {str(e)}")

@router.get("/space/fast-moving-optimization", summary="Optimize Fast-Moving Placement")
async def optimize_fast_moving_placement(db: Session = Depends(get_db)):
    """
    Optimize placement of fast-moving goods near exit/entrance
    """
    try:
        result = space_service.optimize_fast_moving_placement(db)
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing fast-moving placement: {str(e)}")

@router.get("/space/comprehensive-plan", summary="Generate Comprehensive Space Optimization Plan")
async def generate_comprehensive_plan(db: Session = Depends(get_db)):
    """
    Generate comprehensive text-based space optimization plan
    """
    try:
        result = space_service.generate_space_optimization_plan(db)
        
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating comprehensive plan: {str(e)}")

# Ultra-Enhanced Analytics Endpoints
@router.get("/analytics/ultra/multi-dimensional", response_model=UltraAnalyticsResponse, 
           summary="Multi-Dimensional Business Intelligence")
async def get_multi_dimensional_analytics(
    analysis_type: str = "comprehensive",
    db: Session = Depends(get_db)
):
    """
    Get revolutionary multi-dimensional business intelligence analysis
    """
    try:
        result = ultra_analytics_service.multi_dimensional_analysis(db, analysis_type)
        return UltraAnalyticsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in multi-dimensional analysis: {str(e)}")

@router.get("/analytics/ultra/predictive", response_model=PredictiveAnalyticsResponse, 
           summary="Predictive Business Intelligence")
async def get_predictive_analytics(
    horizon: int = 12,
    db: Session = Depends(get_db)
):
    """
    Get advanced predictive analytics with market intelligence
    """
    try:
        result = ultra_analytics_service.predictive_intelligence(db, horizon)
        return PredictiveAnalyticsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in predictive analytics: {str(e)}")

@router.get("/analytics/ultra/cognitive", response_model=CognitiveInsightsResponse, 
           summary="Cognitive Business Insights")
async def get_cognitive_insights(
    focus_area: str = "strategic",
    db: Session = Depends(get_db)
):
    """
    Get cognitive insights and strategic business intelligence
    """
    try:
        result = ultra_analytics_service.cognitive_insights(db, focus_area)
        return CognitiveInsightsResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in cognitive analysis: {str(e)}")

@router.get("/analytics/ultra/optimization-engine", summary="AI Optimization Engine")
async def get_optimization_recommendations(
    scope: str = "full_warehouse",
    db: Session = Depends(get_db)
):
    """
    Get AI-powered optimization engine recommendations
    """
    try:
        result = ultra_analytics_service.optimization_engine(db, scope)
        return {
            "success": True,
            "optimization_scope": scope,
            "recommendations": result.get("recommendations", []),
            "impact_analysis": result.get("impact_analysis", {}),
            "implementation_roadmap": result.get("roadmap", []),
            "roi_projections": result.get("roi", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in optimization engine: {str(e)}")

@router.get("/analytics/ultra/strategic-dashboard", summary="Strategic Intelligence Dashboard")
async def get_strategic_dashboard(
    db: Session = Depends(get_db)
):
    """
    Get comprehensive strategic intelligence for executive dashboard
    """
    try:
        # Get all types of ultra analytics
        multi_dim = ultra_analytics_service.multi_dimensional_analysis(db, "strategic")
        predictive = ultra_analytics_service.predictive_intelligence(db, 6)
        cognitive = ultra_analytics_service.cognitive_insights(db, "strategic")
        optimization = ultra_analytics_service.optimization_engine(db, "strategic")
        
        return {
            "success": True,
            "dashboard_type": "strategic_intelligence",
            "executive_summary": {
                "business_health_score": multi_dim.get("insights", {}).get("health_score", 85),
                "growth_trajectory": predictive.get("predictions", {}).get("growth_rate", 12.5),
                "innovation_index": cognitive.get("innovation_opportunities", []),
                "optimization_potential": optimization.get("impact_analysis", {}).get("efficiency_gain", 18.7)
            },
            "key_insights": multi_dim.get("insights", {}),
            "strategic_recommendations": cognitive.get("strategic_insights", []),
            "predictive_trends": predictive.get("trends", []),
            "optimization_priorities": optimization.get("recommendations", [])[:5],
            "risk_assessment": cognitive.get("risk_assessment", {}),
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating strategic dashboard: {str(e)}")

# Dashboard endpoints
@router.get("/dashboard/overview", summary="Phase 3 Dashboard Overview")
async def get_phase3_dashboard(db: Session = Depends(get_db)):
    """
    Get comprehensive Phase 3 dashboard with forecasting and space optimization data
    """
    try:
        # Get velocity analysis
        velocity_result = space_service.analyze_product_velocity(db)
        
        # Get recent forecasts
        from ..models.database_models import DemandForecast, Product
        recent_forecasts = db.query(DemandForecast, Product).join(Product).filter(
            DemandForecast.forecast_date >= datetime.now()
        ).limit(10).all()
        
        # Get stock alerts
        from ..models.database_models import StockAlert
        active_alerts = db.query(StockAlert).filter(
            StockAlert.resolved == False
        ).limit(10).all()
        
        # Get space optimizations
        from ..models.database_models import SpaceOptimization
        pending_optimizations = db.query(SpaceOptimization).filter(
            SpaceOptimization.status == "pending"
        ).limit(10).all()
        
        return {
            "success": True,
            "overview": {
                "velocity_distribution": velocity_result.get("velocity_distribution", {}),
                "total_forecasts": len(recent_forecasts),
                "active_alerts": len(active_alerts),
                "pending_optimizations": len(pending_optimizations)
            },
            "recent_forecasts": [
                {
                    "product": {"sku": product.sku, "name": product.name},
                    "forecast_date": forecast.forecast_date.isoformat(),
                    "predicted_demand": forecast.predicted_demand,
                    "confidence": forecast.confidence_level
                }
                for forecast, product in recent_forecasts
            ],
            "active_alerts": [
                {
                    "product_id": alert.product_id,
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "message": alert.message
                }
                for alert in active_alerts
            ],
            "pending_optimizations": [
                {
                    "title": opt.title,
                    "priority": opt.priority,
                    "expected_benefit": opt.expected_benefit
                }
                for opt in pending_optimizations
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dashboard: {str(e)}")

@router.get("/health", summary="Phase 3 Health Check")
async def phase3_health_check():
    """
    Health check for Phase 3 services
    """
    try:
        # Check if services can be initialized
        forecasting_available = True
        space_optimization_available = True
        
        try:
            forecasting_service = ForecastingService()
        except Exception:
            forecasting_available = False
        
        try:
            space_service = SpaceOptimizationService()
        except Exception:
            space_optimization_available = False
        
        return {
            "status": "healthy",
            "phase": "Phase 3: Forecasting + Space Planning",
            "services": {
                "forecasting_service": forecasting_available,
                "space_optimization_service": space_optimization_available,
                "ai_integration": True
            },
            "features": [
                "Weekly demand forecasting",
                "Stock risk analysis",
                "AI-generated reorder recommendations",
                "Product velocity analysis",
                "Layout optimization",
                "Category grouping suggestions",
                "Fast-moving goods optimization",
                "Comprehensive space planning"
            ]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
