#!/bin/bash

# Railway Deployment Script for Smart Warehouse System
# Run this after connecting your GitHub repo to Railway

echo "🚀 Setting up Railway deployment..."

# Create railway.json for configuration
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
EOF

# Create .env template for Railway environment variables
cat > .env.railway << 'EOF'
# Railway Environment Variables
# Set these in Railway dashboard: Settings > Variables

DATABASE_URL=sqlite:///./smart_warehouse.db
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8000

# Optional: Add these for enhanced features
# HUGGINGFACE_TOKEN=your_token_here
# OPENAI_API_KEY=your_key_here
EOF

echo "✅ Railway configuration created!"
echo ""
echo "🔧 Next steps:"
echo "1. Push this to GitHub"
echo "2. Go to railway.app and connect your repo"
echo "3. Railway will auto-deploy using your Dockerfile"
echo "4. Set environment variables in Railway dashboard"
echo ""
echo "🌐 Your app will be live at: https://your-app-name.railway.app"
