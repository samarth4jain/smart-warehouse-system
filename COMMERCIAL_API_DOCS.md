# Commercial Smart Warehouse API Documentation

## Overview
The Commercial Smart Warehouse Management System provides enterprise-grade APIs for advanced warehouse operations, analytics, and business intelligence.

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently using basic authentication. Enterprise SSO integration available.

## Commercial Features Endpoints

### Executive Dashboard
Get comprehensive executive dashboard data including KPIs, financial metrics, and performance indicators.

```http
GET /commercial/executive-dashboard
```

**Response:**
```json
{
  "financial_metrics": {
    "revenue": 1500000,
    "profit_margin": 15.5,
    "cost_reduction": 12.3,
    "roi": 22.8
  },
  "operational_kpis": {
    "inventory_turnover": 8.5,
    "order_fulfillment_rate": 98.2,
    "warehouse_utilization": 85.0,
    "accuracy_rate": 99.1
  },
  "trends": {
    "revenue_growth": 8.5,
    "efficiency_improvement": 15.2,
    "cost_savings": 180000
  }
}
```

### Financial Metrics
Track detailed financial performance metrics.

```http
GET /commercial/financial-metrics
```

**Response:**
```json
{
  "total_revenue": 1500000,
  "cost_of_goods": 1200000,
  "operating_expenses": 150000,
  "net_profit": 150000,
  "profit_margin": 10.0,
  "inventory_value": 500000,
  "carrying_cost": 25000,
  "storage_cost_per_unit": 2.50,
  "handling_cost_per_order": 15.00
}
```

### QR Code Management
Generate and manage QR codes for products and locations.

```http
POST /commercial/qr-codes/generate
Content-Type: application/json

{
  "product_id": 123,
  "sku": "ABC123",
  "location": "A1-B2-C3",
  "additional_data": {}
}
```

**Response:**
```json
{
  "qr_code_id": "qr_abc123",
  "qr_code_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "data": {
    "product_id": 123,
    "sku": "ABC123",
    "location": "A1-B2-C3"
  },
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Advanced Analytics

#### ABC Analysis
Perform ABC analysis on inventory to categorize products by value.

```http
GET /commercial/analytics/abc-analysis
```

**Response:**
```json
{
  "category_a": {
    "products": 150,
    "percentage": 20,
    "value_percentage": 80
  },
  "category_b": {
    "products": 300,
    "percentage": 40,
    "value_percentage": 15
  },
  "category_c": {
    "products": 300,
    "percentage": 40,
    "value_percentage": 5
  }
}
```

#### Velocity Analysis
Analyze product movement velocity for optimization.

```http
GET /commercial/analytics/velocity-analysis
```

**Response:**
```json
{
  "fast_moving": {
    "count": 45,
    "products": ["SKU001", "SKU002", "SKU003"]
  },
  "medium_moving": {
    "count": 120,
    "products": ["SKU004", "SKU005"]
  },
  "slow_moving": {
    "count": 85,
    "products": ["SKU006", "SKU007"]
  }
}
```

#### Predictive Insights
Get AI-powered predictive insights for inventory management.

```http
GET /commercial/analytics/predictive-insights
```

**Response:**
```json
{
  "demand_forecast": {
    "next_30_days": 1250,
    "confidence": 0.92,
    "trend": "increasing"
  },
  "stockout_risk": {
    "high_risk_products": ["SKU001", "SKU005"],
    "medium_risk_products": ["SKU003"],
    "risk_score": 0.35
  },
  "optimization_recommendations": [
    {
      "product_id": 123,
      "action": "increase_stock",
      "priority": "high",
      "reason": "High demand forecast with low current stock"
    }
  ]
}
```

### Layout Optimization
Optimize warehouse layout for maximum efficiency.

```http
POST /commercial/layout/optimize
Content-Type: application/json

{
  "zone": "A",
  "optimization_type": "efficiency",
  "constraints": ["max_distance", "picking_frequency"]
}
```

**Response:**
```json
{
  "optimization_id": "opt_123",
  "recommendations": [
    {
      "product_id": 123,
      "current_location": "A1-B2-C3",
      "suggested_location": "A1-B1-C1",
      "reason": "High picking frequency, move closer to dispatch",
      "estimated_savings": "15% reduction in picking time"
    }
  ],
  "estimated_improvement": {
    "efficiency_gain": 18.5,
    "cost_savings": 25000,
    "implementation_time": "2 weeks"
  }
}
```

### KPI Monitoring
Set and monitor key performance indicators.

```http
POST /commercial/kpis/targets
Content-Type: application/json

{
  "metric_name": "order_fulfillment_rate",
  "target_value": 98.0,
  "warning_threshold": 95.0,
  "critical_threshold": 90.0,
  "measurement_period": "daily"
}
```

```http
GET /commercial/kpis/current
```

**Response:**
```json
{
  "kpis": [
    {
      "metric_name": "order_fulfillment_rate",
      "current_value": 97.5,
      "target_value": 98.0,
      "status": "warning",
      "trend": "stable",
      "last_updated": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### Smart Alerts
Configure and manage intelligent alerts.

```http
POST /commercial/alerts/configure
Content-Type: application/json

{
  "alert_type": "low_stock",
  "threshold_value": 10,
  "notification_method": "email",
  "recipients": ["manager@company.com"],
  "severity": "high"
}
```

### Compliance Reporting
Generate compliance reports for regulatory requirements.

```http
GET /commercial/compliance/inventory-report
```

**Response:**
```json
{
  "report_id": "comp_123",
  "generated_at": "2024-01-01T12:00:00Z",
  "compliance_status": "compliant",
  "inventory_accuracy": 99.2,
  "audit_trail": [
    {
      "action": "stock_adjustment",
      "user": "admin",
      "timestamp": "2024-01-01T10:00:00Z",
      "details": "Adjusted SKU001 quantity from 100 to 95"
    }
  ],
  "exceptions": []
}
```

### Automation Features
Manage and monitor automation systems.

```http
GET /commercial/automation/status
```

**Response:**
```json
{
  "automated_processes": [
    {
      "process_name": "auto_reorder",
      "status": "active",
      "last_run": "2024-01-01T11:00:00Z",
      "success_rate": 98.5,
      "next_run": "2024-01-01T13:00:00Z"
    }
  ],
  "system_health": {
    "overall_status": "healthy",
    "cpu_usage": 45.2,
    "memory_usage": 62.1,
    "storage_usage": 35.8
  }
}
```

### AMR Fleet Management
Monitor and control Autonomous Mobile Robot fleet.

```http
GET /commercial/amr/fleet-status
```

**Response:**
```json
{
  "total_robots": 12,
  "active_robots": 10,
  "idle_robots": 2,
  "robots_in_maintenance": 0,
  "fleet_efficiency": 87.5,
  "total_tasks_completed": 1250,
  "average_task_time": 8.5,
  "robots": [
    {
      "robot_id": "AMR001",
      "status": "active",
      "current_task": "picking",
      "location": "Zone A",
      "battery_level": 85,
      "tasks_completed": 45
    }
  ]
}
```

### Computer Vision QC
Quality control using computer vision systems.

```http
GET /commercial/computer-vision/qc-status
```

**Response:**
```json
{
  "system_status": "operational",
  "cameras_active": 8,
  "detection_accuracy": 97.2,
  "items_inspected_today": 2450,
  "defects_detected": 12,
  "false_positive_rate": 1.8,
  "recent_detections": [
    {
      "timestamp": "2024-01-01T11:30:00Z",
      "product_id": 123,
      "defect_type": "packaging_damage",
      "confidence": 0.95,
      "action_taken": "quarantine"
    }
  ]
}
```

### IoT Sensor Management
Monitor IoT sensors throughout the warehouse.

```http
GET /commercial/iot/sensor-status
```

**Response:**
```json
{
  "total_sensors": 150,
  "active_sensors": 148,
  "offline_sensors": 2,
  "sensor_types": {
    "temperature": 50,
    "humidity": 30,
    "motion": 40,
    "door": 20,
    "weight": 10
  },
  "alerts": [
    {
      "sensor_id": "TEMP001",
      "type": "temperature",
      "value": 28.5,
      "threshold": 25.0,
      "location": "Cold Storage Zone",
      "severity": "warning"
    }
  ]
}
```

## Error Responses
All endpoints return standard HTTP status codes. Error responses include:

```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "details": {},
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Rate Limiting
- Standard API: 1000 requests/hour
- Premium API: 10000 requests/hour
- Enterprise API: Unlimited

## Support
For enterprise support and custom integrations:
- Email: enterprise@smartwarehouse.com
- Phone: 1-800-WAREHOUSE
- Documentation: https://docs.smartwarehouse.com
