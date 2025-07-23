#!/bin/bash

# SMART WAREHOUSE MANAGEMENT SYSTEM - PRODUCTION DEPLOYMENT
# Enterprise-grade deployment script for full system

set -e  # Exit on any error

echo "SMART WAREHOUSE MANAGEMENT SYSTEM"
echo "Production Deployment Script v4.0"
echo "=================================="
echo "Date: $(date)"
echo ""

# Configuration
PROJECT_NAME="smart-warehouse"
DOCKER_IMAGE="smart-warehouse:latest"
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
LOG_FILE="./logs/deployment_$(date +%Y%m%d_%H%M%S).log"

# Create necessary directories
mkdir -p logs backups data ssl

echo "Pre-deployment Checklist"
echo "========================"

# Check prerequisites
echo "Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "ERROR: Docker not installed"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "ERROR: Docker Compose not installed"; exit 1; }

echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"

# Backup existing data
echo ""
echo "Creating Backup"
echo "==============="
if [ -f "smart_warehouse.db" ]; then
    echo "Backing up database..."
    mkdir -p "$BACKUP_DIR"
    cp smart_warehouse.db "$BACKUP_DIR/"
    cp -r data/ "$BACKUP_DIR/" 2>/dev/null || true
    echo "Backup created: $BACKUP_DIR"
else
    echo "No existing database found - fresh installation"
fi

# Environment setup
echo ""
echo "Environment Setup"
echo "==================="

# Create production environment file
cat > .env << EOF
# Smart Warehouse Management System - Production Configuration
ENVIRONMENT=production
DATABASE_URL=sqlite:///./smart_warehouse.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=$(openssl rand -hex 32)
CORS_ORIGINS=*
DEBUG=false

# Security settings
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5
PASSWORD_MIN_LENGTH=8

# Performance settings
WORKER_PROCESSES=4
MAX_CONNECTIONS=1000
CACHE_TTL=3600

# Feature flags
ENABLE_AI_FEATURES=true
ENABLE_REAL_TIME=true
ENABLE_ANALYTICS=true
ENABLE_FORECASTING=true

# External services (configure as needed)
OPENAI_API_KEY=your_openai_api_key_here
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@company.com
EMAIL_PASSWORD=your_app_password

# Monitoring
ENABLE_MONITORING=true
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
EOF

echo " Environment configuration created"

# Update requirements
echo ""
echo " Installing Dependencies"
echo "========================="

# Create comprehensive requirements file
cat > requirements.txt << EOF
# Smart Warehouse Management System - Production Requirements
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
sqlite3
pydantic==2.5.0
python-multipart==0.0.6
jinja2==3.1.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# AI and ML
openai==1.3.0
langchain==0.0.350
chromadb==0.4.18
sentence-transformers==2.2.2
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2

# Visualization and Analytics
plotly==5.17.0
matplotlib==3.8.2
seaborn==0.13.0

# Performance and Caching
redis==5.0.1
aioredis==2.0.1
aiocache==0.12.2

# Production server
gunicorn==21.2.0
psycopg2-binary==2.9.9

# Monitoring and logging
prometheus-client==0.19.0
structlog==23.2.0

# Security
cryptography==41.0.7
bcrypt==4.1.2

# Async support
aiohttp==3.9.1
aiofiles==23.2.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
EOF

echo " Requirements updated"

# Database setup
echo ""
echo "🗄️  Database Setup"
echo "=================="

# Initialize database if needed
if [ ! -f "smart_warehouse.db" ]; then
    echo "🔄 Initializing new database..."
    python3 -c "
from backend.app.database import engine, Base
from backend.app.models.database_models import *
Base.metadata.create_all(bind=engine)
print(' Database tables created')
"
    
    # Setup sample data
    if [ -f "setup_phase3_data.py" ]; then
        echo " Setting up sample data..."
        python3 setup_phase3_data.py
    fi
else
    echo " Using existing database"
fi

# Build and deploy
echo ""
echo "🐳 Docker Deployment"
echo "==================="

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t $DOCKER_IMAGE . --no-cache

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans || true

# Start production deployment
echo "🚀 Starting production deployment..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 30

# Verify deployment
echo ""
echo " Deployment Verification"
echo "========================="

# Test main application
echo "🔍 Testing main application..."
if curl -f -s http://localhost:8001/health > /dev/null; then
    echo " Main application: HEALTHY"
else
    echo " Main application: UNHEALTHY"
    exit 1
fi

# Test API endpoints
echo "🔍 Testing API endpoints..."
if curl -f -s http://localhost:8001/docs > /dev/null; then
    echo " API documentation: ACCESSIBLE"
else
    echo " API documentation: INACCESSIBLE"
fi

# Test Phase 3 features
if curl -f -s http://localhost:8001/api/phase3/health > /dev/null; then
    echo " Phase 3 features: OPERATIONAL"
else
    echo " Phase 3 features: NOT OPERATIONAL"
fi

# Test advanced dashboard
if curl -f -s http://localhost:8001/advanced-dashboard > /dev/null; then
    echo " Advanced dashboard: ACCESSIBLE"
else
    echo " Advanced dashboard: INACCESSIBLE"
fi

# Display deployment summary
echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================"
echo "📅 Deployment Date: $(date)"
echo "🏷️  Version: Smart Warehouse v4.0"
echo "🐳 Docker Image: $DOCKER_IMAGE"
echo "💾 Backup Location: $BACKUP_DIR"
echo ""
echo "🌐 Access Points:"
echo "   🏠 Main Dashboard: http://localhost:8001/"
echo "   🤖 AI Chatbot: http://localhost:8001/chatbot"
echo "    Advanced Analytics: http://localhost:8001/advanced-dashboard"
echo "   📋 API Documentation: http://localhost:8001/docs"
echo "   📈 Monitoring: http://localhost:3000 (Grafana)"
echo "   🔧 Metrics: http://localhost:9090 (Prometheus)"
echo ""
echo "🔧 Management Commands:"
echo "    View logs: docker-compose logs -f"
echo "   🔄 Restart: docker-compose restart"
echo "   🛑 Stop: docker-compose down"
echo "   💾 Backup: ./backup_system.sh"
echo ""
echo " Smart Warehouse Management System is PRODUCTION READY!"

# Create system status check script
cat > check_system_status.sh << 'EOF'
#!/bin/bash
echo "🔍 Smart Warehouse System Status Check"
echo "====================================="
echo "Date: $(date)"
echo ""

# Check Docker containers
echo "🐳 Container Status:"
docker-compose ps

echo ""
echo "🌐 Service Health Checks:"

# Main application
if curl -f -s http://localhost:8001/health > /dev/null; then
    echo " Main Application: HEALTHY"
else
    echo " Main Application: UNHEALTHY"
fi

# Database
if [ -f "smart_warehouse.db" ]; then
    echo " Database: ACCESSIBLE"
else
    echo " Database: NOT FOUND"
fi

# Redis
if docker-compose exec redis redis-cli ping > /dev/null 2>&1; then
    echo " Redis Cache: OPERATIONAL"
else
    echo " Redis Cache: DOWN"
fi

echo ""
echo " Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
EOF

chmod +x check_system_status.sh

echo ""
echo " System Status Check Script Created: ./check_system_status.sh"
echo "Run './check_system_status.sh' to monitor system health"

# Log deployment
echo "$(date): Production deployment completed successfully" >> "$LOG_FILE"
