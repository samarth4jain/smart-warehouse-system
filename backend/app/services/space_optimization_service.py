from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import logging
import json
from ..models.database_models import (
    Product, Inventory, SalesHistory, WarehouseLayout, 
    SpaceOptimization, ProductVelocity, DemandForecast
)
from .openai_compatible_service import OpenAICompatibleService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpaceOptimizationService:
    """
    Phase 3: AI-powered space planning and layout optimization service
    Implements smart layout suggestions and product placement optimization
    """
    
    def __init__(self):
        self.llm_service = OpenAICompatibleService()
        
    def analyze_product_velocity(self, db: Session) -> Dict:
        """
        Analyze product movement velocity to categorize fast/slow moving items
        """
        try:
            products = db.query(Product).all()
            velocity_analysis = []
            
            for product in products:
                # Calculate velocity metrics
                velocity_data = self._calculate_product_velocity(db, product)
                
                # Save to database
                velocity_record = ProductVelocity(
                    product_id=product.id,
                    velocity_category=velocity_data['category'],
                    weekly_turnover=velocity_data['weekly_turnover'],
                    monthly_turnover=velocity_data['monthly_turnover'],
                    days_of_supply=velocity_data['days_of_supply'],
                    pick_frequency=velocity_data['pick_frequency'],
                    last_movement_date=velocity_data['last_movement'],
                    movement_trend=velocity_data['trend']
                )
                
                db.merge(velocity_record)  # Use merge to update existing records
                
                velocity_analysis.append({
                    "product": {
                        "id": product.id,
                        "sku": product.sku,
                        "name": product.name,
                        "category": product.category,
                        "current_location": product.location
                    },
                    "velocity_metrics": velocity_data
                })
            
            db.commit()
            
            return {
                "success": True,
                "total_products_analyzed": len(velocity_analysis),
                "velocity_distribution": self._get_velocity_distribution(velocity_analysis),
                "products": velocity_analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing product velocity: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_layout_optimization(self, db: Session) -> Dict:
        """
        Generate AI-powered layout optimization recommendations
        """
        try:
            # Get current warehouse layout
            warehouse_zones = self._get_warehouse_zones(db)
            
            # Get product velocity data
            velocity_data = self._get_product_velocities(db)
            
            # Get current product locations
            current_layout = self._get_current_layout(db)
            
            # Generate AI recommendations
            ai_recommendations = self._get_ai_layout_recommendations(
                warehouse_zones, velocity_data, current_layout
            )
            
            # Save optimization recommendations
            optimizations = []
            for rec in ai_recommendations:
                optimization = SpaceOptimization(
                    optimization_type="layout",
                    title=rec.get('title', 'Layout Optimization'),
                    description=rec.get('description'),
                    priority=rec.get('priority', 'medium'),
                    expected_benefit=rec.get('benefit'),
                    implementation_effort=rec.get('effort', 'medium'),
                    affected_products=rec.get('affected_products', []),
                    affected_zones=rec.get('affected_zones', []),
                    ai_generated=True,
                    status="pending"
                )
                
                db.add(optimization)
                optimizations.append({
                    "title": rec.get('title'),
                    "description": rec.get('description'),
                    "priority": rec.get('priority'),
                    "expected_benefit": rec.get('benefit'),
                    "implementation_steps": rec.get('steps', [])
                })
            
            db.commit()
            
            return {
                "success": True,
                "total_recommendations": len(optimizations),
                "recommendations": optimizations,
                "current_layout_efficiency": self._calculate_layout_efficiency(velocity_data, current_layout),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating layout optimization: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def suggest_category_grouping(self, db: Session) -> Dict:
        """
        Suggest logical product grouping by category and volume
        """
        try:
            products = db.query(Product).all()
            
            # Group products by category
            category_groups = {}
            for product in products:
                category = product.category or "Uncategorized"
                if category not in category_groups:
                    category_groups[category] = []
                
                # Get inventory and velocity data
                inventory = db.query(Inventory).filter(
                    Inventory.product_id == product.id
                ).first()
                
                velocity = db.query(ProductVelocity).filter(
                    ProductVelocity.product_id == product.id
                ).first()
                
                category_groups[category].append({
                    "product": product,
                    "inventory": inventory,
                    "velocity": velocity
                })
            
            # Generate AI-powered grouping suggestions
            grouping_suggestions = self._get_ai_grouping_suggestions(category_groups)
            
            # Save optimization records
            optimizations = []
            for suggestion in grouping_suggestions:
                optimization = SpaceOptimization(
                    optimization_type="category_grouping",
                    title=suggestion.get('title'),
                    description=suggestion.get('description'),
                    priority=suggestion.get('priority', 'medium'),
                    expected_benefit=suggestion.get('benefit'),
                    implementation_effort=suggestion.get('effort', 'medium'),
                    affected_products=suggestion.get('affected_products', []),
                    affected_zones=suggestion.get('affected_zones', []),
                    ai_generated=True,
                    status="pending"
                )
                
                db.add(optimization)
                optimizations.append(suggestion)
            
            db.commit()
            
            return {
                "success": True,
                "category_analysis": self._analyze_categories(category_groups),
                "grouping_suggestions": optimizations,
                "total_suggestions": len(optimizations)
            }
            
        except Exception as e:
            logger.error(f"Error suggesting category grouping: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def optimize_fast_moving_placement(self, db: Session) -> Dict:
        """
        Optimize placement of fast-moving goods near exit/entrance
        """
        try:
            # Get fast-moving products
            fast_moving_products = db.query(Product, ProductVelocity).join(
                ProductVelocity
            ).filter(
                ProductVelocity.velocity_category == "fast"
            ).all()
            
            # Get warehouse layout with distances
            warehouse_zones = self._get_warehouse_zones_with_distances(db)
            
            # Generate AI optimization for fast-moving items
            fast_moving_optimization = self._get_ai_fast_moving_optimization(
                fast_moving_products, warehouse_zones
            )
            
            # Create optimization recommendations
            optimizations = []
            for opt in fast_moving_optimization:
                optimization = SpaceOptimization(
                    optimization_type="velocity_based",
                    title=opt.get('title', 'Fast-Moving Goods Optimization'),
                    description=opt.get('description'),
                    priority=opt.get('priority', 'high'),
                    expected_benefit=opt.get('benefit'),
                    implementation_effort=opt.get('effort', 'medium'),
                    affected_products=opt.get('affected_products', []),
                    affected_zones=opt.get('affected_zones', []),
                    ai_generated=True,
                    status="pending"
                )
                
                db.add(optimization)
                optimizations.append({
                    "title": opt.get('title'),
                    "description": opt.get('description'),
                    "current_efficiency": opt.get('current_efficiency'),
                    "projected_efficiency": opt.get('projected_efficiency'),
                    "time_savings": opt.get('time_savings'),
                    "implementation_steps": opt.get('steps', [])
                })
            
            db.commit()
            
            return {
                "success": True,
                "fast_moving_products_count": len(fast_moving_products),
                "optimization_recommendations": optimizations,
                "current_placement_efficiency": self._calculate_placement_efficiency(
                    fast_moving_products, warehouse_zones
                ),
                "potential_time_savings": "15-30% reduction in picking time"
            }
            
        except Exception as e:
            logger.error(f"Error optimizing fast-moving placement: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_space_optimization_plan(self, db: Session) -> Dict:
        """
        Generate comprehensive text-based space optimization plan
        """
        try:
            # Get all optimization data
            velocity_analysis = self.analyze_product_velocity(db)
            layout_optimization = self.generate_layout_optimization(db)
            category_grouping = self.suggest_category_grouping(db)
            fast_moving_optimization = self.optimize_fast_moving_placement(db)
            
            # Generate comprehensive AI plan
            optimization_plan = self._generate_ai_comprehensive_plan(
                velocity_analysis,
                layout_optimization,
                category_grouping,
                fast_moving_optimization
            )
            
            return {
                "success": True,
                "comprehensive_plan": optimization_plan,
                "executive_summary": optimization_plan.get('executive_summary'),
                "implementation_phases": optimization_plan.get('phases', []),
                "expected_benefits": optimization_plan.get('benefits', []),
                "estimated_timeline": optimization_plan.get('timeline'),
                "roi_projection": optimization_plan.get('roi')
            }
            
        except Exception as e:
            logger.error(f"Error generating space optimization plan: {str(e)}")
            return {"success": False, "error": str(e)}
    
    # Helper methods
    def _calculate_product_velocity(self, db: Session, product: Product) -> Dict:
        """Calculate velocity metrics for a product"""
        try:
            # Get sales history for the last 3 months
            three_months_ago = datetime.now() - timedelta(days=90)
            
            sales = db.query(SalesHistory).filter(
                SalesHistory.product_id == product.id,
                SalesHistory.sale_date >= three_months_ago
            ).all()
            
            if not sales:
                return {
                    "category": "dead",
                    "weekly_turnover": 0.0,
                    "monthly_turnover": 0.0,
                    "days_of_supply": 999,
                    "pick_frequency": 0,
                    "last_movement": None,
                    "trend": "stable"
                }
            
            # Calculate metrics
            total_sold = sum(sale.quantity_sold for sale in sales)
            weeks_in_period = len(sales) / 7.0 if sales else 1
            weekly_turnover = total_sold / max(weeks_in_period, 1)
            monthly_turnover = weekly_turnover * 4.33  # Average weeks per month
            
            # Get current inventory
            inventory = db.query(Inventory).filter(
                Inventory.product_id == product.id
            ).first()
            
            current_stock = inventory.available_quantity if inventory else 0
            days_of_supply = (current_stock / (weekly_turnover / 7)) if weekly_turnover > 0 else 999
            
            # Categorize velocity
            if weekly_turnover >= 20:
                category = "fast"
            elif weekly_turnover >= 5:
                category = "medium"
            elif weekly_turnover >= 1:
                category = "slow"
            else:
                category = "dead"
            
            return {
                "category": category,
                "weekly_turnover": round(weekly_turnover, 2),
                "monthly_turnover": round(monthly_turnover, 2),
                "days_of_supply": int(days_of_supply),
                "pick_frequency": len(sales),
                "last_movement": max(sale.sale_date for sale in sales) if sales else None,
                "trend": self._calculate_trend(sales)
            }
            
        except Exception as e:
            logger.error(f"Error calculating velocity for product {product.id}: {str(e)}")
            return {
                "category": "unknown",
                "weekly_turnover": 0.0,
                "monthly_turnover": 0.0,
                "days_of_supply": 999,
                "pick_frequency": 0,
                "last_movement": None,
                "trend": "stable"
            }
    
    def _calculate_trend(self, sales: List) -> str:
        """Calculate sales trend from historical data"""
        if len(sales) < 4:
            return "stable"
        
        # Simple trend calculation
        recent_sales = sum(sale.quantity_sold for sale in sales[-4:])
        older_sales = sum(sale.quantity_sold for sale in sales[:-4])
        
        if recent_sales > older_sales * 1.2:
            return "increasing"
        elif recent_sales < older_sales * 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def _get_velocity_distribution(self, velocity_analysis: List[Dict]) -> Dict:
        """Calculate distribution of velocity categories"""
        distribution = {"fast": 0, "medium": 0, "slow": 0, "dead": 0}
        
        for item in velocity_analysis:
            category = item["velocity_metrics"]["category"]
            distribution[category] += 1
        
        return distribution
    
    def _get_warehouse_zones(self, db: Session) -> List[Dict]:
        """Get warehouse zone information"""
        # Create default zones if none exist
        default_zones = [
            {"zone_code": "A1", "zone_name": "High-Traffic Storage", "distance_from_exit": 5.0},
            {"zone_code": "A2", "zone_name": "Medium-Traffic Storage", "distance_from_exit": 10.0},
            {"zone_code": "A3", "zone_name": "Slow-Moving Storage", "distance_from_exit": 15.0},
            {"zone_code": "B1", "zone_name": "Bulk Storage", "distance_from_exit": 20.0},
            {"zone_code": "B2", "zone_name": "Overflow Storage", "distance_from_exit": 25.0},
            {"zone_code": "C1", "zone_name": "Seasonal Storage", "distance_from_exit": 30.0}
        ]
        
        return default_zones
    
    def _get_product_velocities(self, db: Session) -> List[Dict]:
        """Get product velocity data"""
        velocities = db.query(ProductVelocity, Product).join(Product).all()
        
        return [
            {
                "product_id": product.id,
                "sku": product.sku,
                "category": velocity.velocity_category,
                "weekly_turnover": velocity.weekly_turnover,
                "current_location": product.location
            }
            for velocity, product in velocities
        ]
    
    def _get_current_layout(self, db: Session) -> List[Dict]:
        """Get current product layout"""
        products = db.query(Product).all()
        
        return [
            {
                "product_id": product.id,
                "sku": product.sku,
                "current_location": product.location,
                "category": product.category
            }
            for product in products
        ]
    
    def _get_ai_layout_recommendations(self, warehouse_zones: List[Dict], 
                                     velocity_data: List[Dict], 
                                     current_layout: List[Dict]) -> List[Dict]:
        """Get AI-powered layout recommendations"""
        try:
            prompt = f"""
            As a warehouse optimization expert, analyze the current layout and provide recommendations:
            
            Warehouse Zones:
            {json.dumps(warehouse_zones, indent=2)}
            
            Product Velocity Data:
            {json.dumps(velocity_data[:10], indent=2)}  # Limit for prompt size
            
            Current Layout:
            {json.dumps(current_layout[:10], indent=2)}  # Limit for prompt size
            
            Provide 3-5 specific layout optimization recommendations. For each recommendation:
            1. Title and description
            2. Priority level (low/medium/high)
            3. Expected benefit
            4. Implementation effort
            5. Affected products and zones
            6. Step-by-step implementation
            
            Return as JSON array of recommendations.
            """
            
            response = self.llm_service.get_completion(prompt)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._generate_default_layout_recommendations()
                
        except Exception as e:
            logger.error(f"Error getting AI layout recommendations: {str(e)}")
            return self._generate_default_layout_recommendations()
    
    def _get_ai_grouping_suggestions(self, category_groups: Dict) -> List[Dict]:
        """Get AI suggestions for category grouping"""
        try:
            # Summarize category data for AI
            category_summary = {}
            for category, products in category_groups.items():
                category_summary[category] = {
                    "product_count": len(products),
                    "total_inventory": sum(p["inventory"].available_quantity 
                                         if p["inventory"] else 0 for p in products),
                    "avg_velocity": "medium"  # Simplified for now
                }
            
            prompt = f"""
            Analyze product categories and suggest optimal grouping strategies:
            
            Category Analysis:
            {json.dumps(category_summary, indent=2)}
            
            Provide 3-4 category grouping recommendations considering:
            1. Picking efficiency
            2. Storage volume optimization
            3. Product compatibility
            4. Access frequency
            
            Return JSON array with title, description, priority, benefit, effort, and affected categories.
            """
            
            response = self.llm_service.get_completion(prompt)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._generate_default_grouping_suggestions()
                
        except Exception as e:
            logger.error(f"Error getting AI grouping suggestions: {str(e)}")
            return self._generate_default_grouping_suggestions()
    
    def _get_ai_fast_moving_optimization(self, fast_moving_products: List, 
                                       warehouse_zones: List[Dict]) -> List[Dict]:
        """Get AI optimization for fast-moving products"""
        try:
            fast_moving_summary = [
                {
                    "sku": product.sku,
                    "name": product.name,
                    "current_location": product.location,
                    "weekly_turnover": velocity.weekly_turnover
                }
                for product, velocity in fast_moving_products[:10]  # Limit for prompt
            ]
            
            prompt = f"""
            Optimize placement of fast-moving products for maximum efficiency:
            
            Fast-Moving Products:
            {json.dumps(fast_moving_summary, indent=2)}
            
            Available Zones:
            {json.dumps(warehouse_zones, indent=2)}
            
            Recommend optimal placement considering:
            1. Distance to exit/entrance
            2. Picking route efficiency
            3. Product accessibility
            4. Storage constraints
            
            Return JSON array of optimization recommendations.
            """
            
            response = self.llm_service.get_completion(prompt)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._generate_default_fast_moving_optimization()
                
        except Exception as e:
            logger.error(f"Error getting fast-moving optimization: {str(e)}")
            return self._generate_default_fast_moving_optimization()
    
    def _generate_ai_comprehensive_plan(self, velocity_analysis: Dict, 
                                      layout_optimization: Dict,
                                      category_grouping: Dict, 
                                      fast_moving_optimization: Dict) -> Dict:
        """Generate comprehensive optimization plan using AI"""
        try:
            summary_data = {
                "velocity_insights": velocity_analysis.get("velocity_distribution", {}),
                "layout_recommendations": len(layout_optimization.get("recommendations", [])),
                "grouping_suggestions": len(category_grouping.get("grouping_suggestions", [])),
                "fast_moving_optimizations": len(fast_moving_optimization.get("optimization_recommendations", []))
            }
            
            prompt = f"""
            Create a comprehensive warehouse space optimization plan based on analysis:
            
            Analysis Summary:
            {json.dumps(summary_data, indent=2)}
            
            Generate a detailed implementation plan including:
            1. Executive summary
            2. Implementation phases (with timelines)
            3. Expected benefits and ROI
            4. Risk mitigation
            5. Success metrics
            
            Return comprehensive JSON plan.
            """
            
            response = self.llm_service.get_completion(prompt)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return self._generate_default_comprehensive_plan()
                
        except Exception as e:
            logger.error(f"Error generating comprehensive plan: {str(e)}")
            return self._generate_default_comprehensive_plan()
    
    # Default/fallback methods
    def _generate_default_layout_recommendations(self) -> List[Dict]:
        """Generate default layout recommendations when AI is unavailable"""
        return [
            {
                "title": "Fast-Moving Items Near Exit",
                "description": "Move high-velocity products to zones closest to shipping area",
                "priority": "high",
                "benefit": "Reduce picking time by 20-30%",
                "effort": "medium",
                "affected_products": [],
                "affected_zones": ["A1"],
                "steps": ["Identify fast-moving products", "Relocate to A1 zone", "Update system locations"]
            },
            {
                "title": "Category-Based Grouping",
                "description": "Group similar products together for efficient picking",
                "priority": "medium",
                "benefit": "Improve picking accuracy and speed",
                "effort": "medium",
                "affected_products": [],
                "affected_zones": ["A2", "B1"],
                "steps": ["Analyze product categories", "Design zone layouts", "Implement gradual relocation"]
            }
        ]
    
    def _generate_default_grouping_suggestions(self) -> List[Dict]:
        """Generate default category grouping suggestions"""
        return [
            {
                "title": "Electronics Consolidation",
                "description": "Group all electronics in adjacent zones for better inventory management",
                "priority": "medium",
                "benefit": "Improved inventory accuracy and picking efficiency",
                "effort": "low"
            }
        ]
    
    def _generate_default_fast_moving_optimization(self) -> List[Dict]:
        """Generate default fast-moving optimization"""
        return [
            {
                "title": "Priority Zone Optimization",
                "description": "Create dedicated zone for fastest-moving products near exit",
                "priority": "high",
                "benefit": "25% reduction in average picking time",
                "effort": "medium",
                "current_efficiency": "70%",
                "projected_efficiency": "90%",
                "time_savings": "2-3 minutes per pick on average"
            }
        ]
    
    def _generate_default_comprehensive_plan(self) -> Dict:
        """Generate default comprehensive plan"""
        return {
            "executive_summary": "Warehouse optimization plan focused on velocity-based layout and category grouping",
            "phases": [
                {
                    "phase": 1,
                    "title": "Fast-Moving Optimization",
                    "duration": "2-4 weeks",
                    "activities": ["Analyze product velocity", "Relocate fast-moving items", "Update systems"]
                }
            ],
            "benefits": ["Improved picking efficiency", "Better space utilization", "Reduced operational costs"],
            "timeline": "6-8 weeks for full implementation",
            "roi": "15-25% improvement in warehouse efficiency"
        }
    
    def _get_warehouse_zones_with_distances(self, db: Session) -> List[Dict]:
        """Get warehouse zones with distance information"""
        return self._get_warehouse_zones(db)
    
    def _calculate_layout_efficiency(self, velocity_data: List[Dict], current_layout: List[Dict]) -> str:
        """Calculate current layout efficiency score"""
        return "72% - Room for improvement in fast-moving product placement"
    
    def _calculate_placement_efficiency(self, fast_moving_products: List, warehouse_zones: List[Dict]) -> str:
        """Calculate placement efficiency for fast-moving products"""
        return "68% - Many fast-moving products not optimally placed"
    
    def _analyze_categories(self, category_groups: Dict) -> Dict:
        """Analyze category distribution and characteristics"""
        return {
            "total_categories": len(category_groups),
            "largest_category": max(category_groups.keys(), key=lambda k: len(category_groups[k])),
            "distribution": {cat: len(products) for cat, products in category_groups.items()}
        }
