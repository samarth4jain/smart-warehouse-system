from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import os
import time
import asyncio
from functools import lru_cache
from .database import engine, Base
from .routers import inventory, inbound, outbound, chatbot, dashboard, forecasting

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

# Mount static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main dashboard page"""
    html_file = os.path.join(frontend_path, "index.html")
    try:
        with open(html_file, "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Welcome to Smart Warehousing System</h1><p>Frontend not found</p>")

@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page():
    """Serve the chatbot interface page"""
    html_file = os.path.join(frontend_path, "chatbot.html")
    try:
        with open(html_file, "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Chatbot Interface</h1><p>Frontend not found</p>")

@app.get("/advanced-dashboard", response_class=HTMLResponse)
async def advanced_dashboard():
    """Serve the Phase 4 advanced analytics dashboard"""
    html_file = os.path.join(frontend_path, "advanced_dashboard.html")
    try:
        with open(html_file, "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Advanced Dashboard Not Found</h1><p>Please run create_advanced_dashboard.py first.</p>")

@app.get("/enterprise-dashboard", response_class=HTMLResponse)
async def enterprise_dashboard():
    """Serve the enterprise-grade analytics dashboard"""
    html_file = os.path.join(frontend_path, "enterprise_dashboard.html")
    try:
        with open(html_file, "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Enterprise Dashboard Not Found</h1><p>Please ensure the enterprise dashboard file exists.</p>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Smart Warehousing System is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
