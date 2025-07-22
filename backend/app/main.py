from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import os
import time
import asyncio
from datetime import datetime
from functools import lru_cache
from .database import engine, Base
from .routers import inventory, inbound, outbound, chatbot, dashboard, forecasting, commercial_features, ultra_analytics
from datetime import datetime

# Create database tables
Base.metadata.create_all(bind=engine)

# Ultra-High Performance FastAPI Configuration
app = FastAPI(
    title="Smart Warehousing System - Ultra Performance Edition",
    description="Enterprise-grade warehouse management with ultra-high performance optimization - Version 4.0 Ultra",
    version="4.0.0-ultra",
    docs_url="/docs",
    redoc_url="/redoc",
    # Performance optimizations
    generate_unique_id_function=lambda route: f"{route.tags[0] if route.tags else 'default'}-{route.name}"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(inbound.router, prefix="/api/inbound", tags=["Inbound"])
app.include_router(outbound.router, prefix="/api/outbound", tags=["Outbound"])
app.include_router(chatbot.router, prefix="/api/chat", tags=["Chatbot"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(forecasting.router, prefix="/api/phase3", tags=["Phase 3: Forecasting & Space Planning"])
app.include_router(ultra_analytics.router, prefix="/api", tags=["Ultra Analytics"])
app.include_router(commercial_features.router, prefix="/api", tags=["Commercial Features"])

# Mount static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main dashboard page"""
    html_file = os.path.join(frontend_path, "index.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Welcome to Smart Warehousing System</h1><p>Frontend not found</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Welcome to Smart Warehousing System</h1><p>Error reading file - encoding issue</p>")

@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page():
    """Serve the chatbot interface page"""
    html_file = os.path.join(frontend_path, "chatbot.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Chatbot Interface</h1><p>Frontend not found</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Chatbot Interface</h1><p>Error reading file - encoding issue</p>")

@app.get("/chatbot.html", response_class=HTMLResponse)
async def chatbot_html():
    """Alternative route for chatbot.html"""
    return await chatbot_page()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    """Serve the main dashboard page"""
    html_file = os.path.join(frontend_path, "dashboard.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard Not Found</h1><p>Please ensure the dashboard file exists.</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Dashboard</h1><p>Error reading file - encoding issue</p>")

@app.get("/advanced-dashboard", response_class=HTMLResponse)
async def advanced_dashboard():
    """Redirect to enterprise dashboard (consolidated)"""
    html_file = os.path.join(frontend_path, "enterprise_dashboard.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Advanced Analytics</h1><p>Please use the enterprise dashboard for advanced features.</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Advanced Dashboard</h1><p>Error reading file - encoding issue</p>")

@app.get("/enterprise-dashboard", response_class=HTMLResponse)
async def enterprise_dashboard():
    """Serve the enterprise-grade analytics dashboard"""
    html_file = os.path.join(frontend_path, "enterprise_dashboard.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Enterprise Dashboard Not Found</h1><p>Please ensure the enterprise dashboard file exists.</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Enterprise Dashboard</h1><p>Error reading file - encoding issue</p>")

@app.get("/enterprise-analytics", response_class=HTMLResponse)
async def enterprise_analytics_dashboard():
    """Serve the enhanced enterprise analytics dashboard"""
    html_file = os.path.join(frontend_path, "enterprise_analytics_dashboard.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Enterprise Analytics Not Found</h1><p>Please ensure the analytics dashboard file exists.</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Enterprise Analytics</h1><p>Error reading file - encoding issue</p>")

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page():
    """Serve the analytics dashboard page"""
    html_file = os.path.join(frontend_path, "enterprise_dashboard.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Analytics Dashboard</h1><p>Analytics dashboard not found</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Analytics Dashboard</h1><p>Error reading file - encoding issue</p>")

@app.get("/docs", response_class=HTMLResponse)
async def docs_page():
    """Serve the documentation page"""
    docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs")
    html_file = os.path.join(docs_path, "index.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Documentation</h1><p>Documentation not found. Please check the docs folder.</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Documentation</h1><p>Error reading file - encoding issue</p>")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Enterprise Analytics Dashboard Not Found</h1><p>Please ensure the enhanced dashboard file exists.</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Enterprise Analytics Dashboard</h1><p>Error reading file - encoding issue</p>")

@app.get("/commercial-intelligence", response_class=HTMLResponse)
async def commercial_intelligence_dashboard():
    """Serve the commercial intelligence dashboard"""
    html_file = os.path.join(frontend_path, "commercial_intelligence_dashboard.html")
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Commercial Intelligence Dashboard Not Found</h1><p>Please ensure the commercial dashboard file exists.</p>")
    except UnicodeDecodeError:
        return HTMLResponse(content="<h1>Commercial Intelligence Dashboard</h1><p>Error reading file - encoding issue</p>")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        from .database import get_db
        db = next(get_db())
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "version": "4.0.0-commercial",
        "database": db_status,
        "features": {
            "commercial_intelligence": True,
            "ai_analytics": True,
            "qr_management": True,
            "iot_integration": True,
            "automation": True
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
